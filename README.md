# CRM Capstone — UI Prototype

This project implements the interface-design milestone only. Its screens are
defined in `crm_interface.ui`, an XML form that can be opened and edited with
Qt Designer. `main.py` loads that form and connects its buttons and navigation.
It contains login, regular and admin preferences, applications, mentor
interviews, interviews, and the admin menu.

Navigation is wired between windows. Search, filtering, Google Drive/Calendar,
and mail actions are placeholders; there is no backend or persistent storage.

For the demo, enter `admin` as the username to open the admin preferences
window. Any other username opens regular preferences. The password is not
validated.

To edit the visual layout, open `crm_interface.ui` in Qt Designer, save it, and
run the application again. The application requires PyQt6, not Qt Designer, to
run.

## Run on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```
