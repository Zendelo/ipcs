import json

with open('fullPassagesDict') as json_data:
    data = json.load(json_data)

counter = 0
for k, v in data.items():
    if len(v.split()) > 300:
        print(k)
        print(len(v.split()))
        print('Oi Vavoi')
        print(v.split())
        counter += 1

print(counter)
print(len(data))
