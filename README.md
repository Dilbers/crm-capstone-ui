# CRM Capstone — UI Prototype

This project implements the interface-design milestone only. It contains
separate windows for login, regular and admin preferences, applications,
mentor interviews, interviews, and the admin menu.

Navigation is wired between windows. Search, filtering, Google Drive/Calendar,
and mail actions are placeholders; there is no backend or persistent storage.

For the demo, enter `admin` as the username to open the admin preferences
window. Any other username opens regular preferences. The password is not
validated.

## Run on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```
