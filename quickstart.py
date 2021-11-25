from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import date
import time
import os.path

today = date.today()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.coursework.students',
          'https://www.googleapis.com/auth/classroom.coursework.me.readonly']

dates = []


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])

    def make_list():
        for course in courses:
            course_id = course['id']
            results1 = service.courses().courseWork().list(courseId=course_id, orderBy='dueDate desc',
                                                           pageSize=2).execute()
            try:
                for courseWork in results1["courseWork"]:
                    try:
                        dueDate = courseWork['dueDate']
                        d3 = time.strptime(today.strftime("%d/%m/20%y"), "%d/%m/%Y")
                        duedates = str(dueDate['day']) + "/" + str(dueDate['month']) + "/" + str(dueDate['year'])
                        newdate1 = time.strptime(duedates, "%d/%m/%Y")
                        if d3 < newdate1:
                            dates.append([int((time.mktime(newdate1) - time.mktime(d3)) // 86400), str(courseWork['title']),
                                          str(courseWork['description']), str(courseWork['id'])])
                    except KeyError:
                        continue
            except KeyError:
                continue
        dates.sort()
        if len(dates) < 3:
            dates.append(['-', 'Take a break', 'BreakTime :)'])
            dates.append(['-', 'Take a break', 'BreakTime :)'])
            dates.append(['-', 'Take a break', 'BreakTime :)'])
    make_list()


if __name__ == '__main__':
    main()
