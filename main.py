import requests
import re
import math
import json

import testImport as monster
import test_indeed as indeed

# jobs = monster.getMonster()

# Get user's position (city and province/state)
location_response = requests.get('http://ipinfo.io/json').json()
# store user city and province/state
# City (ex: 'Montreal')
user_city = location_response['city']
# State/Province (ex: 'Quebec')
user_region = location_response['region']

print('Location: ' + str(user_city) + ', ' + str(user_region))

## Ask for job title from user
job_search_title = input('Enter job search parameter: ').lower().split(" ")

# Create a list to store all job postings
job_postings = []

## Get jobs from monster
job_postings.extend(monster.getMonster(job_search_title, user_city, user_region))

## Get jobs from indeed
job_postings.extend(indeed.getIndeed(job_search_title, user_city, user_region))

print()
print('jobs : ')

for job in job_postings:
  print(job)
  print()

json_object = json.dumps(job_postings, indent=2)

with open("job.json", "w") as outfile:
  outfile.write(json_object)