# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-19 12:22:30
# @Last Modified by:   rish
# @Last Modified time: 2020-08-20 00:37:52

### Imports START
import config
import json
import logging
import pandas as pd
### Imports END


### Global declarations
logger = logging.getLogger(__name__)


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
		data = f.read().splitlines()

	# Parse json
	df = pd.DataFrame(data, columns=['json'])
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


# [START Function to read file in chunks]
def read_in_chunks(file_object, chunk_size=1024 * 1024):
	'''
	Lazy function (generator) to read a file piece by piece.
	Default chunk size: 1MB.

	Args:
		- file object
		- chunk size
	Returns:
		- data generator object
	'''
	logger.info('Initialized generator object to read data in chunks')
	while True:
		data = file_object.read(chunk_size)
		if not data:
			break
		yield data
# [END]


# [START Function to process the specific data chunks]
def process_chunk(piece, leftover, frame_for_day):
	'''
	Function to process the specific data chunks. Fuction takes in the
	specific data chunk, left over string from previous parse, frame for
	current date and the last recorded date.

	Args:
		- piece
		- leftover
		- frame for date
	Returns:
		- leftover string after processing chunk
		- updated frame for date
	'''
	# Extracting lines from chunk receoved
	lines = piece.split('\n')

	# Check if data is available
	if len(lines) > 0:

		# Check if leftover available
		if leftover != '':
			lines[0] = (leftover + lines[0]).strip()

		# Check if last line from yield is a complete json string
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
			# Handling case for EOL
			lowerbound = len(lines) - 1
			logger.error(e)
			logger.info('Reached end of file')

		# Process json strings to get the data in pandas
		lines_frame = pd.DataFrame(lines[0:lowerbound], columns=['json'])
		lines_frame = pd.json_normalize(lines_frame['json'].apply(json.loads))

		# Append data in existing frame for the date
		frame_for_day = frame_for_day.append(lines_frame)

	return leftover, frame_for_day
# [END]


# [START Function to process the data for the day to update stats frame]
def process_frame_for_day(frame_for_day, stats_frame, last_date_recorded):
	'''
	Function to process the data for the day to update stats frame.

	Args:
		- Frame for date
		- current stats frame
	Returns:
		- updated stats frame
	'''

	# Group by sensors and date
	medians_for_day = frame_for_day.groupby(['date', 'input']).median('value')
	medians_for_day.reset_index(inplace=True)
	medians_for_day.rename(columns={'value': 'median_value'}, inplace=True)

	# Append data to previously recorded data.
	stats_frame = stats_frame.append(medians_for_day)

	logger.info('Medians computed for {}'.format(last_date_recorded))
	return stats_frame
# [END]


# [START Function to return the start date]
def get_start_date(input_file):
	'''
	Function to read the first line of the input file and return the start
	date for the log data.
	Args:
		- input file
	Returns:
		- start date
	'''
	with open(config.BASE_PATH + input_file, 'r') as f:
		_json = f.readline()
	first_line = json.loads(_json)
	return first_line['date']
# [END]


# [START Function to load data in chunks and compute median]
def process_data_in_chunks(input_file, chunk_size):
	'''
	Function to load data in chunks and compute median. The function loads the
	data in chunks using the read in chunks function, processes the data in each
	chunk, handles incomplete lines and computes the data on daily basis.

	Args:
		- input file
		- chunk size
	Returns:
		- stats frame
	'''

	# Initialize required variables
	frame_for_day = pd.DataFrame(columns=['date', 'time', 'input', 'value'])
	stats_frame = pd.DataFrame(columns=['date', 'input', 'median_value'])
	leftover = ''
	last_date_recorded = get_start_date(input_file)

	# Context to read file
	with open(config.BASE_PATH + input_file) as f:

		# Processing filke chunks
		for idx, piece in enumerate(read_in_chunks(f, chunk_size)):
			leftover, frame_for_day = process_chunk(
				piece, leftover, frame_for_day
			)

			# Check if data for new date has come in
			if frame_for_day.loc[frame_for_day.date > last_date_recorded].shape[0] > 0:

				# Get median values for previous date when new date comes in
				stats_frame = process_frame_for_day(
					frame_for_day.loc[frame_for_day.date == last_date_recorded],
					stats_frame, last_date_recorded
				)

				# Drop records out of memory for previous date after stats have updated
				frame_for_day = frame_for_day.loc[
					~(frame_for_day.date == last_date_recorded)
				]

				# Update last_date_recorded
				last_date_recorded = frame_for_day.date.unique()[0]

		stats_frame = process_frame_for_day(
			frame_for_day, stats_frame, last_date_recorded
		)
		logger.info(
			'File processed in {} chunks of size {} bytes'.format(idx, chunk_size)
		)
		logger.info('')

	return stats_frame
# [END]
