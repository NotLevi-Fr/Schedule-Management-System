from data.data import Database
from features.schedule.model import Schedule
from features.schedule.repository import ScheduleRepository

repository = ScheduleRepository(Database())


def get_schedule():
    run = True
    while run:
        title = input("Title: ")
        date = input("Date (MM/DD/YYYY): ")
        time = input("Time (HH:MM): ")
        typ = input("Type (Ex. Activity/Exam): ")
        desc = input("Descripiton (Opitonal): ")
        choose = input("\n1.Save \n2.Reenter \n3.Exit \n\nChoose: ")

        if choose == "1":
            repository.add(Schedule(title, date, time, typ, desc))
            print("Saved.")
            break
        elif choose == "2":
            continue
        elif choose == "3":
            run = False
            break


def delete_schedule():
    run = True
    while run:
        x = input("Cotinue(y/n): ")
        if x != "y":
            run = False
            break
        show_schedule()

        remove = input("Select index to remove: ")
        try:
            remove = int(remove) - 1
            schedules = repository.list()
            if 0 <= remove < len(schedules):
                repository.delete(schedules[remove].id)
                print(f"Removed: {schedules[remove].title}")
            else:
                print("Index out of range.")
        except ValueError:
            print("Please enter a valid number.")


def show_schedule():
    schedules = repository.list()
    if not schedules:
        print("No schedules found.")
        return
    for i, item in enumerate(schedules):
        print(
            f"{i + 1}. {item.title} | {item.date} | {item.time} | {item.typ} | {item.desc}"
        )