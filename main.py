import requests
from time import sleep
from random import randrange


# Stack Overflow API KEY
API_KEY = ''

# User Location
LOCATIONS = ['Romania', 'Moldova']

# User minimum reputation
MIN_REPUTATION = 223

# User tags
TAGS = ['java', '.net', 'docker', 'c#']

# User minimum answers count
MIN_ANSWERS = 1

# Users page count to check
PAGES_TO_PARSE = 30

# Users per page
PAGESIZE = 100


# Getting all user tags
def get_user_tags(account_id):
	has_more = True
	page = 1
	tags = []
	while has_more:
		try:
			response = requests.get(f'https://api.stackexchange.com/2.3/users/{account_id}/tags?page={page}&pagesize=100&order=desc&sort=popular&site=stackoverflow&key={API_KEY}').json()
		except Exception as ex:
			print(ex)

		for i in range(0, 100):
			try:
				tags.append(response['items'][i]['name'])
			except Exception:
				continue
		try:
			has_more = response['has_more']
		except Exception:
			has_more = False

		page += 1
	return tags


# Getting user information
def get_data(page):
	has_more = True
	try:
		response = requests.get(f'https://api.stackexchange.com/2.3/users?page={page}&pagesize={PAGESIZE}&order=desc&sort=reputation&site=stackoverflow&key={API_KEY}&filter=!LnNkvq1K.9fD9cvj5ZlZKF').json()
	except Exception as ex:
		print(ex)

	for i in range(0, PAGESIZE):
		try:
			account_id = response['items'][i]['account_id']
			location = response['items'][i]['location']
			reputation = response['items'][i]['reputation']
			answer_count = response['items'][i]['answer_count']
			question_count = response['items'][i]['question_count']
			user_name = response['items'][i]['display_name']
			profile_link = response['items'][i]['link']
			profile_image = response['items'][i]['profile_image']
			has_more = response['has_more']
		except Exception:
			continue

		if reputation >= MIN_REPUTATION:
			if answer_count >= MIN_ANSWERS:
				if any(x in location for x in LOCATIONS):
					tags = get_user_tags(account_id)
					if all(x in tags for x in TAGS):
						user_name = response['items'][0]['display_name']
						profile_link = response['items'][0]['link']
						profile_image = response['items'][0]['profile_image']
						tags = ', '.join(tags)
						print(f'User name: {user_name}, Location: {location}, Answer count: {answer_count}, Question count: {question_count}, Tags: {tags}, Profile: {profile_link}, Avatar: {profile_image}')
						print('Searching...')
	return has_more


def main():
	print('Searching...')
	for i in range(1, PAGES_TO_PARSE + 1):
		has_more = get_data(i)
		if has_more:
			sleep(randrange(1, 3))
		else:
			break
	print('All done!')


if __name__ == '__main__':
	main()
