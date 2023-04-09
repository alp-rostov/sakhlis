# Введите свое решение ниже

def replace_duplicates(s: str):
    alf = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    while True:
        a = len(s)
        for i in s:
            s=s.replace(i * 2, alf[alf.index(i)+1])
        b = len(s)

        if a == b:
            break
    return s

print(replace_duplicates('aaafggjhgjggjghhj'))