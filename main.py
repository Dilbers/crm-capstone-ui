import sys
from pathlib import Path

from PyQt6 import QtCore, QtWidgets, uic


class CRMPrototype(QtWidgets.QMainWindow):
    COLORS = {
        "login": "#5B61D6",
        "preferences": "#168A83",
        "preferences_admin": "#A35BB5",
        "applications": "#3478C8",
        "mentor": "#E28A3B",
        "interviews": "#298C68",
        "admin": "#C45665",
    }

    PAGES = {
        "login": "loginPage",
        "preferences": "preferencesPage",
        "preferences_admin": "adminPreferencesPage",
        "applications": "applicationsPage",
        "mentor": "mentorPage",
        "interviews": "interviewsPage",
        "admin": "adminMenuPage",
    }

    def __init__(self, app: QtWidgets.QApplication) -> None:
        super().__init__()
        self.app = app
        self.is_admin = False
        ui_path = Path(__file__).with_name("crm_interface.ui")
        uic.loadUi(str(ui_path), self)
        self._configure_layouts()
        self._configure_tables()
        self._connect_actions()
        self._show("login")

    def _apply_style(self, key: str) -> None:
        accent = self.COLORS[key]
        self.setStyleSheet(
            f"""
            QMainWindow, QWidget#centralwidget {{
                background: #F3F5F9;
            }}
            QWidget {{
                color: #202A3A; font-family: "Segoe UI", sans-serif;
                font-size: 13px;
            }}
            QFrame#loginCard, QFrame#preferencesTopBar,
            QFrame#adminPreferencesTopBar, QFrame#applicationsTopBar,
            QFrame#mentorTopBar, QFrame#interviewsTopBar, QFrame#adminTopBar,
            QFrame#preferencesCard, QFrame#adminPreferencesCard,
            QFrame#applicationsCard, QFrame#mentorCard,
            QFrame#interviewsCard, QFrame#adminCard {{
                background: #FFFFFF; border: 1px solid #E4E8F0;
                border-radius: 14px;
            }}
            QFrame#preferencesTopBar, QFrame#adminPreferencesTopBar,
            QFrame#applicationsTopBar, QFrame#mentorTopBar,
            QFrame#interviewsTopBar, QFrame#adminTopBar {{
                border-radius: 11px;
            }}
            QWidget#loginPage {{ background: #F0F2FF; }}
            QFrame#loginHeroPanel {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #514BCB, stop:0.55 #6256D9, stop:1 #278C9A);
                border: none; border-radius: 18px;
            }}
            QLabel#loginHeroBrand {{
                color: #DCD9FF; font-size: 12px; font-weight: 700;
                letter-spacing: 1px;
            }}
            QLabel#loginHeroTitle {{
                color: #FFFFFF; font-size: 32px; font-weight: 700;
            }}
            QLabel#loginHeroBody {{
                color: #E7E7FF; font-size: 14px; line-height: 1.4;
            }}
            QLabel#loginHeroFooter {{
                color: #DCD9FF; font-size: 10px; font-weight: 600;
            }}
            QFrame#loginCard {{
                border: 1px solid #E4E7F2; border-radius: 18px;
            }}
            QPushButton#applicationsNavButton,
            QPushButton#adminApplicationsNavButton {{
                background: #F0F5FD; color: #315F96; border: 1px solid #DFE9F7;
                border-radius: 11px; text-align: left; padding: 17px 20px;
                font-size: 15px; font-weight: 700;
            }}
            QPushButton#applicationsNavButton:hover,
            QPushButton#adminApplicationsNavButton:hover {{
                background: #E8F0FB; border-color: #B6CBE8; color: #20558F;
            }}
            QPushButton#mentorNavButton,
            QPushButton#adminMentorNavButton {{
                background: #FBF4ED; color: #94603B; border: 1px solid #F0E3D5;
                border-radius: 11px; text-align: left; padding: 17px 20px;
                font-size: 15px; font-weight: 700;
            }}
            QPushButton#mentorNavButton:hover,
            QPushButton#adminMentorNavButton:hover {{
                background: #F7EBDD; border-color: #E4C8AA; color: #8F4518;
            }}
            QPushButton#interviewsNavButton,
            QPushButton#adminInterviewsNavButton {{
                background: #EFF6F2; color: #34715A; border: 1px solid #DCEBE2;
                border-radius: 11px; text-align: left; padding: 17px 20px;
                font-size: 15px; font-weight: 700;
            }}
            QPushButton#interviewsNavButton:hover,
            QPushButton#adminInterviewsNavButton:hover {{
                background: #E5F1EA; border-color: #B9D7C5; color: #1C6245;
            }}
            QPushButton#adminMenuNavButton {{
                background: #F5F1F8; color: #745885; border: 1px solid #E9E1EF;
                border-radius: 11px; text-align: left; padding: 17px 20px;
                font-size: 15px; font-weight: 700;
            }}
            QPushButton#adminMenuNavButton:hover {{
                background: #EEE7F3; border-color: #D3C2DE; color: #63358A;
            }}
            QLabel#preferencesBrand, QLabel#adminPreferencesBrand,
            QLabel#applicationsBrand, QLabel#mentorBrand,
            QLabel#interviewsBrand, QLabel#adminBrand {{
                color: {accent}; font-size: 12px; font-weight: 700;
                letter-spacing: 0.5px;
            }}
            QLabel#preferencesTitle, QLabel#adminPreferencesTitle,
            QLabel#applicationsTitle, QLabel#mentorTitle,
            QLabel#interviewsTitle, QLabel#adminTitle,
            QLabel#loginTitle {{
                color: #172033; font-size: 27px; font-weight: 700;
            }}
            QLabel#preferencesSubtitle, QLabel#adminPreferencesSubtitle,
            QLabel#applicationsSubtitle, QLabel#mentorSubtitle,
            QLabel#interviewsSubtitle, QLabel#adminSubtitle {{
                color: #737F91; font-size: 13px;
            }}
            QLabel#preferencesDemoLabel, QLabel#adminPreferencesDemoLabel,
            QLabel#applicationsDemoLabel, QLabel#mentorDemoLabel,
            QLabel#interviewsDemoLabel, QLabel#adminDemoLabel,
            QLabel#loginHelper {{
                color: #8791A1; font-size: 11px;
            }}
            QLineEdit, QComboBox {{
                background: #FFFFFF; color: #273246; border: 1px solid #DDE3EC;
                border-radius: 8px; padding: 10px 12px; min-height: 22px;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border: 1px solid {accent}; background: #FFFFFF;
            }}
            QComboBox::drop-down {{ border: none; width: 28px; }}
            QPushButton {{
                background: #FFFFFF; color: #465266; border: 1px solid #DDE3EC;
                border-radius: 8px; padding: 10px 15px; font-weight: 600;
            }}
            QPushButton:hover {{
                background: #F7F8FB; border-color: #B9C3D2; color: #29364A;
            }}
            QPushButton:pressed {{
                background: #E8ECF3; border-color: #CBD3DF; color: #202A3A;
            }}
            QPushButton#loginButton, QPushButton#applicationsSearchButton,
            QPushButton#mentorSearchButton, QPushButton#interviewsSearchButton,
            QPushButton#allConversationsButton, QPushButton#projectSentButton,
            QPushButton#eventRecordButton {{
                background: #354A69; color: #FFFFFF; border: 1px solid #354A69;
            }}
            QPushButton#loginButton:hover, QPushButton#applicationsSearchButton:hover,
            QPushButton#mentorSearchButton:hover, QPushButton#interviewsSearchButton:hover,
            QPushButton#allConversationsButton:hover, QPushButton#projectSentButton:hover,
            QPushButton#eventRecordButton:hover {{
                background: #263B58; border-color: #263B58;
            }}
            QPushButton#loginButton {{
                background: #5B61D6; border: none; border-radius: 8px;
                color: #FFFFFF; font-size: 14px; font-weight: 700;
            }}
            QPushButton#loginButton:hover {{ background: #484FC0; }}
            QPushButton#closeButton {{ color: #8A4E57; }}
            QPushButton#closeButton:hover {{
                background: #FBF1F2; border-color: #E7C9CD; color: #85444D;
            }}
            QTableWidget {{
                background: #FFFFFF; alternate-background-color: #F8F9FC;
                color: #344054; border: 1px solid #E4E8F0; border-radius: 10px;
                gridline-color: #EEF1F5; selection-background-color: #E9EEF6;
                selection-color: #1F2937; outline: 0;
            }}
            QTableWidget::item {{ padding: 9px; border: none; }}
            QHeaderView::section {{
                background: #F3F5F9; color: #667286; padding: 11px 9px;
                border: none; border-bottom: 1px solid #E6EAF0;
                font-size: 11px; font-weight: 700;
            }}
            QStatusBar {{
                background: #FFFFFF; color: #647084;
                border-top: 1px solid #E7EAF0;
            }}
            """
        )

    def _configure_layouts(self) -> None:
        for name in (
            "preferencesLayout",
            "adminPreferencesLayout",
            "applicationsLayout",
            "mentorLayout",
            "interviewsLayout",
            "adminMenuLayout",
        ):
            layout = self.findChild(QtWidgets.QLayout, name)
            if layout is not None:
                layout.setContentsMargins(8, 6, 8, 6)
                layout.setSpacing(16)

        for name in (
            "preferencesCardLayout",
            "adminPreferencesCardLayout",
            "applicationsCardLayout",
            "mentorCardLayout",
            "interviewsCardLayout",
            "adminCardLayout",
        ):
            layout = self.findChild(QtWidgets.QLayout, name)
            if layout is not None:
                layout.setContentsMargins(22, 20, 22, 20)
                layout.setSpacing(16)

        for name in (
            "preferencesTopBarLayout",
            "adminPreferencesTopBarLayout",
            "applicationsTopBarLayout",
            "mentorTopBarLayout",
            "interviewsTopBarLayout",
            "adminTopBarLayout",
        ):
            layout = self.findChild(QtWidgets.QLayout, name)
            if layout is not None:
                layout.setContentsMargins(17, 11, 17, 11)
                layout.setSpacing(10)

        for name in (
            "applicationsTopBar",
            "adminTopBar",
            "mentorTopBar",
            "interviewsTopBar",
            "preferencesTopBar",
            "adminPreferencesTopBar",
        ):
            bar = self.findChild(QtWidgets.QFrame, name)
            if bar is not None:
                bar.setMinimumHeight(48)

        for name in ("mentorHelper", "interviewsHelper"):
            label = self.findChild(QtWidgets.QLabel, name)
            if label is not None:
                label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                label.setMinimumHeight(60)

    def _configure_tables(self) -> None:
        for table in (self.applicationsTable, self.eventsTable):
            table.setAlternatingRowColors(True)
            table.setShowGrid(False)
            table.setWordWrap(False)
            table.setMinimumHeight(220)
            table.setEditTriggers(
                QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
            )
            table.setSelectionBehavior(
                QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
            )
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.ResizeMode.Stretch
            )

    def _connect_actions(self) -> None:
        self.loginButton.clicked.connect(self._login)
        for button in (
            self.loginCloseButton,
            self.preferencesCloseButton,
            self.adminPreferencesCloseButton,
            self.adminExitButton,
        ):
            button.clicked.connect(self.close)

        for button, page in (
            (self.applicationsNavButton, "applications"),
            (self.adminApplicationsNavButton, "applications"),
            (self.mentorNavButton, "mentor"),
            (self.adminMentorNavButton, "mentor"),
            (self.interviewsNavButton, "interviews"),
            (self.adminInterviewsNavButton, "interviews"),
            (self.adminMenuNavButton, "admin"),
        ):
            button.clicked.connect(lambda _checked=False, target=page: self._show(target))

        for button in (
            self.applicationsReturnButton,
            self.mentorReturnButton,
            self.interviewsReturnButton,
            self.adminReturnButton,
        ):
            button.clicked.connect(self._go_preferences)

        self.applicationsSearchButton.clicked.connect(
            lambda: self._show_placeholder("Search is a placeholder in this UI-only milestone.")
        )
        self.mentorSearchButton.clicked.connect(
            lambda: self._show_placeholder("Search is a placeholder in this UI-only milestone.")
        )
        self.interviewsSearchButton.clicked.connect(
            lambda: self._show_placeholder("Search is a placeholder in this UI-only milestone.")
        )
        for button, label in (
            (self.allApplicationsFilter, "All Applications"),
            (self.mentorDefinedFilter, "Mentor Meeting Defined"),
            (self.mentorNotDefinedFilter, "Mentor Meeting Not Defined"),
        ):
            button.clicked.connect(
                lambda _checked=False, text=label: self._show_placeholder(
                    f"{text} filter is a placeholder."
                )
            )

    def _show(self, key: str) -> None:
        page = self.findChild(QtWidgets.QWidget, self.PAGES[key])
        if page is None:
            raise RuntimeError(f"UI page not found: {self.PAGES[key]}")
        self.pageStack.setCurrentWidget(page)
        title = {
            "login": "Welcome back",
            "preferences": "Preferences",
            "preferences_admin": "Preferences — Admin",
            "applications": "Applications",
            "mentor": "Mentor Interview",
            "interviews": "Interviews",
            "admin": "Admin Menu",
        }[key]
        self.setWindowTitle(f"CRM • {title}")
        self._apply_style(key)

    def _login(self) -> None:
        self.is_admin = self.usernameInput.text().strip().casefold() == "admin"
        self._show("preferences_admin" if self.is_admin else "preferences")

    def _go_preferences(self) -> None:
        self._show("preferences_admin" if self.is_admin else "preferences")

    def _show_placeholder(self, message: str) -> None:
        self.statusBar().showMessage(message, 4000)


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("CRM Interface Prototype")
    prototype = CRMPrototype(app)
    prototype.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
