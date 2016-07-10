#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   shibahara
# Created:  2016-02-03
#

import MySQLdb


class Database():
    '''Database util'''

    def __init__(self):
        # variable
        self.HOST = 'sbdb.cgzlcnft7ehv.ap-northeast-1.rds.amazonaws.com'
        self.DATABASE = 'narou'
        self.USER = 'shibahara'
        self.PASSWD = '8ik,.lo9'
        self.PORT = 63306
        self.CHARSET = 'utf8'
        #Connect DB
        self.connector = MySQLdb.connect(host = self.HOST, db = self.DATABASE, user = self.USER, passwd = self.PASSWD, port = self.PORT, charset = self.CHARSET)
        self.cursor = self.connector.cursor()


    # Confirm with existing data
    def sql_confirm(self, table, column, value):

        try:
            sql = 'select id from %s where %s = "%s"' % (table, column, MySQLdb.escape_string(value.encode('utf-8')))
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if len(result) > 0:
                return True
            else:
                return False
        except Exception as e:
            print e

    # Insert data into the database
    def sql_insert(self, table, data_array):

        try:
            values = []
            for i in data_array:
                if (type(i) != str and type(i) != unicode):
                    values.append(MySQLdb.escape_string(str(i)))
                else:
                    values.append(MySQLdb.escape_string(i.encode('utf-8')))
            values = '","'.join(values)
            sql = 'insert into %s values(NULL, "%s")' % (table, values)
            self.cursor.execute(sql)
            self.connector.commit()
        except Exception as e:
            print e

    # Get record_id
    def get_record_id(self, table, column, value):

        try:
            sql = 'select id from %s where %s = "%s"' % (table, column, MySQLdb.escape_string(value.encode('utf-8')))
            self.cursor.execute(sql)
            result = self.cursor.fetchall()

            for row in result[0]:
                return row
        except Exception as e:
            print e

    # Get result by using original sql
    def get_by_original_sql(self, sql):

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()

            for row in result:
                return row
        except Exception as e:
            print e

    # Get # of data
    def get_num_of_data(self, table, column, where="1"):

        try:
            sql = 'SELECT COUNT(DISTINCT %s) FROM %s WHERE %s' % (column, table, where)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()

            for row in result[0]:
                return row
        except Exception as e:
            print e

    # Close database object
    def close(self):
        self.cursor.close()
        self.connector.close()

