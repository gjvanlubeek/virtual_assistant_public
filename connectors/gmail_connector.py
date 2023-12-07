import os
from dotenv import load_dotenv
import imaplib
import email

load_dotenv()

EMAIL = os.getenv('GMAIL_ADRES')
PASSWORD = os.getenv('GMAIL_PASSWORD')

class PostReceiver:
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
                            for part in message.get_payload():
                                if part.get_content_type() == 'text/plain':
                                    mail_content += part.get_payload()
                        else:
                            mail_content = message.get_payload()

                        email_data = f'email: {mail_nr}, sender: {message["from"]}, subject: {message["subject"]}, date: {message["date"]}, content: {mail_content}'
                        if len(email_data) <= 4000:
                            sorted_mail.append(email_data)
                        
                        else:
                            sorted_mail.append(f'email: {mail_nr}, sender: {message["from"]}, subject: {message["subject"]}, date: {message["date"]}, content: Message is to long!')

            if not sorted_mail:
                sorted_mail = []

            return sorted_mail
    

if __name__ == '__main__':
    mail = PostReceiver()
    messages = mail.retreive_messages('UNSEEN')
    for i in messages:
        print(i)