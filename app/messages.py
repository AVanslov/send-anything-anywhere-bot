import json

SAY_HI = 'Hello, {}'


with open("all_countries_and_cities.json", "r") as fh:
    countries_and_cities = json.load(fh)
# json файла со всеми странами и городами
print(sorted(list(set(sorted([i[:1] for i in countries_and_cities.keys()])))))
# a = sorted([i[:1] for i in countries_and_cities.keys()])
# b = set(a)
# c = sorted(list(b))
# print(b)
# print(c)
