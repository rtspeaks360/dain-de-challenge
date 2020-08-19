# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-19 12:02:45
# @Last Modified by:   rish
# @Last Modified time: 2020-08-19 13:14:15


### Imports START
import os
import sys
import time
import logging

import parser
### Imports END

# Logger settings
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get script name and extract script path.
script_name = sys.argv[0]
script_path = script_name[:-8]

# Get arguments received
args = parser.parser_args()


if args.env == 'prod':
	print('prod environment')
	os.environ['ENV-INDICATOR'] = 'PROD'
	os.environ['SCPATH'] = script_path

	# Activate virtual environment with installed dependencies
	activate_this = script_path + 'env/bin/activate_this.py'
	with open(activate_this) as file_:
		exec(file_.read(), dict(__file__=activate_this))

	# Use project directory
	sys.path.insert(0, script_path)
else:
	os.environ['ENV-INDICATOR'] = 'DEV'


from get_median import core as get_median


# [START Main function for the script]
def main(args):
	'''
	Main function that handles the main functionality for the command line
	application.

	Args:
		Arguments from argparse
	Returns:
		None
	'''

	if args.mode == 'full':
		get_median.get_median_for_sesnors_full(
			args.input, args.target
		)
	elif args.mode == 'chunked':
		get_median.get_median_for_sesnors_chunked(
			args.input, args.target, args.chunk_size, args.start_date
		)
	else:
		logger.error('Invalid mode input.')
	return
# [END]


if __name__ == '__main__':
	# Process start time
	process_start = time.time()

	logger.info('Your namespace - ' + str(args))
	logger.info('')

	# Call for main function
	main(args)

	process_time = time.time() - process_start
	mins = int(process_time / 60)
	secs = int(process_time % 60)

	logger.info(
		'Total time consumed: {mins} minutes {secs} seconds'
		.format(mins=mins, secs=secs)
	)
	logger.info('')
	logger.info('-*-*-*-*-*-*-*-*-*-*-*-*-END-*-*-*-*-*-*-*-*-*-*-*-*-')
	logger.info('')
