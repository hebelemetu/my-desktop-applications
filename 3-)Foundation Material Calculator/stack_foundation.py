class Stack:
    def __init__(self):
        self.depth_exc = None
        self.depth_fill = None
        self.depth_found = None
        self.width = None
        self.length = None
        self.steel_weight = None
        self.grout_depth1 = None
        self.grout_depth2 = None
        self.p1_width = None
        self.p1_length = None
        self.p1_depth = None
        self.p1_qty = None
        self.p2_width = None
        self.p2_length = None
        self.p2_depth = None
        self.p2_qty = None

    def excavation(self):
        print("Calculating Excavation...")
        work_space = 2
        print(type(work_space))
        print(type(self.width))
        print(type(self.length))
        A1 = (self.width + work_space) * (self.length + work_space)
        A2 = (self.width + work_space + 2 * self.depth_exc) * (self.length + work_space + 2 * self.depth_exc)
        A3 = (self.width + work_space + self.depth_exc / 2) * (self.length + work_space + self.depth_exc / 2)
        exc = round((A1 + A2 + 4 * A3) * self.depth_exc / 6, 2)
        print(A1, A2, A3, exc, sep="\n")
        print("Excavation: ", exc)

        return exc

    def structuralfill(self):
        print("Calculating Strfill...")
        work_space = 2
        A1 = (self.width + work_space) * (self.length + work_space)
        A2 = (self.width + work_space + 2 * self.depth_fill) * (self.length + work_space + 2 * self.depth_fill)
        A3 = (self.width + work_space + self.depth_fill / 2) * (self.length + work_space + self.depth_fill / 2)
        depth = self.depth_fill
        strfill = round((A1 + A2 + 4 * A3) * depth / 6, 2)
        print(A1,A2,A3,strfill,sep="\n")
        print("Strfill: ",strfill)

        return strfill

    def concreteFoundation(self):
        found_concrete = round(self.width * self.length * self.depth_found, 2)
        p1_concrete = (self.p1_width * self.p1_length) * self.p1_depth * self.p1_qty
        p2_concrete = (self.p2_width * self.p2_length) * self.p2_depth * self.p2_qty

        self.found_concrete = found_concrete + p1_concrete + p2_concrete

        return self.found_concrete

    def lean_concrete(self):
        self.lc_area = (self.width + 0.4) * (self.length + 0.4)

        return self.lc_area

    def formwork(self):
        formwork_foundation = 2 * (self.width + self.length) * self.depth_found
        formwork_p1 = 2 * (self.p1_width + self.p1_length) * self.p1_depth * self.p1_qty
        formwork_p2 = 2 * (self.p2_width + self.p2_length) * self.p2_depth * self.p2_qty

        formwork = formwork_foundation + formwork_p1 + formwork_p2

        return formwork

    def rebar(self):
        rebar_foundation = self.found_concrete * 0.1

        return rebar_foundation

    def pe_sheet(self):
        pe_sheet = (self.width * self.length)

        return pe_sheet

    def insulationSika(self):
        insulation_height = self.depth_exc - self.depth_found - self.depth_fill - 0.1 - 0.05
        insulation_foundation = 2 * (self.width + self.length) * self.depth_found + (self.width * self.length)

        return insulation_foundation

    def grout(self):
        grout_p1 = self.p1_width * self.p1_length * self.grout_depth1 * self.p1_qty
        grout_p2 = self.p2_width * self.p2_length * self.grout_depth2 * self.p2_qty
        grout = grout_p1 + grout_p2

        return grout

    def screed(self):
        return 0

    def embeddedPlate(self):
        return 0

    def anchor24(self):
        return 0

    def anchor30(self):
        return 0

    def anchor36(self):
        return 0

    def anchor42(self):
        return 0

    def structuralSteel(self):
        return 0


    def backfill(self):
        excavation = self.excavation()
        fill = self.structuralfill()
        foundation_underground = self.depth_exc - self.depth_found - self.depth_fill - 0.1 - 0.05
        foundation = self.concreteFoundation() / self.depth_found * foundation_underground
        lean_concrete = self.lean_concrete()
        isolation_under_foundation = lean_concrete / 2
        bf = excavation - fill - foundation - lean_concrete - isolation_under_foundation

        return bf

    def waterStopper(self):
        ws = 2 * (self.width + self.length)
        return ws

    def jointIsolation(self):
        joint = 2 * (self.width + self.length)
        return joint




