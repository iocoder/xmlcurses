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

    def getTransactSQL(self, row_indx, firstday, lastday):
        sqlcmd  = "SELECT *, "
        sqlcmd += "(SELECT SUM(T2.AMNT) FROM TRANSACT AS T2 WHERE T2.CARD='DEBIT' AND "
        sqlcmd += "(T2.DAY < T1.DAY OR (T2.DAY = T1.DAY AND T2.ID <= T1.ID))"
        sqlcmd += ") AS 'DEBIT', "
        sqlcmd += "(SELECT SUM(AMNT) FROM TRANSACT AS T3 WHERE T3.CARD='CREDIT' AND "
        sqlcmd += "(T3.DAY < T1.DAY OR (T3.DAY = T1.DAY AND T3.ID <= T1.ID))"
        sqlcmd += ") AS 'CREDIT' "
        sqlcmd += "FROM TRANSACT AS T1 WHERE %s "
        sqlcmd += "ORDER BY DAY, ID;"
        if row_indx != "all":
            sqlcmd = sqlcmd % "ID = '%s'" % row_indx;
        else:
            sqlcmd = sqlcmd % ("T1.DAY >= '%s' AND T1.DAY <= '%s'" % (firstday, lastday))
        return sqlcmd

    def getAllTransacts(self, firstday, lastday):
        # create empty list
        rowdata = []
        # get SQL command
        sqlcmd = self.getTransactSQL("all", firstday, lastday)
        # create cursor
        cur = self.conn.cursor()
        # execute SQL command
        cur.execute(sqlcmd)
        # get all rows
        for row in cur:            
            currow = {}
            currow["ID"    ] = str(row[0])
            currow["DAY"   ] = str(row[1])
            currow["NAME"  ] = str(row[2])
            currow["CARD"  ] = str(row[3])
            currow["AMNT"  ] = str(row[4])
            currow["DEBIT" ] = str(row[5])
            currow["CREDIT"] = str(row[6])
            rowdata.append(currow)
        # close cursor
        cur.close()
        # return data
        return rowdata

    def addTransact(self, day, name, card, amnt):
        # create sql cmd string
        sqlcmd = "INSERT INTO TRANSACT (DAY, NAME, CARD, AMNT) VALUES ('%s', '%s', '%s', '%s');"
        sqlcmd = sqlcmd % (day, name, card, amnt)
        # create cursor
        cur = self.conn.cursor()
        # execute SQL command
        cur.execute(sqlcmd)
        # close cursor
        cur.close()
        # commit changes to database        
        self.conn.commit()

    def getTransact(self, indx):
        # create empty list
        rowdata = {}
        # get SQL command
        sqlcmd = self.getTransactSQL(indx, None, None)
        # create cursor
        cur = self.conn.cursor()
        # execute SQL command
        cur.execute(sqlcmd)
        # get all rows
        for row in cur:            
            rowdata["ID"    ] = str(row[0])
            rowdata["DAY"   ] = str(row[1])
            rowdata["NAME"  ] = str(row[2])
            rowdata["CARD"  ] = str(row[3])
            rowdata["AMNT"  ] = str(row[4])
            rowdata["DEBIT" ] = str(row[5])
            rowdata["CREDIT"] = str(row[6])
        # close cursor
        cur.close()
        # return data
        return rowdata

    def updateTransact(self, indx, day, name, card, amnt):
        # create sql cmd string
        sqlcmd = "UPDATE TRANSACT SET DAY='%s', NAME='%s', CARD='%s', AMNT='%s' WHERE ID=%s;"
        sqlcmd = sqlcmd % (day, name, card, amnt, indx)
        # create cursor
        cur = self.conn.cursor()
        # execute SQL command
        cur.execute(sqlcmd)
        # close cursor
        cur.close()
        # commit changes to database        
        self.conn.commit()

    def delTransact(self, indx):
        # create sql cmd string
        sqlcmd = "DELETE FROM TRANSACT WHERE ID=%s;" % indx
        # create cursor
        cur = self.conn.cursor()
        # execute SQL command
        cur.execute(sqlcmd)
        # close cursor
        cur.close()
        # commit changes to database        
        self.conn.commit()

