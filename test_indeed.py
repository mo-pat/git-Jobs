import requests
from bs4 import BeautifulSoup
import re
import math
import hashlib
import json

def getIndeed(job_title, city, region):

  print('---gitJobs from Indeed---')
  jobURL = '+'.join(job_title)

  ## Add query string to request URL to get job postings
  URL = 'https://ca.indeed.com/jobs?q={}&l={}%2C+{}&fromage=1'.format(jobURL, city, region)
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
    return

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
      # Include a hash ID that will be parsed using the job title + company name
      # hash_string: "Job Title" + "Company Name"
      hash_string = title.text.strip() + " " + company.text.strip()
      hash_id = hashlib.md5(hash_string.encode('utf-8')).hexdigest()

      #print(title.text.strip())
      #print(company.text.strip())
      #print(location.text.strip())
      #print(full_path)

      job = {
        "hash_id": hash_id,
        "title": title.text.strip(),
        "company": company.text.strip(),
        "location": location.text.strip(),
        "job_URL": full_path
      }

      jobListings.append(job)


  return jobListings

## FOR DEBUGGING
# title = input('Enter job search parameter: ').lower().split(" ")
# test = getIndeed(title, 'Montréal', 'QC')

# for job in test:
#   print(job)
#   print()


# json_object = json.dumps(test, indent=4)

# with open("sample_inded.json", "w") as outfile:
#   outfile.write(json_object)