#!/usr/bin/env python

import pymysql

class Session():

    conn = None

    def connect(self, hostname, portnumb, username, password, database):
        self.conn = pymysql.connect(host=hostname, 
                                    port=int(portnumb), 
                                    user=username, 
                                    passwd=password, 
                                    db=database)

    def getPeriodSQL(self, row_indx):
        cmd = "SELECT * FROM PERIOD"
        if (row_indx != "all"):
            cmd += " WHERE ID = '%s';" % row_indx;
        else:
            cmd += ";"
        return cmd

    def getPeriod(self, indx):
        pass

    def getAllPeriods(self):
        # create empty list
        rowdata = []
        # get SQL command
        sqlcmd = self.getPeriodSQL("all")
        # create cursor
        cur = self.conn.cursor()
        # execute SQL command
        cur.execute(sqlcmd)
        # get all rows
        for row in cur:            
            currow = {}
            currow["ID"      ] = str(row[0])
            currow["FIRSTDAY"] = str(row[1])
            currow["LASTDAY" ] = str(row[2])
            rowdata.append(currow)
        # close cursor
        cur.close()
        # return data
        return rowdata

    def addPeriod(self, firstday, lastday):
        # create sql cmd string
        sqlcmd = "INSERT INTO PERIOD (FIRSTDAY, LASTDAY) VALUES ('%s', '%s');"
        sqlcmd = sqlcmd % (firstday, lastday)
        # create cursor
        cur = self.conn.cursor()
        # execute SQL command
        cur.execute(sqlcmd)
        # close cursor
        cur.close()
        # commit changes to database        
        self.conn.commit()

    def getPeriod(self, indx):
        # create empty list
        rowdata = {}
        # get SQL command
        sqlcmd = self.getPeriodSQL(indx)
        # create cursor
        cur = self.conn.cursor()
        # execute SQL command
        cur.execute(sqlcmd)
        # get all rows
        for row in cur:            
            rowdata["ID"      ] = str(row[0])
            rowdata["FIRSTDAY"] = str(row[1])
            rowdata["LASTDAY" ] = str(row[2])
        # close cursor
        cur.close()
        # return data
        return rowdata

    def updatePeriod(self, indx, firstday, lastday):
        # create sql cmd string
        sqlcmd = "UPDATE PERIOD SET FIRSTDAY='%s', LASTDAY='%s' WHERE ID=%s;"
        sqlcmd = sqlcmd % (firstday, lastday, indx)
        # create cursor
        cur = self.conn.cursor()
        # execute SQL command
        cur.execute(sqlcmd)
        # close cursor
        cur.close()
        # commit changes to database        
        self.conn.commit()

    def delPeriod(self, indx):
        # create sql cmd string
        sqlcmd = "DELETE FROM PERIOD WHERE ID=%s;" % indx
        # create cursor
        cur = self.conn.cursor()
        # execute SQL command
        cur.execute(sqlcmd)
        # close cursor
        cur.close()
        # commit changes to database        
        self.conn.commit()

