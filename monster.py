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
URL = "https://www.monster.ca/jobs/search/?q={}&where={}".format(jobURL, user_city)
print('URL: ' + str(URL))
root_url = 'https://www.monster.ca/'

# Array of job listings
jobListings = []

# Request URL
page = requests.get(URL)
print('status code: ' + str(page.status_code))

soup = BeautifulSoup(page.content, 'html.parser')
getSearchResults = soup.find_all(class_="card-content")
# print(getSearchResults)

for cards in getSearchResults:
  title = cards.find('a')
  print(title)

exit()
