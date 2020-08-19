# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-19 12:22:30
# @Last Modified by:   rish
# @Last Modified time: 2020-08-19 13:23:50

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


def read_in_chunks(file_object, chunk_size=1024 * 1024):
	'''
	Lazy function (generator) to read a file piece by piece.
	Default chunk size: 1MB.
	'''
	while True:
		data = file_object.read(chunk_size)
		if not data:
			break
		yield data


def process_chunk(piece, leftover, frame_for_day, last_date_recorded):

	lines = piece.split('\n')

	if len(lines) > 0:
		# Check if leftover available
		if leftover != '':
			lines[0] = (leftover + lines[0]).strip()

		# Check if last line from yield is a complete json
		try:
			if lines[-1][-1] != '}':
				leftover = lines[-1].strip()
				lowerbound = -2
			elif lines[-1][-1] != '\n':
				leftover = lines[-1].strip()
				lowerbound = -1
			else:
				leftover = ''
				lowerbound = -1
		except IndexError as e:
			lowerbound = len(lines) - 1

		lines_frame = pd.DataFrame(lines[0:lowerbound], columns=['json'])
		lines_frame = pd.json_normalize(lines_frame['json'].apply(json.loads))
		frame_for_day = frame_for_day.append(lines_frame)

	return leftover, frame_for_day, last_date_recorded


def process_frame_for_day(frame_for_day, stats_frame):

	medians_for_day = frame_for_day.groupby(['date', 'input']).median('value')
	medians_for_day.reset_index(inplace=True)
	medians_for_day.rename(columns={'value': 'median_value'}, inplace=True)
	stats_frame = stats_frame.append(medians_for_day)
	return stats_frame


# [START Function to load data in chunks and compute median]
def process_data_in_chunks(input_file, chunk_size, start_date):
	'''
	Function to load data in chunks and compute median. The function loada the
	data in chunks using the read in chunks function, processes the data in each
	chunk, handles incomplete lines and computes the data on daily basis.

	Args:
		- input file
		- chunk size
		- start_date
	Returns:
		- stats frame


	'''
	# Initialize required variables
	frame_for_day = pd.DataFrame(columns=['date', 'time', 'input', 'value'])
	stats_frame = pd.DataFrame(columns=['date', 'input', 'median_value'])
	leftover = ''
	last_date_recorded = '2019-01-01'

	with open(config.BASE_PATH + input_file) as f:

		for piece in read_in_chunks(f, chunk_size):
			leftover, frame_for_day, last_date_recorded = process_chunk(
				piece, leftover, frame_for_day, last_date_recorded
			)

			# Check if data for new Zdate has come in
			if frame_for_day.loc[frame_for_day.date > last_date_recorded].shape[0] > 0:
				stats_frame = process_frame_for_day(
					frame_for_day.loc[frame_for_day.date == last_date_recorded], stats_frame
				)
				frame_for_day = frame_for_day.loc[
					~(frame_for_day.date == last_date_recorded)
				]
				last_date_recorded = frame_for_day.date.unique()[0]

		stats_frame = process_frame_for_day(
			frame_for_day, stats_frame
		)

	return stats_frame
