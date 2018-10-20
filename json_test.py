import json


j = {
    "employee": [
        {"id": 111, "name": "Mike"},
        {"id": 222, "name": "Nancy"}
    ]
}

print(j)
print("##################")

print(json.dumps(j))
print("##################")

a = json.dumps(j)
print(json.loads(a))
print("##################")

with open('test.json', 'w') as f:
    json.dump(j, f)

with open('test.json', 'r') as f:
    print(json.load(f))
print("##################")
