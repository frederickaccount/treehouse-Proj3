import csv
import re

class Menu:
    def __init__(self):
        self.alert = 0
        self.lookup_pattern()

    def take_pattern(self):
        while True:
            try:
                user_input = input("Enter Valid Regex Pattern to search."
                                    "(Example:r'[YOUR INPUT HERE]'\n")
                self.pattern = (r'%s' % user_input)
                re.compile(self.pattern)

            except re.error:
                print(user_input + " is not a valid regex expression")
            else:
                break


    def lookup_pattern(self):
        # self.clear()
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
        # if self.row_count == 0:
        #     self.no_pages()
        # else:
        #     self.paging()


Menu()
