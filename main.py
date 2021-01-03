import requests
import re
import math

import testImport as monster

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

## Get jobs from monster
jobs_monster = monster.getMonster(job_search_title, user_city, user_region)

## Get jobs from indeed

print(jobs_monster)

