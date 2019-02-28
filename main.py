import cmd
import json
import logging
import os
import subprocess
import sys
import tempfile

from urllib.parse import urlparse

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def format_file_content(filename):
    with open(filename, 'r+') as f:
        try:
            content = json.load(f)
            f.seek(0)
            f.truncate()
            json.dump(content, f, indent=4, sort_keys=True)
        except json.JSONDecodeError:
            pass


class S3BreezeShell(cmd.Cmd):
    intro = (
        'Welcome to the s3breeze shell.   Type help or ? to list commands.\n'
    )
    prompt = 's3 object key > '

    def emptyline(self):
        """Do not repeat last entered command on empty line."""

    def do_quit(self, line):
        print('Bye!')
        return True

    def do_show(self, line):
        """Show s3 object in the browser tab."""
        parse_result = urlparse(line)
        s3_uri = f's3:/{parse_result.path}'
        logger.debug('Open s3 uri %s', s3_uri)
        try:
            with tempfile.NamedTemporaryFile(delete=False) as output_file:
                logger.debug('Output file is %s', output_file.name)
                process = subprocess.run(
                    ['s3cmd', 'get', s3_uri, output_file.name, '--force'],
                    stdin=sys.stdin,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    check=True,
                )
        except subprocess.CalledProcessError as err:
            print(f'Command "{err.cmd}" failed!')
        else:
            format_file_content(output_file.name)

    def default(self, line):
        if line == 'EOF':
            print()
            return self.do_quit(line)
        return self.do_show(line)


if __name__ == '__main__':
    S3BreezeShell().cmdloop()
