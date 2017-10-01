#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   shibahara
# Created:  2016-02-03
#

import sys
import os
import json
import datetime
import logging
from logging import FileHandler, Formatter
from janome.tokenizer import Tokenizer
from database import Database


class Narou():
    '''Narou Analysis'''

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
        # File Setting
        self.file = open(json_file, 'r')
        self.json_data = json.load(self.file)
        # DB Setting
        self.DB = Database()
        self.date = ' '.join(os.path.splitext(json_file)[0].split('_')[1:])


    # Morphological analysis
    def morphological_analysis(self):

        # janome Setting
        t = Tokenizer()

        # Start Analysis
        self.logger.info('Analysis start.')
        logstr = 'Collection date:%s' % (self.date)
        self.logger.info(logstr)
        for row in self.json_data:
            cnt = 0
            print row['name']
            dataset = row[row['name']]
            while cnt < len(dataset)-1:
                try:
                    for i in xrange(cnt, len(dataset)):
                        cnt = i
                        tokens = t.tokenize(dataset[cnt]['title'])
                        self.insert_database(dataset[cnt], tokens, row['name'])
                except Exception as e:
                    logstr = 'Error:' + e.message
                    self.logger.error(logstr)
                    logstr = '[%d]%s' % (dataset[cnt]['rank'], dataset[cnt]['title'])
                    self.logger.error(logstr)
                    cnt += 1

        self.logger.info('Analysis is completed.')
        self.DB.close()
        self.file.close()


    # Insert analysis data into the database
    def insert_database(self, dataset, tokens, term):

        # Title
        table, column, value = 'analysis_title', 'name', dataset['title']
        if not self.DB.sql_confirm(table, column, value):
            data_array = [value]
            self.DB.sql_insert(table, data_array)
        title_id = self.DB.get_record_id(table, column, value)

        # Term
        table, column, value = 'analysis_term', 'type', term
        if not self.DB.sql_confirm(table, column, value):
            data_array = [value, '']
            self.DB.sql_insert(table, data_array)
        term_id = self.DB.get_record_id(table, column, value)

        # Score
        table = 'analysis_score'
        if "pt" in dataset['point']:
            data_array = [dataset['rank'], dataset['point'][:-2].replace(',',''), self.date, term_id, title_id]
        else:
            data_array = [dataset['rank'], dataset['point'].replace(',',''), self.date, term_id, title_id]
        self.DB.sql_insert(table, data_array)

        for row in tokens:
            # Part of Speech
            table, column, value = 'analysis_pos', 'type', row.part_of_speech.split(',')[0]
            if not self.DB.sql_confirm(table, column, value):
                data_array = [value]
                self.DB.sql_insert(table, data_array)
            pos_id = self.DB.get_record_id(table, column, value)

            # Letter
            table = 'analysis_letter'
            data_array = [row.surface, self.date, pos_id, term_id, title_id]
            self.DB.sql_insert(table, data_array)

# main
if __name__ == '__main__':

    argv = sys.argv

    if len(argv) < 2:
        print 'argv 1: Narou data'
        sys.exit('Error')

    narou = Narou(argv[1])
    narou.morphological_analysis()
