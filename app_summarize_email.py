from connectors.openai_connector import DigitalBrain
from connectors.gmail_connector import PostReceiver, PostSender
from connectors.list_maker import create_list
import os
from dotenv import load_dotenv

load_dotenv()

PRIVATE_EMAIL = EMAIL = os.getenv('PRIVATE_EMAIL')


va = DigitalBrain("Act as a virtual assistant named Dorothy, tasked with reviewing emails and \
                  summarizing specific details within the email. Additionally, you excel at \
                  crafting concise and playful responses to emails. Always use the native \
                  language from the sender's email")

mail = PostReceiver()
check_mail = mail.retreive_messages('unseen')
mail_list = create_list(check_mail)

if not mail_list:
    print('no messages')

else:
    response = []
    for mail in mail_list:
        va.insert_data(mail)
        response.append(va.generate_response("Summarize the provided email message in bullet points, using the \
                                             native language from the sender's email. Descibe specific and detailed \
                                             information always start by senders emailadres, the name of the sender date and \
                                             than the content. Additionally, create a short draft email response use \
                                             a cheecky tone of voice. Always end the draft email with 'Groeten \
                                             Dorothy, \n Virtual assistant van Gert-Jan van Lubeek.'"))
    
    dashed_line = "-" * 50  # Create a dashed line with 30 dashes
    message = f"\n\n{dashed_line}\n\n".join(response)

    reply = PostSender()
    reply.add_message(PRIVATE_EMAIL, 'overview of ' + str(len(mail_list)) + ' messages', message)
    reply.send_message()