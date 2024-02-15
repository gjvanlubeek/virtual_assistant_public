import datetime
import os
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class DigitalPlanner(object):
    def __init__(self, calender):
        self.scopes = ["https://www.googleapis.com/auth/calendar"]
        self.calender = calender
        
        self.creds = None
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.scopes)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        self.service = build("calendar", "v3", credentials=self.creds)

    def get_events(self, calendar_name, max_results=10):
        upcomming_events = []
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = self.service.events().list(
            calendarId=calendar_name,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        else:
            for event in events:
                start_time_str = event['start'].get('dateTime', event['start'].get('date'))
                end_time_str = event['end'].get('dateTime', event['end'].get('date'))

                # Attempt to convert the strings to datetime objects
                start_time = datetime.datetime.fromisoformat(start_time_str)
                end_time = datetime.datetime.fromisoformat(end_time_str)

                # Format the datetime objects
                formatted_start_time = start_time.strftime('%d-%m-%Y %H:%M')
                formatted_end_time = end_time.strftime('%d-%m-%Y %H:%M')

                # Check if the event spans multiple days
                if start_time.date() != end_time.date():
                    formatted_start_time = start_time.strftime('%d-%m-%Y')
                    formatted_end_time = end_time.strftime('%d-%m-%Y')
                else:
                    formatted_start_time = start_time.strftime('%d-%m-%Y %H:%M')
                    formatted_end_time = end_time.strftime('%H:%M')

                upcomming_events.append(f'Start: {formatted_start_time} - End: {formatted_end_time} - Summary: {event["summary"]} - Location: {event.get("location", "No location available")} - Content: {event.get("description", "No description available")}')
        
        return upcomming_events

    def create_event(self, event_json):
        event = json.loads(event_json)
        event = self.service.events().insert(calendarId=self.calender, body=event).execute()

    def delete_calendar(self, calendar_id):
        self.service.calendars().delete(calendarId=calendar_id).execute()

    def create_calendar(self, name):
        calendar = {'summary': name, 'timeZone': 'Europe/Amsterdam'}
        self.service.calendars().insert(body=calendar).execute()

if __name__ == "__main__":
    calendar = DigitalPlanner()
    calendar.create_calendar("test-calendar")
    
