import cmd
import json
import logging
import os
import os.path
import subprocess
import sys
import tempfile
import webbrowser
import xml
import xml.dom.minidom

from urllib.parse import urlparse
from xml.parsers.expat import ExpatError

OUTPUT_DIR = os.environ.get('OUTPUT_DIR', tempfile.gettempdir())
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def xml_formatter(text):
    try:
        text = json.loads(text)
        if not isinstance(text, str):
            return
    except json.JSONDecodeError:
        pass
    try:
        return xml.dom.minidom.parseString(text).toprettyxml()
    except ExpatError:
        logger.debug('Failed to parse xml', exc_info=True)


def json_formatter(text):
    try:
        return json.dumps(json.loads(text), indent=4, sort_keys=True)
    except json.JSONDecodeError:
        logger.debug('Failed to parse json', exc_info=True)


def double_json_formatter(text):
    try:
        value = json.loads(text)
        return json.dumps(json.loads(value), indent=4, sort_keys=True)
    except (json.JSONDecodeError, TypeError):
        logger.debug('Failed to parse double json', exc_info=True)


class S3BreezeShell(cmd.Cmd):
    intro = f"""\
Welcome to the s3breeze shell.

Type help or ? to list commands.

Files will be stored in {OUTPUT_DIR}
"""
    prompt = 'KEY > '

    def emptyline(self):
        """Do not repeat last entered command on empty line."""

    def do_quit(self, line):
        print('Bye!')
        return True

    def do_show(self, line):
        """Show s3 object in the browser tab."""
        parse_result = urlparse(line)
        path = parse_result.path.strip('/')
        filename = os.path.basename(path)
        s3_uri = f's3://{path}'
        logger.debug('Open s3 uri %s', s3_uri)
        filepath = os.path.abspath(os.path.join(OUTPUT_DIR, filename))
        with open(filepath, mode='w+') as f:
            logger.debug('Output file is %s', f.name)
            try:
                subprocess.run(
                    ['s3cmd', 'get', s3_uri, f.name, '--force'],
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    check=True,
                )
            except subprocess.CalledProcessError as err:
                print(f'Command "{err.cmd}" failed!')
                return

            f.seek(0)
            content = f.read()
            for formatter in (
                xml_formatter,
                double_json_formatter,
                json_formatter,
            ):
                formatted_content = formatter(content)
                if formatted_content:
                    f.seek(0)
                    f.truncate()
                    f.write(formatted_content)
                    break

        webbrowser.open_new_tab(f'file://{f.name}')

    def default(self, line):
        if line == 'EOF':
            print()
            return self.do_quit(line)
        return self.do_show(line)


def main():
    S3BreezeShell().cmdloop()


if __name__ == '__main__':
    main()
