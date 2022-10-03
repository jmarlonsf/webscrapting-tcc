ages = {'Jim': 30, 'Pam': 28, 'Kevin': 33}
person = input('Get age for: ')

try:
    print(f'{person} is {ages[person]} years old.')
except KeyError:
    print(f"{person}'s age is unknown.")


print("segue a vida")