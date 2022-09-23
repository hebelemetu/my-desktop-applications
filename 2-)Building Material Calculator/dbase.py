import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS buildings (id INTEGER PRIMARY KEY, name text, storeyno INTEGER, storeyheight DOUBLE, structuraltype text, steeltype text, insulationtype text, seperatedroom text, middlefloor text, soilproperty text, beam_connection text, ground_wall text ,basement text, width DOUBLE, length DOUBLE, exc_depth DOUBLE, strfill_depth DOUBLE, foundation_depth DOUBLE, foundation_D1 DOUBLE, foundation_D2 DOUBLE,tie_beam_d1 DOUBLE,tie_beam_d2 DOUBLE,steel_pedestal_d1 DOUBLE,steel_pedestal_d2 DOUBLE,steel_pedestal_depth DOUBLE, steel_pedestal_rangex DOUBLE,steel_pedestal_rangey DOUBLE, rc_column_width DOUBLE, rc_column_length DOUBLE, rc_column_rangex DOUBLE,rc_column_rangey DOUBLE, basement_wall_height DOUBLE, basement_wall_thickness DOUBLE, ground_wall_height DOUBLE, ground_wall_thickness DOUBLE, steel_weight DOUBLE,grouting_depth DOUBLE, rc_beam_width DOUBLE, rc_beam_length DOUBLE,rc_secondary_beam_D1 DOUBLE,rc_secondary_beam_D2 DOUBLE,  concrete_slab DOUBLE, ground_slab DOUBLE,paraphet_height DOUBLE, paraphet_thickness DOUBLE)")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS rooms (room_id INTEGER PRIMARY KEY, building_name TEXT,room_name text, floor_no TEXT, area DOUBLE, quantity INTEGER,inside_brick_wall DOUBLE,gypsum_part_wall DOUBLE,aliminum_suspended_ceiling DOUBLE,acoustical_ceiling DOUBLE,gypsum_suspended_ceiling DOUBLE,rockwool_suspended_ceiling DOUBLE,non_slip_ceramic_tile DOUBLE,glazed_ceramic_tile DOUBLE,glazed_ceramic_skirting DOUBLE,epoxy_painting_floor DOUBLE,resistant_floor DOUBLE,acid_tile DOUBLE,raised_floor DOUBLE,laminated_parquet DOUBLE,int_plaster DOUBLE,ceiling_plaster DOUBLE,ceramic_wall_tile DOUBLE,int_paint DOUBLE,acid_resistant_int_paint DOUBLE,ceiling_paint DOUBLE,epoxy_wall_paint DOUBLE,steel_door1 INTEGER, steel_door2 INTEGER, roller_shutter INTEGER, sliding_steel_door INTEGER, double_wing_aliminium_door INTEGER, compacted_laminate_door INTEGER, wooden_internal_door INTEGER, aliminum_door INTEGER, aliminum_double_win_door INTEGER, screed DOUBLE, building_name TEXT, room_place TEXT, around_rooms TEXT)")
        self.conn.commit()
        #düzelt----> başlangıçta rooms,buildings temizle

    def drop_table_works(self):
        self.cur.execute("DROP TABLE IF EXISTS works")
        self.conn.commit()

    def drop_table_data(self):
        self.cur.execute("DROP TABLE IF EXISTS data")
        self.conn.commit()

    def deleteFromBuildings(self):
        self.cur.execute("DELETE FROM buildings")
        self.conn.commit()

    def deleteFromRooms(self):
        self.cur.execute("DELETE FROM rooms")
        self.conn.commit()

    def alter_add_column(self,column):
        self.cur.execute("ALTER TABLE works ADD COLUMN '{}' DOUBLE".format(column))
        rows = self.cur.fetchall()
        return rows

    def fetch(self):
        self.cur.execute("SELECT * FROM buildings")
        rows = self.cur.fetchall()
        return rows

    def fetch_works(self):
        self.cur.execute("SELECT * FROM works")
        works = self.cur.fetchall()
        return works

    def fetch_results_steel(self):
        self.cur.execute("SELECT * FROM results_steel")
        steels = self.cur.fetchall()
        return steels

    def fetch_results_rc(self):
        self.cur.execute("SELECT * FROM results_rc")
        rcs = self.cur.fetchall()
        return rcs

    def fetch_rooms_execute(self,building_name):
        self.cur.execute("SELECT * FROM rooms WHERE building_name ='{}'".format(building_name))
        rooms = self.cur.fetchall()
        return rooms

    def fetch_rooms_by_floor(self,building_name,floor_no):
        self.cur.execute("SELECT * FROM rooms WHERE building_name ='{}' AND floor_no = '{}' ".format(building_name,floor_no))
        rooms = self.cur.fetchall()
        return rooms

    def fetch_rooms(self):
        self.cur.execute("SELECT * FROM rooms")
        rooms = self.cur.fetchall()
        return rooms

    def fetch_rooms_treeview(self):
        self.cur.execute("SELECT room_id, room_name, floor_no, area, quantity,room_place,around_rooms, building_name FROM rooms")
        rooms = self.cur.fetchall()
        return rooms

    def fetch_parameters(self,id,type):
        if type=="RC":
            self.cur.execute("SELECT exc_depth, strfill_depth, foundation_depth, foundation_D1, foundation_D2, tie_beam_d1  FROM buildings WHERE name=? ",(id,))
        elif type=="STEEL":
            self.cur.execute("SELECT exc_depth,strfill_depth, foundation_depth, foundation_D1, foundation_D2, tie_beam_d1 FROM buildings WHERE name=? ", (id,))
        parameters = self.cur.fetchall()
        return parameters

    def fetch_parameters2(self,id,type):
        if type=="RC":
            self.cur.execute("SELECT tie_beam_d2,rc_column_width,rc_column_length,rc_column_rangex,rc_column_rangey,basement_wall_height  FROM buildings WHERE name=? ",(id,))
        elif type=="STEEL":
            self.cur.execute("SELECT tie_beam_d2,steel_pedestal_d1,steel_pedestal_d2,steel_pedestal_depth,steel_pedestal_rangex, steel_pedestal_rangey FROM buildings WHERE name=? ", (id,))
        parameters = self.cur.fetchall()
        return parameters

    def fetch_parameters3(self,id,type):
        if type=="RC":
            self.cur.execute("SELECT basement_wall_thickness,ground_wall_height,ground_wall_thickness,rc_beam_width,rc_beam_length,rc_secondary_beam_D1  FROM buildings WHERE name=? ",(id,))
        elif type=="STEEL":
            self.cur.execute("SELECT ground_wall_height,ground_wall_thickness,steel_weight,grouting_depth,concrete_slab,ground_slab FROM buildings WHERE name=? ", (id,))
        parameters = self.cur.fetchall()
        return parameters

    def fetch_parameters4(self,id,type):
        if type=="RC":
            self.cur.execute("SELECT rc_secondary_beam_D2,concrete_slab,ground_slab,paraphet_height,paraphet_thickness  FROM buildings WHERE name=? ",(id,))
        elif type=="STEEL":
            self.cur.execute("SELECT exc_depth,strfill_depth, foundation_depth, foundation_D1, foundation_D2, tie_beam_d1, tie_beam_d2,steel_pedestal_d1,steel_pedestal_d2,steel_pedestal_depth,steel_pedestal_rangex, steel_pedestal_rangey,ground_wall_height,ground_wall_thickness,steel_weight,grouting_depth,concrete_slab,ground_slab FROM buildings WHERE name=? ", (id,))
        parameters = self.cur.fetchall()
        return parameters

    def fetch_parameters_all(self,id,type):
        if type=="RC":
            self.cur.execute("SELECT exc_depth, strfill_depth, foundation_depth, foundation_D1, foundation_D2, tie_beam_d1, tie_beam_d2,rc_column_width,rc_column_length,rc_column_rangex,rc_column_rangey,basement_wall_height,basement_wall_thickness,ground_wall_height,ground_wall_thickness,rc_beam_width,rc_beam_length,rc_secondary_beam_D1,rc_secondary_beam_D2,concrete_slab,ground_slab,paraphet_height,paraphet_thickness  FROM buildings WHERE name=? ",(id,))
        elif type=="STEEL":
            self.cur.execute("SELECT exc_depth,strfill_depth, foundation_depth, foundation_D1, foundation_D2, tie_beam_d1, tie_beam_d2,steel_pedestal_d1,steel_pedestal_d2,steel_pedestal_depth,steel_pedestal_rangex, steel_pedestal_rangey,ground_wall_height,ground_wall_thickness,steel_weight,grouting_depth,concrete_slab,ground_slab FROM buildings WHERE name=? ", (id,))
        parameters = self.cur.fetchall()
        return parameters

    def parameter_selection(self,storeyno,storeyheightcode,structuraltype,foundationtype,foundation_beam,foundation_ground_wall,widthcode,lengthcode):
        self.cur.execute("SELECT excavation, strfill, foundationdepth, foundation_d1, foundation_d2, tiebeam_d1, tie_beam_d2, steel_pedestal_d1, steel_pedestal_d2,	steel_pedestal_depth, steel_pedestal_rangex, steel_pedestal_rangey, rccolumn_d1, rccolumn_d2, rccolumnrangex, rccolumnrangey, rc_beam_d1, rc_beam_d2, rc_secondary_beam_d1, rc_secondary_beam_d2, basement_perimeterwall_groundwall_height, basement_perimeterwall_groundwall_thickness, concreteslabthk, grdslbthk, paraphet_thickness, paraphet_height  FROM data WHERE storeyno = ? AND storeyheightcode = ? AND structuraltype = ? AND foundationtype = ? AND foundation_beam = ? AND foundation_ground_wall =? AND lengthcode =? AND widthcode =?",(storeyno,storeyheightcode,structuraltype,foundationtype,foundation_beam,foundation_ground_wall,lengthcode,widthcode))
        parameters_selected = self.cur.fetchall()
        return parameters_selected

    def fetch_building_names(self):
        self.cur.execute("SELECT name,structuraltype FROM buildings")
        names = self.cur.fetchall()
        return names

    def insert(self,  name, storeyno,storeyheight,structuraltype,steeltype,insulationtype,seperatedroom,middlefloor,soilproperty,beam_connection,ground_wall,basement,width,length,exc_depth, strfill_depth,foundation_depth, foundation_D1, foundation_D2, tie_beam_d1, tie_beam_d2, steel_pedestal_d1,steel_pedestal_d2, steel_pedestal_depth, steel_pedestal_rangex, steel_pedestal_rangey, rc_column_width, rc_column_length, rc_column_rangex, rc_column_rangey, basement_wall_height, basement_wall_thickness, ground_wall_height, ground_wall_thickness, steel_weight, grouting_depth, rc_beam_width,rc_beam_length, rc_secondary_beam_D1, rc_secondary_beam_D2, concrete_slab, ground_slab, paraphet_height, paraphet_thickness):
        self.cur.execute("INSERT INTO buildings VALUES (NULL, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?)",
                         (name, storeyno,storeyheight,structuraltype,steeltype,insulationtype,seperatedroom,middlefloor,soilproperty,beam_connection,ground_wall,basement,width,length,exc_depth, strfill_depth,foundation_depth, foundation_D1, foundation_D2, tie_beam_d1, tie_beam_d2, steel_pedestal_d1,steel_pedestal_d2, steel_pedestal_depth, steel_pedestal_rangex, steel_pedestal_rangey, rc_column_width, rc_column_length, rc_column_rangex, rc_column_rangey, basement_wall_height, basement_wall_thickness, ground_wall_height, ground_wall_thickness, steel_weight, grouting_depth, rc_beam_width,rc_beam_length, rc_secondary_beam_D1, rc_secondary_beam_D2, concrete_slab, ground_slab, paraphet_height, paraphet_thickness))
        self.conn.commit()


    def insert_rooms(self,room_name, floor_no, area, quantity,inside_brick_wall,gypsum_part_wall,aliminum_suspended_ceiling,acoustical_ceiling,gypsum_suspended_ceiling,rockwool_suspended_ceiling,non_slip_ceramic_tile,glazed_ceramic_tile,glazed_ceramic_skirting,epoxy_painting_floor,resistant_floor,acid_tile,raised_floor,laminated_parquet,int_plaster,ceiling_plaster,ceramic_wall_tile,int_paint,acid_resistant_int_paint,ceiling_paint,epoxy_wall_paint, steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door,screed,building_name,room_place,around_rooms):
        self.cur.execute("INSERT INTO rooms VALUES (NULL, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (room_name, floor_no, area, quantity,inside_brick_wall,gypsum_part_wall,aliminum_suspended_ceiling,acoustical_ceiling,gypsum_suspended_ceiling,rockwool_suspended_ceiling,non_slip_ceramic_tile,glazed_ceramic_tile,glazed_ceramic_skirting,epoxy_painting_floor,resistant_floor,acid_tile,raised_floor,laminated_parquet,int_plaster,ceiling_plaster,ceramic_wall_tile,int_paint,acid_resistant_int_paint,ceiling_paint,epoxy_wall_paint,steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door,screed,building_name,room_place,around_rooms))
        self.conn.commit()

    def insert_results_rc(self,name,exc,strfill,foundation,lean_conc,conc_wall,backfill,rc_column,rc_beam,concrete_slab,ground_slab,formwork,rebar,wire_mesh,rainwater_gutter,rainwater_pipe,insulation_sika,insulation_membrane,pe_sheet,inside_brick_wall,gypsum_part_wall,aliminum_suspended_ceiling,acoustical_ceiling,gypsum_suspended_ceiling,rockwool_suspended_ceiling,non_slip_ceramic_tile,glazed_ceramic_tile,glazed_ceramic_skirting,epoxy_painting_floor,resistant_floor,acid_tile,raised_floor,laminated_parquet,int_plaster,ceiling_plaster,ceramic_wall_tile,int_paint,acid_resistant_int_paint,ceiling_paint,epoxy_wall_paint,pvc,water_stop,marble_cladding,alucobond_cladding,exterior_brick,exterior_plaster,exterior_painting, steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door,screed,concrete_stairs,catch_basin,concrete_pavement,joint_cutting,steel_ladder):
        self.cur.execute("INSERT INTO results_rc VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (name,exc,strfill,foundation,lean_conc,conc_wall,backfill,rc_column,rc_beam,concrete_slab,ground_slab,formwork,rebar,wire_mesh,rainwater_gutter,rainwater_pipe,insulation_sika,insulation_membrane,pe_sheet,inside_brick_wall,gypsum_part_wall,aliminum_suspended_ceiling,acoustical_ceiling,gypsum_suspended_ceiling,rockwool_suspended_ceiling,non_slip_ceramic_tile,glazed_ceramic_tile,glazed_ceramic_skirting,epoxy_painting_floor,resistant_floor,acid_tile,raised_floor,laminated_parquet,int_plaster,ceiling_plaster,ceramic_wall_tile,int_paint,acid_resistant_int_paint,ceiling_paint,epoxy_wall_paint,pvc,water_stop,marble_cladding,alucobond_cladding,exterior_brick,exterior_plaster,exterior_painting, steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door,screed,concrete_stairs,catch_basin,concrete_pavement,joint_cutting,steel_ladder))
        self.conn.commit()

    def insert_results_steel(self,name,exc,strfill,foundation,lean_conc,conc_wall,backfill,steel_column,ground_slab,steel_formwork,steel_rebar,concrete_slab,steelweight,grouting,embedded_steel,anchorbolt_m24,anchorbolt_m30,insulation_sika,insulation_membrane,pe_sheet,handrail,steel_grating,steel_ladder,chequered_plate,water_stop, rainwater_gutter, rainwater_pipe ,inside_brick_wall ,gypsum_part_wall ,aliminum_suspended_ceiling ,acoustical_ceiling ,gypsum_suspended_ceiling ,rockwool_suspended_ceiling  ,non_slip_ceramic_tile  ,glazed_ceramic_tile  ,glazed_ceramic_skirting  ,epoxy_painting_floor  ,resistant_floor  ,acid_tile  ,raised_floor  ,laminated_parquet  ,int_plaster  ,ceiling_plaster  ,ceramic_wall_tile  ,int_paint  ,acid_resistant_int_paint  ,ceiling_paint  ,epoxy_wall_paint ,pvc, wire_mesh,roof_cladding, steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door,catch_basin,concrete_pavement,insulated_wall,insulated_roof):
        self.cur.execute("INSERT INTO results_steel VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (name,exc,strfill,foundation,lean_conc,conc_wall,backfill,steel_column,ground_slab,steel_formwork,steel_rebar,concrete_slab,steelweight,grouting,embedded_steel,anchorbolt_m24,anchorbolt_m30,insulation_sika,insulation_membrane,pe_sheet,handrail,steel_grating,steel_ladder,chequered_plate,water_stop, rainwater_gutter, rainwater_pipe ,inside_brick_wall ,gypsum_part_wall ,aliminum_suspended_ceiling ,acoustical_ceiling ,gypsum_suspended_ceiling ,rockwool_suspended_ceiling  ,non_slip_ceramic_tile  ,glazed_ceramic_tile  ,glazed_ceramic_skirting  ,epoxy_painting_floor  ,resistant_floor  ,acid_tile  ,raised_floor  ,laminated_parquet  ,int_plaster  ,ceiling_plaster  ,ceramic_wall_tile  ,int_paint  ,acid_resistant_int_paint  ,ceiling_paint  ,epoxy_wall_paint ,pvc, wire_mesh,roof_cladding, steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door,catch_basin,concrete_pavement,insulated_wall,insulated_roof))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM buildings WHERE id=?", (id,))
        self.conn.commit()

    def remove_rooms(self, room_id):
        self.cur.execute("DELETE FROM rooms WHERE room_id=?", (room_id,))
        self.conn.commit()

    def update(self, id, name, storeyno,storeyheight,structuraltype,steeltype,insulationtype,seperatedroom,middlefloor,soilproperty,beam_connection,ground_wall,basement,width,length,exc_depth, strfill_depth,foundation_depth, foundation_D1, foundation_D2, tie_beam_d1, tie_beam_d2, steel_pedestal_d1,steel_pedestal_d2, steel_pedestal_depth, steel_pedestal_rangex, steel_pedestal_rangey, rc_column_width, rc_column_length, rc_column_rangex, rc_column_rangey, basement_wall_height, basement_wall_thickness, ground_wall_height, ground_wall_thickness, steel_weight, grouting_depth, rc_beam_width,rc_beam_length, rc_secondary_beam_D1, rc_secondary_beam_D2, concrete_slab, ground_slab, paraphet_height, paraphet_thickness):
        self.cur.execute("UPDATE buildings SET name = ?, storeyno = ?, storeyheight = ?, structuraltype = ?, steeltype = ?, insulationtype = ?, seperatedroom = ?, middlefloor = ?, soilproperty = ?, beam_connection = ?,ground_wall = ?,basement = ?, width = ?, length = ?, exc_depth = ?, strfill_depth = ?, foundation_depth = ?, foundation_D1 = ?, foundation_D2 = ?, tie_beam_d1 = ?, tie_beam_d2 = ?, steel_pedestal_d1 = ?, steel_pedestal_d2 = ?, steel_pedestal_depth = ?, steel_pedestal_rangex = ?, steel_pedestal_rangey = ?, rc_column_width = ?, rc_column_length = ?, rc_column_rangex = ?, rc_column_rangey = ?, basement_wall_height = ?, basement_wall_thickness = ?, ground_wall_height = ?, ground_wall_thickness = ?, steel_weight = ?, grouting_depth = ?, rc_beam_width = ?,rc_beam_length = ?, rc_secondary_beam_D1 = ?, rc_secondary_beam_D2 = ?, concrete_slab = ?, ground_slab = ?, paraphet_height = ?, paraphet_thickness = ? WHERE id = ?",
                         ( name, storeyno,storeyheight,structuraltype,steeltype,insulationtype,seperatedroom,middlefloor,soilproperty,beam_connection,ground_wall,basement,width,length,exc_depth, strfill_depth,foundation_depth, foundation_D1, foundation_D2, tie_beam_d1, tie_beam_d2, steel_pedestal_d1,steel_pedestal_d2, steel_pedestal_depth, steel_pedestal_rangex, steel_pedestal_rangey, rc_column_width, rc_column_length, rc_column_rangex, rc_column_rangey, basement_wall_height, basement_wall_thickness, ground_wall_height, ground_wall_thickness, steel_weight, grouting_depth, rc_beam_width,rc_beam_length, rc_secondary_beam_D1, rc_secondary_beam_D2, concrete_slab, ground_slab, paraphet_height, paraphet_thickness, id))
        self.conn.commit()

    def update_rooms(self, room_id, room_name, floor_no, area, quantity,inside_brick_wall,gypsum_part_wall,aliminum_suspended_ceiling,acoustical_ceiling,gypsum_suspended_ceiling,rockwool_suspended_ceiling,non_slip_ceramic_tile,glazed_ceramic_tile,glazed_ceramic_skirting,epoxy_painting_floor,resistant_floor,acid_tile,raised_floor,laminated_parquet,int_plaster,ceiling_plaster,ceramic_wall_tile,int_paint,acid_resistant_int_paint,ceiling_paint,epoxy_wall_paint,steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door,screed,building_name,room_place,around_rooms):
        self.cur.execute("UPDATE rooms SET room_name = ?, floor_no=?, area=?, quantity=?, inside_brick_wall = ?,gypsum_part_wall=?, aliminum_suspended_ceiling=?,acoustical_ceiling=?,gypsum_suspended_ceiling=?,rockwool_suspended_ceiling=? ,non_slip_ceramic_tile=?, glazed_ceramic_tile=? , glazed_ceramic_skirting=? ,epoxy_painting_floor =? , resistant_floor =?, acid_tile=?, raised_floor=?, laminated_parquet=?, int_plaster=?, ceiling_plaster=?, ceramic_wall_tile=?, int_paint=?, acid_resistant_int_paint=?, ceiling_paint=?, epoxy_wall_paint=? ,steel_door1=?,steel_door2=?,roller_shutter=?,sliding_steel_door=?,double_wing_aliminium_door=?,compacted_laminate_door=?,wooden_internal_door=?,aliminum_door=?,aliminum_double_win_door=?,screed=?,building_name=?,room_place = ?, around_rooms =? WHERE room_id = ?",
                         (room_name, floor_no, area, quantity,inside_brick_wall,gypsum_part_wall,aliminum_suspended_ceiling,acoustical_ceiling,gypsum_suspended_ceiling,rockwool_suspended_ceiling,non_slip_ceramic_tile,glazed_ceramic_tile,glazed_ceramic_skirting,epoxy_painting_floor,resistant_floor,acid_tile,raised_floor,laminated_parquet,int_plaster,ceiling_plaster,ceramic_wall_tile,int_paint,acid_resistant_int_paint,ceiling_paint,epoxy_wall_paint,steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door,screed,building_name,room_place,around_rooms ,room_id))
        self.conn.commit()

    def update_works(self,row,result,code):
        self.cur.execute("UPDATE works SET '{}'=? where no=?".format(row), (result,code))
        self.conn.commit()

    def update_parameters(self,column,size,index):
        self.cur.execute("UPDATE buildings SET {}=? where name=?".format(column), (size,index))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


#db = Database('main.db')
