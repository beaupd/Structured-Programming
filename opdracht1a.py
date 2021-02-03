# Formatieve opdracht 1a: algoritmisch programmeren
# Jonathan Williams (1790472)

import random  # Opdracht 7


# Opdracht 1: Pyramide

def pyramide1(n):                    # Normale pyramide, twee for-loops
    for i in range(1, n+1):
        print("*" * i)
    for i in range(n - 1, 0, -1):
        print("*" * i)


def pyramide2(n):                   # Normale pyramide, twee while-loops
    i = 1
    while i < n:
        print("*" * i)
        i += 1
    while i > 0:
        print("*" * i)
        i -= 1


def pyramide3(n):                   # Inverted pyramide, twee for-loops
    for i in range(1, n+1):
        print(" " * (n-i) + "*" * i)
    for i in range(n - 1, 0, -1):
        print(" " * (n-i) + "*" * i)


def pyramide4(n):                   # Inverted pyramide, twee while-loops
    i = 1
    while i < n:
        print(" " * (n-i) + "*" * i)
        i += 1
    while i > 0:
        print(" " * (n-i) + "*" * i)
        i -= 1


# Opdracht 2: Tekstcheck

def differ_at():
    a = input("Please enter some text: ")
    b = input("Please enter other text: ")

    n = 0
    if a and b:
        while a[n] == b[n]:
            n += 1

    print(f"The two strings differ at index {n}")


# Opdracht 3: Lijstcheck

# a:
def count(x, lst):
    c = 0
    for n in lst:
        c += 1 if n == x else 0
    return c


# b:
def consecutive_range(lst):
    r = 0
    for i in range(len(lst) - 1):
        rnew = abs(lst[i] - lst[i + 1])
        if rnew > r:
            r = rnew
    return r


# c:
def qualify(lst):
    if count(0, lst) > 12:
        return False
    return count(1, lst) > count(0, lst)


# Opdracht 4: Palindroom
def palindroom(s):                      # Gebruikmaking van bibliotheekfunctie
    return s == "".join(reversed(s))


def palindrome(s):                      # Zelf omdraaien verzorgen
    return s == s[::-1]


# Opdracht 5: Sorteren
def minsort(lst):                       # Een sorteerfunctie die nummers sorteert door ze van klein naar groot te pakken
    result = []
    while lst:
        m = min(lst)
        result.append(m)
        lst.remove(m)
    return result


# Opdracht 6: Gemiddelde berekenen
def average(lst):                       # Een lijst van cijfers als input
    return sum(lst) / len(lst)


def averages(megalst):                  # Een lijst van lijsten met cijfers als input
    return [sum(lst) / len(lst) for lst in megalst]


# Opdracht 7: Random
def guess():
    r = random.randint(0, 9)
    while True:
        g = int(input("Guess a number (0-9): "))
        if g == r:
            print("Correct! You win!")
            break
        print("Too bad! Guess again!")


# Opdracht 8: Compressie
def compress(file):
    result = []
    f = open(file, 'r')
    for line in f:
        result.append(line.lstrip())
    f.close()

    f = open("compressed-" + file, 'w')
    for line in result:
        f.write(line)
    f.close()


# Opracht 9: Cyclisch verschuiven
def cyclic(ch, n):
    binary = f"{ord(ch):b}"
    return binary[n:] + binary[:n]


# Opdracht 10: Fibonacci
def fibonacci(n, a=0, b=1):
    return b if n <= 1 else fibonacci(n-1, b, a+b)


# Opdracht 11: Caesarcijfer
def caesar(s, shift):
    result = ""
    for c in s:
        v = ord(c)
        if v in range(65, 91):
            result += chr(((v - 65 + shift) % 26) + 65)
        elif v in range(97, 123):
            result += chr(((v - 97 + shift) % 26) + 97)
        else:
            result += c
    return result


# Opdracht 12: FizzBuzz
def fizzbuzz():
    for n in range(1, 101):
        fizz = "fizz" if not n % 3 else ""
        buzz = "buzz" if not n % 5 else ""
        print(f"{fizz+buzz or n}")
