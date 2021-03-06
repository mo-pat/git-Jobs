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
print('---gitJobs from Indeed---')
job_search_title = input('Enter job search parameter: ').lower().split(" ")
jobURL = '+'.join(job_search_title)
print('Location: ' + str(user_city) + ', ' + str(user_region))

# Indeed URL with job title, user city and province as query parameters
URL = 'https://ca.indeed.com/jobs?q={}&l={}%2C+{}&fromage=1'.format(jobURL, user_city, user_region)
print('URL: ' + str(URL))
root_url = 'https://ca.indeed.com'

## TODO: Get location of users request (currently fixed for 'Montreal, QC')

# Get total number of pagination (iteration count)
getPage = requests.get(URL)
getSoup = BeautifulSoup(getPage.content, 'html.parser')
getCount = getSoup.find(id='searchCountPages')

## Check if no search count is available, indicating no search results were found
## Return nothing
if getCount is None:
  print('Sorry, no jobs found on Indeed')
  exit()

# Grab numbers from new jobs string
paginationCount = re.findall(r'\b\d+\b', getCount.text)

# FOR DEBUG
print('---')
print(paginationCount[1])
print(math.ceil(int(paginationCount[1])/15))
print('---')

page_limit = math.ceil(int(paginationCount[1])/15)

# Array of job listings
jobListings = []

# pageCount for url
pageCount = 0
page_route = '&start={}'.format(pageCount)

while(pageCount < page_limit*10):

  # Add next page query parameter to URL to request new jobs
  if (pageCount > 0):
    myURL = URL + '&start={}'.format(pageCount)
  else:
    myURL = URL

  pageCount+=10

  # Request URL
  page = requests.get(myURL)

  # print routes
  print(myURL)
  print('status code: ' + str(page.status_code))
  print()

  # If request fails, get out of loop
  if page.status_code != 200:
    print('Unable to process GET request for: ' + str(myURL))
    break

  soup = BeautifulSoup(page.content, 'html.parser')
  results = soup.find(id='resultsCol')
  resultsCards = soup.find_all(class_="jobsearch-SerpJobCard")

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
      "job_URL": full_path
    }

    jobListings.append(job)


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

