import requests
import re
import math

import testImport as monster

# jobs = monster.getMonster()

print(jobs)

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

