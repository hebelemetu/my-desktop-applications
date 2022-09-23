#Functions to calculate quantities
import math
class building:
    def __init__(self,name,storey,storey_height,structural_type,soil_property,beam_connection,ground_wall,basement,width,length,steel_type,insulation,seperated_room,middle_floor):
        self.storey=storey
        self.storey_height=storey_height
        self.structural_type=structural_type
        self.soil_property=soil_property
        self.beam_connection = beam_connection
        self.ground_wall = ground_wall
        self.basement=basement
        self.width=width
        self.length=length
        self.steel_type=steel_type
        self.insulation=insulation
        self.seperated_room=seperated_room
        self.middle_floor=middle_floor
        self.name=name


        #ROUGH WORKS
    #2.4
    def excavation(self,depth_exc):
        print("Calculating Excavation...")
        self.depth_exc = depth_exc
        print("depth_exc: ",depth_exc)
        print("width: ", self.width)
        print("length: ", self.length)
        work_space = 2
        A1 = (self.width + work_space) * (self.length + work_space)
        A2 = (self.width + work_space + 2 * self.depth_exc) * (self.length + work_space + 2 * self.depth_exc)
        A3 = (self.width + work_space + self.depth_exc) * (self.length + work_space + self.depth_exc)
        exc = round((A1 + A2 + 4 * A3) * self.depth_exc / 6, 2)
        print(A1,A2,A3,exc,sep="\n")
        print("Excavation: ",exc)
        return exc

    #2.7
    def strfill(self,depth_fill):
        print("Calculating Strfill...")
        self.depth_fill=depth_fill
        work_space = 2
        A1 = (self.width + work_space) * (self.length + work_space)
        A2 = (self.width + work_space + 2 * self.depth_fill) * (self.length + work_space + 2 * self.depth_fill)
        A3 = (self.width + work_space + self.depth_fill) * (self.length + work_space + self.depth_fill)
        depth = self.depth_fill
        strfill = round((A1 + A2 + 4 * A3) * depth / 6, 2)
        print(A1,A2,A3,strfill,sep="\n")
        print("Strfill: ",strfill)
        return strfill
    #3.1
    def lean_concrete(self,depth_lc):
        print("Calculating Lean Concrete")
        """ MAT:
        -NOBEAM-->WIDTH LENGTH
            STRIP:
        -tie_beam_d1
        -tie_beam_d2
        -foundation_d1
        -fondation_d2
            SINGLE FOOTING:
        -tie_beam_d1
        -tie_beam_d2
        -foundation_d1
        -fondation_d2
        """
        self.depth_lc=depth_lc
        self.lc_volume = self.lc_area * self.depth_lc
        print("Lean Concrete(m2): ", self.lc_area)
        print("Lean Concrete(m3): ",self.lc_volume)
        return round(self.lc_volume, 2)
    #3.2
    def foundation(self,depth_found,column_rangex,column_rangey,d1,d2,tie_beam_d1,tie_beam_d2,ground_wall_thickness,ground_wall_height):  #https://www.rgscontractors.com/the-different-types-of-concrete-foundations-for-industrial-buildings/
        print("Calculating Foundation")
        #MAT,STRIP,SINGLE FOOTING
        #ONE_WAY_BEAM,TWO_WAY_BEAM,NO_BEAM
        #GROUND_WALL,NO_GROUND_WALL
        self.depth_found=depth_found
        self.column_rangex=column_rangex
        self.column_rangey=column_rangey
        self.d1=d1
        self.d2=d2
        self.tie_beam_d1=tie_beam_d1
        self.tie_beam_d2=tie_beam_d2
        self.ground_wall_thickness=ground_wall_thickness
        self.ground_wall_height=ground_wall_height

        if self.soil_property == "MAT":
            return self.mat_foundation(self.depth_found,self.d1, self.column_rangex,self.column_rangey,tie_beam_d1,tie_beam_d2)
        elif self.soil_property == "STRIP":
            return self.strip_foundation(self.depth_found,self.d1, self.column_rangex,self.column_rangey,tie_beam_d1,tie_beam_d2)
        elif self.soil_property == "SINGLE_FOOTING":
            return self.single_footing(self.depth_found,self.d1,self.d2, self.column_rangex,self.column_rangey,tie_beam_d1,tie_beam_d2)
        elif self.soil_property == "SINGLE_FOOTING(ONLY EDGE)":
            return self.single_footing_only_edge(self.depth_found,self.d1,self.d2, self.column_rangex,self.column_rangey,tie_beam_d1,tie_beam_d2)
        else:
            print("FOUNDATION NOT SELECTED")

    def mat_foundation(self,depth_found,foundation_d1,column_rangex,column_rangey,tie_beam_d1,tie_beam_d2):
        print("mat foundation")
        y_axis_tie_beam = round(self.width / column_rangey,0) - 1
        print(y_axis_tie_beam)
        x_axis_tie_beam = round(self.length / column_rangex,0) - 1
        print(x_axis_tie_beam)
        if self.beam_connection == "TWO_WAY": #Checked
            print("two_way")
            self.x_tb_qty=x_axis_tie_beam
            self.y_tb_qty=y_axis_tie_beam
            edge_width = self.width - 2 * foundation_d1
            beam_length = self.width - (self.y_tb_qty + 2) * foundation_d1
            beam_length2 = self.length - 2 * foundation_d1
            beam_perimeter_area = (2 * depth_found) * beam_length
            beam_perimeter_area2 = (2 * depth_found) * beam_length2
            insulation_foundation = 2 * (edge_width * depth_found) * 2 + 2 * (self.length  * depth_found) * 2 + y_axis_tie_beam * depth_found * beam_length2 * 2 + x_axis_tie_beam * depth_found * beam_length * 2 +  2 * (edge_width * foundation_d1) + 2 * (self.length  * foundation_d1) + y_axis_tie_beam * foundation_d1 * beam_length2 + x_axis_tie_beam * foundation_d1 * beam_length
            formwork_foundation = 2 * (edge_width * depth_found * 2) + 2 * (self.length * depth_found * 2) + y_axis_tie_beam * beam_perimeter_area2 + x_axis_tie_beam * beam_perimeter_area
            self.found_concrete = round(2 * (edge_width * foundation_d1 * depth_found) + 2 * (self.length * foundation_d1 * depth_found) + y_axis_tie_beam * foundation_d1 * depth_found * beam_length2 + x_axis_tie_beam * foundation_d1 * depth_found * beam_length,2)
            rebar_foundation = self.found_concrete * self.rebar_weight
            self.lc_area = 2 * (edge_width + 0.4) * (foundation_d1 + 0.4) + 2 * (self.length + 0.4) * (foundation_d1+0.4) + y_axis_tie_beam * (foundation_d1 + 0.4) * beam_length2 + x_axis_tie_beam * (foundation_d1 + 0.4) * beam_length
            self.insulation_sika(insulation_foundation)
            self.insulation_membrane(insulation_foundation)
            self.formwork(formwork_foundation)
            self.rebar(rebar_foundation)
            print("Lean Concrete Area = {}, insulation sika = {}, formwork = {}, rebar = {}".format(self.lc_area,insulation_foundation,formwork_foundation,rebar_foundation))
            return self.found_concrete
        elif self.beam_connection == "NO_BEAM":#Checked
            print("no_beam")
            self.x_tb_qty=0
            self.y_tb_qty=0
            insulation_foundation = 2 * (self.width + self.length) * depth_found + (self.width * self.length)
            formwork_foundation = 2 * (self.width + self.length) * depth_found
            self.found_concrete = round(self.width * self.length * depth_found,2)
            rebar_foundation = self.found_concrete * self.rebar_weight
            self.lc_area = (self.width + 0.4) * (self.length + 0.4)
            self.insulation_sika(insulation_foundation)
            self.insulation_membrane(insulation_foundation)
            self.formwork(formwork_foundation)
            self.rebar(rebar_foundation)
            print("Lean Concrete Area = {}, insulation sika = {}, formwork = {}, rebar = {}".format(self.lc_area,insulation_foundation,formwork_foundation,rebar_foundation))
            return self.found_concrete

    def strip_foundation(self,depth_found,foundation_d1,column_rangex,column_rangey,tie_beam_d1,tie_beam_d2):
        print("strip foundation")
        y_axis_tie_beam = round(self.width / column_rangey,0) - 1
        print(y_axis_tie_beam)
        x_axis_tie_beam = round(self.length / column_rangex,0) - 1
        print(x_axis_tie_beam)
        print(depth_found,foundation_d1,column_rangex,column_rangey,tie_beam_d1,tie_beam_d2,sep="\n")
        if self.beam_connection == "ONE_WAY":#Checked
            print("one_way")
            self.x_tb_qty=x_axis_tie_beam
            self.y_tb_qty=0
            beam_length = self.width - 2 * foundation_d1
            beam_perimeter_area = (2 * tie_beam_d2) * beam_length
            insulation_foundation = 2 * (beam_length * depth_found)  * 2 + 2 * (self.length * depth_found) * 2 +  x_axis_tie_beam * tie_beam_d2 * beam_length * 2 + 2 * (self.width * foundation_d1) + 2 * (self.length * foundation_d1) +  x_axis_tie_beam * tie_beam_d1 * beam_length
            formwork_foundation = 2 * (beam_length * depth_found * 2) + 2 * (self.length * depth_found * 2) + x_axis_tie_beam * beam_perimeter_area
            self.found_concrete = round(2 * (beam_length * foundation_d1 * depth_found) + 2 * (self.length * foundation_d1 * depth_found) +  x_axis_tie_beam * tie_beam_d1 * tie_beam_d2 * beam_length,2)
            rebar_foundation = self.found_concrete * self.rebar_weight
            self.lc_area = 2 * beam_length * (foundation_d1 + 0.4) + 2 * (self.length + 0.4) * (foundation_d1 + 0.4) + x_axis_tie_beam * (tie_beam_d1 + 0.4) * beam_length
            self.insulation_sika(insulation_foundation)
            self.insulation_membrane(insulation_foundation)
            self.formwork(formwork_foundation)
            self.rebar(rebar_foundation)
            print("Lean Concrete Area = {}, insulation sika = {}, formwork = {}, rebar = {}".format(self.lc_area,insulation_foundation,formwork_foundation,rebar_foundation))
            return self.found_concrete
        elif self.beam_connection == "TWO_WAY":#Checked
            print("two_way")
            self.x_tb_qty=x_axis_tie_beam
            self.y_tb_qty=y_axis_tie_beam
            edge_width = self.width - 2 * foundation_d1
            beam_length = self.width - (self.y_tb_qty + 2) * foundation_d1
            beam_length2 = self.length - 2 * foundation_d1
            beam_perimeter_area = (2 * tie_beam_d2) * beam_length
            beam_perimeter_area2 = (2 * tie_beam_d2) * beam_length2
            insulation_foundation = 2 * (edge_width * depth_found) * 2 + 2 * (self.length  * depth_found) * 2 + y_axis_tie_beam * tie_beam_d2 * beam_length2 * 2 + x_axis_tie_beam * tie_beam_d2 * beam_length * 2 +  2 * (edge_width * foundation_d1) + 2 * (self.length  * foundation_d1) + y_axis_tie_beam * tie_beam_d1 * beam_length2 + x_axis_tie_beam * tie_beam_d1 * beam_length
            formwork_foundation = 2 * (edge_width * depth_found * 2) + 2 * (self.length * depth_found * 2) + y_axis_tie_beam * beam_perimeter_area2 + x_axis_tie_beam * beam_perimeter_area
            self.found_concrete = round(2 * (edge_width * foundation_d1 * depth_found) + 2 * (self.length * foundation_d1 * depth_found) + y_axis_tie_beam * foundation_d1 * tie_beam_d2 * beam_length2 + x_axis_tie_beam * tie_beam_d1 * tie_beam_d2 * beam_length,2)
            rebar_foundation = self.found_concrete * self.rebar_weight
            self.lc_area = 2 * (edge_width + 0.4) * (foundation_d1 + 0.4) + 2 * (self.length + 0.4) * (foundation_d1 + 0.4) + y_axis_tie_beam * (foundation_d1 + 0.4) * beam_length2 + x_axis_tie_beam * (tie_beam_d1 + 0.4) * beam_length
            self.insulation_sika(insulation_foundation)
            self.insulation_membrane(insulation_foundation)
            self.formwork(formwork_foundation)
            self.rebar(rebar_foundation)
            print("Lean Concrete Area = {}, insulation sika = {}, formwork = {}, rebar = {}".format(self.lc_area,insulation_foundation,formwork_foundation,rebar_foundation))
            return self.found_concrete
        elif self.beam_connection == "NO_BEAM":#Checked
            print("no_beam")
            self.x_tb_qty = 0
            self.y_tb_qty = 0
            insulation_foundation = 2 * ((self.width - 2 * foundation_d1) * depth_found) * 2 + 2 * (self.length * depth_found) * 2 + 2 * ((self.width - 2 * foundation_d1) * foundation_d1) + 2 * (self.length * foundation_d1)
            formwork_foundation = 2 * ((self.width - 2 * foundation_d1) * depth_found * 2) + 2 * (self.length * depth_found * 2)
            self.found_concrete = round(2 * ((self.width - 2 * foundation_d1) * foundation_d1 * depth_found) + 2 * (self.length * foundation_d1 * depth_found),2)
            rebar_foundation = self.found_concrete * self.rebar_weight
            self.lc_area = 2 * ((self.width - 2 * foundation_d1) + 0.4) * (foundation_d1 + 0.4) + 2 * (self.length + 0.4) * (foundation_d1 + 0.4)
            self.insulation_sika(insulation_foundation)
            self.insulation_membrane(insulation_foundation)
            self.formwork(formwork_foundation)
            self.rebar(rebar_foundation)
            print("Lean Concrete Area = {}, insulation sika = {}, formwork = {}, rebar = {}".format(self.lc_area,insulation_foundation,formwork_foundation,rebar_foundation))
            return self.found_concrete
    def single_footing(self,depth_found,foundation_d1,foundation_d2,column_rangex,column_rangey,tie_beam_d1,tie_beam_d2):
        print("single_footing")
        #düzelt column_rangey
        y_axis_tie_beam = round(self.width / column_rangey,0)
        print(y_axis_tie_beam)
        x_axis_tie_beam = round(self.length / column_rangex,0)
        print(x_axis_tie_beam)
        footing_qty_x = x_axis_tie_beam + 1
        footing_qty_y = y_axis_tie_beam + 1

        if self.beam_connection == "STRAP_BEAM":#Checked
            print("strap_beam")
            self.x_tb_qty = x_axis_tie_beam
            self.y_tb_qty = y_axis_tie_beam
            footing_qty = footing_qty_x * footing_qty_y
            tie_beam_length_y = column_rangey - foundation_d2
            tie_beam_length_x = column_rangex - foundation_d1
            insulation_foundation = footing_qty * depth_found * 2 * (foundation_d1 + foundation_d2) + (y_axis_tie_beam + 1) * x_axis_tie_beam * tie_beam_d2 * tie_beam_length_x * 2 + (x_axis_tie_beam + 1) * y_axis_tie_beam * tie_beam_d2 * tie_beam_length_y * 2 + footing_qty * (foundation_d1 * foundation_d2) + (y_axis_tie_beam + 1) * x_axis_tie_beam * tie_beam_d1 * tie_beam_length_x + (x_axis_tie_beam + 1) * y_axis_tie_beam * tie_beam_d1 * tie_beam_length_y
            formwork_foundation = footing_qty * depth_found * 2 * (foundation_d1 + foundation_d2) + (y_axis_tie_beam + 1) * x_axis_tie_beam * tie_beam_d2 * tie_beam_length_x * 2 + (x_axis_tie_beam + 1) * y_axis_tie_beam  * tie_beam_d2 * tie_beam_length_y * 2
            self.found_concrete = round(footing_qty * depth_found * foundation_d1 * foundation_d2 + (y_axis_tie_beam + 1) * x_axis_tie_beam * tie_beam_d1 * tie_beam_d2 * tie_beam_length_x + (x_axis_tie_beam + 1) * y_axis_tie_beam  * tie_beam_d1 * tie_beam_d2 * tie_beam_length_y,2)
            print("depth_found: ",depth_found)
            print("footing_qty: ",footing_qty)
            print("foundation_d1: ", foundation_d1)
            print("foundation_d2: ", foundation_d2)
            print("without beam single footing concrete: ",footing_qty * depth_found * foundation_d1 * foundation_d2)
            print("tie_beam_length_x",tie_beam_length_x)
            print("tie_beam_length_y",tie_beam_length_y)
            rebar_foundation = self.found_concrete * self.rebar_weight
            self.lc_area = footing_qty * (foundation_d1 + 0.4) * (foundation_d2 + 0.4) + (y_axis_tie_beam + 1) * x_axis_tie_beam  * (tie_beam_d1 + 0.4) * tie_beam_length_x + (x_axis_tie_beam + 1) * y_axis_tie_beam * (tie_beam_d1 + 0.4) * tie_beam_length_y
            self.insulation_sika(insulation_foundation)
            self.insulation_membrane(insulation_foundation)
            self.formwork(formwork_foundation)
            self.rebar(rebar_foundation)
            print("Lean Concrete Area = {}, insulation sika = {}, formwork = {}, rebar = {}".format(self.lc_area,insulation_foundation,formwork_foundation,rebar_foundation))
            return self.found_concrete

        elif self.beam_connection == "NO_BEAM":#Checked
            print("no_beam")
            self.x_tb_qty=x_axis_tie_beam
            self.y_tb_qty=y_axis_tie_beam
            insulation_foundation = footing_qty_x * footing_qty_y * depth_found * 2 * (foundation_d1 + foundation_d2) +  footing_qty_y * footing_qty_x * (foundation_d1 * foundation_d2)
            formwork_foundation=footing_qty_x * footing_qty_y * depth_found * 2 * (foundation_d1 + foundation_d2)
            self.found_concrete = round(footing_qty_x * footing_qty_y * depth_found * foundation_d1 * foundation_d2,2)
            rebar_foundation = self.found_concrete * self.rebar_weight
            self.lc_area = footing_qty_x * footing_qty_y * (foundation_d1 + 0.4) * (foundation_d2 + 0.4)
            self.insulation_sika(insulation_foundation)
            self.insulation_membrane(insulation_foundation)
            self.formwork(formwork_foundation)
            self.rebar(rebar_foundation)
            print("Lean Concrete Area = {}, insulation sika = {}, formwork = {}, rebar = {}".format(self.lc_area,insulation_foundation,formwork_foundation,rebar_foundation))
            return self.found_concrete

    def single_footing_only_edge(self,depth_found,foundation_d1,foundation_d2,column_rangex,column_rangey,tie_beam_d1,tie_beam_d2):
        print("single_footing")
        #düzelt column_rangey
        y_axis_tie_beam = round(self.width / column_rangey,0)
        print(y_axis_tie_beam)
        x_axis_tie_beam = round(self.length / column_rangex,0)
        print(x_axis_tie_beam)
        footing_qty_x = (x_axis_tie_beam + 1) * 2
        footing_qty_y = (y_axis_tie_beam - 1) * 2

        if self.beam_connection == "STRAP_BEAM":#Checked
            print("strap_beam")
            self.x_tb_qty = 0
            self.y_tb_qty = 0
            tie_beam_length_y = column_rangey - foundation_d2
            tie_beam_length_x = column_rangex - foundation_d1
            insulation_foundation = footing_qty_x * depth_found * 2 * (foundation_d1 + foundation_d2) + footing_qty_y * depth_found * 2 * (foundation_d1 + foundation_d2) + 2 * y_axis_tie_beam * tie_beam_d2 * tie_beam_length_y * 2  + 2 * x_axis_tie_beam * tie_beam_d2 * tie_beam_length_x * 2  + footing_qty_x * (foundation_d1 * foundation_d2) + footing_qty_y * (foundation_d1 * foundation_d2) + y_axis_tie_beam * tie_beam_d1 * tie_beam_length_y * 2 + x_axis_tie_beam * tie_beam_d1 * tie_beam_length_x * 2
            formwork_foundation = footing_qty_x * depth_found * 2 * (foundation_d1 + foundation_d2) + footing_qty_y * depth_found * 2 * (foundation_d1 + foundation_d2) + 2 * y_axis_tie_beam * tie_beam_d2 * tie_beam_length_y * 2 + 2 * x_axis_tie_beam * tie_beam_d2 * tie_beam_length_x * 2
            print("depth_found: ", depth_found)
            print("foundation_d1: ", foundation_d1)
            print("foundation_d2: ", foundation_d2)
            print("without beam single footing concrete: ", footing_qty_x * depth_found * 2 * (foundation_d1 + foundation_d2) + footing_qty_y * depth_found * 2 * (foundation_d1 + foundation_d2))
            print("tie_beam_length_x", tie_beam_length_x)
            print("tie_beam_length_y", tie_beam_length_y)
            self.found_concrete = round(footing_qty_x * depth_found * foundation_d1 * foundation_d2 + footing_qty_y * depth_found * foundation_d1 * foundation_d2 + 2 * y_axis_tie_beam * tie_beam_d1 * tie_beam_d2 * tie_beam_length_y + 2 * x_axis_tie_beam * tie_beam_d1 * tie_beam_d2 * tie_beam_length_x,2)
            rebar_foundation = self.found_concrete * self.rebar_weight
            self.lc_area = (footing_qty_x + footing_qty_y) * (foundation_d1 + 0.4) * (foundation_d2 + 0.4) + y_axis_tie_beam * (tie_beam_d1 + 0.4) * tie_beam_length_y * 2 + x_axis_tie_beam * (tie_beam_d1 + 0.4) * tie_beam_length_x * 2
            self.insulation_sika(insulation_foundation)
            self.insulation_membrane(insulation_foundation)
            self.formwork(formwork_foundation)
            self.rebar(rebar_foundation)
            print("Lean Concrete Area = {}, insulation sika = {}, formwork = {}, rebar = {}".format(self.lc_area,insulation_foundation,formwork_foundation,rebar_foundation))
            return self.found_concrete
        elif self.beam_connection == "NO_BEAM":#Checked
            print("no_beam")
            self.x_tb_qty = 0
            self.y_tb_qty = 0
            insulation_foundation = (footing_qty_x + footing_qty_y) * depth_found * 2 * (foundation_d1 + foundation_d2) +  (footing_qty_x + footing_qty_y) * (foundation_d1 * foundation_d2)
            formwork_foundation = (footing_qty_x + footing_qty_y) * depth_found * 2 * (foundation_d1 + foundation_d2)
            self.found_concrete = round((footing_qty_x + footing_qty_y) * depth_found * foundation_d1 * foundation_d2,2)
            rebar_foundation = self.found_concrete * self.rebar_weight
            self.lc_area = (footing_qty_x + footing_qty_y) * (foundation_d1 + 0.4) * (foundation_d2 + 0.4)
            self.insulation_sika(insulation_foundation)
            self.insulation_membrane(insulation_foundation)
            self.formwork(formwork_foundation)
            self.rebar(rebar_foundation)
            print("Lean Concrete Area = {}, insulation sika = {}, formwork = {}, rebar = {}".format(self.lc_area,insulation_foundation,formwork_foundation,rebar_foundation))
            return self.found_concrete
    #3.5
    def basement_wall(self,basement_height,basement_thickness,ground_wall_thickness,ground_wall_height,column_rangex,column_rangey,column_width,column_length,foundation_d1): #Checked
        print("calculating basement wall...")
        #print("concrete wall")
        self.basement_height = basement_height
        self.basement_thickness = basement_thickness

        insulation_height = self.depth_exc - self.depth_found - self.depth_fill - self.depth_lc -0.05
        y_axis_column_qty = round(self.width / column_rangey, 0) + 1
        x_axis_column_qty = round(self.length / column_rangex, 0) + 1
        edge_column_area_basement = ((y_axis_column_qty - 2) * 2 * column_width + x_axis_column_qty * 2 * column_length) * basement_height
        edge_column_area_gw = ((y_axis_column_qty - 2) * 2 * column_width + x_axis_column_qty * 2 * column_length) * ground_wall_height
        print(edge_column_area_gw)

        if foundation_d1 == None:
            foundation_d1 = 2

        if self.basement=="YES":#Checked
            print("there is a basement")
            insulation_basement_wall = 2 * (self.width + self.length) * insulation_height - edge_column_area_basement / basement_height * insulation_height
            formwork_basement_wall = (2 * (self.width + self.length) * self.basement_height - edge_column_area_basement) * 2
            basement_wall_conc = round((2 * (self.width + self.length) * self.basement_height - edge_column_area_basement) * self.basement_thickness,2)
            rebar_basement_wall = basement_wall_conc * self.rebar_weight
            self.insulation_sika(insulation_basement_wall)
            self.insulation_membrane(insulation_basement_wall)
            print("formwork_basement: ",formwork_basement_wall)
            self.formwork(formwork_basement_wall)
            self.rebar(rebar_basement_wall)
        elif self.basement=="NO":#Checked
            print("no basement")
            basement_wall_conc = 0
        insulation_height_gw = (self.depth_exc - self.depth_fill - self.depth_lc - self.depth_found - 0.05)
        print("insulation_height_gw: ",insulation_height_gw)

        if self.ground_wall=="YES":#Checked
            print("there is a ground wall")
            insulation_ground_wall = (2 * (self.width - (foundation_d1) + self.length - (foundation_d1)) * insulation_height_gw - edge_column_area_gw / self.ground_wall_height * insulation_height_gw) * 2
            formwork_ground_wall = (2 * (self.width - (foundation_d1) + self.length - (foundation_d1)) * self.ground_wall_height - edge_column_area_gw) * 2
            self.ground_wallc = (2 * (self.width - (foundation_d1) + self.length - (foundation_d1)) * self.ground_wall_height - edge_column_area_gw) * self.ground_wall_thickness
            rebar_ground_wall = self.ground_wallc * self.rebar_weight
            self.insulation_sika(insulation_ground_wall)
            print("insulation ground_wall: ",insulation_ground_wall)
            self.insulation_membrane(insulation_ground_wall)
            print("formwork ground_wall: ",formwork_ground_wall)
            self.formwork(formwork_ground_wall)
            self.rebar(rebar_ground_wall)
        elif self.ground_wall == "NO":#Checked
            print("no ground wall")
            self.ground_wallc = 0
        wall = self.ground_wallc + basement_wall_conc

        return wall

    #2.11
    def backfill(self):
        print("calculating backfill...")
        #1.25 compaction
        if self.structural_type=="RC":
            print("rc backfill")
            return self.rc_backfill()
        elif self.structural_type=="STEEL":
            print("steel backfill")
            return self.steel_backfill()
        else:
            return 0

    def steel_backfill(self):
        excavation=self.excavation(self.depth_exc)
        fill=self.strfill(self.depth_fill)
        foundation=self.found_concrete
        lean_concrete=self.lc_volume
        isolation_under_foundation = self.lc_volume / 2
        steel_pedestal_below_ground = (self.depth_exc - self.depth_fill - self.depth_found - self.depth_lc - 0.05) * self.pedestal_d1 * self.pedestal_d2 * self.pedestal_qty
        ground_wall=self.ground_wallc
        basement_volume = (self.width * self.length) * (self.depth_exc - self.depth_fill - self.depth_found - self.depth_lc - 0.05)
        if self.basement=="YES":
            steel_backfill = round(excavation - fill - foundation - lean_concrete - isolation_under_foundation - basement_volume,2)
        elif self.ground_wall=="YES" and self.basement =="NO":
            steel_backfill = round(excavation - fill - foundation - lean_concrete - isolation_under_foundation - steel_pedestal_below_ground - ground_wall ,2)
        elif self.ground_wall=="NO" and self.basement == "NO":
            steel_backfill = round(excavation - fill - foundation - lean_concrete - isolation_under_foundation - steel_pedestal_below_ground ,2)
        else:
            steel_backfill = round(excavation - fill - foundation - lean_concrete - isolation_under_foundation - steel_pedestal_below_ground ,2)
        print(f"backfill: {steel_backfill}")
        return steel_backfill

    def rc_backfill(self):
        excavation=self.excavation(self.depth_exc)
        fill=self.strfill(self.depth_fill)
        foundation=self.found_concrete
        lean_concrete=self.lc_volume
        isolation_under_foundation = self.lc_volume / 2
        rc_column_below_ground = (self.depth_exc - self.depth_fill - self.depth_found - self.depth_lc - 0.05) * self.rc_column_width * self.rc_column_length * self.column_qty
        print("rc_column_below_ground: ",rc_column_below_ground)
        ground_wall=self.ground_wallc
        basement_volume = (self.width * self.length) * (self.depth_exc - self.depth_fill - self.depth_found - self.depth_lc - 0.05)

        if self.basement=="YES":
            rc_backfill = round(excavation - fill - foundation - lean_concrete - isolation_under_foundation - basement_volume,2)
        elif self.ground_wall == "YES" and self.basement == "NO":
            rc_backfill = round(excavation - fill - foundation - lean_concrete - isolation_under_foundation - rc_column_below_ground - ground_wall ,2)
        elif self.ground_wall == "NO" and self.basement == "NO":
            rc_backfill = round(excavation - fill - foundation - lean_concrete - isolation_under_foundation - rc_column_below_ground  ,2)
        else:
            rc_backfill = round(excavation - fill - foundation - lean_concrete - isolation_under_foundation - rc_column_below_ground  ,2)

        print(f"backfill: {rc_backfill}")

        return rc_backfill

    # 3.7
    def ground_slab(self,grd_slb_thk,column_rangex,column_rangey,column_width,column_length):#Checked
        #print("ground slab without screed")
        self.grd_slb_thk=grd_slb_thk
        formwork_ground_slab = self.formwork_ground_slab(column_rangex,column_rangey,column_width,column_length)
        if self.is_steel() == True:
            print("yes steel")
            ground_slab_concrete = round((self.width * self.length - self.pedestal_qty * self.single_pedestal_top_area) * self.grd_slb_thk, 2)
        else:
            print("not steel")
            ground_slab_concrete = round((self.width * self.length - self.column_qty * self.single_column_top_area) * self.grd_slb_thk, 2)
        rebar_ground_slab = ground_slab_concrete * self.rebar_weight
        print("formwork ground_slab: ",formwork_ground_slab)
        self.formwork(formwork_ground_slab)
        self.rebar(rebar_ground_slab)
        return ground_slab_concrete


    #3.9
    def concrete_for_pavement(self):
        perimeter = 2 * (self.width + self.length)
        width = 1.5
        pavement = perimeter * width * 0.1
        return pavement

    def formwork_ground_slab(self,column_rangex,column_rangey,column_width,column_length):#Checked
        print("calculating formwork ground slab")
        y_axis_column_qty = round(self.width / column_rangey, 0) + 1
        x_axis_column_qty = round(self.length / column_rangex, 0) + 1
        edge_column_area = ((y_axis_column_qty - 2) * 2 * column_width + x_axis_column_qty * 2 * column_length) * self.grd_slb_thk
        if self.ground_wall == "NO" and self.basement == "NO":
            return round(2 * (self.width + self.length) * self.grd_slb_thk - edge_column_area,2)
        else:
            return 0

    # 4.1
    def formwork(self,formwork):#Checked
        self.formworks.append(formwork)
        print("formwork total: ",round(sum(self.formworks), 2))
        return round(sum(self.formworks), 2)

    # 5.1
    def rebar(self,rebar):#Checked
        #print("rebar")
        #(found+beam+wall+slab+ground slab+column+concrete slab)*0.1
        self.rebartotal.append(rebar)
        print("rebar total: ",sum(self.rebartotal))
        return round(sum(self.rebartotal), 2)

    #5.2
    def wire_mesh(self):
        #print("wire_mesh")
        perimeter = 2 * (self.width + self.length)
        width = 1.5
        wire_mesh = perimeter * width * 2
        self.wire_mesh_total.append(wire_mesh)
        return round(sum(self.wire_mesh_total),2)

    #17.1
    def insulation_sika(self,insulation):
        #print("sika igolflex")
        self.insulation_work.append(insulation)
        print("insulation sika total: ", round(sum(self.insulation_work),2))
        return round(sum(self.insulation_work),2)

    #17.2
    def insulation_membrane(self,insulation):
        #print("membrane")
        self.insulation_work_membrane.append(insulation)
        print("membrane total: ",round(sum(self.insulation_work_membrane),2))
        return round(sum(self.insulation_work_membrane),2)

    #17.4
    def pe_sheet(self):
        #print("pe_sheet")
        return(round(self.lc_area*2.1,2))

    #19.2
    def rainwater_pipe(self):
        #print("rainwater pipe")
        if self.width > 40:
            width_pipe=math.floor(self.width/40)
        else:
            width_pipe = 0
        if self.length > 40:
            length_pipe=math.floor(self.length/40)
        else:
            length_pipe = 0
        return (width_pipe * 2 + length_pipe * 2 + 4) * self.storey * self.storey_height

    #19.4
    def rainwater_gutter(self):
        #print("rainwater gutter")
        if self.is_steel()  == True:
            return(round(2*(self.length),2))
        else:
            return (round(2 * (self.width + self.length), 2))

    #20.11
    def catch_basin(self):
        if self.width > 40:
            width_pipe=math.floor(self.width/40)
        else:
            width_pipe = 0
        if self.length > 40:
            length_pipe=math.floor(self.length/40)
        else:
            length_pipe = 0
        return (width_pipe * 2 + length_pipe * 2 + 4)

    #21.2
    def walkable_roof(self):
        print("walkable roof")

    #21.5
    def water_stop(self):
        print("water stop")
        if self.basement == "YES":
            water_stop = 2 * (self.width + self.length) + 4 * self.basement_height
        else:
            water_stop = 2 * (self.width + self.length)
        return round(water_stop,2)
    #21.8
    def joint_cutting(self,column_rangex,column_rangey):
        print("joint cutting")
        y_axis = round(self.width / column_rangey,0) - 1
        x_axis = round(self.length / column_rangex,0) - 1
        joint_cutting = (y_axis * self.length + x_axis * self.width) * self.storey
        return joint_cutting
    #ARCHITECTURAL WORKS
    #CLADDING
    #9.1
    def single_sheet_roof_cladding(self):#Checked
        if self.insulation=="SHEET":
            return round(self.width * self.length * 1.1,2)
        print("single sheet roof cladding")
    #9.2
    def double_sheet_roof_cladding(self):
        print("Calculating roof cladding")
        if self.insulation=="CLADDING":
            return round(self.width * self.length * 1.1, 2)
        print("double sheet roof cladding")
    #9.3
    def insulated_wall_cladding(self):
        print("Calculating wall cladding")
        wall_cladding = 2 * (self.width + self.length) * (self.storey_height * self.storey) - self.window_area / 2
        if self.insulation=="CLADDING":
            return round(wall_cladding,2)
            print("Wall cladding calculated")
        else:
            return 0
        #print("insulated wall cladding")

    #WALLS
    #10.1
    #with external heat insulation
    def brick_wall300mm(self):
        #düzelt
        print("brick_wall300mm")
    #10.2
    def brick_wall200mm(self):#Checked
        #düzelt
        brick_wall_200mm = 2 * (self.width + self.length) * self.storey * (self. storey_height - self.rc_beam_width) - self.window_area - self.edge_column_area
        return round(brick_wall_200mm,2)
        print("brick_wall200mm")

    #10.3
    def brick_wall150mm(self,room_width, room_length, room_qty, floor_no,room_place,around_rooms):
        #print("brick_wall150mm")
        if room_place == "EDGE" and around_rooms == "ONE SIDE":
            room_perimeter = 2 * room_width
        elif room_place == "EDGE" and around_rooms == "BOTH SIDE":
            room_perimeter = room_width
        elif room_place == "EDGE" and around_rooms == "NONE":
            room_perimeter = 3 * room_width
        elif room_place == "MIDDLE" and around_rooms == "ONE SIDE":
            room_perimeter = 3 * room_width
        elif room_place == "MIDDLE" and around_rooms == "BOTH SIDE":
            room_perimeter = 2 * room_width
        elif room_place == "MIDDLE" and around_rooms == "NONE":
            room_perimeter = 4 * room_width
        room_perimeter = float(room_perimeter)
        #print(room_perimeter,type(room_perimeter))
        print(self.storey_height,type(self.storey_height))

        if floor_no == "BASEMENT":
            brick_wall = room_perimeter * self.basement_height
        else:
            if self.is_steel() == True:
                brick_wall = room_perimeter * self.storey_height / 2
            else:
                brick_wall = room_perimeter * self.storey_height

        return round(brick_wall * room_qty, 2)
    #10.4
    def gypsum_wall(self,room_width, room_length, room_qty, floor_no):
        #print("gypsum partition wall")
        if floor_no == "BASEMENT":
            gypsum_wall = 2 * (room_width + room_length) * self.basement_height
        else:
            if self.is_steel() == True:
                gypsum_wall = 2 * (room_width + room_length) * self.storey_height / 2
            else:
                gypsum_wall = 2 * (room_width + room_length) * self.storey_height
        return round(gypsum_wall*room_qty, 2)
    #SUSPENDED CEILINGS
    #11.1
    def aliminum_suspended_ceiling(self,room_width, room_length, room_qty, floor_no):
        #print("aliminum suspended ceiling")
        aliminum_ceiling = (room_width * room_length)
        return round(aliminum_ceiling*room_qty, 2)
    #11.2
    def acoustical_ceiling(self,room_width, room_length, room_qty, floor_no):
        #print("acoustical ceiling")
        acoustical_ceiling = (room_width * room_length)
        return round(acoustical_ceiling*room_qty, 2)
    #11.3
    def gypsum_suspended_ceiling(self,room_width, room_length, room_qty, floor_no):
        #print("gypsum suspended ceiling")
        gypsum_ceiling = (room_width * room_length)
        return round(gypsum_ceiling*room_qty, 2)
    #11.4
    def rockwool_suspended_ceiling(self,room_width, room_length, room_qty, floor_no):
        #print("rockwool suspended ceiling")
        rockwool_ceiling = (room_width * room_length)
        return round(rockwool_ceiling*room_qty, 2)

    #FLOOR FINISHES
    # 3.12
    def concrete_screed(self,room_width, room_length, room_qty, floor_no):
        #düzelt
        #print("screed")
        #before floor covering
        screed = (room_width * room_length * 0.05)
        return round(screed*room_qty, 2)
    #12.1
    def non_slip_ceramic_tiles(self,room_width, room_length, room_qty, floor_no):
        #print("non slip ceramic tiles for sanitary&kitchen rooms")
        non_slip_tile = (room_width * room_length)
        return round(non_slip_tile*room_qty, 2)
    #12.2
    def glazed_ceramic_tiles(self,room_width, room_length, room_qty, floor_no):
        #print("glazed ceramic tiles")
        glazed_tile = (room_width * room_length)
        return round(glazed_tile*room_qty, 2)
    #12.3
    def glazed_heavy_duty_ceramic_skirting(self,room_width, room_length, room_qty, floor_no):
        #print("glazed heavy duty ceramic skirting")
        glazed_skirting = 2 * (room_width + room_length)
        return round(glazed_skirting*room_qty, 2)
    #12.4
    def heavy_duty_epoxy(self,room_width, room_length, room_qty, floor_no):
        #print("heavy duty epoxy for RC floors")
        epoxy_floor = (room_width * room_length)
        return round(epoxy_floor*room_qty, 2)
    #12.5
    def resistant_flooring(self,room_width, room_length, room_qty, floor_no):
        #print("electrolite/chemical resistant flooring or ceramic tiling")
        resistant_flooring = (room_width * room_length)
        return round(resistant_flooring*room_qty, 2)
    #12.6
    def acid_resistant_tiles(self,room_width, room_length, room_qty, floor_no):
        #print("acid resistant tiles")
        acid_tile = (room_width * room_length)
        return round(acid_tile*room_qty, 2)
    #12.7
    def raised_floor(self,room_width, room_length, room_qty, floor_no):
        #print("raised floor(including all access and supports")
        raised_floor = (room_width * room_length)
        return round(raised_floor*room_qty, 2)
    #12.8
    def laminated_parquet_flooring(self,room_width, room_length, room_qty, floor_no):
        #print("laminated parquet flooring")
        laminate = (room_width * room_length)
        return round(laminate*room_qty, 2)
    #PLASTERING
    #13.1
    def interior_wall_plaster(self,room_width, room_length, room_qty, floor_no):
        #print("interior wall plaster")
        if floor_no == "BASEMENT":
            interior_plaster = 2 * (room_width + room_length)*self.basement_height
        else:
            if self.is_steel() == True:
                interior_plaster = 2 * (room_width + room_length) * self.storey_height / 2
            else:
                interior_plaster = 2 * (room_width + room_length) * self.storey_height
        return round(interior_plaster*room_qty, 2)
    #13.2
    def exterior_wall_plaster(self): # Checked
        #print("exterior wall plaster")
        exterior_wall_plaster = 2 * (self.width + self.length) * self.storey * (self.storey_height) - self.window_area
        return round(exterior_wall_plaster, 2)
    # 13.3
    def ceiling_plaster(self,room_width, room_length, room_qty, floor_no):
        #print("ceiling wall plaster")
        ceiling_plaster = (room_width * room_length)
        return round(ceiling_plaster*room_qty, 2)
    #WALL FINISHING
    #14.1
    def ceramic_wall_tiles(self,room_width, room_length, room_qty, floor_no):
        #print("ceramic wall tiles")
        if floor_no == "BASEMENT":
            ceramic_wall_tiles = 2 * (room_width + room_length)*self.basement_height
        else:
            if self.is_steel() == True:
                ceramic_wall_tiles = 2 * (room_width + room_length) * self.storey_height / 2
            else:
                ceramic_wall_tiles = 2 * (room_width + room_length) * self.storey_height
        return round(ceramic_wall_tiles*room_qty, 2)
    #14.2
    def interior_wall_paint(self,room_width, room_length, room_qty, floor_no):
        #print("interior wall paint")
        if floor_no == "BASEMENT":
            interior_wall_paint = 2 * (room_width + room_length) * self.basement_height
        else:
            if self.is_steel() == True:
                interior_wall_paint = 2 * (room_width + room_length) * self.storey_height / 2
            else:
                interior_wall_paint = 2 * (room_width + room_length) * self.storey_height
        return round(interior_wall_paint * room_qty, 2)
    #14.3
    def exterior_wall_paint(self):#Checked
        #düzelt
        #print("exterior wall paint")
        exterior_wall_paint = 2 * (self.width + self.length) * self.storey * (self. storey_height) - self.window_area
        return round(exterior_wall_paint,2)
    #14.4
    def acid_resistant_interior_paint(self,room_width, room_length, room_qty, floor_no):
        #print("acid resistant interior paint")
        if floor_no == "BASEMENT":
            acid_resistant_interior_paint = 2 * (room_width + room_length) * 3
        else:
            if self.is_steel() == True:
                acid_resistant_interior_paint = 2 * (room_width + room_length) * self.storey_height / 2
            else:
                acid_resistant_interior_paint = 2 * (room_width + room_length) * self.storey_height
        return round(acid_resistant_interior_paint * room_qty, 2)
    #14.5
    def ceiling_paint(self,room_width, room_length, room_qty, floor_no):
        #print("ceiling paint (water based paint)")
        ceiling_paint = (room_width * room_length)
        return round(ceiling_paint*room_qty, 2)
    #14.6
    def epoxy_wall_painting(self,room_width, room_length, room_qty, floor_no):
        #print("epoxy wall painting (interior walls)")
        if floor_no == "BASEMENT":
            epoxy_wall_painting = 2 * (room_width + room_length) * self.basement_height
        else:
            if self.is_steel() == True:
                epoxy_wall_painting = 2 * (room_width + room_length) * self.storey_height / 2
            else:
                epoxy_wall_painting = 2 * (room_width + room_length) * self.storey_height
        return round(epoxy_wall_painting * room_qty, 2)
    #14.7
    def alucobond_cladding(self):
        #düzelt
        #print("alucobond cladding (external)")
        if self.insulation == "ALUCOBOND":
            alucobond = 2 * (self.width + self.length) * (self.storey_height - self.rc_beam_width) * self.storey - self.window_area - self.edge_column_area
            return round(alucobond,2)
        else:
            return 0
    #14.8
    def marble_cladding(self):
        #düzelt
        #print("alucobond cladding (external)")
        if self.insulation == "MARBLE":
            marble = 2 * (self.width + self.length) * (self.storey_height - self.rc_beam_width) * self.storey - self.window_area - self.edge_column_area
            return round(marble,2)
        else:
            return 0
    #DOORS
    #15.1
    def steel_door1(self,room_width, room_length, room_qty, floor_no):
        return room_qty
    #15.2
    def steel_door2(self,room_width, room_length, room_qty, floor_no):
        return room_qty
    #15.3
    def roller_shutter(self,room_width, room_length, room_qty, floor_no):
        return room_qty
    #15.4
    def sliding_steel_door(self,room_width, room_length, room_qty, floor_no):
        return room_qty

    #15.4
    def sliding_steel_door_building(self,structural_type):
        if structural_type == "STEEL":
            door_qty = 2
        else:
            door_qty = 0
        return door_qty

    #15.5
    def double_wing_aliminium_door_entrance(self,room_width, room_length, room_qty, floor_no):
        return room_qty

    #15.5
    def double_wing_aliminium_door_entrance_building(self,structural_type):
        if structural_type == "RC":
            door_qty = 1
        else:
            door_qty = 0
        return door_qty

    #15.6
    def compacted_laminate_door(self,room_width, room_length, room_qty, floor_no):
        return room_qty * 2
    #15.7
    def wooden_internal_door(self,room_width, room_length, room_qty, floor_no):
        return room_qty
    #15.8
    def aliminum_door(self,room_width, room_length, room_qty, floor_no):
        return room_qty
    #15.9
    def aliminum_double_win_door(self,room_width, room_length, room_qty, floor_no):
        return room_qty

    #WINDOWS
    #16.1
    def pvc_window(self):
        #print("pvc window double glazed")
        self.window_area =  2 * (self.width + self.length) * self.storey_height * self.storey * 0.35
        return self.window_area


    def is_steel(self):
        if self.structural_type == "STEEL":
            return True
        else:
            return False

