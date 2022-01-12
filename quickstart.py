# imports
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import date
import time
import os

# Scopes that the user must accept to give permission to use and modify data for
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.coursework.students',
          'https://www.googleapis.com/auth/classroom.coursework.me.readonly']
dates = []


# User authentication for Google Classroom
def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the
    # authorization flow completes for the first time
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                os.remove("token.json")
                main()
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save user credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('classroom', 'v1', credentials=creds)
    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    # Get list of courses user is enrolled in
    courses = results.get('courses', [])

    def make_list():
        for course in courses:
            course_id = course['id']
            # Make a list of all homework tasks that user has for each course in descending order of due date
            results1 = service.courses().courseWork().list(courseId=course_id, orderBy='dueDate desc').execute()
            try:
                for courseWork in results1["courseWork"]:
                    try:
                        # Calculate how many days until the homework task needs to be submitted
                        # Get today's date
                        today = date.today()
                        # Get date of homework task
                        dueDate = courseWork['dueDate']
                        # convert both dates into a usable format
                        d3 = time.strptime(today.strftime("%d/%m/20%y"), "%d/%m/%Y")
                        duedates = str(dueDate['day']) + "/" + str(dueDate['month']) + "/" + str(dueDate['year'])
                        newdate1 = time.strptime(duedates, "%d/%m/%Y")
                        # If the homework is past its due date do not add it to the list
                        if d3 < newdate1:
                            # Subtract current date from homework date to find time between dates in seconds
                            # then divide by the number of seconds in a day to find the number of days between
                            # now and the homework due date
                            days = int((time.mktime(newdate1) - time.mktime(d3)) // 86400)
                            dates.append([days, str(courseWork['title']), str(courseWork['description']),
                                          str(courseWork['id'])])
                    # Try Except block for if classroom has no homework tasks with due dates or if classroom has been
                    # deactivated
                    except KeyError:
                        continue
            # Try Except block for if classroom has no homework tasks
            except KeyError:
                continue
        # sort list of dates
        dates.sort()
        # If user does not have enough homework tasks add break times to put in timetable
        if len(dates) < 3:
            dates.append(['-', 'Take a break', 'BreakTime :)'])
            dates.append(['-', 'Take a break', 'BreakTime :)'])
            dates.append(['-', 'Take a break', 'BreakTime :)'])

    make_list()


if __name__ == '__main__':
    main()
