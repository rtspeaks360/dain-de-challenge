# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-19 12:22:30
# @Last Modified by:   rish
# @Last Modified time: 2020-08-19 12:51:51

import config
import json
import pandas as pd


# [START Function to get data into memory in one go]
def get_data(input_file):
	'''
	Function to load the data in memory in one go.

	Args:
		- input file name / relative path
	Returns:
		- parsed data frame
	'''

	# Get data in memory
	with open(config.BASE_PATH + input_file) as f:
		data = f.read()

	# Parse json
	df = pd.DataFrame(data, columns='json')
	df = pd.json_normalize(df['json'].apply(json.loads))

	return df
# [END]


# [START Function to compute median values overall.]
def compute_median_overall(df):
	'''
	Function to compute median values overall.

	Args:
		- df
	returns:
		- medians frame
	'''

	# Group by and compute median
	medians_df = df.groupby(['date', 'input']).median('value')
	medians_df.reset_index(inplace=True)
	medians_df.rename(columns={'value': 'median_value'}, inplace=True)
	return df
# [END]


# [START write the given frame into given targetfile in jsonl]
def output_to_jsonl(df, target_file):
	'''
	Function to write the given frame into given targetfile in jsonl format.

	Args:
		- dataframe
		- target file
	'''

	# write into file
	df.to_json(
		config.BASE_PATH + target_file,
		orient='records', lines=True
	)
	return
# [END]
