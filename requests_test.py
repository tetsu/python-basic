import requests


payload = {"key1": "value1", "key2": "value2"}

r = requests.get('http://httpbin.org/get', params=payload)
print(r.status_code)
print(r.text)
print(r.json())
print('############')

r = requests.post('http://httpbin.org/post', params=payload)
print(r.status_code)
print(r.text)
print(r.json())
print('############')

r = requests.put('http://httpbin.org/put', params=payload)
print(r.status_code)
print(r.text)
print(r.json())
print('############')

r = requests.delete('http://httpbin.org/delete', params=payload)
print(r.status_code)
print(r.text)
print(r.json())
print('############')
