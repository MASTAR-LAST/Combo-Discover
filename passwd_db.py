import sqlite3

class Prospector:
    def __init__(self, combo_file, base_file, email_file):
        self.combo = combo_file
        self.base = base_file
        self.email = email_file
        self.conn = sqlite3.connect('prospector.db')
        self.cursor = self.conn.cursor()

        # create tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS base_passwords (
                password TEXT PRIMARY KEY
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_addresses (
                email TEXT PRIMARY KEY
            )
        ''')
        self.conn.commit()

    def run(self):
        with open(self.combo, 'r') as combo:
            print("Start extraction...", sep='\n')
            print("Note: This process may take a long time for very large combo files.")

            find_passwd = 0
            total_passwd = 0
            find_email = 0
            total_email = 0

            for line in combo:
                line = line.strip()
                email, passwd = line.split(':')[-2:]

                total_passwd += 1
                if self.check_password(passwd):
                    self.add_password(passwd)
                else:
                    find_passwd += 1

                total_email += 1
                if self.check_email(email):
                    self.add_email(email)
                else:
                    find_email += 1

            percentage_passwd = (find_passwd / total_passwd) * 100
            percentage_email = (find_email / total_email) * 100

            print("Extraction completed!", sep='\n')
            print("------------------------------Passwords-info------------------------------")
            print(f"{find_passwd} of the {total_passwd} pre-existing passwords have been found", sep='\n')
            print(f"Pre-existing passwords: {percentage_passwd:.2f}%\n")

            print("------------------------------Emails-info------------------------------")
            print(f"{find_email} of the {total_email} pre-existing emails have been found", sep='\n')
            print(f"Pre-existing emails: {percentage_email:.2f}%\n")

        def check_password(self, password):
            self.cursor.execute('SELECT password FROM base_passwords WHERE password=?', (password,))
            return self.cursor.fetchone() is not None

        def add_password(self, password):
            self.cursor.execute('INSERT INTO base_passwords VALUES (?)', (password,))
            self.conn.commit()

        def check_email(self, email):
            self.cursor.execute('SELECT email FROM email_addresses WHERE email=?', (email,))
            return self.cursor.fetchone() is not None

        def add_email(self, email):
            self.cursor.execute('INSERT INTO email_addresses VALUES (?)', (email,))
            self.conn.commit()

        def __del__(self):
            self.conn.close()

test = Prospector('extracted/336K UK.txt', 'test.txt', 'emails.txt')
test.run()