import cmd


class S3BreezeShell(cmd.Cmd):
    intro = (
        'Welcome to the s3breeze shell.   Type help or ? to list commands.\n'
    )
    prompt = 's3 object key > '


if __name__ == '__main__':
    S3BreezeShell().cmdloop()
