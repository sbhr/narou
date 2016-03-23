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
        self.HOST = '127.0.0.1'
        self.DATABASE = 'narou'
        self.USER = 'shibahara'
        self.PASSWD = 'ylab920'
        self.PORT = 3306
        self.CHARSET = 'utf8'
        #Connect DB
        self.connector = MySQLdb.connect(host = self.HOST, db = self.DATABASE, user = self.USER, passwd = self.PASSWD, port = self.PORT, charset = self.CHARSET)
        self.cursor = self.connector.cursor()


    # Confirm with existing data
    def sql_confirm(self, table, column, value):

        sql = u'select id from %s where %s = "%s"' % (table, column, value)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if len(result) > 0:
            return True
        else:
            return False

    # Insert data into the database
    def sql_insert(self, table, data_array):

        values = []
        for i in data_array:
            if (type(i) != str and type(i) != unicode):
                values.append(str(i))
            else:
                values.append(i)
        values = '","'.join(values)
        sql = u'insert into %s values(NULL, "%s")' % (table, values)
        # print sql
        self.cursor.execute(sql)
        self.connector.commit()

    # Get record_id
    def get_record_id(self, table, column, value):

        sql = u'select id from %s where %s = "%s"' % (table, column, value)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        for row in result[0]:
            return row

    # Close database object
    def close(self):
        self.cursor.close()
        self.connector.close()

