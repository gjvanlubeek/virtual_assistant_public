import os
from dotenv import load_dotenv
import imaplib
import smtplib

import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

EMAIL = os.getenv('GMAIL_ADRES')
PASSWORD = os.getenv('GMAIL_PASSWORD')

class PostSender:
    def __init__(self):
        self.message = MIMEMultipart()
        self.message['From'] = EMAIL
        self.__password = PASSWORD
        self.smtp_server = 'smtp.gmail.com'

    def add_message(self, to, subject, content):
        # Create the email message
        self.message['To'] = to
        self.message['Subject'] = subject
        self.message.attach(MIMEText(content, 'plain'))

    def send_message(self):
        # Connect to the Gmail SMTP server using SSL
        with smtplib.SMTP_SSL(self.smtp_server, 465) as server:
            # Log in to the Gmail account
            server.login(self.message['From'], self.__password)

            # Send the email
            server.sendmail(self.message['From'], self.message['To'], self.message.as_string())
        print("Message to " + self.message['To'] + " is sent successful")


class PostReceiver(object):
    def __init__(self):
        self.emailadres = EMAIL
        self.__password = PASSWORD
        self.imap_server = 'imap.gmail.com'

    def retreive_messages(self, sorted_by):
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.emailadres, self.__password)
            mail.select('inbox')

            status, data = mail.search(None, sorted_by)
            mail_ids = []
            sorted_mail = []
            mail_nr = 0

            for block in data:
                mail_ids += block.split()

            for i in mail_ids:
                status, data = mail.fetch(i, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        mail_nr += 1
                        mail_content = ''
                        message = email.message_from_bytes(response_part[1])

                        if message.is_multipart():
                            for part in message.walk():
                                if part.get_content_type() == 'text/plain':
                                    mail_content += part.get_payload(decode=True).decode("utf-8", "ignore")
                        else:
                            mail_content = message.get_payload()

                        email_data = {
                                'email': mail_nr,
                                'sender': message["from"],
                                'subject': message["subject"],
                                'date': message["date"],
                                'content': mail_content
                            }
                        
                        if len(email_data.get('content')) <= 8000:
                            sorted_mail.append(email_data)
                        
                        else:
                            email_data['content'] = "message is to long"
                            sorted_mail.append(email_data)

            if not sorted_mail:
                sorted_mail = {}

            return sorted_mail


if __name__ == '__main__':
    mail = PostReceiver()
    mailbag = mail.retreive_messages('unseen')
    print(mailbag)
