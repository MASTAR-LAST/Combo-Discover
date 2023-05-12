import sys
import re

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

def email_slicer(emails_file):

    with open(f"{emails_file}", "r") as file:
            lines = file.readlines()

            email_list = []
            for line in lines:
                emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
                email_list.extend(emails)

            gmail_list: list[str] = []
            yahoo_list: list[str] = []
            hotmail_list: list[str] = []
            garbage_list: list[str] = []
            live_list: list[str] = []

            gmail_num: int = 0
            yahoo_num: int = 0
            hotmail_num: int = 0
            garbage_num: int = 0
            live_num: int = 0

            for email in email_list:
                if 'gmail.com' in email:
                    gmail_list.append(email)
                    gmail_num += 1
                elif 'yahoo.com' in email:
                    yahoo_list.append(email)
                    yahoo_num += 1
                elif 'hotmail.com' in email:
                    hotmail_list.append(email)
                    hotmail_num += 1
                elif 'live.com' in email:
                    live_list.append(email)
                    live_num += 1
                else:
                    garbage_list.append(email)
                    garbage_num += 1

            with open('email_slicer/gmail_list.txt', 'w') as f:
                for email in gmail_list:
                    f.write(email + '\n')

            with open('email_slicer/yahoo_list.txt', 'w') as f:
                for email in yahoo_list:
                    f.write(email + '\n')

            with open('email_slicer/hotmail_list.txt', 'w') as f:
                for email in hotmail_list:
                    f.write(email + '\n')

            with open('email_slicer/garbage_list.txt', 'w') as f:
                for email in garbage_list:
                    f.write(email + '\n')

            with open('email_slicer/live_list.txt', 'w') as f:
                for email in live_list:
                    f.write(email + '\n')

    print("Results:")
    print(f"gmail emails: {gmail_num}")
    print(f"yahoo emails: {yahoo_num}")
    print(f"hotmail emails: {hotmail_num}")
    print(f"live emails: {live_num}")
    print(f"garbage emails: {garbage_num}")

test = Prospector('extracted/336K UK.txt', 'test.txt', 'emails.txt')

test.run()

email_slicer("emails.txt")
