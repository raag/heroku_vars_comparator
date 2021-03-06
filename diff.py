#!/usr/bin/env python3

import requests
import sys

BOLD = '\033[1m'
BOLD_END = '\033[0m'


if len(sys.argv) < 4:
	print('Usage: diff.py <heroku_api_key> <app1> <app2>')
	sys.exit(1)

HEROKU_API_KEY = sys.argv[1]
APP1 = sys.argv[2]
APP2 = sys.argv[3]


def get_heroku_vars_diff(app1, app2):
	vars_app_1 = get_heroku_vars(app1) 
	vars_app_2 = get_heroku_vars(app2)
	var_names_app_1 = set(vars_app_1.keys())
	var_name_app_2 = set(vars_app_2.keys())
	return var_names_app_1.difference(var_name_app_2), var_name_app_2.difference(var_names_app_1)


def get_heroku_vars(app):
	return requests.get('https://api.heroku.com/apps/{}/config-vars'.format(app), headers={
		'Accept': 'application/vnd.heroku+json; version=3',
		'Authorization': 'Bearer {}'.format(HEROKU_API_KEY)
	}).json()

def print_formatted_vars(vars):
	for var in vars:
		print(f'\t- {var}')


if __name__ == '__main__':
	diffs = get_heroku_vars_diff(APP1, APP2)
	if (len(diffs[0]) > 0 or len(diffs[1]) > 0):
		print('\n')
		print(f'Differences between {BOLD}{APP1}{BOLD_END} and {BOLD}{APP2}{BOLD_END}:')
		print('\n')
		if len(diffs[0]) > 0:
			print(f'Only in {BOLD}{APP1}{BOLD_END}:')
			print_formatted_vars(diffs[0])
			print('\n')
		if len(diffs[1]) > 0:
			print(f'Only in {BOLD}{APP2}{BOLD_END}:')
			print_formatted_vars(diffs[1])
			print('\n')
		sys.exit(1)
	print('\n')
