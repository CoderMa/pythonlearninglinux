import yagmail
import configparser

config = configparser.ConfigParser()
config.read('..\\config\\config.ini')

try:

    email_address = config['EMAIL']['email_address']
    email_password = config['EMAIL']['email_password']
except Exception as e:
    email_address = "mjlei6025@gmail.com"
    email_password = "mjlei!@0051"



class Mailer:
    @staticmethod
    def send_email(subject, contents):
        yag = yagmail.SMTP(email_address, email_password)
        yag.send(to=email_address, subject=subject, contents=contents)
