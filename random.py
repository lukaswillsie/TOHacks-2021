import math

def get_value(start, end):
    lst = []
    for i in range(1, math.ceil(math.sqrt(end)) + 1):
        if (i * i) % 2 != 0 and i * i <= end:
            lst.append(i * i)
    return sum(lst)

if __name__ == "__main__":
    print(get_value(1, 935))
