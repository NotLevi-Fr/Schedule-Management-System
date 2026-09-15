import Controller.schedule as schedule


def main():
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
            break

        else:
            print("Invalid choice, Please try again.")


main()
