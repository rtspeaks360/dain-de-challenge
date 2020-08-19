# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-19 12:22:27
# @Last Modified by:   rish
# @Last Modified time: 2020-08-19 13:15:13

### Imports START
from get_median import utils

### Imports END


# [START Procedure to calculate median and create output]
def get_median_for_sesnors_full(input_file, target_file):
	'''
	Procedure to compute required median values and create the output while\
	loading all the data in memory at one time.

	Args:
		- input file
		- tagret file
	'''
	# get data
	jsonl_data = utils.get_data_frame(input_file)

	# compute stats
	stats_frame = utils.compute_median_overall(jsonl_data)

	# output
	utils.output_to_jsonl(stats_frame, target_file)

	return
# [END]


# [START Procedure to calculate median and create output]
def get_median_for_sesnors_chunked(
	input_file, target_file, chunk_size, start_date
):
	'''
	Procedure to calculate median and create output while loading data in chunks.

	Args:
		- input file
		- target file
		- chunk size
		- start date
	'''

	# Load and process chunks
	stats_frame = utils.process_data_in_chunks(input_file, chunk_size, start_date)

	# output
	utils.output_to_jsonl(stats_frame, target_file)

	return
# [END]
