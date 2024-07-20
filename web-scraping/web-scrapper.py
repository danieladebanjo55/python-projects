import requests
from bs4 import BeautifulSoup

website = requests.get('https://realpython.github.io/fake-jobs/')

soup = BeautifulSoup(website.text, 'html.parser')

job_titles = soup.find_all("h2", attrs={'class' : 'title'})
apply_links = soup.findAll("a", href=True)

f = open("jobs.txt", "w")

for title, link in zip(job_titles, apply_links):
    result = f"{title.text}: {link.get('href')}\n"
    f.write(str(result))

    


