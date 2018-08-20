import csv



def add_entry():
    # self.clear()
    task_name = input("Task Name:\n ")
    while True:
        if isinstance(task_name, str):
            break
        else:
            task_name = input ("Please enter a string for the Task Name:\n")

    minutes = input("Number of minutes spent working on task:\n")
    while True:
        try:
            minutes = int(minutes)
        except ValueError:
            minutes = input("Please enter an integer for number of minutes:\n")
        else:
            break
    notes = input("Optional additional notes:\n")
    while True:
        if (isinstance(notes, str) or notes == False):
            break
        else:
            task_name = input ("Please enter a string for Notes or :\n")

add_entry()
