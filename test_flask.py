import requests


r = requests.get('http://127.0.0.1:5000/employee/Mike')
print(r.text)

r = requests.post(
    'http://127.0.0.1:5000/employee', data={'name': 'Mike'}
)
print(r.text)


r = requests.put(
    'http://127.0.0.1:5000/employee', data={'name': 'Mike', 'new_name': 'Michael'}
)
print(r.text)

r = requests.delete(
    'http://127.0.0.1:5000/employee', data={'name': 'Michael'}
)
print(r.text)
