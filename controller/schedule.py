schedule_file = "schedules.txt"
schedules = []


def get_schedule():
    run = True
    while run:
        title = input("Title: ")
        date = input("Date (MM/DD/YYYY): ")
        time = input("Time (HH:MM): ")
        typ = input("Type (Ex. Activity/Exam): ")
        desc = input("Descripiton (Opitonal): ")
        # color = input("Select a color: ")
        choose = input("\n1.Save \n2.Reenter \n3.Exit \n\nChoose: ")

        if choose == "1":
            dat = {
                "title": title,
                "date": date,
                "time": time,
                "type": typ,
                "desc": desc,
            }
            schedules.append(dat)
            save_schedules()
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
            if 0 <= remove < len(schedules):
                removed = schedules.pop(remove)
                save_schedules()
                print(f"Removed: {removed['title']}")
            else:
                print("Index out of range.")
        except ValueError:
            print("Please enter a valid number.")


def show_schedule():
    if not schedules:
        print("No schedules found.")
        return
    i = 0
    for schedule in schedules:
        print(
            f"{i + 1}. {schedule['title']} | {schedule['date']} | {schedule['time']} | {schedule['type']} | {schedule['desc']}"
        )
        i += 1


def save_schedules():
    with open(schedule_file, "w") as file:
        for schedule in schedules:
            file.write(
                f"{schedule['title']}|{schedule['date']}|{schedule['time']}|{schedule['type']}|{schedule['desc']}\n"
            )


def load_schedules():
    try:
        with open(schedule_file, "r") as file:
            for line in file:
                title, date, time, typ, desc = line.strip().split("|")
                schedules.append(
                    {
                        "title": title,
                        "date": date,
                        "time": time,
                        "type": typ,
                        "desc": desc,
                    }
                )
    except FileNotFoundError:
        print("No saved schedules found.")


load_schedules()
