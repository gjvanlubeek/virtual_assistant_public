import os
from dotenv import load_dotenv
from datetime import datetime

from connectors.openai_connector import DigitalBrain
from connectors.calendar_connector import DigitalPlanner
from connectors.voice_recorder import VoiceRecorder
from connectors.whisper_connector import NoteTaker
from connectors.openai_tts import generate_speech, play_mp3

load_dotenv()
calendar_starc = os.getenv("STARC_CALENDER")
current_datetime = datetime.now()
formatted_date = current_datetime.strftime("%d-%m-%Y")
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

view_agenda_job = f"You are a master planner , today is {formatted_date}, i'm going to give you a list of my personal events, the list \
                contains: start day and time, end day and time, location, summary which is the title of the event and the content. I'm going \
                to ask you about them, please respond properly the date format is day-month-year and the time format is hours:minutes. \
                please use natural language in your respond regarding time and dates. that means that you'll convert time format to \
                time in am and pm"

planner_job = f"You are a master planner for google calendar, today is {formatted_date}. I am gooing to ask you to plan events. \
                Giving you the summary, description, date, time, duration and location. You will repley only in the format suitable \
                for google calendar API. Please make absolutly sure to only repley the json tekst, so no additional context of formatting,\
                use the following format . Here is the format: {event_template}"

virtual_assistant_agenda = DigitalBrain(view_agenda_job)
virtual_assistant_planner = DigitalBrain(planner_job)
calendar = DigitalPlanner()

print("create event:")

recorder = VoiceRecorder(10)

recorder.record_voice()
file = NoteTaker('output.wav')
text = file.write_speech()

if "check planning" in text.lower():
    print("check planning:")
    recorder.record_voice()
    file = NoteTaker('output.wav')
    text = file.write_speech()
    events = calendar.get_events(calendar_starc, 10)
    virtual_assistant_agenda.insert_data_list(events)
    response = virtual_assistant_agenda.generate_response(text)
    generate_speech(response)
    play_mp3("speech.mp3")

elif "create event" in text.lower():
    print("create event:")
    recorder.record_voice()
    file = NoteTaker('output.wav')
    text = file.write_speech()
    event = virtual_assistant_planner.generate_response(text)
    print(event)
    calendar.create_event(event)

else:
    pass

print("end programm")



