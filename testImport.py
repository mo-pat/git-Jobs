import requests
from bs4 import BeautifulSoup
import re
import math
import hashlib

def getMonster(job_title, city, region):

  print('---gitJobs from Monster---')
  jobURL = '-'.join(job_title)

  ## Add query string to request URL to get job postings
  URL = "https://www.monster.ca/jobs/search/?q={}&where={}&rad=50&tm=0".format(jobURL, city)
  print('URL: ' + str(URL))
  root_url = 'https://www.monster.ca/'

  # Array of job listings
  jobListings = []

  # Request URL
  page = requests.get(URL)
  print('status code: ' + str(page.status_code))
  print('---')

  soup = BeautifulSoup(page.content, 'html.parser')
  getSearchResults = soup.find_all('section', class_='card-content')

  for cards in getSearchResults:
    title = cards.find('h2', class_='title')
    company = cards.find('span', class_='name')
    location = cards.find('div', class_='location')
    path = cards.find('a')

    # If no job card tags are found in html, go to next card
    if None in (title, company, location):
      continue

    # Include a hash ID that will be parsed using the job title + company name
    # hash_string: "Job Title" + "Company Name"
    hash_string = title.text.strip() + " " + company.text.strip()
    hash_id = hashlib.md5(hash_string.encode('utf-8')).hexdigest()

    job = {
      "hash_id": hash_id,
      "title": title.text.strip(),
      "company": company.text.strip(),
      "location": location.text.strip(),
      "job_URL": path['href'].strip()
    }

    jobListings.append(job)


  # Return job listings
  return jobListings


## FOR DEBUGGING
getTitle = input('Enter job search parameter: ').lower().split(" ")
test = getMonster(getTitle, 'Montréal', 'QC')

for job in test:
  print(job)
  print()