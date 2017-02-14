"""
input:
    list - list of inputs
output:
    mean of the list's values
"""

def mean_of_list(list):
    accum = 0
    for index in range (len(list)):
        accum += list[index]

    return accum/len(list)
