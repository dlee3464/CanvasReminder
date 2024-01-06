from pprint import pprint
from Google import create_service
from Google import convert_to_RFC_datetime

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def getCalId(id):
    return id

def makeEvent(startY, startM, startD, startH, startMin, endY, endM, endD, endH, endMin, summary, desc, calId):
    calendar_id = getCalId(calId)
    to_est = -5
    event_request_body = {
        'start': {
            'dateTime': convert_to_RFC_datetime(startY, startM, startD, startH + to_est, startMin),
            'timeZone': 'EST'
        },
        'end': {
            'dateTime': convert_to_RFC_datetime(endY, endM, endD, endH + to_est, endMin),
            'timeZone': 'EST'
        },
        'summary': summary,
        'desc': desc,
        'colorId': 5,
        'status': 'confirmed',
        'visibility': 'private'
    }

    sendNotifications = True
    sendUpdates = 'all'

    response = service.events().insert(
        calendarId= calendar_id,
        maxAttendees=5,
        sendNotifications=sendNotifications,
        sendUpdates=sendUpdates,
        supportsAttachments=True,
        body=event_request_body

    ).execute()