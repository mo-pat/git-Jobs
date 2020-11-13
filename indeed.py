import requests
from bs4 import BeautifulSoup

URL = 'https://ca.indeed.com/jobs?q=software+developer&l=Montr%C3%A9al%2C+QC&fromage=1'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='resultsCol')

resultsCards = soup.find_all(class_="jobsearch-SerpJobCard")

root_url = 'https://ca.indeed.com'

# Array of job listings
jobListings = []

for cards in resultsCards:
  title = cards.find('a', class_='jobtitle turnstileLink')
  company = cards.find('div', class_='sjcl').find(class_='company')
  location = cards.find('div', class_='sjcl').find(class_='location')
  path = cards.find('a', class_='jobtitle turnstileLink').get('href')
  full_path = root_url + path

  #print(title.text.strip())
  #print(company.text.strip())
  #print(location.text.strip())
  #print(full_path)

  job = {
    "title": title.text.strip(),
    "company": company.text.strip(),
    "location": location.text.strip(),
    "URL": full_path
  }

  jobListings.append(job)


print(jobListings)

