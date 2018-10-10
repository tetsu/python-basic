import csv
import os
from tempfile import NamedTemporaryFile
import shutil

fieldnames = ['Restaurant', 'Count']
filepath = 'restaurant.csv'
tempfile = NamedTemporaryFile(mode='w', delete=False)

print('Hi, my name is Roboko. What is your name?')

while True:
    name = input('Enter your name: ')
    if len(name) > 0:
        break
    else:
        print("Sorry, I didn't get your name.")

if not os.path.exists(filepath):
    with open(filepath, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

with open(filepath, 'r') as csv_file, tempfile:
    reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    header = next(reader)
    writer = csv.DictWriter(tempfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        while True:
            print("Is {} your favorite restaurant?".format(row['Restaurant']))
            fav = input("[Yes/No]").lower()

            if fav == 'yes' or fav == 'y':
                writer.writerow({
                    'Restaurant': row['Restaurant'],
                    'Count': int(row['Count'])+1
                })
                break
            elif fav == 'no' or fav == 'n':
                writer.writerow({
                    'Restaurant': row['Restaurant'],
                    'Count': row['Count']
                })
                break
            else:
                print('Pardon?')

    print("What's your favorite restaurant?")
    new_fav = input('Enter your favorite restaurant name: ')
    while True:
        if len(new_fav) > 0:
            writer.writerow({'Restaurant':new_fav, 'Count': 1})
            break
        else:
            print("Sorry, I didn't get your favorite resutaurant name.")

    shutil.move(tempfile.name, filepath)

print('Thank you {}! Have a nice day!'.format(name))
