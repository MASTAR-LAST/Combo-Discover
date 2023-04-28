import sys

class Prospector:
    def __init__(self, combo_file, base_file, email_file):
        self.combo = combo_file
        self.base = base_file
        self.email = email_file

    def run(self):
        with open(self.combo, 'r') as combo, \
                open(self.base, 'a+') as base, \
                open(self.email, 'a+') as email_file:

            print("Start extraction...", sep='\n')
            print("Note: This process may take a long time for very large combo files.")

            base.seek(0)
            base_passwords = set(base.read().split('\n'))
            email_file.seek(0)
            email_addresses = set(email_file.read().split('\n'))

            find_passwd = 0
            total_passwd = 0
            find_email = 0
            total_email = 0

            for line in combo:
                line = line.strip()
                email, passwd = line.split(':')[-2:]

                total_passwd += 1
                if passwd not in base_passwords:
                    base.write(passwd + '\n')
                    base_passwords.add(passwd)
                else:
                    find_passwd += 1

                total_email += 1
                if email not in email_addresses:
                    email_file.write(email + '\n')
                    email_addresses.add(email)
                else:
                    find_email += 1

            percentage_passwd = (find_passwd / total_passwd) * 100
            percentage_email = (find_email / total_email) * 100

        print("Extraction completed !", sep='\n')
        print("------------------------------Passwords-info------------------------------")
        print(f"{find_passwd} of the {total_passwd} pre-existing passwords have been found", sep='\n')
        print(f"Pre-existing passwords: {percentage_passwd:.2f}%\n")

        print("------------------------------Emails-info------------------------------")
        print(f"{find_email} of the {total_email} pre-existing emails have been found", sep='\n')
        print(f"Pre-existing emails: {percentage_email:.2f}%\n")

test = Prospector('extracted/336K UK.txt', 'test.txt', 'emails.txt')

test.run()
