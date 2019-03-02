import requests
from bs4 import BeautifulSoup

page = requests.get("http://www.allrecipes.com/recipes")
soup = BeautifulSoup(page.content, 'html.parser')
