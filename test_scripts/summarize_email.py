import os
from dotenv import load_dotenv

from connectors.openai_connector import DigitalBrain
from connectors.gmail_connector import PostReceiver, PostSender
from connectors.list_maker import create_list

load_dotenv()
emailadres = os.getenv("PRIVATE_EMAIL")

va = DigitalBrain("Fungeren als een virtuele assistent genaamd Dorothy, die mijn e-mail zal afhandelen. Ik geef jou e-mailberichten en jij\
                  gaan ze voor mij samenvatten conform de speciefieke opgave.")

mail = PostReceiver()
check_mail = mail.retreive_messages('all')
mail_list = create_list(check_mail)

if not mail_list:
    print('no messages')

else:
    response = []
    for mail in mail_list:
        va.insert_data(mail)
        response.append(va.generate_response("vat dit berichten samen en geef specifieke informatie die belangrijk is voor de ontvanger de opbouw van de mail is als volgt:\
                                             afzender inclusief email, onderwerp van de email, samenvatting met specifieke informatie, concept mail voor dit bericht wat ik \
                                             kan versturen"))

text = ""
for message in response:
    text += message
    text += "\n"
    text += "---------------------------------------------------------"
    text += "\n"

reply = PostSender()
reply.add_message(emailadres, 'overview of ' + str(len(mail_list)) + ' messages', text)
reply.send_message()