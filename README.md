# ReviseTime

A desktop revision planner for IB Diploma students, built with Python, Kivy/KivyMD and SQLite as my IB Computer Science Internal Assessment (2021–22).

ReviseTime builds a daily study timetable around school hours. It fills the slots with homework pulled from Google Classroom, your own to-do items, IA work and revision subjects it picks from your six IB subjects.

## Features

- **Daily timetable (Main Menu):** an afternoon/evening plan that mixes in:
  - Google Classroom homework, soonest deadline first
  - to-do items
  - an IA slot and two revision slots, re-chosen from your subjects each day
- **Weekly timetable:** a Monday–Sunday view of the week's schedule.
- **Google Classroom integration:** signs in with OAuth and reads your courses and coursework through the Classroom API. Assignments that are past their due date are skipped. If there's too little homework, the gaps are filled with breaks.
- **To-do list:** add tasks with a due date. Tasks are ordered by days remaining (held in a linked list) and removed automatically once the deadline passes.
- **Test dates:** record upcoming tests, kept sorted by date.
- **Study timer:** 15, 30 or 60-minute countdowns that ring a bell when they finish.
- **Accounts and settings:**
  - sign-up with your name, email, password and your 3 HL + 3 SL subjects
  - edit your details later
  - adjust the alarm volume

## Tech stack

| Area | Used |
|---|---|
| UI | Kivy + KivyMD (`kivy.kv` for layouts) |
| Storage | SQLite (`ReviseTime.db`), plain text (`Dates.txt`) |
| Integration | Google Classroom API via `google-api-python-client` and `google-auth-oauthlib` |

## Getting started

### 1. Install dependencies

```bash
git clone https://github.com/Onafuwadav/ReviseTime.git
cd ReviseTime
pip install -r requirements.txt
```

The app was written against **KivyMD 0.104.x**. It imports `kivymd.uix.picker`, which was renamed in KivyMD 1.0, so newer versions won't run it without changes.

### 2. Set up Google Classroom credentials

The app connects to Google Classroom at startup, so it needs an OAuth client of your own. No credentials are included in this repo.

1. In the [Google Cloud Console](https://console.cloud.google.com/), create a project and enable the **Google Classroom API**.
2. Set up the OAuth consent screen and add your Google account as a test user.
3. Under **APIs & Services → Credentials**, create an **OAuth client ID** of type **Desktop app**.
4. Download the JSON file and save it as `credentials.json` in the project folder. See `credentials.example.json` for the expected format.

The first time you run the app, a browser window opens so you can sign in. Your access token is then saved to `token.json`. Both `credentials.json` and `token.json` are git-ignored, so keep them on your computer and never commit them.

### 3. Run

```bash
python ReviseTime.py
```

### Demo login

The bundled `ReviseTime.db` contains a sample account. These are local demo details only:

- Email: `Admin@outlook.com`
- Password: `admin123`

## Project structure

```
ReviseTime.py      # App, screens and logic
kivy.kv            # UI layouts
quickstart.py      # Google Classroom sign-in and homework fetch
ReviseTime.db      # SQLite database (account, subjects, to-dos)
Dates.txt          # Stored test dates
bell.wav, *.ttf    # Timer sound and Poppins fonts
```

## Known limitations

- It's a single-user app: the database holds one account at a time.
- Passwords are stored in plain text in the local SQLite database. That's fine for a local demo, but not something to reuse for real accounts.
- Timetable hours are fixed around a school day.
