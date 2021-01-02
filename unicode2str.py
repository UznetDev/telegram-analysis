import json

with open('xushnudbek.json') as f:
  data = json.load(f)

print(data[2]["message"])