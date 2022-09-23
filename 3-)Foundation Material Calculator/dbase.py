import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def fetch_selection_config(self):
        self.cur.execute("SELECT CONFIG FROM selection WHERE CONFIG IS NOT NULL ")
        rows = self.cur.fetchall()
        return rows

    def fetch_selection_region(self):
        self.cur.execute("SELECT REGION FROM selection WHERE REGION IS NOT NULL ")
        rows = self.cur.fetchall()
        return rows

    def fetch_selection_fgc_redundancy(self):
        self.cur.execute("SELECT FGC_redundancy FROM selection WHERE FGC_redundancy IS NOT NULL ")
        rows = self.cur.fetchall()
        return rows

    def fetch_selection_gt(self):
        self.cur.execute("SELECT * FROM gt_db ")
        rows = self.cur.fetchall()
        return rows

    def fetchGTG(self,gt):
        self.cur.execute("SELECT Model, ConcreteFoundation, LeanConcrete, Formwork, Rebar, InsulationSika, PeSheet, Excavation, StructuralFill, Backfill, Grout, Screed, EmbeddedPlate, wire_mesh, Anchor_m24, Anchor_m30, Anchor_m36, Anchor_m42, StructuralSteel FROM gtg WHERE Model = ? ", (gt,))
        rows = self.cur.fetchall()
        return rows

    def fetchStack(self):
        self.cur.execute("SELECT depth_exc, depth_fill, depth_found, width, length, steel_weight, grout_depth1, grout_depth2, p1_width, p1_length, p1_depth, p1_qty, p2_width, p2_length, p2_depth, p2_qty from stack")
        rows = self.cur.fetchall()
        return rows

    def fetchAuxNames(self):
        self.cur.execute("SELECT skid from skid_work")
        rows = self.cur.fetchall()
        return rows

    def fetchAUX(self,aux):
        self.cur.execute("SELECT skid, ConcreteFoundation, LeanConcrete, Formwork, Rebar, InsulationSika, PeSheet, Excavation, StructuralFill, Backfill, Grout, Screed, EmbeddedPlate, wire_mesh, Anchor_m24, Anchor_m30, Anchor_m36, Anchor_m42, StructuralSteel FROM skid_work WHERE skid = ? ", (aux,))
        rows = self.cur.fetchall()
        return rows

    def fetchAUX_indoor(self,aux):
        self.cur.execute("SELECT skid, ConcreteFoundation, LeanConcrete, Formwork, Rebar, InsulationSika, PeSheet, Excavation, StructuralFill, Backfill, Grout, Screed, EmbeddedPlate, wire_mesh, Anchor_m24, Anchor_m30, Anchor_m36, Anchor_m42, StructuralSteel FROM skid_work_indoor WHERE skid = ? ", (aux,))
        rows = self.cur.fetchall()
        return rows

    def insertResultGTG(self,  item_type, item, concrete_foundation, lean_concrete, formwork, rebar, insulation_sika, pe_sheet, excavation, structural_fill, backfill, grout, screed, embedded_plate, wire_mesh, anchor_m24, anchor_m30, anchor_m36, anchor_m42, structural_steel,joint_isolation,water_stopper):
        self.cur.execute("INSERT INTO results VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (item_type, item, concrete_foundation, lean_concrete, formwork, rebar, insulation_sika, pe_sheet, excavation, structural_fill, backfill, grout, screed, embedded_plate, wire_mesh, anchor_m24, anchor_m30, anchor_m36, anchor_m42, structural_steel,joint_isolation,water_stopper))
        self.conn.commit()

    def insertSF(self,found_name, exc_depth, strfill, foundation_depth, foundation_width, foundation_length, anchor_type, anchor_quantity, grout_depth, pedestal_width, pedestal_length, pedestal_depth, qty):
        self.cur.execute("INSERT INTO single_footing VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (found_name, exc_depth, strfill, foundation_depth, foundation_width, foundation_length, anchor_type, anchor_quantity, grout_depth, pedestal_width, pedestal_length, pedestal_depth, qty))
        self.conn.commit()

    def insertCF(self,found_name, exc_depth, strfill, foundation_depth, foundation_width, foundation_length, anchor_type, anchor_quantity, grout_depth, pedestal_width, pedestal_length, pedestal_depth, pedestal_qty, qty):
        self.cur.execute("INSERT INTO combined_footing VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (found_name, exc_depth, strfill, foundation_depth, foundation_width, foundation_length, anchor_type, anchor_quantity, grout_depth, pedestal_width, pedestal_length, pedestal_depth, pedestal_qty, qty))
        self.conn.commit()

    def insertMF(self,found_name, exc_depth, strfill, foundation_depth, foundation_width, foundation_length, anchor_type, anchor_quantity, grout_depth, qty):
        self.cur.execute("INSERT INTO mat_foundation VALUES (NULL, ?,?,?,?,?,?,?,?,?,?)",
                         (found_name, exc_depth, strfill, foundation_depth, foundation_width, foundation_length, anchor_type, anchor_quantity, grout_depth, qty))
        self.conn.commit()

    def insertPIT(self,found_name, dim_a, dim_b, dim_c, dim_d, dim_e, dim_f, dim_g, dim_h, dim_k, strfill, qty):
        self.cur.execute("INSERT INTO pit_calculator VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?)",
                         (found_name, dim_a, dim_b, dim_c, dim_d, dim_e, dim_f, dim_g, dim_h, dim_k, strfill, qty))
        self.conn.commit()


    def insertDW(self,wall_name, dw_thickness, dw_height, dw_perimeter_width, dw_perimeter_length, dw_foundation_depth, dw_foundation_width, dw_exc_depth, dw_fill):
        self.cur.execute("INSERT INTO dyke_wall VALUES (NULL, ?,?,?,?,?,?,?,?,?)",
                         (wall_name, dw_thickness, dw_height, dw_perimeter_width, dw_perimeter_length, dw_foundation_depth, dw_foundation_width, dw_exc_depth, dw_fill))
        self.conn.commit()

    def insertcylinderTANK(self,found_name,tank_type,is_chemical,D1, D2, dim_a, dim_b, dim_c, dim_d, dim_e, exc_depth, strfill, tank_height, anchor_type, anchor_qty, qty):
        self.cur.execute("INSERT INTO tank_foundation VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (found_name,tank_type,is_chemical,D1, D2, dim_a, dim_b, dim_c, dim_d, dim_e, exc_depth, strfill, tank_height, anchor_type, anchor_qty, qty))
        self.conn.commit()

    def insertTANK(self,found_name,tank_type,is_chemical,D1, D2, dim_a, dim_b, exc_depth, strfill, tank_height, anchor_type, anchor_qty, qty):
        self.cur.execute("INSERT INTO tank_foundation VALUES (NULL, ?,?,?,?,?,?,?,NULL,NULL,NULL,?,?,?,?,?,?)",
                         (found_name,tank_type,is_chemical,D1, D2, dim_a, dim_b, exc_depth, strfill, tank_height, anchor_type, anchor_qty, qty))
        self.conn.commit()

    def insertStack(self, depth_exc, depth_fill, depth_found, width, length, steel_weight, grout_depth1, grout_depth2,
                    p1_width, p1_length, p1_depth, p1_qty, p2_width, p2_length, p2_depth, p2_qty):
        self.cur.execute("INSERT INTO stack VALUES (NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (depth_exc, depth_fill, depth_found, width, length, steel_weight, grout_depth1, grout_depth2,
                          p1_width, p1_length, p1_depth, p1_qty, p2_width, p2_length, p2_depth, p2_qty))
        self.conn.commit()

    def delFromResults(self):
        self.cur.execute("DELETE FROM results")
        self.conn.commit()

    def removeFoundation(self, id):
        self.cur.execute("DELETE FROM results WHERE item='{}'".format(id))
        self.conn.commit()

    def removeIndFound(self,id,type):
        types = {"SINGLE FOOTING":"single_footing",
                 "COMBINED FOOTING":"combined_footing",
                 "MAT FOUNDATION":"mat_foundation",
                 "PIT":"pit_calculator",
                 "CYLINDER TANK":"tank_foundation",
                 "OCTAGON TANK":"tank_foundation",
                 "HEXAGON TANK":"tank_foundation",
                 "OCTAGON(SQUARE_BASE) TANK":"tank_foundation",
                 "HEXAGON(SQUARE_BASE) TANK":"tank_foundation",
                 "GT FOUNDATION":"results"}
        table = types.get(type)
        if table == "pit_calculator":
            self.cur.execute("DELETE FROM {} WHERE pit_name='{}'".format(table,id))
        elif table == "dyke_wall":
            self.cur.execute("DELETE FROM {} WHERE wall_name='{}'".format(table, id))
        elif table == "results":
            self.cur.execute("DELETE FROM {} WHERE item='{}'".format(table, id))
        else:
            self.cur.execute("DELETE FROM {} WHERE found_name='{}'".format(table,id))
        self.conn.commit()

    def removeAllIndFound(self,type):
        types = {"SINGLE FOOTING":"single_footing",
                 "COMBINED FOOTING":"combined_footing",
                 "MAT FOUNDATION":"mat_foundation",
                 "PIT":"pit_calculator",
                 "CYLINDER TANK":"tank_foundation",
                 "OCTAGON TANK":"tank_foundation",
                 "HEXAGON TANK":"tank_foundation",
                 "OCTAGON(SQUARE_BASE) TANK":"tank_foundation",
                 "HEXAGON(SQUARE_BASE) TANK":"tank_foundation",
                 "GT FOUNDATION":"results"}
        table = types.get(type)
        self.cur.execute("DELETE FROM {}".format(table))
        self.conn.commit()

    def delFromStack(self):
        self.cur.execute("DELETE FROM stack")
        self.conn.commit()

    def alter_add_column(self,column):
        self.cur.execute("ALTER TABLE works ADD COLUMN '{}'  DOUBLE".format(column))
        self.conn.commit()

    def fetchResults(self):
        self.cur.execute("SELECT * FROM results")
        rows = self.cur.fetchall()
        return rows

    def fetchIndFound(self,table,item):
        if table == "pit_calculator":
            self.cur.execute(f"SELECT * FROM {table} WHERE pit_name = '{item}'")
        elif table == "dyke_wall":
            self.cur.execute(f"SELECT * FROM {table} WHERE wall_name = '{item}'")
        else:
            self.cur.execute(f"SELECT * FROM {table} WHERE found_name = '{item}'")
        rows = self.cur.fetchall()
        return rows

    def update_works(self,row,result,code):
        self.cur.execute("UPDATE works SET '{}'=? where no=?".format(row), (result,code))
        self.conn.commit()

    def drop_table_works(self):
        self.cur.execute("DROP TABLE IF EXISTS works")
        self.conn.commit()

