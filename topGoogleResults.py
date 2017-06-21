#! python3
# Open top Google search results

import requests
from bs4 import BeautifulSoup
import webbrowser
import sys

if len(sys.argv) < 2:
	print("Enter topic to search")
else:
	topic = sys.argv[1:]

print("Googling...")

res = requests.get('http://google.com/search?q=' + ' '.join(topic))
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

links = soup.select('.r a') # Select links

num_links = min(5, len(links))

for i in range(num_links):
	webbrowser.open('http://google.com' + links[i].get('href'))