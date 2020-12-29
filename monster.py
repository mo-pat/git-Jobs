import requests
from bs4 import BeautifulSoup
import re
import math

# Get user's position (city and province/state)
location_response = requests.get('http://ipinfo.io/json').json()
# store user city and province/state
# City (ex: 'Montreal')
user_city = location_response['city']
# State/Province (ex: 'Quebec')
user_region = location_response['region']

## Ask for job title from user
print('---gitJobs from Monster---')
job_search_title = input('Enter job search parameter: ').lower().split(" ")
jobURL = '-'.join(job_search_title)
print('Location: ' + str(user_city) + ', ' + str(user_region))

# Indeed URL with job title, user city and province as query parameters
# https://www.monster.ca/jobs/search/?q=Software-Developer&intcid=skr_navigation_nhpso_searchMain&where=Montreal__2c-QC&rad=20&tm=0
# URL = 'https://ca.indeed.com/jobs?q={}&l={}%2C+{}&fromage=1'.format(jobURL, user_city, user_region)
#https://www.monster.ca/jobs/search/?q=Software-Engineer&where=Montreal&rad=50&tm=1
URL = "https://www.monster.ca/jobs/search/?q={}&where={}&rad=50&tm=0".format(jobURL, user_city)
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
# print(getSearchResults)

for cards in getSearchResults:
  title = cards.find('h2', class_='title')
  company = cards.find('span', class_='name')
  location = cards.find('div', class_='location')
  path = cards.find('a')

  if None in (title, company, location):
    continue

  job = {
    "title": title.text.strip(),
    "company": company.text.strip(),
    "location": location.text.strip(),
    "job_URL": path['href'].strip()
  }

  jobListings.append(job)

  #print(title.text.strip())
  #print(company.text.strip())
  #print(location.text.strip())
  #print(path['href'].strip())
  #print()

count = 0
## print all jobs
for jobs in jobListings:
  count+=1
  print('Job#: ' + str(count))
  print(jobs['title'])
  print(jobs['company'])
  print(jobs['location'])
  print(jobs['job_URL'])
  print()


