#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   shibahara
# Created:  2016-05-16
#

import sys
import os
import datetime
import logging
from logging import FileHandler, Formatter
from database import Database


class Overview():
    '''Overview of data'''

    def __init__(self, json_file):
        # Log Setting
        self.LOG_DIR = './log/'
        logging.basicConfig(level = logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.formatter = Formatter(fmt = '%(asctime)s  %(message)s', datefmt = '%Y/%m/%d %p %I:%M:%S',)
        self.logfilename = self.LOG_DIR + 'narou_analysis-' + datetime.datetime.now().strftime('%Y-%m') + '.log'
        self.file_handler = FileHandler(self.logfilename, 'a+')
        self.file_handler.level = logging.INFO
        self.file_handler.formatter = self.formatter
        self.logger.addHandler(self.file_handler)
        # DB Setting
        self.DB = Database()
        self.date = ' '.join(os.path.splitext(json_file)[0].split('_')[1:])


    # Morphological analysis
    def calc(self):

        # Start calculation
        self.logger.info('calculate overview of data.')

        # overview of letter
        table, column, where = 'analysis_letter', 'value', 'pos_id = 2 and date = "%s"' % (self.date)
        daily_num_of_letter = self.DB.get_num_of_data(table, column, where)
        where = 'pos_id = 2 and date <= "%s"' % (self.date)
        total_num_of_letter = self.DB.get_num_of_data(table, column, where)

        # overview of title
        table, column, where = 'analysis_score', 'title_id', 'date = "%s"' % (self.date)
        daily_num_of_title = self.DB.get_num_of_data(table, column, where)
        where = 'date <= "%s"' % (self.date)
        total_num_of_title = self.DB.get_num_of_data(table, column, where)

        # Insert
        table = 'analysis_overview'
        data_array = [daily_num_of_letter, daily_num_of_title, total_num_of_letter, total_num_of_title, self.date]
        self.DB.sql_insert(table, data_array)

        self.logger.info('calculation is completed.')
        self.DB.close()

# main
if __name__ == '__main__':

    argv = sys.argv

    if len(argv) < 2:
        print 'argv 1: Narou data'
        sys.exit('Error')

    overview = Overview(argv[1])
    overview.calc()
