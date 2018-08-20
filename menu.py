import csv
import datetime
import os
import re
import sys

class Menu:
    """docstring for Menu."""
    def __init__(self):
        self.fieldnames = ['row_number', 'date', 'task', 'minutes', 'notes']

        self.menu()


    def clear(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def menu(self, alert=None):
        self.clear()
        if alert:
            print(alert)
        menu_choice = input("Choose:\n"
                            "[A]dd new entry\n"
                            "[L]ook up previous entries\n"
                            "[Q]uit\n\n"
                            ).upper()
        menu_choices = ['A', 'L', 'Q']

        while menu_choice not in menu_choices:
            menu_choice = input("You must select [A] to add "
                                "[L] to look up previous entries "
                                "or [Q] to quit.\n\n"
                                ).upper()
        if menu_choice == "A":
            self.add_entry()
        elif menu_choice == "L":
            self.lookup()
        elif menu_choice == "Q":
            self.quit()

    def take_task(self):
        self.task_name = input("Task Name:\n ")
        while True:
            if (isinstance(self.task_name, str)):
                if (len(self.task_name) < 51) and (len(self.task_name) > 0):
                    break
                else:
                    self.task_name = input ("Please enter a string for the Task Name (Max Length 50 characters):\n")
            else:
                self.task_name = input ("Please enter a string for the Task Name (Max Length 50 characters):\n")

    def take_min(self):
        self.minutes = input("Number of minutes spent working on task:\n")
        while True:
            if (len(str(self.minutes)) <= 10):
                try:
                    self.minutes = int(self.minutes)

                except ValueError:
                    self.minutes = input("Please enter an integer for number of minutes (10 digit max):\n")

                else:
                    break
            else:
                self.minutes = input("Please enter an integer for number of minutes (10 digit max):\n")

    def take_notes(self):
        self.notes = input("Optional additional notes:\n")
        while True:
            if self.notes == False:
                break
            elif (isinstance(self.notes, str) and (len(self.notes)<501)):
                break
            else:
                self.notes = input ("Please enter a string for Notes (Max Length 500 characters):\n")

    def take_match(self):
        self.take_search = input("Enter text to search for in task names and notes:\n")
        while True:
            if ((len(self.take_search)>0) and (len(self.take_search)<501)):
                break
            else:
                self.take_search = input ("Enter text to search for in task names and notes (Max Length 500 characters):\n")

    def take_date(self):
        while True:
            try:
                self.date = input("Enter date (Must be in mm/dd/yy format):\n")
                self.date = datetime.datetime.strptime(self.date, "%m/%d/%y")
                self.date = self.date.strftime("%m/%d/%y")
            except ValueError:
                print("Must be in mm/dd/yy format!")
            else:
                break

    def add_entry(self):
        self.clear()
        self.take_task()
        self.take_min()
        self.take_notes()

        self.date= datetime.datetime.now().strftime("%m/%d/%y")
        self.add()

    def add(self):
        if os.path.exists('./entries.csv'):
            self.row_count = 0
            with open('entries.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.row_count+=1

            with open('entries.csv', 'a', newline='') as csvfile:

                entrywriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                entrywriter.writerow({'row_number': self.row_count, 'date': self.date, 'task': self.task_name,
                                        'minutes': self.minutes, 'notes': self.notes})
        else:
            with open('entries.csv', 'a', newline='') as csvfile:
                self.row_count = 0
                entrywriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                entrywriter.writeheader()
                entrywriter.writerow({'row_number': self.row_count, 'date': self.date, 'task': self.task_name,
                                        'minutes': self.minutes, 'notes': self.notes})
        alert = "Entry Added\n"
        self.menu(alert)


    def lookup(self):
        self.clear()
        menu_choice = input("How would you like to search:\n"
                            "By [D]ate\n"
                            "By [R]ange of Dates\n"
                            "By [T]ime spent\n"
                            "By [E]xact match\n"
                            "By [P]attern match\n"
                            "[B]ack to previous menu\n"
                            "[Q]uit\n\n"
                            ).upper()
        menu_choices = ['D', 'R', 'T', 'E', 'P', 'B', 'Q']
        while menu_choice not in menu_choices:
            menu_choice = input("You must select [D], [R], [T], [E], [P], [B] or [Q] \n"
                                ).upper()
        if menu_choice == 'D':
            self.lookup_date()
        elif menu_choice == 'R':
            self.lookup_range()
        elif menu_choice == 'T':
            self.lookup_time()
        elif menu_choice == 'E':
            self.lookup_match()
        elif menu_choice == 'P':
            self.lookup_pattern()
        elif menu_choice == 'B':
            self.menu()
        elif menu_choice == 'Q':
            self.quit()

    def take_pattern(self):
        while True:
            try:
                user_input = input("Enter Valid Regex Pattern to search.\n"
                                    "(Example:r'[YOUR INPUT HERE]')\n")
                self.pattern = (r'%s' % user_input)
                re.compile(self.pattern)

            except re.error:
                print(user_input + " is not a valid regex expression")
            else:
                break


    def lookup_pattern(self):
        self.clear()
        self.take_pattern()
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.row_count = 0
            self.matches= []
            self.search_results=[]
            for row in reader:
                if ((re.search(self.pattern, row['task'])) or (re.search(self.pattern, row['notes']))):
                    self.row_count +=1
                    self.matches.append(row)
                    print(str(self.row_count)+ ". " + row['task'])
                    self.search_results.append(str(self.row_count)+ ". " + row['task'])
        if self.row_count == 0:
            self.no_pages()
        else:
            self.paging()


    def lookup_range(self):
        self.clear()
        self.show_dates()
        print("Enter First Date")
        self.take_date()
        first_date = datetime.datetime.strptime(self.date, '%m/%d/%y')
        self.clear()
        self.show_dates()
        print("Enter Second Date")
        self.take_date()
        second_date = datetime.datetime.strptime(self.date, '%m/%d/%y')
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.row_count = 0
            self.matches= []
            self.search_results=[]
            for row in reader:
                search_dates= datetime.datetime.strptime(row['date'], '%m/%d/%y')
                if ((first_date <= search_dates and second_date >= search_dates) or
                    (first_date >= search_dates and second_date <= search_dates)):
                    self.row_count +=1
                    self.matches.append(row)
                    print(str(self.row_count)+ ". " + row['task'])
                    self.search_results.append(str(self.row_count)+ ". " + row['task'])

        if self.row_count == 0:
            self.no_pages()
        else:
            self.paging()

    def show_dates(self):
        print("The following dates have entries:\n")
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.row_count = 0
            self.all_dates= []
            for row in reader:
                if (row['date'] not in self.all_dates):
                    self.row_count +=1
                    self.all_dates.append(row['date'])
                    print(str(self.row_count)+ ". " + row['date'])


    def lookup_date(self):
        self.clear()
        self.show_dates()
        self.take_date()
        self.clear()
        print("Task Names for \"" + self.date + "\":\n")
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.row_count = 0
            self.matches= []
            self.search_results=[]
            for row in reader:
                if (self.date == row['date']):
                    self.row_count +=1
                    self.matches.append(row)
                    print(str(self.row_count)+ ". " + row['task'])
                    self.search_results.append(str(self.row_count)+ ". " + row['task'])

        if self.row_count == 0:
            self.no_pages()
        else:
            self.paging()

    def lookup_time(self):
        self.clear()
        self.take_min()
        self.clear()
        print("Task Names with \"" + str(self.minutes) + "\" minutes spent:\n")
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.row_count = 0
            self.matches= []
            self.search_results=[]
            for row in reader:
                if (str(self.minutes) == row['minutes']):
                    self.row_count +=1
                    self.matches.append(row)
                    print(str(self.row_count)+ ". " + row['task'])
                    self.search_results.append(str(self.row_count)+ ". " + row['task'])

        if self.row_count == 0:
            self.no_pages()
        else:

            self.paging()


    def lookup_match(self):
        self.clear()
        self.take_match()

        self.clear()
        print("Task Names and notes with Exact Match Results For \"" + self.take_search + "\":\n")
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.row_count = 0
            self.matches= []
            self.search_results=[]
            for row in reader:
                if (self.take_search in row['task'] or self.take_search in row['notes']):
                    self.row_count +=1
                    self.matches.append(row)
                    print(str(self.row_count)+ ". " + row['task'])
                    self.search_results.append(str(self.row_count)+ ". " + row['task'])
        if self.row_count == 0:
            self.no_pages()
        else:
            self.paging()

    def no_pages(self):
        print("\nNo results found")
        menu_choice = input("[M]ain menu\n"
                            "[B]ack to search menu\n"
                            "[Q]uit\n\n"
                            ).upper()
        menu_choices = ['M', 'B', 'Q', 'S']
        while menu_choice not in menu_choices:
            menu_choice = input("You must select [M], [B] or [Q] \n"
                                ).upper()
        if menu_choice == 'M':
            self.menu()
        elif menu_choice == 'B':
            self.lookup()
        elif menu_choice == 'Q':
            self.quit()

    def make_pages(self):
        print ("\nPage For Result " + str((self.match_count + 1)) + ":\n")
        print ("entry id : " + self.matches[self.match_count]['row_number'] +
                "\nDate: " + self.matches[self.match_count]['date'] + "\n" +
                "Task Name: " + self.matches[self.match_count]['task'] +
                "\nMinutes Spent: " + self.matches[self.match_count]['minutes'] +
                 "\nOptional Notes:" + self.matches[self.match_count]['notes'] +
                 "\n\n")


    def paging(self):
        paging = True
        self.match_count = 0
        while paging == True:
            if self.match_count < 0:
                self.match_count = 0
                print ("\nNo previous results")
            if self.match_count == len(self.matches):
                self.match_count = (len(self.matches) -1)
                print ("\nNo further results")
            self.make_pages()
            entry_number = self.matches[self.match_count]['row_number']
            self.match_choices = []
            for i in range (len(self.matches)):
                self.match_choices.append(str(i+1))
            menu_choice = input("Menu Options:\n"
                                "[N]ext Page, "
                                "[P]revious Page,\n"
                                "[E]dit,"
                                "[D]elete,\n"
                                "[M]ain menu, "
                                "[B]ack to search menu, "
                                "[Q]uit\n"
                                "or you can enter the number of the search result to jump to its page\n"
                                ).upper()
            menu_choices = ['M', 'B', 'Q', 'E', 'N', 'P', 'D']
            menu_choices.extend(self.match_choices)
            while menu_choice not in menu_choices:
                self.clear()
                print("Task Names of  Results:\n")
                print("\n".join(self.search_results))
                menu_choice = input("You must select [N], [P], [D], [M], [E], [B], [Q],\n"
                                    "or the number of the search result\n"
                                    ).upper()
            if menu_choice == 'M':
                self.menu()
            elif menu_choice == 'B':
                self.lookup()
            elif menu_choice == 'S':
                self.lookup_match()
            elif menu_choice == 'N':
                self.clear()
                print("Task Names of  Results:\n")
                print("\n".join(self.search_results))
                self.match_count +=1
            elif menu_choice == 'E':
                self.alteration = "Edit"
                self.alter(entry_number)
            elif menu_choice == 'P':
                self.clear()
                print("Task Names of  Results:\n")
                print("\n".join(self.search_results))
                self.match_count -=1
            elif menu_choice == 'D':
                self.alteration = "Delete"
                self.alter(entry_number)
            elif menu_choice == 'Q':
                self.quit()
            elif menu_choice in self.match_choices:
                self.clear()
                print("Task Names of  Results:\n")
                print("\n".join(self.search_results))
                self.match_count = (int(menu_choice) - 1)

    def edit(self, row_count, all_entries):
        self.clear()
        while True:
            task_check = input("Current Task Name: " + all_entries[row_count]['task'] +
                                "\nOptions:"
                                "\n[L]eave Task Name as is" +
                                "\n[C]hange Task Name\n").upper()
            if task_check == "L":
                self.clear()
                break
            elif task_check == "C":
                self.take_task()
                all_entries[row_count]['task'] = self.task_name
                self.clear()
                break
            else:
                self.clear()
                print("You must enter [L] or [C]")
        while True:
            min_check = input("Current Minutes Spent: " + all_entries[row_count]['minutes'] +
                                "\nOptions:"
                                "\n[L]eave Minutes Spent as is" +
                                "\n[C]hange Minutes Spent\n").upper()
            if min_check == "L":
                self.clear()
                break
            elif min_check == "C":
                self.take_min()
                all_entries[row_count]['minutes'] = self.minutes
                self.clear()
                break
            else:
                self.clear()
                print("You must enter [L] or [C]")
        while True:
            dates_check = input("Current date for entry: " + all_entries[row_count]['date'] +
                                "\nOptions:"
                                "\n[L]eave Date" +
                                "\n[C]hange Date\n").upper()
            if dates_check == "L":
                self.clear()
                break
            elif dates_check == "C":
                self.take_date()
                all_entries[row_count]['date'] = self.date
                self.clear()
                break
            else:
                self.clear()
                print("You must enter [L] or [C]")

        while True:
            notes_check = input("Current Optional Notes: " +
                                all_entries[row_count]['notes'] +
                                "\nOptions:"
                                "\n[L]eave Notes as they are" +
                                "\n[C]hange Notes\n").upper()
            if notes_check == "L":
                self.clear()
                break
            elif notes_check == "C":
                self.take_notes()
                all_entries[row_count]['notes'] = self.notes
                self.clear()
                break
            else:
                self.clear()
                print("You must enter [L] or [C]")

    def alter(self, entry_number):
        """
        Reads in csv file while placing its rows into a list
        If a row is being deleted that row will not be added to the list
        If a row is being edited the edited row will be added to the list
        The edit method is used to take updated values from the user
        The row number for each row will be sequential from one
        An alert message is sent when returning to the main menu
        """
        with open('entries.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0
            altered = False
            all_entries = []
            for row in reader:
                if ((row['row_number'] == str(entry_number))
                        and (altered is False)):

                    if self.alteration == "Delete":
                        alert = "Entry Deleted\n"
                    elif self.alteration == "Edit":
                        alert = "Edit Complete\n"
                        all_entries.append(dict(row))
                        self.edit(row_count, all_entries)
                        all_entries[row_count]['row_number'] = row_count
                        row_count += 1
                    altered = True
                else:
                    all_entries.append(dict(row))
# Update the row number so that if an entry was deleted there is not a skip
                    all_entries[row_count]['row_number'] = row_count
                    row_count += 1
# Rewrite the csv file with edits or deletions
        with open('entries.csv', 'w', newline='') as csvfile:
            entrywriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            entrywriter.writeheader()
            entrywriter.writerows(all_entries)
# Return to main menu and indicate delete or edit complete
        self.menu(alert)

    def quit(self):
        """
        Quits the program
        """
        sys.exit(0)


# Program wont run automatically if imported
if __name__ == "__main__":
    Menu()
