import re
# \w{4}
def find_words(count, string):

    while True:
        try:
            j = input("o")
            test = (r'%s' % j)
            re.compile(test)
            f = re.search(test, string)

        except re.error:
            print("ce")
        else:
            return f


count = 4

# test = ('\w \{ {} \},'.format(count))
# print (test)
print (find_words(4, "dog, cat, baby, balloon, me"))
