import sys
import threading
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

import controller.schedule as schedule
from data.data import Database
from features.schedule.service import StudentService
from view import StudentView


class Bridge(QObject):
    refreshed = pyqtSignal()
    quit_requested = pyqtSignal()


def main():
    database = Database()
    database.create_table()

    app = QApplication(sys.argv)
    service = StudentService(database)
    window = StudentView(service)
    window.show(1)

    bridge = Bridge()
    bridge.refreshed.connect(window.refresh)
    bridge.quit_requested.connect(app.quit)

    def cli_loop():
        run = True
        while run:
            print("\n====== Schedule Management System =======")
            print("1. Input Schedule")
            print("2. Remove Schedule")
            print("3. Show all Schedules")
            print("5. Exit")

            choose = input("Choice: ")

            if choose == "1":
                schedule.get_schedule()
            elif choose == "2":
                schedule.delete_schedule()
            elif choose == "3":
                schedule.show_schedule()
            elif choose == "5":
                run = False
            else:
                print("Invalid choice, Please try again.")

            bridge.refreshed.emit()

        bridge.quit_requested.emit()

    threading.Thread(target=cli_loop, daemon=True).start()

    sys.exit(app.exec())


main()