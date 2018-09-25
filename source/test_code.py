

'''
REFERENCES:
https://stackoverflow.com/questions/10666163/how-to-check-if-all-elements-of-a-list-matches-a-condition
https://stackoverflow.com/questions/7270321/finding-the-index-of-elements-based-on-a-condition-using-python-list-comprehensi

'''

x = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1]


def check_until():



    # theta = eval("x[i]==0")
    # phi = eval("x[i]==1")

    t = 0
    a = 5
    b = 15

    # list that contains indexes where the second condition holds true
    c = [i for i in range(a,b) if (x[i]==1)]
    print("list that contains indexes within the range where the second condition holds true \n{}".format(c))

    # check if all values in the provided list satisfy the condition
    cc = all(i == 0 for i in x[0:10])


    d = [True if (all(i == 0 for i in x[0:val])) else False for idx, val in enumerate(c)]
    print("Is there any range obtained from the previous formula where the first condition always holds true \n{}".format(d))

    if True in d: print("Until conditions holds true")


    # single line until statement

    print(
        True if True in [True if (all(i == 0 for i in x[0:val])) else False for idx, val in enumerate([i for i in range(a,b) if (x[i]==1)])] else False

    )






if __name__ == "__main__":
    print("Length of signal: {}".format(len(x)))

    check_until()

    # z = [x if x % 2 else x * 100 for x in range(1, 10) ]
    print(x[0:10])
    z = all(i == 0 for i in x[0:10])
    print(z)