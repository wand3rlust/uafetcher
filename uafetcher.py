import json
import requests
from bs4 import BeautifulSoup

url = requests.get('https://www.useragents.me/')
soup = BeautifulSoup(url.content, features="html.parser")
containers = [title.parent for title in soup.select("div.container h2")]
#print(containers)

us_types: list[str] = ["most-common", "latest"]
uas = {}

for container in containers:
    title = container.select("h2")[0]
    table = container.select_one("table")
    if not table:
        continue

    data = [[col.text.strip() for col in row.find_all('td')] for row in table.find_all('tr') if row.find_all('td')]
    section: str = title.text

    for ua in us_types:
        if title.attrs['id'].strip().startswith(ua):
            uas.setdefault(ua, []).append({'section': section, 'data': data})

for ua, sections in uas.items():
    print(f"User Agent Type: {ua}")
    for section in sections:
        print(f"Section: {section['section']}")
        for row in section['data']:
            print(row)

with open('user_agents.json', 'w') as file:
    json.dump(uas, file, indent=4)
