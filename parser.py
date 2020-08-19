# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-19 12:02:17
# @Last Modified by:   rish
# @Last Modified time: 2020-08-19 12:31:29


### Imports START
import argparse
### Imports END


# [START Function to define parser]
def parser_args():
	'''
	Function to define the structure for command line arguments parser.

	Args:
		-
	Retuns:
		- args
	'''

	parser = argparse.ArgumentParser(
		description='Pipeline to parse the log files from the IOT system and\
		get the output file with the median values for the sensors day wise.\
		Application can be run in two ways.'
	)

	parser.add_argument(
		'--mode', dest='mode', choices=['full', 'chunked'], default='chunked',
		help='Use full mode to load the complete input file and batches to \
		load the input file in chunks,'
	)

	parser.add_argument(
		'--chunk_size', dest='chunk_size', type=int, default=1024 * 1024 * 10,
		help='Use this to specify the size of chunks in  which the file is \
		loaded. The default size for the chunks is 10 MB.'
	)

	parser.add_argument(
		'--input_file', dest='input', type=str,
		help='Use this to specify the input file path.'
	)

	parser.add_argument(
		'--target', dest='target', type=str, default='output.jsonl',
		help='Use this file to specify the target file in  which the output is\
		to be stored.'
	)

	parser.add_argument(
		'--env', choices=['dev', 'prod'], default='dev',
		help='Use this argument to specify whether the processes are to be run in a\
		development environment or production.'
	)

	# Parsing the arguments received
	args = parser.parse_args()

	return args
