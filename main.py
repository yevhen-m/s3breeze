import cmd
import json
import logging
import os
import subprocess
import sys
import tempfile
import webbrowser

from urllib.parse import urlparse

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


class S3BreezeShell(cmd.Cmd):
    intro = f"""\
Welcome to the s3breeze shell.

Type help or ? to list commands.

Files will be stored in {tempfile.gettempdir()}
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
        s3_uri = f's3://{path}'
        logger.debug('Open s3 uri %s', s3_uri)
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            logger.debug('Output file is %s', f.name)
            try:
                process = subprocess.run(
                    ['s3cmd', 'get', s3_uri, f.name, '--force'],
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    check=True,
                )
            except subprocess.CalledProcessError as err:
                print(f'Command "{err.cmd}" failed!')
                return

            # Try to format file content in case it's json
            f.seek(0)
            try:
                content = json.load(f)
                f.seek(0)
                f.truncate()
                json.dump(content, f, indent=4, sort_keys=True)
            except json.JSONDecodeError:
                pass

        webbrowser.open_new_tab(f'file://{f.name}')

    def default(self, line):
        if line == 'EOF':
            print()
            return self.do_quit(line)
        return self.do_show(line)


if __name__ == '__main__':
    S3BreezeShell().cmdloop()
