# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-19 12:17:23
# @Last Modified by:   rish
# @Last Modified time: 2020-08-19 12:18:44

import os

if os.environ.keys().__contains__('ENV-INDICATOR') \
	and os.environ['ENV-INDICATOR'] == 'PROD':
	# Environment string
	env_str = 'PROD'
	BASE_PATH = os.environ['SCPATH']
else:
	# Environment string
	env_str = 'DEV'
	BASE_PATH = ''
