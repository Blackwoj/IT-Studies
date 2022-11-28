import json
import requests

# P1
f=open("binfile.bin", "wb")
num=[0, 10, 20, 30, 40, 50]
arr=bytearray(num)
f.write(arr)
f.close()

f=open("binfile.bin", "ab")
num=[60]
f.write(bytearray(num))
f.close()

f=open("binfile.bin", "rb")
d=f.read()
l=len(d)
for i in range(l):
    print(f"First: {d[i]}")
f.close()
#  p2

openfile = open("JsonFile.json")
edit_file = json.load(openfile)

edit_file.append({
    "ID" : 4,
    "Name": "Michal",
    "email": "michal@nowak.com"
})
openfile.close()
with open('JsonFile.json', 'w') as outfile:
    json.dump(edit_file, outfile, indent=2)
outfile.close()
#  p3

file = requests.get('https://api.github.com')
print(file.json())
sort = file.json()
sorted = json.dumps(sort,indent=1,sort_keys=True)
print(sorted)