class steel_bldg(building):
    def __init__(self):
        super(building, self).__init__()
        self.insulation_work = []
        self.insulation_work_membrane = []
        self.formworks = []
        self.rebartotal = []
        self.rebar_weight = 0.1
        self.lc_total = []
        self.wire_mesh_total = []

#3.3
    def steel_pedestal(self,pedestal_rangex, pedestal_rangey, pedestal_d1, pedestal_d2, pedestal_depth):#Checked
        #print("steel column")
        #düzeltildi
        self.pedestal_d1=pedestal_d1
        self.pedestal_d2=pedestal_d2
        self.pedestal_depth=pedestal_depth
        self.pedestal_rangex=pedestal_rangex
        self.pedestal_rangey=pedestal_rangey

        y_axis_pedestal_qty = round(self.width / pedestal_rangey,0) + 1
        x_axis_pedestal_qty = round(self.length / pedestal_rangex,0) + 1

        single_pedestal_volume = pedestal_d1 * pedestal_d2 * pedestal_depth
        single_pedestal_below_ground_area = 2 * (pedestal_d1 + pedestal_d2) * (self.depth_exc - self.depth_fill - self.depth_found - self.depth_lc - 0.05)
        single_pedestal_perimeter_area = 2 * (pedestal_d1 + pedestal_d2) * self.pedestal_depth
        self.single_pedestal_top_area = pedestal_d1 * pedestal_d2

        print("PEDESTAL",pedestal_rangex, pedestal_rangey, pedestal_d1, pedestal_d2, pedestal_depth,sep="\n")

        if self.beam_connection=="NO_BEAM" and self.soil_property=="MAT" or self.soil_property=="SINGLE_FOOTING":#Checked
            concrete_pedestal = round((y_axis_pedestal_qty * x_axis_pedestal_qty) * single_pedestal_volume,2)
            insulation_pedestal = round((y_axis_pedestal_qty * x_axis_pedestal_qty) * single_pedestal_below_ground_area,2)
            formwork_pedestal = round((y_axis_pedestal_qty * x_axis_pedestal_qty) * single_pedestal_perimeter_area,2)
            self.pedestal_qty = (y_axis_pedestal_qty * x_axis_pedestal_qty)

        elif self.beam_connection=="NO_BEAM" and self.soil_property=="STRIP":#Checked
            concrete_pedestal = round(((y_axis_pedestal_qty - 2) * single_pedestal_volume + x_axis_pedestal_qty * single_pedestal_volume) * 2, 2)
            insulation_pedestal = round(((y_axis_pedestal_qty - 2) * single_pedestal_below_ground_area + x_axis_pedestal_qty * single_pedestal_below_ground_area) * 2,2)
            formwork_pedestal = round(((y_axis_pedestal_qty - 2) * single_pedestal_perimeter_area + x_axis_pedestal_qty * single_pedestal_perimeter_area) * 2 ,2)
            self.pedestal_qty = round((y_axis_pedestal_qty - 2  + x_axis_pedestal_qty) * 2 ,2)

        else:#Checked
            print("there is a beam")
            concrete_pedestal = round(((y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2) * single_pedestal_volume + self.y_tb_qty * (x_axis_pedestal_qty - 2) * single_pedestal_volume,2)
            print("True concrete_pedestal: ",((y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2) * single_pedestal_volume )
            insulation_pedestal = round(((y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2) * single_pedestal_below_ground_area + self.y_tb_qty * (x_axis_pedestal_qty - 2) * single_pedestal_below_ground_area,2)
            formwork_pedestal = round(((y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2) * single_pedestal_perimeter_area + self.y_tb_qty * (x_axis_pedestal_qty - 2) * single_pedestal_perimeter_area,2)
            self.pedestal_qty = (y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2 + self.y_tb_qty * (x_axis_pedestal_qty - 2)

        rebar_pedestal = concrete_pedestal * self.rebar_weight

        self.insulation_sika(insulation_pedestal)
        self.insulation_membrane(insulation_pedestal)
        self.formwork(formwork_pedestal)
        self.rebar(rebar_pedestal)


        return concrete_pedestal

    #3.6
    def steel_concrete_slab(self,slab_thickness):
        self.concrete_slab_thickness=slab_thickness

        if self.middle_floor =="YES":
            concrete_conc_slab = round((self.width * self.length - self.pedestal_qty * self.single_pedestal_top_area) * self.concrete_slab_thickness ,2)
            formwork_conc_slab = round(self.concrete_slab_thickness * 2 * (self.width + self.length) + self.width * self.length - self.pedestal_qty * self.single_pedestal_top_area,2)
            self.wire_mesh_total.append(self.width * self.length)
            self.formwork(formwork_conc_slab)
            print("steel_concrete_slab: ",concrete_conc_slab)
            return concrete_conc_slab


        else:

            return 0


#3.11
    def grouting(self,depth_grout): #Checked
        #print("grout")
        self.depth_grout = depth_grout
        y_axis_pedestal_qty = round(self.width / self.pedestal_rangey,0) + 1
        x_axis_pedestal_qty = round(self.length / self.pedestal_rangex,0) + 1
        single_pedestal_area = self.pedestal_d1 * self.pedestal_d2
        single_pedestal_perimeter = 2 * (self.pedestal_d1 + self.pedestal_d2)
        if self.beam_connection=="NO_BEAM" and self.soil_property=="MAT" or self.soil_property=="SINGLE_FOOTING": #no_beam means mat foundation or single footing
            concrete_grout = round((y_axis_pedestal_qty * x_axis_pedestal_qty) * single_pedestal_area * depth_grout,2)
            return concrete_grout
        elif self.beam_connection=="NO_BEAM" and self.soil_property=="STRIP":
            return round(((y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2) * single_pedestal_area * depth_grout,2)
        else:
            return round(((y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2) * single_pedestal_area * depth_grout + self.y_tb_qty * (x_axis_pedestal_qty - 2) * single_pedestal_area * depth_grout ,2)

# 6.1
    def embedded_steel(self):
        #print("embedded")
        es = self.lc_area * 0.001
        return es

# 6.2,6.3,6.4,6.5,6.6
    def anchorbolt_m24(self):#CHECKED
        #print("m24")
        y_axis_pedestal_qty = round(self.width / self.pedestal_rangey,0) + 1
        x_axis_pedestal_qty = round(self.length / self.pedestal_rangex,0) + 1
        if self.beam_connection=="NO_BEAM" and self.soil_property=="MAT" or self.soil_property=="SINGLE_FOOTING": #no_beam means mat foundation or single footing
            return round((y_axis_pedestal_qty * x_axis_pedestal_qty) * 4,2)
        elif self.beam_connection=="NO_BEAM" and self.soil_property=="STRIP":
            return round(((y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2) * 4,2)
        else:
            return round((((y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2) + self.y_tb_qty * (x_axis_pedestal_qty - 2)) * 4,2)

    def anchorbolt_m30(self):#CHECKED
        #print("m30")
        y_axis_pedestal_qty = round(self.width / self.pedestal_rangey,0) + 1
        x_axis_pedestal_qty = round(self.length / self.pedestal_rangex,0) + 1

        if self.beam_connection=="NO_BEAM" and self.soil_property=="MAT" or self.soil_property=="SINGLE_FOOTING": #no_beam means mat foundation or single footing
            return round((y_axis_pedestal_qty * x_axis_pedestal_qty) * 2,2)
        elif self.beam_connection=="NO_BEAM" and self.soil_property=="STRIP":
            return round(((y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2) * 2,2)
        else:
            return round((((y_axis_pedestal_qty - 2) * 2 + x_axis_pedestal_qty * 2) + self.y_tb_qty * (x_axis_pedestal_qty - 2)) * 2,2)

#7.1
    def steel_weight(self,unit_weight): #Checked
        self.unit_weight=unit_weight
        print("steel weight: ",self.unit_weight)
        return round(self.width * self.length * self.storey_height * self.storey * self.unit_weight / 1000,2)

#Secondary Steel Works

#8.1
    def handrail(self):
        #print("handrail")
        return 0

#8.3
    def steel_grating(self):
        #print("steel grating")
        return 0
#8.4
    def chequered_plate(self):
        #print("chequered plate")
        return 0
#8.6
    def steel_ladder(self):
        #print("steel ladder")
        steel_ladder = self.storey_height * 2
        return steel_ladder

class rc_bldg(building):
    def __init__(self):
        super(building, self).__init__()

        self.insulation_work = []
        self.insulation_work_membrane = []
        self.formworks = []
        self.rebartotal = []
        self.rebar_weight = 0.1
        self.lc_total =[]
        self.wire_mesh_total = []

    #3.3
    def rc_column(self,rc_column_length,rc_column_width,rc_column_rangex,rc_column_rangey):#Checked
       # print("rc column")

        self.rc_column_length=rc_column_length
        self.rc_column_width=rc_column_width
        self.rc_column_rangex=rc_column_rangex
        self.rc_column_rangey=rc_column_rangey

        y_axis_column_qty = round(self.width / rc_column_rangey,0)  + 1
        x_axis_column_qty = round(self.length / rc_column_rangex,0) + 1
        self.single_column_top_area = rc_column_length * rc_column_width
        self.edge_column_area = ((y_axis_column_qty - 2) * 2 * self.rc_column_width +  x_axis_column_qty * 2 * self.rc_column_length) * self.storey * self.storey_height

        if self.basement=="YES":
            single_column_height = self.storey * self.storey_height + self.basement_height
            single_column_volume = single_column_height * self.rc_column_length * self.rc_column_width
            single_column_perimeter_area = single_column_height * 2 * (self.rc_column_length + self.rc_column_width)
            single_column_below_ground_area = 2 * (self.rc_column_length + self.rc_column_width) * (self.basement_height + (self.depth_exc - self.depth_fill - self.depth_found - self.depth_lc - 0.05))

            if self.beam_connection == "NO_BEAM" and self.soil_property == "MAT" or self.soil_property == "SINGLE_FOOTING":  # it means mat foundation or single footing
                concrete_column = round((y_axis_column_qty * x_axis_column_qty) * single_column_volume, 2)
                formwork_column = round((y_axis_column_qty * x_axis_column_qty) * single_column_perimeter_area, 2)
                self.column_qty = (y_axis_column_qty * x_axis_column_qty)

            elif self.beam_connection == "NO_BEAM" and self.soil_property == "STRIP":
                concrete_column = round(((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) * single_column_volume, 2)
                formwork_column = round(((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) * single_column_perimeter_area, 2)
                self.column_qty = ((y_axis_column_qty - 2) * 2 +  x_axis_column_qty * 2)

            else:
                concrete_column = round(((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) * single_column_volume + self.y_tb_qty * (x_axis_column_qty - 2) * single_column_volume , 2)
                formwork_column = round(((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) * single_column_perimeter_area + self.y_tb_qty * (x_axis_column_qty - 2) * single_column_perimeter_area, 2)
                self.column_qty = ((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) + self.y_tb_qty * (x_axis_column_qty - 2)
        else:
            single_column_height = self.storey * self.storey_height
            single_column_volume = single_column_height * self.rc_column_length*self.rc_column_width
            single_column_perimeter_area = single_column_height * 2 * (self.rc_column_length + self.rc_column_width)
            single_column_below_ground_area = 2 * (self.rc_column_length + self.rc_column_width) * ((self.depth_exc - self.depth_fill - self.depth_found - self.depth_lc - 0.05))

            if self.beam_connection == "NO_BEAM" and self.soil_property == "MAT" or self.soil_property == "SINGLE_FOOTING":  # it means mat foundation or single footing
                concrete_column = round((y_axis_column_qty * x_axis_column_qty) * single_column_volume, 2)
                print("concrete_column: ",concrete_column)
                formwork_column = round((y_axis_column_qty * x_axis_column_qty) * single_column_perimeter_area, 2)
                insulation_column = round((y_axis_column_qty * x_axis_column_qty) * single_column_below_ground_area,2)
                self.column_qty = (y_axis_column_qty * x_axis_column_qty)

            elif self.beam_connection == "NO_BEAM" and self.soil_property == "STRIP":
                concrete_column = round(((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) * single_column_volume, 2)
                formwork_column = round(((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) * single_column_perimeter_area, 2)
                insulation_column = round(((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) * single_column_below_ground_area,2)
                self.column_qty = ((y_axis_column_qty - 2) * 2 +  x_axis_column_qty * 2)

            else:
                concrete_column = round(((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) * single_column_volume + self.y_tb_qty * (x_axis_column_qty - 2) * single_column_volume , 2)
                formwork_column = round(((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) * single_column_perimeter_area + self.y_tb_qty * (x_axis_column_qty - 2) * single_column_perimeter_area, 2)
                insulation_column = round(((y_axis_column_qty - 2) * 2+x_axis_column_qty * 2) * single_column_below_ground_area + self.y_tb_qty * (x_axis_column_qty-2) * single_column_below_ground_area,2)
                self.column_qty = ((y_axis_column_qty - 2) * 2 + x_axis_column_qty * 2) + self.y_tb_qty * (x_axis_column_qty - 2)
            print("insulation_column: ", insulation_column)
            self.insulation_sika(insulation_column)
            self.insulation_membrane(insulation_column)
        rebar_column = concrete_column * self.rebar_weight
        print("formwork_column: ", formwork_column)
        self.formwork(formwork_column)
        self.rebar(rebar_column)


        return concrete_column

    #3.4
    def rc_beam(self,rc_beam_width,rc_beam_length,rc_secondary_beam_d1,rc_secondary_beam_d2):#Checked
        self.rc_beam_width = rc_beam_width
        self.rc_beam_length = rc_beam_length
        self.rc_secondary_beam_d1 = rc_secondary_beam_d1
        self.rc_secondary_beam_d2 = rc_secondary_beam_d2

        y_axis_beam_qty = round(self.width / self.rc_column_rangey,0)
        y_axis_beam_length = self.rc_column_rangey - self.rc_column_width
        print("y_axis_beam: ",y_axis_beam_length)
        x_axis_beam_qty = round(self.length / self.rc_column_rangex,0)
        x_axis_beam_length = self.rc_column_rangex - self.rc_column_length
        print("x_axis_beam: ",x_axis_beam_length)
        beam_section_area = rc_beam_length * rc_beam_width
        beam_section_perimeter = rc_beam_length + rc_beam_width * 2
        secondary_beam_section_area = rc_secondary_beam_d1 * rc_secondary_beam_d2
        secondary_beam_section_perimeter = rc_secondary_beam_d1 + 2 * rc_secondary_beam_d2
        secondary_beam_top_area = rc_secondary_beam_d1 * y_axis_beam_length
        beam_top_area = rc_beam_length * x_axis_beam_length
        beam_volume = rc_beam_length * rc_beam_width * x_axis_beam_length
        secondary_beam_volume = rc_secondary_beam_d1 * rc_secondary_beam_d2 * x_axis_beam_length

        if self.basement=="YES":

            if self.beam_connection == "NO_BEAM" and self.soil_property == "MAT" or self.soil_property == "SINGLE_FOOTING":
                # WHEN THERE IS NO TIE BEAM
                y_beam_qty = y_axis_beam_qty * (x_axis_beam_qty + 1)#1*3
                print("y_beam_qty: ",y_beam_qty)
                x_beam_qty = (y_axis_beam_qty + 1) * x_axis_beam_qty#2*2
                print("x_beam_qty: ",x_beam_qty)
                concrete_beam = round((self.storey + 1)*(y_beam_qty * y_axis_beam_length * secondary_beam_section_area + x_beam_qty * x_axis_beam_length * beam_section_area),2)
                formwork_beam = round((self.storey + 1)*(y_beam_qty * y_axis_beam_length * secondary_beam_section_perimeter + x_beam_qty * x_axis_beam_length * beam_section_perimeter) ,2)
                self.beam_area = round((y_beam_qty * secondary_beam_top_area + x_beam_qty * beam_top_area) ,2)
                self.beam_volume = round((self.storey + 1)*(y_beam_qty * secondary_beam_volume + x_beam_qty * beam_volume) ,2)
                print("formwork_beam: ",formwork_beam)

            elif self.beam_connection == "NO_BEAM" and self.soil_property == "STRIP":
                concrete_beam = round((self.storey + 1)*(y_axis_beam_qty * y_axis_beam_length * secondary_beam_section_area + x_axis_beam_qty * x_axis_beam_length * beam_section_area) * 2,2)
                formwork_beam = round((self.storey + 1)*(y_axis_beam_qty * y_axis_beam_length * secondary_beam_section_perimeter + x_axis_beam_qty * x_axis_beam_length * beam_section_perimeter) * 2,2)
                self.beam_area = round((y_axis_beam_qty * 2 * secondary_beam_top_area + x_axis_beam_qty * 2 * beam_top_area) ,2)
                self.beam_volume = round((self.storey + 1)*(y_axis_beam_qty * 2 * secondary_beam_volume + x_axis_beam_qty * 2 * beam_volume) ,2)

            else:
                y_beam_qty = y_axis_beam_qty * (x_axis_beam_qty + 1)
                x_beam_qty = (y_axis_beam_qty + 1) * x_axis_beam_qty
                concrete_beam = round((self.storey + 1)*(y_beam_qty * y_axis_beam_length * secondary_beam_section_area + x_beam_qty * x_axis_beam_length * beam_section_area) ,2)
                formwork_beam = round((self.storey + 1)*(y_beam_qty * y_axis_beam_length * secondary_beam_section_perimeter + x_beam_qty * x_axis_beam_length * beam_section_perimeter) ,2)
                self.beam_area = round((y_beam_qty * secondary_beam_top_area + x_beam_qty * beam_top_area) ,2)
                self.beam_volume = round((self.storey + 1)*(y_beam_qty * secondary_beam_volume + x_beam_qty * beam_volume) ,2)

        else:
            if self.beam_connection == "NO_BEAM" and self.soil_property == "MAT" or self.soil_property == "SINGLE_FOOTING":
                # WHEN THERE IS NO TIE BEAM
                y_beam_qty = y_axis_beam_qty * (x_axis_beam_qty + 1)#1*3
                print("y_beam_qty: ",y_beam_qty)
                x_beam_qty = (y_axis_beam_qty + 1) * x_axis_beam_qty#2*2
                print("x_beam_qty: ",x_beam_qty)
                concrete_beam = round((self.storey)*(y_beam_qty * y_axis_beam_length * secondary_beam_section_area + x_beam_qty * x_axis_beam_length * beam_section_area),2)
                formwork_beam = round((self.storey)*(y_beam_qty * y_axis_beam_length * secondary_beam_section_perimeter + x_beam_qty * x_axis_beam_length * beam_section_perimeter) ,2)
                self.beam_area = round((y_beam_qty * secondary_beam_top_area + x_beam_qty * beam_top_area) ,2)
                self.beam_volume = round((self.storey)*(y_beam_qty * secondary_beam_volume + x_beam_qty * beam_volume) ,2)

            elif self.beam_connection == "NO_BEAM" and self.soil_property == "STRIP":
                concrete_beam = round((self.storey) * (y_axis_beam_qty * y_axis_beam_length * secondary_beam_section_area + x_axis_beam_qty * x_axis_beam_length * beam_section_area) * 2,2)
                formwork_beam = round((self.storey) * (y_axis_beam_qty * y_axis_beam_length * secondary_beam_section_perimeter + x_axis_beam_qty * x_axis_beam_length * beam_section_perimeter) * 2,2)
                self.beam_area = round((y_axis_beam_qty * 2 * secondary_beam_top_area + x_axis_beam_qty * 2 * beam_top_area) ,2)
                self.beam_volume = round((self.storey) * (y_axis_beam_qty * 2 * secondary_beam_volume + x_axis_beam_qty * 2 * beam_volume) ,2)

            else:
                y_beam_qty = y_axis_beam_qty * (x_axis_beam_qty+1)
                x_beam_qty = (y_axis_beam_qty + 1) * x_axis_beam_qty
                concrete_beam = round((self.storey)*(y_beam_qty * y_axis_beam_length * secondary_beam_section_area + x_beam_qty * x_axis_beam_length * beam_section_area) ,2)
                formwork_beam = round((self.storey)*(y_beam_qty * y_axis_beam_length * secondary_beam_section_perimeter + x_beam_qty * x_axis_beam_length * beam_section_perimeter) ,2)
                self.beam_area = round((y_beam_qty * secondary_beam_top_area + x_beam_qty * beam_top_area) ,2)
                self.beam_volume = round((self.storey)*(y_beam_qty * secondary_beam_volume + x_beam_qty * beam_volume) ,2)


        print("formwork_beam: ",formwork_beam)
        rebar_beam = concrete_beam * self.rebar_weight
        self.formwork(formwork_beam)
        self.rebar(rebar_beam)


        return concrete_beam

    #3.6
    def concrete_slab(self,slab_thickness,paraphet_height,paraphet_thickness):#Checked
        self.concrete_slab_thickness=slab_thickness

        if self.basement=="YES":#Checked
            if self.structural_type == "RC":
                concrete_conc_slab = round((self.storey+1) * self.concrete_slab_thickness * (self.width * self.length - self.single_column_top_area * self.column_qty - self.beam_area) + self.paraphet(paraphet_height, paraphet_thickness), 2)
                formwork_conc_slab = round((self.storey+1) * (self.concrete_slab_thickness * 2 * (self.width + self.length) + (self.width * self.length - self.beam_area - self.single_column_top_area * self.column_qty)),2)
            else:
                concrete_conc_slab = round((self.storey+1) * self.concrete_slab_thickness * self.width * self.length, 2)
                formwork_conc_slab = round((self.storey+1) * (self.concrete_slab_thickness * 2 * (self.width + self.length) + (self.width * self.length -self.pedestal_qty * self.single_pedestal_top_area)),2)
            rebar_conc_slab = concrete_conc_slab * self.rebar_weight
            self.formwork(formwork_conc_slab)
            self.rebar(rebar_conc_slab)


        else:
            if self.structural_type == "RC":#Checked
                concrete_conc_slab = round((self.storey) * self.concrete_slab_thickness * (self.width * self.length - self.single_column_top_area * self.column_qty - self.beam_area) + self.paraphet(paraphet_height, paraphet_thickness), 2)
                formwork_conc_slab = round((self.storey) * (self.concrete_slab_thickness * 2 * (self.width + self.length) + (self.width * self.length - self.beam_area - self.single_column_top_area * self.column_qty)),2)
            else:
                concrete_conc_slab = round((self.storey) * self.concrete_slab_thickness * self.width * self.length, 2)
                formwork_conc_slab = round((self.storey) * (self.concrete_slab_thickness * 2 * (self.width + self.length) + (self.width * self.length -self.pedestal_qty * self.single_pedestal_top_area)),2)
            rebar_conc_slab = concrete_conc_slab * self.rebar_weight
            self.formwork(formwork_conc_slab)
            self.rebar(rebar_conc_slab)
        print("formwork_slab: ", formwork_conc_slab)
        return concrete_conc_slab

    def paraphet(self,paraphet_height,paraphet_thickness):#Checked
        print("paraphet")
        perimeter = 2 * (self.width + self.length)
        concrete_paraphet = perimeter * paraphet_height * paraphet_thickness
        formwork_paraphet = perimeter * paraphet_height * 2
        rebar_paraphet = concrete_paraphet * self.rebar_weight

        print("formwork_paraphet: ",formwork_paraphet)
        self.formwork(formwork_paraphet)
        self.rebar(rebar_paraphet)

        return concrete_paraphet

    def concrete_stairs(self):
        #12 steps for floor
        #width = 30cm depth = 15cm
        #1.2m genişlik
        if self.storey>1:
            up_floor = round(self.storey_height*self.storey / 0.15,0)
        else:
            up_floor = 0
        basement = round(self.basement_height / 0.15,0)
        step_volume = (0.3 * 0.15 * 1.2) * 1.5
        print(self.basement)
        if self.basement == "YES":
            stair_concrete = round((up_floor + basement) * step_volume,2)
        else:
            stair_concrete = round(up_floor * step_volume,2)
        return stair_concrete

    #STEEL LADDER
    #8.6
    def steel_ladder(self):
        steel_ladder = self.storey_height * self.storey * 2
        return steel_ladder


class room(building):
    def __init__(self):
        super(building, self).__init__()

    # ROOMS
    def rooms(self, room_type,room_area,room_qty,floor_no,room_place,around_rooms):
        room_width = room_length = float(math.sqrt(room_area))
        inside_brick_wall = self.brick_wall150mm(room_width, room_length, room_qty, floor_no,room_place,around_rooms)
        gypsum_part_wall = self.gypsum_wall(room_width, room_length, room_qty, floor_no)
        aliminum_suspended_ceiling = self.aliminum_suspended_ceiling(room_width, room_length, room_qty, floor_no)
        acoustical_ceiling = self.acoustical_ceiling(room_width, room_length, room_qty, floor_no)
        gypsum_suspended_ceiling = self.gypsum_suspended_ceiling(room_width, room_length, room_qty, floor_no)
        rockwool_suspended_ceiling = self.rockwool_suspended_ceiling(room_width, room_length, room_qty, floor_no)
        non_slip_ceramic_tile = self.non_slip_ceramic_tiles(room_width, room_length, room_qty, floor_no)
        glazed_ceramic_tile = self.glazed_ceramic_tiles(room_width, room_length, room_qty, floor_no)
        glazed_ceramic_skirting = self.glazed_heavy_duty_ceramic_skirting(room_width, room_length, room_qty, floor_no)
        epoxy_painting_floor = self.heavy_duty_epoxy(room_width, room_length, room_qty, floor_no)
        resistant_floor = self.resistant_flooring(room_width, room_length, room_qty, floor_no)
        acid_tile = self.acid_resistant_tiles(room_width, room_length, room_qty, floor_no)
        raised_floor = self.raised_floor(room_width, room_length, room_qty, floor_no)
        laminated_parquet = self.laminated_parquet_flooring(room_width, room_length, room_qty, floor_no)
        int_plaster = self.interior_wall_plaster(room_width, room_length, room_qty, floor_no)
        ceiling_plaster = self.ceiling_plaster(room_width, room_length, room_qty, floor_no)
        ceramic_wall_tile = self.ceramic_wall_tiles(room_width, room_length, room_qty, floor_no)
        int_paint = self.interior_wall_paint(room_width, room_length, room_qty, floor_no)
        acid_resistant_int_paint = self.acid_resistant_interior_paint(room_width, room_length, room_qty, floor_no)
        ceiling_paint = self.ceiling_paint(room_width, room_length, room_qty, floor_no)
        epoxy_wall_paint = self.epoxy_wall_painting(room_width, room_length, room_qty, floor_no)
        steel_door1 = self.steel_door1(room_width, room_length, room_qty, floor_no)#steel_door1,steel_door2,roller_shutter,sliding_steel_door,double_wing_aliminium_door,compacted_laminate_door,wooden_internal_door,aliminum_door,aliminum_double_win_door
        steel_door2 =self.steel_door2(room_width, room_length, room_qty, floor_no)
        roller_shutter = self.roller_shutter(room_width, room_length, room_qty, floor_no)
        sliding_steel_door = self.sliding_steel_door(room_width, room_length, room_qty, floor_no)
        double_wing_aliminium_door = self.double_wing_aliminium_door_entrance(room_width, room_length, room_qty, floor_no)
        compacted_laminate_door = self.compacted_laminate_door(room_width, room_length, room_qty, floor_no)
        wooden_internal_door = self.wooden_internal_door(room_width, room_length, room_qty, floor_no)
        aliminum_door = self.aliminum_door(room_width, room_length, room_qty, floor_no)
        aliminum_double_win_door = self.aliminum_double_win_door(room_width, room_length, room_qty, floor_no)
        screed = self.concrete_screed(room_width, room_length, room_qty, floor_no)
        """DEFAULTS:
        -inside brick wall
        -İnterior wall plaster
        -Ceiling plaster
        -Ceiling paint eğer asma tavan yoksa!!
        -Interior wall paint
        -Ceiling paint
        -Epoxy wall painting??
        """
        room_works = {"OFFICE":[inside_brick_wall,0,0,acoustical_ceiling,0,0,0,0,0,0,0,0,0,laminated_parquet,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,wooden_internal_door,0,0,screed]
                    , "SPECIAL_OFFICE":[inside_brick_wall,0,0,acoustical_ceiling,0,0,0,0,0,0,0,0,0,laminated_parquet,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,wooden_internal_door,0,0,screed]
                    , "ELECTRICAL_ROOM":[inside_brick_wall,0,0,0,0,0,0,0,0,0,resistant_floor,0,0,0,int_plaster,ceiling_plaster,0,int_paint,0,ceiling_paint,0,0,0,0,0,0,0,0,aliminum_door,0,screed]
                    , "CONTROL_ROOM":[inside_brick_wall,0,0,acoustical_ceiling,0,0,0,0,0,0,0,0,raised_floor,0,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,0,aliminum_door,0,screed]
                    , "STORE":[inside_brick_wall,0,0,0,0,rockwool_suspended_ceiling,0,0,0,epoxy_painting_floor,0,0,0,0,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,wooden_internal_door,0,0,screed]
                    , "WORKSHOP":[inside_brick_wall,0,0,0,0,0,0,0,0,epoxy_painting_floor,0,0,0,0,int_plaster,ceiling_plaster,0,int_paint,0,ceiling_paint,0,0,0,0,0,0,0,0,aliminum_door,0,screed]
                    ,"BATTERY_ROOM":[inside_brick_wall,0,0,0,0,0,0,0,0,0,0,acid_tile,0,0,int_plaster,ceiling_plaster,0,int_paint,acid_resistant_int_paint,ceiling_paint,0,0,0,0,0,0,0,0,aliminum_door,0,screed]
                    ,"BEDROOM":[inside_brick_wall,0,0,acoustical_ceiling,0,0,0,0,0,0,0,0,0,laminated_parquet,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,wooden_internal_door,0,0,screed]
                    , "ENTRANCE":[inside_brick_wall,0,aliminum_suspended_ceiling,0,0,0,0,glazed_ceramic_tile,glazed_ceramic_skirting,0,0,0,0,0,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,0,0,aliminum_double_win_door,screed]
                    , "KITCHEN":[inside_brick_wall,0,aliminum_suspended_ceiling,0,0,0,non_slip_ceramic_tile,0,0,0,0,0,0,0,int_plaster,ceiling_plaster,ceramic_wall_tile,0,0,0,0,0,0,0,0,0,0,wooden_internal_door,0,0,screed]
                    , "WC":[inside_brick_wall,0,aliminum_suspended_ceiling,0,0,0,non_slip_ceramic_tile,0,0,0,0,0,0,0,int_plaster,ceiling_plaster,ceramic_wall_tile,0,0,0,0,0,0,0,0,0,compacted_laminate_door,wooden_internal_door,0,0,screed]
                    ,"HALL":[inside_brick_wall,0,0,0,0,rockwool_suspended_ceiling,0,glazed_ceramic_tile,glazed_ceramic_skirting,0,0,0,0,0,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,0,0,0,screed]
                    , "CANTEEN":[inside_brick_wall,0,0,0,0,rockwool_suspended_ceiling,0,0,0,epoxy_painting_floor,0,0,0,0,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,0,0,0,screed]
                    ,"MEETING ROOM":[inside_brick_wall,0,0,acoustical_ceiling,0,0,0,0,0,0,0,0,0,laminated_parquet,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,wooden_internal_door,0,0,screed]
                    ,"CONFERENCE ROOM":[inside_brick_wall,0,0,acoustical_ceiling,0,0,0,0,0,0,0,0,0,laminated_parquet,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,0,0,aliminum_double_win_door,screed]
                    ,"INDUCTION ROOM":[inside_brick_wall,0,0,0,0,rockwool_suspended_ceiling,0,glazed_ceramic_tile,glazed_ceramic_skirting,0,0,0,0,0,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,wooden_internal_door,0,0,screed]
                    ,"STAIRHALL":[inside_brick_wall,0,0,0,0,rockwool_suspended_ceiling,0,glazed_ceramic_tile,glazed_ceramic_skirting,0,0,0,0,0,int_plaster,ceiling_plaster,0,int_paint,0,0,0,0,0,0,0,0,0,0,0,aliminum_double_win_door,0]
                    }
        work_list = room_works.get(room_type)
        #print(work_list)
        return work_list

        # [inside_brick_wall,gypsum_part_wall,aliminum_suspended_ceiling,acoustical_ceiling,gypsum_suspended_ceiling,rockwool_suspended_ceiling,non_slip_ceramic_tile,glazed_ceramic_tile,glazed_ceramic_skirting,epoxy_painting_floor,resistant_floor,acid_tile,raised_floor,laminated_parquet,int_plaster,ceiling_plaster,ceramic_wall_tile,int_paint,acid_resistant_int_paint,ceiling_paint,epoxy_wall_paint]

if __name__ == '__main__':

    steel=steel_bldg()
    steel.width=13
    steel.length=13
    steel.structural_type="STEEL"
    steel.depth_exc=2.5
    exc_depth = self.basement_check()  # ok
    strfill_depth = 1  # ok
    foundation_depth = 0.51
    foundation_D1 = 2.5
    foundation_D2 = 3
    tie_beam_d1 = 1
    tie_beam_d2 = 0.55
    steel_pedestal_d1 = 0.7
    steel_pedestal_d2 = 0.65
    steel_pedestal_depth = 1.3
    steel_pedestal_rangex = 6
    steel_pedestal_rangey = 3
    rc_column_width = 0.6
    rc_column_length = 0.6
    rc_column_rangex = 6
    rc_column_rangey = 6
    rc_beam_width = 0.4
    rc_beam_length = 0.6
    rc_secondary_beam_D1 = 0.6
    rc_secondary_beam_D2 = 0.4
    basement_wall_height = 3
    basement_wall_thickness = 0.25
    ground_wall_height = 1
    ground_wall_thickness = 0.15
    steel_weight = self.steel_check()
    grouting_depth = 0.07
    concrete_slab = 0.15
    ground_slab = 0.2
    paraphet_height = 0.7
    paraphet_thickness = 0.15

