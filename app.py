import os
from dotenv import load_dotenv
from datetime import datetime
import json

from connectors.openai_connector import DigitalBrain
from connectors.calendar_connector import DigitalPlanner
from connectors.voice_recorder import VoiceRecorder
from connectors.whisper_connector import NoteTaker
from connectors.openai_tts import generate_speech, play_mp3
from connectors.gmail_connector import PostReceiver

load_dotenv()
current_calender = os.getenv("TEST_CALENDER")
current_datetime = datetime.now()
formatted_date = current_datetime.strftime("%A, %m %B %Y")
print(formatted_date)
event_template = '{ \
                    "summary": "summary", \
                    "location": "location", \
                    "description": "description", \
                    "start": { \
                        "dateTime": "0000-00-00T00:00:00", \
                        "timeZone": "Europe/Amsterdam", \
                    }, \
                    "end": { \
                        "dateTime": "0000-00-00T00:00:00", \
                        "timeZone": "Europe/Amsterdam", \
                    }, \
                    "reminders": { \
                        "useDefault": False, \
                        "overrides": [ \
                            {"method": "popup", "minutes": 60}, \
                        ], \
                    }, \
                }'

view_agenda_job = f"You are a master planner; today is {formatted_date}. I'm going to give you a list of my personal events. The list \
                contains: start day and time, end day and time, location, summary (which is the title of the event), and the description. \
                I'm going to ask you about them; please respond properly. The date format is day-month-year, and the time format is \
                hours:minutes. Please use natural language in your response regarding time and dates. That means you'll convert the \
                time format to time in AM and PM."

planner_job = f"You are a master planner for Google Calendar; today is {formatted_date}. I am going to ask you to plan events. Giving \
                you the summary, description, date, time, duration, and location. You will reply only in the format suitable for \
                Google Calendar API. Please make absolutely sure to only reply in the JSON text, so no additional context or formatting. \
                Use the following format: {event_template}. So once again, use only the provided format without further context."

mailsorter_job = f"You are an expert in sorting mail and have one job only. You will receive an email, and I want you to check the \
                content of this email to see if there is a: calendar event, task, action, reminder, vacation, or invitation. If there \
                is such an event, your reaction will only contain a summary of this event, including: 'start day and time, end day \
                and time, location, summary (which is the title of the event), and the description' which is the title of the event \
                and the description. If there is nothing regarding any events, then your reaction will only be 'no event detected,' \
                without further context."

virtual_assistant_agenda = DigitalBrain(view_agenda_job)
virtual_assistant_planner = DigitalBrain(planner_job)
virtual_assistant_mailsorter = DigitalBrain(mailsorter_job)
virtual_mail_man = PostReceiver()
calendar = DigitalPlanner(current_calender)

message_list = virtual_mail_man.retreive_messages("seen")

def mail_to_calendar():
    for message in message_list:
        mail_item = json.dumps(message)
        virtual_assistant_mailsorter.insert_data(mail_item)
        result = virtual_assistant_mailsorter.generate_response("Does this email contain an event?")
        if "no event detected" in result.lower():
            print("This mail contains no events.")

        else:
            print(result)
            print("This email contains an event.")
            event = virtual_assistant_planner.generate_response(result)
            print(event)
            calendar.create_event(event)

def fit_event(text):
    print("check planning:")
    events = calendar.get_events(current_calender, 50)
    virtual_assistant_agenda.insert_data_list(events)
    response = virtual_assistant_agenda.generate_response(text)
    print(response)
    generate_speech(response)
    play_mp3("speech.mp3")

if __name__ == "__main__":
    fit_event("get the current date and then I want you to plan a diner with friends in the next 2 weeks from 20:00 till 24:00 in \
              Amsterdam, do you have 5 suggestion dates that will suit for this event. Make sure the next day i don't have any \
              events planned due to hangover potential. Keep your responce short within 100 words maximum. Keep in mind I work \
              during the week from 9 till 5, and i need to sleep at least 8 hours, give me your preffered suggestion and explain \
              why this is your favorite, please.")
