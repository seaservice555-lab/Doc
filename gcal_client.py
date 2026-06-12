import os, json
from datetime import datetime, date, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class GoogleCalendarClient:
    def __init__(self):
        self._service = None

    def _connect(self):
        if self._service:
            return
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as f:
                f.write(creds.to_json())
        self._service = build("calendar", "v3", credentials=creds)

    def add_event(self, title, date, time_start=None, time_end=None, all_day=False, description=""):
        self._connect()
        if all_day or not time_start:
            event = {"summary": title, "description": description,
                "start": {"date": date.strftime("%Y-%m-%d")},
                "end": {"date": (date + timedelta(days=1)).strftime("%Y-%m-%d")}}
        else:
            tz = os.environ.get("TIMEZONE", "Asia/Vladivostok")
            event = {"summary": title, "description": description,
                "start": {"dateTime": f"{date.strftime('%Y-%m-%d')}T{time_start}:00", "timeZone": tz},
                "end": {"dateTime": f"{date.strftime('%Y-%m-%d')}T{time_end}:00", "timeZone": tz}}
        return self._service.events().insert(calendarId="primary", body=event).execute().get("id", "")
