from connectors.openai_connector import DigitalBrain
from connectors.gmail_connector import PostReceiver, PostSender
from connectors.list_maker import create_list

va = DigitalBrain("Act as a virtual assistant, named Dorothy, that reviews emails and summarizes specific details \
                  within the email.")

mail = PostReceiver()
check_mail = mail.retreive_messages('seen')
mail_list = create_list(check_mail)

if not mail_list:
    print('no messages')

else:
    response = []
    for mail in mail_list:
        va.insert_data(mail)
        response.append(va.generate_response("please summarize this email in the native language in bullets and descibe specific and detailed information \
                                             always start bij specifing sender + emailadres, date and than the content. then create a draft as a reply in \
                                             dutch use a little cheecky tone of voice, ending with 'met vriendelijke groet \
                                             Dorothy, \n Virtual assistant van Gert-Jan van Lubeek'"))
    
    dashed_line = "-" * 50  # Create a dashed line with 30 dashes
    message = f"\n\n{dashed_line}\n\n".join(response)

    reply = PostSender()
    reply.add_message('gert-jan@vanlubeek.com', 'overview of ' + str(len(mail_list)) + ' messages', message)
    reply.send_message()