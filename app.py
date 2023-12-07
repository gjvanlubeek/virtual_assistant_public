from connectors.openai_connector import DigitalBrain
from connectors.gmail_connector import PostReceiver
from connectors.openai_tts import generate_speech, play_mp3

va = DigitalBrain("Act as a virtual assistant named Dorothy and always reply in English, no more than 50 words. \
                  You'll receive a list of emails, and I want you to inform me about this.")

mail = PostReceiver()
check_mail = mail.retreive_messages('unseen')

if not check_mail:
    response = va.generate_response('Please let me know there are no new emails')

else:
    va.insert_data(check_mail)
    response = va.generate_response('Please summarize my emails')

print(response)

# generate_speech(response)
play_mp3('speech.mp3')