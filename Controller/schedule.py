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
                print(f"Removed: {removed['title']}")
            else:
                print("Index out of range.")
        except ValueError:
            print("Please enter a valid number.")


def show_schedule():
    i = 0
    for schedule in schedules:
        print(
            f"{i}. {schedule['title']} | {schedule['date']} | {schedule['time']} | {schedule['type']} | {schedule['desc']}"
        )
        i += 1
