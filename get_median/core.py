# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-19 12:22:27
# @Last Modified by:   rish
# @Last Modified time: 2020-08-20 00:30:34

### Imports START
import logging

from get_median import utils
### Imports END

### Global declarations
logger = logging.getLogger(__name__)


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
	logger.info('Loading data into memory')
	jsonl_data = utils.get_data(input_file)

	# compute stats
	logger.info('Computing medians for each day')
	stats_frame = utils.compute_median_overall(jsonl_data)

	# output
	logger.info('Creating output file')
	utils.output_to_jsonl(stats_frame, target_file)

	return
# [END]


# [START Procedure to calculate median and create output]
def get_median_for_sesnors_chunked(
	input_file, target_file, chunk_size
):
	'''
	Procedure to calculate median and create output while loading data in chunks.

	Args:
		- input file
		- target file
		- chunk size
	Rerruns:
		-
	'''

	# Load and process chunks
	logger.info('Laoding data in chunks and processing them')
	stats_frame = utils.process_data_in_chunks(input_file, chunk_size)

	# output
	logger.info('Creating output file')
	utils.output_to_jsonl(stats_frame, target_file)

	return
# [END]
