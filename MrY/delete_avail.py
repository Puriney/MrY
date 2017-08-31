'''
Delete available installations at root_dir
'''
import os
import glob
from tabulate import tabulate
from collections import defaultdict, OrderedDict
from operator import itemgetter
from MrY import join_path as jpath
