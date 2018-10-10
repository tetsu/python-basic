import string

with open('template-text.txt') as f:
    t = string.Template(f.read())

contents = t.substitute(name='Mike', content='How are you?')

print(contents)
