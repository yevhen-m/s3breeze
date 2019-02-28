import cmd

from urllib.parse import urlparse


class S3BreezeShell(cmd.Cmd):
    intro = (
        'Welcome to the s3breeze shell.   Type help or ? to list commands.\n'
    )
    prompt = 's3 object key > '

    def do_quit(self, line):
        print('Bye!')
        return True

    def do_show(self, line):
        parse_result = urlparse(line)
        s3_bucket, s3_key = parse_result.path.strip('/').split('/', 1)

    def default(self, line):
        if line == 'EOF':
            print()
            return self.do_quit(line)
        return self.do_show(line)


if __name__ == '__main__':
    S3BreezeShell().cmdloop()
