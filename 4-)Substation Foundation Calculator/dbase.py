import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    #WHEN PROGRAM STARTS

    def restartDatabase(self):
        self.cur.execute("DELETE FROM dimensions_tubular")
        self.cur.execute("DELETE FROM dimensions_wire")
        self.cur.execute("DELETE FROM channeldimensions")
        self.cur.execute("DELETE FROM foundationperfeeder")
        self.cur.execute("DELETE FROM site_work_dimension")
        self.cur.execute("INSERT INTO dimensions_tubular SELECT * FROM basedimensions_tubular")
        self.cur.execute("INSERT INTO dimensions_wire SELECT * FROM basedimensions_wire")
        self.cur.execute("INSERT INTO channeldimensions SELECT * FROM basechanneldimensions")
        self.cur.execute("INSERT INTO foundationperfeeder SELECT * FROM basefoundationperfeeder")
        self.cur.execute("INSERT INTO site_work_dimension SELECT * FROM basesite_work_dimension")
        self.conn.commit()

    def resetConfiguration(self):
        self.cur.execute("DELETE FROM foundationperfeeder")
        self.cur.execute("INSERT INTO foundationperfeeder SELECT * FROM basefoundationperfeeder")
        self.conn.commit()

    def resetFoundationDimensions(self):
        self.cur.execute("DELETE FROM dimensions_tubular")
        self.cur.execute("DELETE FROM dimensions_wire")
        self.cur.execute("INSERT INTO dimensions_tubular SELECT * FROM basedimensions_tubular")
        self.cur.execute("INSERT INTO dimensions_wire SELECT * FROM basedimensions_wire")
        self.conn.commit()

    def resetChannelDimensions(self):
        self.cur.execute("DELETE FROM channeldimensions")
        self.cur.execute("INSERT INTO channeldimensions SELECT * FROM basechanneldimensions")
        self.conn.commit()

    def drop_table_works(self):
        self.cur.execute("DROP TABLE IF EXISTS works")
        self.conn.commit()

    def fetchFoundationTubular(self,type):
        self.cur.execute("SELECT foundationtype,equipment,a,b,c,d,e,f,h,fill,bolt,pedestal,es,steel,g,itemtype FROM dimensions_tubular WHERE type = '{}' ".format(type))
        rows = self.cur.fetchall()
        return rows

    def fetchFoundationWire(self,type):
        self.cur.execute("SELECT foundationtype,equipment,a,b,c,d,e,f,h,fill,bolt,pedestal,es,steel,g,itemtype FROM dimensions_wire WHERE type = '{}' ".format(type))
        rows = self.cur.fetchall()
        return rows

    def fetchCable(self,type):
        self.cur.execute("SELECT item,d,e,f,g,fill,divisionwall,channel_length,coverlength,itemtype from channeldimensions WHERE type = '{}' ".format(type))
        rows = self.cur.fetchall()
        return rows

    def fetchFoundationTubular110(self):
        self.cur.execute("SELECT * FROM dimensions_tubular WHERE type = '110kv' ")
        rows = self.cur.fetchall()
        return rows

    def fetchCable110(self):
        self.cur.execute("SELECT * FROM channeldimensions WHERE type = '110kv' ")
        rows = self.cur.fetchall()
        return rows

    def fetchFoundationTubular220(self):
        self.cur.execute("SELECT * FROM dimensions_tubular WHERE type = '220kv' ")
        rows = self.cur.fetchall()
        return rows

    def fetchCable220(self):
        self.cur.execute("SELECT * FROM channeldimensions WHERE type = '220kv' ")
        rows = self.cur.fetchall()
        return rows

    def fetchFoundationTubular500(self):
        self.cur.execute("SELECT * FROM dimensions_tubular WHERE type = '500kv' ")
        rows = self.cur.fetchall()
        return rows

    def fetchCable500(self):
        self.cur.execute("SELECT * FROM channeldimensions WHERE type = '500kv' ")
        rows = self.cur.fetchall()
        return rows

    def fetchFoundationWire110(self):
        self.cur.execute("SELECT * FROM dimensions_wire WHERE type = '110kv' ")
        rows = self.cur.fetchall()
        return rows

    def fetchFoundationWire220(self):
        self.cur.execute("SELECT * FROM dimensions_wire WHERE type = '220kv' ")
        rows = self.cur.fetchall()
        return rows

    def fetchFoundationWire500(self):
        self.cur.execute("SELECT * FROM dimensions_wire WHERE type = '500kv' ")
        rows = self.cur.fetchall()
        return rows

    def fetchChannelDimensions(self):
        self.cur.execute("SELECT * FROM channel_dimensions")
        rows = self.cur.fetchall()
        return rows

    def fetchFoundationPerFeeder(self):
        self.cur.execute("SELECT * FROM foundationperfeeder")
        rows = self.cur.fetchall()
        return rows

    def fetchfeederType110(self,feedertype):
        self.cur.execute("SELECT F13,2*F14,F15,F16,F17,F18,F19,F11,F11A,F11C,F12 FROM foundationperfeeder WHERE feedertype ='{}'".format(feedertype))
        feeders = self.cur.fetchall()
        return feeders

    def fetchfeederType110_base(self,feedertype):
        self.cur.execute("SELECT F13,F14,F15,F16,F17,F18,F19,F11,F11A,F11C,F12 FROM foundationperfeeder WHERE feedertype ='{}'".format(feedertype))
        feeders = self.cur.fetchall()
        return feeders

    def fetchfeederType220(self,feedertype):
        self.cur.execute("SELECT F21,F21A,F21C,F22,F23,3*F24,F25,F26,F27,F28,F29 FROM foundationperfeeder WHERE feedertype ='{}'".format(feedertype))
        feeders = self.cur.fetchall()
        return feeders

    def fetchfeederType220_base(self, feedertype):
        self.cur.execute("SELECT F21,F21A,F21C,F22,F23,F24,F25,F26,F27,F28,F29 FROM foundationperfeeder WHERE feedertype ='{}'".format(feedertype))
        feeders = self.cur.fetchall()
        return feeders

    def fetchfeederType500(self,feedertype):
        self.cur.execute("SELECT F31,F31A,F32,F33,F34,F35,F36,F37,F38 FROM foundationperfeeder WHERE feedertype ='{}'".format(feedertype))
        feeders = self.cur.fetchall()
        return feeders

    def fetchfeederType500_base(self,feedertype):
        self.cur.execute("SELECT F31,F31A,F32,F33,F34,F35,F36,F37,F38 FROM foundationperfeeder WHERE feedertype ='{}'".format(feedertype))
        feeders = self.cur.fetchall()
        return feeders

    def fetchResultsTubular(self):
        all = []
        columns = ['110kv','220kv','500kv']
        for column in columns:
            self.cur.execute("SELECT feedertype , SUM(strfill), SUM(lean_conc), SUM(concrete), SUM(secondary_concrete), SUM(formwork+formwork_precast), SUM(rebar), SUM(embedded_steel), SUM(anchor), SUM(steel), SUM(concrete_protection), SUM(water_stopper), SUM(joint_isolation) FROM results_foundation_tubular WHERE feedertype='{}' ".format(column))
            all.append(self.cur.fetchall())
        return all

    def fetchResultsBackfillTubular(self,feedertype):
        self.cur.execute("SELECT SUM(strfill + lean_conc + concrete - secondary_concrete) FROM results_foundation_tubular WHERE feedertype='{}' AND itemtype = 'foundation' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultsBackfillWire(self,feedertype):
        self.cur.execute("SELECT SUM(strfill + lean_conc + concrete - secondary_concrete) FROM results_foundation_wire WHERE feedertype='{}' AND itemtype = 'foundation' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultTubularExcavation(self,feedertype):
        self.cur.execute("SELECT SUM(exc) FROM results_foundation_tubular WHERE feedertype='{}' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultTubularExcavationFound(self,feedertype):
        self.cur.execute("SELECT SUM(exc) FROM results_foundation_tubular WHERE feedertype='{}' AND itemtype = 'foundation' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultBackfillTubularChannel(self,feedertype):
        self.cur.execute("SELECT SUM(exc) FROM results_foundation_tubular WHERE feedertype='{}' AND itemtype = 'channel' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultBackfillWireChannel(self,feedertype):
        self.cur.execute("SELECT SUM(exc) FROM results_foundation_wire WHERE feedertype='{}' AND itemtype = 'channel' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultTubularJoint(self,feedertype):
        self.cur.execute("SELECT SUM(joint_isolation) FROM results_foundation_tubular WHERE feedertype='{}' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultWireExcavation(self,feedertype):
        self.cur.execute("SELECT SUM(exc) FROM results_foundation_wire WHERE feedertype='{}' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultWireExcavationFound(self,feedertype):
        self.cur.execute("SELECT SUM(exc) FROM results_foundation_wire WHERE feedertype='{}' AND itemtype = 'foundation' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultWireChannelExcavation(self,feedertype):
        self.cur.execute("SELECT SUM(exc) FROM results_foundation_wire WHERE feedertype='{}' AND itemtype = 'channel' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultWireJoint(self,feedertype):
        self.cur.execute("SELECT SUM(joint_isolation) FROM results_foundation_wire WHERE feedertype='{}' ".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultsWire(self):
        all = []
        columns = ['110kv','220kv','500kv']
        for column in columns:
            self.cur.execute("SELECT feedertype , SUM(strfill), SUM(lean_conc), SUM(concrete), SUM(secondary_concrete), SUM(formwork+formwork_precast), SUM(rebar), SUM(embedded_steel), SUM(anchor), SUM(steel), SUM(concrete_protection), SUM(water_stopper), SUM(joint_isolation) FROM results_foundation_wire WHERE feedertype='{}' ".format(column))
            all.append(self.cur.fetchall())
        return all

    def fetchSiteWorkDimension(self,feedertype):
        self.cur.execute("SELECT * FROM site_work_dimension WHERE feedertype = '{}'".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchTotalFoundationArea(self,feedertype):
        self.cur.execute("SELECT SUM(foundation_area) FROM results_foundation_tubular WHERE feedertype = '{}'".format(feedertype))
        rows = self.cur.fetchall()
        if rows[0][0] == None:
            self.cur.execute("SELECT SUM(foundation_area) FROM results_foundation_wire WHERE feedertype = '{}'".format(feedertype))
            rows = self.cur.fetchall()
        return rows

    def fetchMinimumDepthTubular(self,feedertype):
        self.cur.execute("SELECT MIN(f-h+e+0.1+fill) FROM dimensions_tubular WHERE type = '{}'".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchMinimumDepthWire(self,feedertype):
        self.cur.execute("SELECT MIN(f-h+e+0.1+fill) FROM dimensions_wire WHERE type = '{}'".format(feedertype))
        rows = self.cur.fetchall()
        return rows

    def fetchResultsSitework(self):
        self.cur.execute("SELECT * FROM results_sitework")
        rows = self.cur.fetchall()
        return rows

    def insert_results_foundation_tubular(self,foundationtype,feedertype,exc,strfill,backfill,lean_conc,concrete,secondary_concrete,formwork,rebar,embedded_steel,anchor,steel,concrete_protection,foundation_area,formwork_precast,water_stopper,joint_isolation,total_cable_length, itemtype):
        self.cur.execute("INSERT INTO results_foundation_tubular VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (foundationtype,feedertype,exc,strfill,backfill,lean_conc,concrete,secondary_concrete,formwork,rebar,embedded_steel,anchor,steel,concrete_protection,foundation_area,formwork_precast,water_stopper,joint_isolation,total_cable_length, itemtype))
        self.conn.commit()

    def insert_results_cable_tubular(self,foundationtype,feedertype,exc,strfill,backfill,lean_conc,concrete,secondary_concrete,formwork,rebar,embedded_steel,anchor,steel,concrete_protection,foundation_area,formwork_precast,water_stopper,joint_isolation,total_cable_length, itemtype):
        self.cur.execute("INSERT INTO results_foundation_tubular VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (foundationtype,feedertype,exc,strfill,backfill,lean_conc,concrete,secondary_concrete,formwork,rebar,embedded_steel,anchor,steel,concrete_protection,foundation_area,formwork_precast,water_stopper,joint_isolation,total_cable_length, itemtype))
        self.conn.commit()

    def insert_results_foundation_wire(self,foundationtype,feedertype,exc,strfill,backfill,lean_conc,concrete,secondary_concrete,formwork,rebar,embedded_steel,anchor,steel,concrete_protection,foundation_area,formwork_precast,water_stopper,joint_isolation,total_cable_length, itemtype):
        self.cur.execute("INSERT INTO results_foundation_wire VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (foundationtype,feedertype,exc,strfill,backfill,lean_conc,concrete,secondary_concrete,formwork,rebar,embedded_steel,anchor,steel,concrete_protection,foundation_area,formwork_precast,water_stopper,joint_isolation,total_cable_length, itemtype))
        self.conn.commit()

    def insert_results_cable_wire(self,foundationtype,feedertype,exc,strfill,backfill,lean_conc,concrete,secondary_concrete,formwork,rebar,embedded_steel,anchor,steel,concrete_protection,foundation_area,formwork_precast,water_stopper,joint_isolation,total_cable_length, itemtype):
        self.cur.execute("INSERT INTO results_foundation_wire VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (foundationtype,feedertype,exc,strfill,backfill,lean_conc,concrete,secondary_concrete,formwork,rebar,embedded_steel,anchor,steel,concrete_protection,foundation_area,formwork_precast,water_stopper,joint_isolation,total_cable_length, itemtype))
        self.conn.commit()

    def insert_results_sitework(self,feedertype,gravel_surfacing,total_fence_length,pipe_150mm,electric_conduit,pit_manhole,road_area,road_joint,kerbstone,excavation,backfill):
        self.cur.execute("INSERT INTO results_sitework VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)",
                         (feedertype,gravel_surfacing,total_fence_length,pipe_150mm,electric_conduit,pit_manhole,road_area,road_joint,kerbstone,excavation,backfill))
        self.conn.commit()

    def update_works(self,row,result,code):
        self.cur.execute("UPDATE works SET '{}'=? where no=?".format(row), (result,code))
        self.conn.commit()

    def updateFoundationPerFeeder(self,column,value,row):
        print(column,value,row)
        self.cur.execute("UPDATE foundationperfeeder SET '{}'=? where feedertype=?".format(column), (value,row))
        self.conn.commit()

    def updateFoundationTubular(self,column,value,row):
        self.cur.execute("UPDATE dimensions_tubular SET '{}'=? where foundationtype=?".format(column), (value,row))
        self.conn.commit()

    def updateFoundationWire(self,column,value,row):
        self.cur.execute("UPDATE dimensions_wire SET '{}'=? where foundationtype=?".format(column), (value,row))
        self.conn.commit()

    def updateChannelDimension(self,column,value,row,type):
        self.cur.execute("UPDATE channeldimensions SET '{}'=? where item=? AND type = ?".format(column), (value,row,type))
        self.conn.commit()

    def updateSiteDimension(self,column,value,row):
        self.cur.execute("UPDATE site_work_dimension SET '{}'=? where feedertype=?".format(column), (value,row))
        self.conn.commit()

    def alter_add_column(self):
        columns = ['110kv','220kv','500kv']
        for column in columns:
            self.cur.execute("ALTER TABLE works ADD COLUMN '{}'  DOUBLE".format(column))
        self.conn.commit()




    def __del__(self):
        self.conn.close()


#db = Database('main.db')
