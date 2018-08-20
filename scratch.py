import datetime

def to_string(dt):
    return dt.strftime("%m/%d/%y")

def from_string(string, str2):
    return datetime.datetime.strptime(string, str2)

j = to_string(datetime.datetime.now())
print (type(j))

r = from_string(j, "%m/%d/%y")
print (type(r))
print(r)
# while True:
#     try:
#         r = input("test")
#         test = (from_string(r, "%m/%d/%y") )
#         test = test.strftime("%m/%d/%y")
#         r2 = input("test")
#         test2 = (from_string(r, "%m/%d/%y") )
#         test2 = test.strftime("%m/%d/%y")
#     except ValueError:
#         print("h")
#
#     else:
#         print (test)
#         break
#

# test2 = to_string(datetime.datetime.now())
# test2 = (datetime.datetime.now().strftime("%m/%d/%y"))
# print(test2)
# print(type(test2))
# j = to_string(test2)
# print(type(j))


# search_format = '%m /%d'
# while True:
#     search = input('enter m/d')
#     if search.upper() == "QUIT":
#         break
#     try:
#         date= datetime.datetime.strptime(search, search_format)
#         print (date)
#     except ValueError:
#         print ("u fucked up")
