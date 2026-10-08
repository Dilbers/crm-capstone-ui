import sys
from collections.abc import Callable

from PyQt6 import QtCore, QtWidgets


class CRMPrototype:
    COLORS = {
        "login": "#5B61D6",
        "preferences": "#168A83",
        "preferences_admin": "#A35BB5",
        "applications": "#3478C8",
        "mentor": "#E28A3B",
        "interviews": "#298C68",
        "admin": "#C45665",
    }

    def __init__(self, app: QtWidgets.QApplication) -> None:
        self.app = app
        self.is_admin = False
        self.windows: dict[str, QtWidgets.QMainWindow] = {}
        self._build_login()
        self._build_preferences(admin=False)
        self._build_preferences(admin=True)
        self._build_applications()
        self._build_mentor_interview()
        self._build_interviews()
        self._build_admin_menu()

    def _make_window(
        self, key: str, title: str, subtitle: str
    ) -> tuple[QtWidgets.QMainWindow, QtWidgets.QVBoxLayout]:
        accent = self.COLORS[key]
        window = QtWidgets.QMainWindow()
        window.setWindowTitle(f"CRM • {title}")
        window.resize(1080, 720)
        window.setMinimumSize(820, 580)
        window.setStyleSheet(
            f"""
            QMainWindow {{ background: #F4F6FA; }}
            QWidget#pageRoot {{ background: #F4F6FA; color: #202A3A;
                               font-family: "Segoe UI", sans-serif; }}
            QFrame#topBar {{ background: #FFFFFF; border: 1px solid #E7EAF0;
                             border-radius: 12px; }}
            QLabel#brand {{ color: {accent}; font-size: 13px; font-weight: 700; }}
            QLabel#pageTitle {{ color: #172033; font-size: 25px; font-weight: 700; }}
            QLabel#pageSubtitle {{ color: #7A8496; font-size: 12px; }}
            QLabel#sectionCaption {{ color: #4A5568; font-size: 13px;
                                     font-weight: 600; }}
            QLabel#helperText {{ color: #8993A3; font-size: 11px; }}
            QFrame#contentCard {{ background: #FFFFFF; border: 1px solid #E7EAF0;
                                  border-radius: 12px; }}
            QLineEdit, QComboBox {{ background: #FFFFFF; color: #273246;
                                  border: 1px solid #DFE4EC; border-radius: 7px;
                                  padding: 10px 11px; min-height: 20px; }}
            QLineEdit:focus, QComboBox:focus {{ border: 1px solid {accent}; }}
            QPushButton {{ background: #FFFFFF; color: #465266;
                           border: 1px solid #DFE4EC; border-radius: 7px;
                           padding: 10px 15px; font-weight: 600; }}
            QPushButton:hover {{ background: #F5F7FA; border-color: {accent};
                                 color: {accent}; }}
            QPushButton:pressed {{ background: {accent}; color: #FFFFFF; }}
            QPushButton#primaryButton {{ background: {accent}; color: #FFFFFF;
                                         border: 1px solid {accent}; }}
            QPushButton#primaryButton:hover {{ background: #263C55;
                                               border-color: #263C55; }}
            QPushButton#closeButton {{ color: #8A4E57; }}
            QTableWidget {{ background: #FFFFFF; alternate-background-color: #FAFBFD;
                            color: #344054; border: 1px solid #E6EAF0;
                            border-radius: 8px; gridline-color: #EEF1F5;
                            selection-background-color: #E8EDF8;
                            selection-color: #1F2937; }}
            QTableWidget::item {{ padding: 8px; border: none; }}
            QHeaderView::section {{ background: #F7F8FB; color: #687386;
                                    padding: 10px 8px; border: none;
                                    border-bottom: 1px solid #E6EAF0;
                                    font-size: 11px; font-weight: 600; }}
            """
        )

        central = QtWidgets.QWidget()
        central.setObjectName("pageRoot")
        outer = QtWidgets.QVBoxLayout(central)
        outer.setContentsMargins(28, 24, 28, 24)
        outer.setSpacing(18)
        window.setCentralWidget(central)

        top_bar = QtWidgets.QFrame()
        top_bar.setObjectName("topBar")
        top_layout = QtWidgets.QHBoxLayout(top_bar)
        top_layout.setContentsMargins(18, 13, 18, 13)
        brand = QtWidgets.QLabel("CRM  /  INTERFACE PROTOTYPE")
        brand.setObjectName("brand")
        top_layout.addWidget(brand)
        top_layout.addStretch()
        demo = QtWidgets.QLabel("UI DEMO  •  NO BACKEND")
        demo.setObjectName("helperText")
        top_layout.addWidget(demo)
        outer.addWidget(top_bar)

        heading = QtWidgets.QLabel(title)
        heading.setObjectName("pageTitle")
        outer.addWidget(heading)
        description = QtWidgets.QLabel(subtitle)
        description.setObjectName("pageSubtitle")
        outer.addWidget(description)

        self.windows[key] = window
        return window, outer

    @staticmethod
    def _card() -> tuple[QtWidgets.QFrame, QtWidgets.QVBoxLayout]:
        card = QtWidgets.QFrame()
        card.setObjectName("contentCard")
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(14)
        return card, layout

    @staticmethod
    def _button(
        text: str,
        callback: Callable[[], None] | None = None,
        *,
        primary: bool = False,
        close: bool = False,
    ) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(text)
        if primary:
            button.setObjectName("primaryButton")
        if close:
            button.setObjectName("closeButton")
            button.clicked.connect(QtWidgets.QApplication.instance().quit)
        elif callback is not None:
            button.clicked.connect(callback)
        return button

    @staticmethod
    def _table(headers: tuple[str, ...]) -> QtWidgets.QTableWidget:
        table = QtWidgets.QTableWidget(0, len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )
        return table

    def _show(self, key: str) -> None:
        for name, window in self.windows.items():
            if name != key:
                window.hide()
        target = self.windows[key]
        target.show()
        target.raise_()
        target.activateWindow()

    def _go_preferences(self) -> None:
        self._show("preferences_admin" if self.is_admin else "preferences")

    def _build_login(self) -> None:
        window, outer = self._make_window(
            "login",
            "Welcome back",
            "Sign in to continue to the CRM workspace.",
        )
        outer.setContentsMargins(90, 34, 90, 38)
        outer.addStretch(1)
        card, layout = self._card()
        layout.addWidget(QtWidgets.QLabel("Username"))
        username = QtWidgets.QLineEdit()
        username.setObjectName("usernameInput")
        username.setPlaceholderText("Enter your username")
        layout.addWidget(username)
        layout.addWidget(QtWidgets.QLabel("Password"))
        password = QtWidgets.QLineEdit()
        password.setObjectName("passwordInput")
        password.setPlaceholderText("Enter your password")
        password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        layout.addWidget(password)
        warning = QtWidgets.QLabel("Demo only: credentials are not checked.")
        warning.setObjectName("helperText")
        warning.setWordWrap(True)
        layout.addWidget(warning)

        def login() -> None:
            self.is_admin = username.text().strip().casefold() == "admin"
            self._show("preferences_admin" if self.is_admin else "preferences")

        login_button = self._button("Log in", login, primary=True)
        login_button.setObjectName("primaryButton")
        layout.addWidget(login_button)
        layout.addWidget(self._button("Close", close=True))
        outer.addWidget(card)
        outer.addStretch(2)
        self._show("login")

    def _build_preferences(self, *, admin: bool) -> None:
        key = "preferences_admin" if admin else "preferences"
        title = "Preferences — Admin" if admin else "Preferences"
        subtitle = (
            "Administrator workspace and CRM sections."
            if admin
            else "Choose a section to open in the CRM workspace."
        )
        window, outer = self._make_window(key, title, subtitle)
        card, layout = self._card()
        destinations = (
            ("Applications", "applications"),
            ("Mentor Interview", "mentor"),
            ("Interviews", "interviews"),
        )
        for text, destination in destinations:
            layout.addWidget(
                self._button(
                    text,
                    lambda _checked=False, page=destination: self._show(page),
                    primary=True,
                )
            )
        if admin:
            layout.addWidget(
                self._button(
                    "Admin Menu", lambda: self._show("admin"), primary=True
                )
            )
        layout.addWidget(self._button("Close", close=True))
        outer.addWidget(card)
        outer.addStretch()

    def _add_search_row(
        self, layout: QtWidgets.QVBoxLayout, placeholder: str
    ) -> None:
        row = QtWidgets.QHBoxLayout()
        search_input = QtWidgets.QLineEdit()
        search_input.setPlaceholderText(placeholder)
        row.addWidget(search_input, 1)
        row.addWidget(
            self._button(
                "Search",
                lambda: QtWidgets.QApplication.activeWindow().statusBar().showMessage(
                    "Search is a placeholder in this UI-only milestone.", 4000
                ),
                primary=True,
            )
        )
        layout.addLayout(row)

    def _build_applications(self) -> None:
        window, outer = self._make_window(
            "applications",
            "Applications",
            "Review and filter course applications. Data integration comes later.",
        )
        card, layout = self._card()
        self._add_search_row(layout, "Search applications")
        filters = QtWidgets.QHBoxLayout()
        for label in (
            "All Applications",
            "Mentor Meeting Defined",
            "Mentor Meeting Not Defined",
        ):
            filters.addWidget(
                self._button(
                    label,
                    lambda _checked=False, text=label: window.statusBar().showMessage(
                        f"{text} filter is a placeholder.", 4000
                    ),
                )
            )
        layout.addLayout(filters)
        table = self._table(
            (
                "Name",
                "Email",
                "Phone",
                "Application Date",
                "Course",
                "Mentor Meeting",
                "Status",
            )
        )
        layout.addWidget(table, 1)
        outer.addWidget(card, 1)
        outer.addWidget(
            self._button("Return to Preferences Screen", self._go_preferences)
        )

    def _build_mentor_interview(self) -> None:
        window, outer = self._make_window(
            "mentor",
            "Mentor Interview",
            "Browse mentor conversations and choose a category.",
        )
        card, layout = self._card()
        self._add_search_row(layout, "Search conversations")
        row = QtWidgets.QHBoxLayout()
        row.addWidget(self._button("All Conversations", primary=True))
        category = QtWidgets.QComboBox()
        category.setObjectName("conversationCategory")
        category.addItems(
            ("All categories", "Initial contact", "Mentor meeting", "Follow-up")
        )
        row.addWidget(category, 1)
        layout.addLayout(row)
        helper = QtWidgets.QLabel(
            "Conversation results will appear here in a later project stage."
        )
        helper.setObjectName("helperText")
        layout.addWidget(helper)
        layout.addStretch()
        outer.addWidget(card, 1)
        outer.addWidget(
            self._button("Return to Preferences Screen", self._go_preferences)
        )

    def _build_interviews(self) -> None:
        window, outer = self._make_window(
            "interviews",
            "Interviews",
            "Review project delivery status. Filtering will be added later.",
        )
        card, layout = self._card()
        self._add_search_row(layout, "Search interviews")
        row = QtWidgets.QHBoxLayout()
        row.addWidget(self._button("Project Sent", primary=True))
        row.addWidget(self._button("Project Received"))
        row.addStretch()
        layout.addLayout(row)
        helper = QtWidgets.QLabel(
            "Interview records will appear here in a later project stage."
        )
        helper.setObjectName("helperText")
        layout.addWidget(helper)
        layout.addStretch()
        outer.addWidget(card, 1)
        outer.addWidget(
            self._button("Return to Preferences Screen", self._go_preferences)
        )

    def _build_admin_menu(self) -> None:
        window, outer = self._make_window(
            "admin",
            "Admin Menu",
            "Calendar event records and participant mail tools.",
        )
        card, layout = self._card()
        actions = QtWidgets.QHBoxLayout()
        actions.addWidget(self._button("Event Record", primary=True))
        actions.addWidget(self._button("Mail"))
        actions.addStretch()
        layout.addLayout(actions)
        table = self._table(("Event", "Date", "Time", "Participants", "Status"))
        layout.addWidget(table, 1)
        outer.addWidget(card, 1)
        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(
            self._button("Preferences — Return to Admin Screen", self._go_preferences)
        )
        buttons.addStretch()
        buttons.addWidget(self._button("Exit", close=True))
        outer.addLayout(buttons)


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("CRM Interface Prototype")
    prototype = CRMPrototype(app)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
