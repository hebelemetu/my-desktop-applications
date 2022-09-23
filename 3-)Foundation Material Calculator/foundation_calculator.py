import math
class Singlefooting:
    def __init__(self,width,length,pedestal_length,pedestal_width,foundation_depth,pedestal_height,fill,anchor_type,anchor_qty,es,steel,exc_depth,grout_depth):
        self.width = width
        self.length = length
        self.pedestal_length = pedestal_length
        self.pedestal_width = pedestal_width
        self.foundation_depth = foundation_depth
        self.pedestal_height = pedestal_height
        self.exc_depth = exc_depth
        self.fill = fill
        self.height_above_ground = pedestal_height - (exc_depth - 0.1 - foundation_depth - 0.03 - fill)
        self.pedestal = 1
        self.es = es
        self.steel = steel
        self.grout_depth = grout_depth
        self.anchor_type = anchor_type
        self.anchor_qty = anchor_qty


    def excavation(self):
        self.depth_exc = (self.pedestal_height - self.height_above_ground + self.foundation_depth + 0.1 + self.fill)
        work_space = 1
        A1 = (self.width + 2 * work_space) * (self.length + 2 * work_space)
        A2 = (self.width + 2 * work_space + 2 * self.depth_exc) * (self.length + 2 * work_space + 2 * self.depth_exc)
        A3 = (self.width + 2 * work_space + self.depth_exc) * (self.length + 2 * work_space + self.depth_exc)
        exc = round((A1 + A2 + 4 * A3) * self.depth_exc / 6, 2)
        print(A1,A2,A3,exc,sep="\n")
        print("Excavation: ",exc)
        return exc

    def strfill(self):
        work_space = 1
        A1 = (self.width + 2 * work_space) * (self.length + 2 * work_space)
        A2 = (self.width + 2 * work_space + 2 * self.fill) * (self.length + 2 * work_space + 2 * self.fill)
        A3 = (self.width + 2 * work_space + self.fill) * (self.length + 2 * work_space + self.fill)
        depth = self.fill
        strfill = round((A1 + A2 + 4 * A3) * depth / 6, 2)
        print(A1,A2,A3,strfill,sep="\n")
        print("Strfill: ",strfill)
        return strfill

    def leanconc(self):
        return round((self.width + 0.5) * (self.length + 0.5) * 0.1, 2)  # checked

    def backfill(self):
        Exc = self.excavation()
        Fill = self.strfill()
        Lc = self.leanconc()
        return round(Exc - Fill - Lc - self.pedestal * self.pedestal_length * self.pedestal_width * (self.pedestal_height - self.height_above_ground) - self.width * self.length * self.foundation_depth,2)  # checked

    def formwork(self):
        return round(2 * (self.width + self.length) * self.foundation_depth + self.pedestal * 2 * (self.pedestal_length + self.pedestal_width) * self.pedestal_height + self.pedestal * 2 * (self.pedestal_length + self.pedestal_width) * 0.2, 2)  # checked

    def strconcrete(self):
        return round(self.width * self.length * self.foundation_depth + self.pedestal * self.pedestal_length * self.pedestal_width * self.pedestal_height, 2)  # checked

    def rebar(self):
        return round((self.width * self.length * self.foundation_depth + self.pedestal * self.pedestal_length * self.pedestal_width * self.pedestal_height) * 0.12, 2)  # checked

    def anchor(self):
        anchors  = {"M24":0,
                    "M30":0,
                    "M36":0,
                    "M42":0}
        anchors[f"{self.anchor_type}"] = self.anchor_qty
        return anchors #list(anchor().items[0] = anchor_type

    def embeddedsteel(self):
        return round(self.pedestal * self.es, 2)  # checked

    def concreteprot(self):
        return round(self.width * self.length + (self.width * self.length - self.pedestal * self.pedestal_length * self.pedestal_width) + (2 * (self.pedestal_length + self.pedestal_width) * (self.pedestal_height - self.height_above_ground) * self.pedestal) + 2 * (self.width + self.length) * self.foundation_depth, 2)  # checked

    def grout(self):
        return round(self.pedestal_length * self.pedestal_width * self.pedestal * self.grout_depth, 3)  # checked

    def polyethylenesheet(self):
        return round(self.width * self.length * 2,2)

    def waterStopper(self):
        ws = 2 * (self.width + self.length)
        return ws

    def jointIsolation(self):
        joint = 2 * (self.width + self.length)
        return joint

class Combinedfooting:
    def __init__(self,width,length,pedestal_length,pedestal_width,foundation_depth,pedestal_height,fill,anchor_type,anchor_qty,pedestal,es,steel,exc_depth,grout_depth):
        self.width = width
        self.length = length
        self.pedestal_length = pedestal_length
        self.pedestal_width = pedestal_width
        self.foundation_depth = foundation_depth
        self.pedestal_height = pedestal_height
        self.exc_depth = exc_depth
        self.fill = fill
        self.height_above_ground = pedestal_height - (exc_depth - 0.1 - foundation_depth - 0.03 - fill)
        self.pedestal = pedestal
        self.es = es
        self.steel = steel
        self.grout_depth = grout_depth
        self.anchor_qty = anchor_qty
        self.anchor_type = anchor_type

    def excavation(self):
        self.depth_exc = (self.pedestal_height - self.height_above_ground + self.foundation_depth + 0.1 + self.fill)
        work_space = 1
        A1 = (self.width + 2 * work_space) * (self.length + 2 * work_space)
        A2 = (self.width + 2 * work_space + 2 * self.depth_exc) * (self.length + 2 * work_space + 2 * self.depth_exc)
        A3 = (self.width + 2 * work_space + self.depth_exc) * (self.length + 2 * work_space + self.depth_exc)
        exc = round((A1 + A2 + 4 * A3) * self.depth_exc / 6, 2)
        print(A1,A2,A3,exc,sep="\n")
        print("Excavation: ",exc)
        return exc

    def strfill(self):
        work_space = 1
        A1 = (self.width + 2 * work_space) * (self.length + 2 * work_space)
        A2 = (self.width + 2 * work_space + 2 * self.fill) * (self.length + 2 * work_space + 2 * self.fill)
        A3 = (self.width + 2 * work_space + self.fill) * (self.length + 2 * work_space + self.fill)
        depth = self.fill
        strfill = round((A1 + A2 + 4 * A3) * depth / 6, 2)
        print(A1,A2,A3,strfill,sep="\n")
        print("Strfill: ",strfill)
        return strfill

    def leanconc(self):
        return round((self.width + 0.5) * (self.length + 0.5) * 0.1, 2)  # checked

    def backfill(self):
        Exc = self.excavation()
        Fill = self.strfill()
        Lc = self.leanconc()
        return round(Exc - Fill - Lc - self.pedestal * self.pedestal_length * self.pedestal_width * (self.pedestal_height - self.height_above_ground) - self.width * self.length * self.foundation_depth,2)  # checked

    def formwork(self):
        return round(2 * (self.width + self.length) * self.foundation_depth + self.pedestal * 2 * (self.pedestal_length + self.pedestal_width) * self.pedestal_height + self.pedestal * 2 * (self.pedestal_length + self.pedestal_width) * 0.2, 2)  # checked

    def strconcrete(self):
        return round(self.width * self.length * self.foundation_depth + self.pedestal * self.pedestal_length * self.pedestal_width * self.pedestal_height, 2)  # checked

    def rebar(self):
        return round((self.width * self.length * self.foundation_depth + self.pedestal * self.pedestal_length * self.pedestal_width * self.pedestal_height) * 0.12, 2)  # checked

    def anchor(self):
        anchors  = {"M24":0,
                    "M30":0,
                    "M36":0,
                    "M42":0}
        anchors[f"{self.anchor_type}"] = self.anchor_qty
        return anchors #list(anchor().items[0] = anchor_type

    def embeddedsteel(self):
        return round(self.pedestal * self.es, 2)  # checked

    def concreteprot(self):
        return round(self.width * self.length + (self.width * self.length - self.pedestal * self.pedestal_length * self.pedestal_width) + (2 * (self.pedestal_length + self.pedestal_width) * (self.pedestal_height - self.height_above_ground) * self.pedestal) + 2 * (self.width + self.length) * self.foundation_depth, 2)  # checked

    def grout(self):
        return round(self.pedestal_length * self.pedestal_width * self.pedestal * self.grout_depth, 3)  # checked

    def polyethylenesheet(self):
        return round(self.width * self.length * 2,2)

    def waterStopper(self):
        ws = 2 * (self.width + self.length)
        return ws

    def jointIsolation(self):
        joint = 2 * (self.width + self.length)
        return joint

class CylinderTank:
    def __init__(self,D1,D2,dim_a,dim_b,dim_c,dim_d,dim_e,exc_depth,fill,tank_height,anchor_type,anchor_qty,grout_depth,is_chemical):
        self.D1 = D1
        self.D2 = D2
        self.a = dim_a
        self.b = dim_b
        self.c = dim_c
        self.d = dim_d
        self.e = dim_e
        self.depth_exc = exc_depth
        self.tank_height = tank_height
        self.height_above_ground = dim_c - (exc_depth - 0.1 - dim_d - 0.03 - fill)
        self.fill = fill
        self.anchor_qty = anchor_qty
        self.anchor_type = anchor_type
        self.grout_depth = grout_depth
        self.pi = 3.14159265359

    def excavation(self):
        # V = 1/3 × πh(R2 + Rr + r2)
        work_space = 1
        R1 = (self.D1 / 2 + work_space + self.depth_exc)
        R2 = (self.D1 / 2 + work_space)
        exc = round(1/3 * self.pi * self.depth_exc * (R1**2 + R1*R2 + R2**2), 2)
        print("Excavation: ",exc)
        return exc

    def strfill(self):
        work_space = 1
        R1 = (self.D1 / 2 + work_space + self.fill)
        R2 = (self.D1 / 2 + work_space)
        strfill = round(1/3 * self.pi * self.fill * (R1**2 + R1*R2 + R2**2), 2)
        print("Strfill: ",strfill)
        return strfill

    def leanconc(self):
        inner_radius = (self.D2  / 2)
        outer_radius = (self.D1 / 2)
        all_area = self.pi * outer_radius**2
        inner_area = self.pi * inner_radius**2
        lc = (all_area - inner_area) * 0.1
        return round(lc, 2)

    def backfill(self):
        Exc = self.excavation()
        Fill = self.strfill()
        Lc = self.leanconc()
        inner_radius = (self.D2  / 2)
        outer_radius = (self.D1 / 2)
        all_area = self.pi * outer_radius**2
        inner_area = self.pi * inner_radius**2
        pedestal_top_area = self.pi * ((self.D2 / 2 + self.e + self.a))**2 - (self.pi * ((self.D2 / 2 + self.e))**2)
        concrete_under_ground = (all_area - inner_area) * self.d + (self.c - self.height_above_ground - self.d) * pedestal_top_area
        return round(Exc - Fill - Lc - concrete_under_ground,2)

    def formwork(self):
        inner_side_bottom = self.pi * self.d * self.D2
        outer_side_bottom = self.pi * self.d * self.D1
        inner_side_pedestal = self.pi * (self.c - self.d) * (self.D2 + 2 * (self.e + self.a))
        outer_side_pedestal = self.pi * (self.c - self.d) * (self.D1 - 2 * self.b)
        formwork = inner_side_bottom + outer_side_bottom + inner_side_pedestal + outer_side_pedestal
        return round(formwork, 2)

    def strconcrete(self):
        inner_radius = (self.D2  / 2)
        outer_radius = (self.D1 / 2)
        all_area = self.pi * outer_radius**2
        inner_area = self.pi * inner_radius**2
        pedestal_top_area = self.pi * ((self.D2 / 2 + self.e + self.a))**2 - (self.pi * ((self.D2 / 2 + self.e))**2)
        concrete = (all_area - inner_area) * self.d + (self.c - self.d) * pedestal_top_area
        return round(concrete, 2)

    def rebar(self):
        inner_radius = (self.D2  / 2)
        outer_radius = (self.D1 / 2)
        all_area = self.pi * outer_radius**2
        inner_area = self.pi * inner_radius**2
        pedestal_top_area = self.pi * ((self.D2 / 2 + self.e + self.a))**2 - (self.pi * ((self.D2 / 2 + self.e))**2)
        concrete = (all_area - inner_area) * self.d + (self.c - self.d) * pedestal_top_area
        return round(concrete * 0.12, 2)

    def anchor(self):
        anchors  = {"M24":0,
                    "M30":0,
                    "M36":0,
                    "M42":0}
        anchors[f"{self.anchor_type}"] = self.anchor_qty
        return anchors #list(anchor().items[0] = anchor_type

    def embeddedsteel(self):
        return 0  # checked

    def concreteprot(self):
        inner_side_bottom = self.pi * self.d * self.D2
        outer_side_bottom = self.pi * self.d * self.D1
        inner_side_pedestal_underground = self.pi * (self.c - self.height_above_ground - self.d) * (self.D2 + 2 * (self.e + self.a))
        outer_side_pedestal_underground = self.pi * (self.c - self.height_above_ground - self.d) * (self.D1 - 2 * self.b)

        inner_radius = (self.D2  / 2)
        outer_radius = (self.D1 / 2)
        all_area = self.pi * outer_radius**2
        inner_area = self.pi * inner_radius**2
        foundation_bottom = (all_area - inner_area)

        insulation = inner_side_bottom + outer_side_bottom + inner_side_pedestal_underground + outer_side_pedestal_underground + foundation_bottom
        return round(insulation, 2)

    def grout(self):
        pedestal_top_area = self.pi * ((self.D2 / 2 + self.e + self.a))**2 - (self.pi * ((self.D2 / 2 + self.e))**2)
        return round(pedestal_top_area * self.grout_depth, 3)  # checked

    def polyethylenesheet(self):
        inner_radius = (self.D2  / 2)
        outer_radius = (self.D1 / 2)
        all_area = self.pi * outer_radius**2
        inner_area = self.pi * inner_radius**2
        foundation_bottom = (all_area - inner_area)

        return round(foundation_bottom * 2,2)

    def waterStopper(self):
        inner_side_bottom = self.pi * self.d * self.D2
        outer_side_bottom = self.pi * self.d * self.D1
        ws = inner_side_bottom + outer_side_bottom
        return ws

    def jointIsolation(self):
        inner_side_bottom = self.pi * self.d * self.D2
        outer_side_bottom = self.pi * self.d * self.D1
        joint = (inner_side_bottom + outer_side_bottom) / 2
        return joint

class OctTank:
    def __init__(self,D1,D2,dim_a,dim_b,exc_depth,fill,tank_height,anchor_type,anchor_qty,grout_depth,is_chemical):
        self.D1 = D1
        self.D2 = D2
        self.a = dim_a
        self.b = dim_b
        self.depth_exc = exc_depth
        self.tank_height = tank_height
        self.height_above_ground = self.D1 + self.D2 - (exc_depth - 0.1 - 0.03 - fill)
        self.fill = fill
        self.anchor_qty = anchor_qty
        self.anchor_type = anchor_type
        self.grout_depth = grout_depth
        self.pi = 3.14159265359

    def excavation(self):
        #A = 2a2(1+√2)
        #Volume = h/6 x (ABASE + 4 x AMID + ATOP)
        def octagon_excavation(a,depth,work_space):
            a_new = a + 2 * (work_space / math.tan(68))
            exc = 2 * a_new**2 * (1 + math.sqrt(2)) * depth
            return  exc
        work_space = 1
        exc = octagon_excavation(self.a, self.depth_exc, work_space)
        print("Excavation: ",exc)
        return exc

    def strfill(self):
        def octagon_fill(a,depth,work_space):
            a_new = a + 2 * (work_space / math.tan(68))
            fill = 2 * a_new**2 * (1 + math.sqrt(2)) * depth
            return  fill
        work_space = 1
        strfill = octagon_fill(self.a, self.fill, work_space)
        print("Strfill: ",strfill)
        #return strfill
        return strfill

    def leanconc(self):
        a_new = self.a + 2 * (0.5 / math.tan(68))
        bsae_area = 2 * a_new**2 * (1 + math.sqrt(2))
        return bsae_area

    def backfill(self):
        Exc = self.excavation()
        Fill = self.strfill()
        Lc = self.leanconc()
        base_concrete = 2 * self.a**2 * (1 + math.sqrt(2)) * self.D1
        pedestal_concrete = 2 * self.b**2 * (1 + math.sqrt(2)) * (self.D2 - self.height_above_ground)
        concrete_under_ground = base_concrete + pedestal_concrete
        return round(Exc - Fill - Lc - concrete_under_ground,2)

    def formwork(self):
        base = 8 * self.D1 * self.a
        pedestal = 8 * self.D2 * self.b
        formwork = base + pedestal
        return round(formwork,2)

    def strconcrete(self):
        base_concrete = 2 * self.a**2 * (1 + math.sqrt(2)) * self.D1
        pedestal_concrete = 2 * self.b**2 * (1 + math.sqrt(2)) * self.D2
        concrete = base_concrete + pedestal_concrete
        return round(concrete,2)

    def rebar(self):
        base_concrete = 2 * self.a**2 * (1 + math.sqrt(2)) * self.D1
        pedestal_concrete = 2 * self.b**2 * (1 + math.sqrt(2)) * self.D2
        concrete = base_concrete + pedestal_concrete
        return round(concrete * 0.12,2)

    def anchor(self):
        anchors  = {"M24":0,
                    "M30":0,
                    "M36":0,
                    "M42":0}
        anchors[f"{self.anchor_type}"] = self.anchor_qty
        #return anchors #list(anchor().items[0] = anchor_type
        return anchors

    def embeddedsteel(self):
        return 0

    def concreteprot(self):
        base = 8 * self.D1 * self.a
        bottom_base = 2 * self.a**2 * (1 + math.sqrt(2))
        pedestal = 8 * (self.D2 - self.height_above_ground) * self.b
        concreteprot = base + bottom_base + pedestal
        return round(concreteprot,2)

    def grout(self):
        top_pedestal = 2 * self.b**2 * (1 + math.sqrt(2))
        grout = top_pedestal * self.grout_depth
        return round(grout,2)

    def polyethylenesheet(self):
        ps = 2 * self.a**2 * (1 + math.sqrt(2))
        return round(ps * 2,2)

    def waterStopper(self):
        pedestal_underground = self.D2 - self.height_above_ground
        if pedestal_underground >0:
            perimeter = 8 * self.a + 8 * self.b
        else:
            perimeter = 8 * self.a
        return round(perimeter,2)

    def jointIsolation(self):
        pedestal_underground = self.D2 - self.height_above_ground
        if pedestal_underground >0:
            perimeter = 8 * self.a + 8 * self.b
        else:
            perimeter = 8 * self.a
        return round(perimeter,2)

class OctSqTank:
    def __init__(self,D1,D2,dim_a,dim_b,exc_depth,fill,tank_height,anchor_type,anchor_qty,grout_depth,is_chemical):
        self.D1 = D1
        self.D2 = D2
        self.a = dim_a
        self.b = dim_b
        self.depth_exc = exc_depth
        self.tank_height = tank_height
        self.height_above_ground = self.D1 + self.D2 - (exc_depth - 0.1 - 0.03 - fill)
        self.fill = fill
        self.anchor_qty = anchor_qty
        self.anchor_type = anchor_type
        self.grout_depth = grout_depth
        self.pi = 3.14159265359

    def excavation(self):
        work_space = 1
        exc = (self.a + work_space) * (self.a + work_space) * self.depth_exc
        print("Excavation: ", exc)
        return exc

    def strfill(self):
        work_space = 1
        strfill = (self.a + work_space) * (self.a + work_space) * self.fill
        print("Strfill: ", strfill)
        return strfill

    def leanconc(self):
        bsae_area = (self.a + 0.5) * (self.a + 0.5)
        return bsae_area

    def backfill(self):
        Exc = self.excavation()
        Fill = self.strfill()
        Lc = self.leanconc()
        base_concrete = self.a**2 * self.D1
        pedestal_concrete = 2 * self.b ** 2 * (1 + math.sqrt(2)) * (self.D2 - self.height_above_ground)
        concrete_under_ground = base_concrete + pedestal_concrete
        return round(Exc - Fill - Lc - concrete_under_ground, 2)

    def formwork(self):
        base = 4 * self.D1 * self.a
        pedestal = 8 * self.D2 * self.b
        formwork = base + pedestal
        return round(formwork, 2)

    def strconcrete(self):
        base_concrete = self.a**2 * self.D1
        pedestal_concrete = 2 * self.b ** 2 * (1 + math.sqrt(2)) * self.D2
        concrete = base_concrete + pedestal_concrete
        return round(concrete, 2)

    def rebar(self):
        base_concrete = self.a**2 * self.D1
        pedestal_concrete = 2 * self.b ** 2 * (1 + math.sqrt(2)) * self.D2
        concrete = base_concrete + pedestal_concrete
        return round(concrete * 0.12, 2)

    def anchor(self):
        anchors = {"M24": 0,
                   "M30": 0,
                   "M36": 0,
                   "M42": 0}
        anchors[f"{self.anchor_type}"] = self.anchor_qty
        # return anchors #list(anchor().items[0] = anchor_type
        return anchors

    def embeddedsteel(self):
        return 0

    def concreteprot(self):
        base = 4 * self.D1 * self.a
        bottom_base = self.a**2
        pedestal = 8 * (self.D2 - self.height_above_ground) * self.b
        concreteprot = base + bottom_base + pedestal
        return round(concreteprot, 2)

    def grout(self):
        top_pedestal = 2 * self.b ** 2 * (1 + math.sqrt(2))
        grout = top_pedestal * self.grout_depth
        return round(grout, 2)

    def polyethylenesheet(self):
        ps = self.a**2
        return round(ps * 2, 2)

    def waterStopper(self):
        pedestal_underground = self.D2 - self.height_above_ground
        if pedestal_underground > 0:
            perimeter = 4 * self.a + 8 * self.b
        else:
            perimeter = 4 * self.a
        return round(perimeter, 2)

    def jointIsolation(self):
        pedestal_underground = self.D2 - self.height_above_ground
        if pedestal_underground > 0:
            perimeter = 4 * self.a + 8 * self.b
        else:
            perimeter = 4 * self.a
        return round(perimeter, 2)

class HexTank:
    def __init__(self,D1,D2,dim_a,dim_b,exc_depth,fill,tank_height,anchor_type,anchor_qty,grout_depth,is_chemical):
        self.D1 = D1
        self.D2 = D2
        self.a = dim_a
        self.b = dim_b
        self.depth_exc = exc_depth
        self.tank_height = tank_height
        self.height_above_ground = self.D1 + self.D2 - (exc_depth - 0.1 - 0.03 - fill)
        self.fill = fill
        self.anchor_qty = anchor_qty
        self.anchor_type = anchor_type
        self.grout_depth = grout_depth
        self.pi = 3.14159265359

    def excavation(self):
        def hexagon_excavation(a, depth, work_space):
            a_new = a + 2 * (work_space / math.tan(60))
            exc = (3 * math.sqrt(3) * a_new**2 / 2) * depth
            return exc

        work_space = 1
        exc = hexagon_excavation(self.a, self.depth_exc, work_space)
        print("Excavation: ", exc)
        return exc

    def strfill(self):
        def hexagon_fill(a, depth, work_space):
            a_new = a + 2 * (work_space / math.tan(60))
            fill = (3 * math.sqrt(3) * a_new**2 / 2) * depth
            return fill
        work_space = 1
        strfill = hexagon_fill(self.a, self.fill, work_space)
        print("Strfill: ", strfill)
        # return strfill
        return strfill

    def leanconc(self):
        a_new = self.a + 2 * (0.5 / math.tan(60))
        bsae_area = (3 * math.sqrt(3) * a_new**2 / 2)
        return bsae_area

    def backfill(self):
        Exc = self.excavation()
        Fill = self.strfill()
        Lc = self.leanconc()
        base_concrete = (3 * math.sqrt(3) * self.a**2 / 2) * self.D1
        pedestal_concrete = (3 * math.sqrt(3) * self.b**2 / 2) * (self.D2 - self.height_above_ground)
        concrete_under_ground = base_concrete + pedestal_concrete
        return round(Exc - Fill - Lc - concrete_under_ground, 2)

    def formwork(self):
        base = 6 * self.D1 * self.a
        pedestal = 6 * self.D2 * self.b
        formwork = base + pedestal
        return round(formwork, 2)

    def strconcrete(self):
        base_concrete = (3 * math.sqrt(3) * self.a**2 / 2) * self.D1
        pedestal_concrete = (3 * math.sqrt(3) * self.b**2 / 2) * self.D2
        concrete = base_concrete + pedestal_concrete
        return round(concrete, 2)

    def rebar(self):
        base_concrete = (3 * math.sqrt(3) * self.a**2 / 2) * self.D1
        pedestal_concrete = (3 * math.sqrt(3) * self.b**2 / 2) * self.D2
        concrete = base_concrete + pedestal_concrete
        return round(concrete * 0.12, 2)

    def anchor(self):
        anchors = {"M24": 0,
                   "M30": 0,
                   "M36": 0,
                   "M42": 0}
        anchors[f"{self.anchor_type}"] = self.anchor_qty
        # return anchors #list(anchor().items[0] = anchor_type
        return anchors

    def embeddedsteel(self):
        return 0

    def concreteprot(self):
        base = 6 * self.D1 * self.a
        bottom_base = (3 * math.sqrt(3) * self.a**2 / 2)
        pedestal = 6 * (self.D2 - self.height_above_ground) * self.b
        concreteprot = base + bottom_base + pedestal
        return round(concreteprot, 2)

    def grout(self):
        top_pedestal = (3 * math.sqrt(3) * self.b**2 / 2)
        grout = top_pedestal * self.grout_depth
        return round(grout, 2)

    def polyethylenesheet(self):
        ps = (3 * math.sqrt(3) * self.a**2 / 2)
        return round(ps * 2, 2)

    def waterStopper(self):
        pedestal_underground = self.D2 - self.height_above_ground
        if pedestal_underground > 0:
            perimeter = 6 * self.a + 6 * self.b
        else:
            perimeter = 6 * self.a
        return round(perimeter, 2)

    def jointIsolation(self):
        pedestal_underground = self.D2 - self.height_above_ground
        if pedestal_underground > 0:
            perimeter = 6 * self.a + 6 * self.b
        else:
            perimeter = 6 * self.a
        return round(perimeter, 2)

class HexSqTank:
    def __init__(self,D1,D2,dim_a,dim_b,exc_depth,fill,tank_height,anchor_type,anchor_qty,grout_depth,is_chemical):
        self.D1 = D1
        self.D2 = D2
        self.a = dim_a
        self.b = dim_b
        self.depth_exc = exc_depth
        self.tank_height = tank_height
        self.height_above_ground = self.D1 + self.D2 - (exc_depth - 0.1 - 0.03 - fill)
        self.fill = fill
        self.anchor_qty = anchor_qty
        self.anchor_type = anchor_type
        self.grout_depth = grout_depth
        self.pi = 3.14159265359

    def excavation(self):
        work_space = 1
        exc = (self.a + work_space) * (self.a + work_space) * self.depth_exc
        print("Excavation: ", exc)
        return exc

    def strfill(self):
        work_space = 1
        strfill = (self.a + work_space) * (self.a + work_space) * self.fill
        print("Strfill: ", strfill)
        return strfill

    def leanconc(self):
        bsae_area = (self.a + 0.5) * (self.a + 0.5)
        return bsae_area

    def backfill(self):
        Exc = self.excavation()
        Fill = self.strfill()
        Lc = self.leanconc()
        base_concrete = (self.a**2) * self.D1
        pedestal_concrete = (3 * math.sqrt(3) * self.b ** 2 / 2) * (self.D2 - self.height_above_ground)
        concrete_under_ground = base_concrete + pedestal_concrete
        return round(Exc - Fill - Lc - concrete_under_ground, 2)

    def formwork(self):
        base = 4 * self.D1 * self.a
        pedestal = 6 * self.D2 * self.b
        formwork = base + pedestal
        return round(formwork, 2)

    def strconcrete(self):
        base_concrete = (self.a**2) * self.D1
        pedestal_concrete = (3 * math.sqrt(3) * self.b ** 2 / 2) * self.D2
        concrete = base_concrete + pedestal_concrete
        return round(concrete, 2)

    def rebar(self):
        base_concrete = (self.a**2) * self.D1
        pedestal_concrete = (3 * math.sqrt(3) * self.b ** 2 / 2) * self.D2
        concrete = base_concrete + pedestal_concrete
        return round(concrete * 0.12, 2)

    def anchor(self):
        anchors = {"M24": 0,
                   "M30": 0,
                   "M36": 0,
                   "M42": 0}
        anchors[f"{self.anchor_type}"] = self.anchor_qty
        # return anchors #list(anchor().items[0] = anchor_type
        return anchors

    def embeddedsteel(self):
        return 0

    def concreteprot(self):
        base = self.D1 * self.a**2
        bottom_base = self.a**2
        pedestal = 6 * (self.D2 - self.height_above_ground) * self.b
        concreteprot = base + bottom_base + pedestal
        return round(concreteprot, 2)

    def grout(self):
        top_pedestal = (3 * math.sqrt(3) * self.b ** 2 / 2)
        grout = top_pedestal * self.grout_depth
        return round(grout, 2)

    def polyethylenesheet(self):
        ps = self.a**2
        return round(ps * 2, 2)

    def waterStopper(self):
        pedestal_underground = self.D2 - self.height_above_ground
        if pedestal_underground > 0:
            perimeter = 4 * self.a + 6 * self.b
        else:
            perimeter = 4 * self.a
        return round(perimeter, 2)

    def jointIsolation(self):
        pedestal_underground = self.D2 - self.height_above_ground
        if pedestal_underground > 0:
            perimeter = 4 * self.a + 6 * self.b
        else:
            perimeter = 4 * self.a
        return round(perimeter, 2)

class DykeWall:
    def __init__(self,dw_thickness,dw_height,dw_perimeter_width,dw_perimeter_length,dw_foundation_depth,dw_foundation_width,dw_exc_depth,dw_strfill):
        self.dw_perimeter_width = dw_perimeter_width
        self.length = 2 * (dw_perimeter_length + dw_perimeter_width)
        self.pedestal_length = 2 * (dw_perimeter_length + dw_perimeter_width)
        self.pedestal_width = dw_thickness
        self.foundation_depth = dw_foundation_depth
        self.foundation_width = dw_foundation_width
        self.pedestal_height = dw_height
        self.exc_depth = dw_exc_depth
        self.fill = dw_strfill
        self.height_above_ground = dw_height - (dw_exc_depth - 0.1 - dw_foundation_depth - 0.03 - dw_strfill)
        self.pedestal = 1
        self.dw_perimeter_length = dw_perimeter_length

    def excavation(self):
        self.depth_exc = (self.pedestal_height - self.height_above_ground + self.foundation_depth + 0.1 + self.fill)
        work_space = 1
        exc_length = 2 * (self.dw_perimeter_length + 2 * work_space + self.dw_perimeter_width + 2 * work_space)
        exc_length2 = 2 * (self.dw_perimeter_length + 2 * work_space + 2 * self.depth_exc + self.dw_perimeter_width + 2 * work_space + 2 * self.depth_exc)
        exc_length3 = 2 * (self.dw_perimeter_length + 2 * work_space + self.depth_exc + self.dw_perimeter_width + 2 * work_space + self.depth_exc)
        A1 = (self.foundation_width + 2 * work_space) * exc_length
        A2 = (self.foundation_width + 2 * work_space + 2 * self.depth_exc) * exc_length2
        A3 = (self.foundation_width + 2 * work_space + self.depth_exc) * exc_length3
        exc = round((A1 + A2 + 4 * A3) * self.depth_exc / 6, 2)
        print(A1,A2,A3,exc,sep="\n")
        print("Excavation: ",exc)
        return exc

    def strfill(self):
        work_space = 1
        fill_length = 2 * (self.dw_perimeter_length + 2 * work_space + self.dw_perimeter_width + 2 * work_space)
        fill_length2 = 2 * (self.dw_perimeter_length + 2 * work_space + 2 * self.depth_exc + self.dw_perimeter_width + 2 * work_space + 2 * self.depth_exc)
        fill_length3 = 2 * (self.dw_perimeter_length + 2 * work_space + self.depth_exc + self.dw_perimeter_width + 2 * work_space + self.depth_exc)
        A1 = (self.foundation_width + 2 * work_space) * fill_length
        A2 = (self.foundation_width + 2 * work_space + 2 * self.fill) * fill_length2
        A3 = (self.foundation_width + 2 * work_space + self.fill) * fill_length3
        depth = self.fill
        strfill = round((A1 + A2 + 4 * A3) * depth / 6, 2)
        print(A1,A2,A3,strfill,sep="\n")
        print("Strfill: ",strfill)
        return strfill

    def leanconc(self):
        return round((self.foundation_width + 0.5) * (self.length) * 0.1, 2)

    def backfill(self):
        Exc = self.excavation()
        Fill = self.strfill()
        Lc = self.leanconc()
        return round(Exc - Fill - Lc - self.pedestal_length * self.pedestal_width * (self.pedestal_height - self.height_above_ground) - self.foundation_width * self.length * self.foundation_depth,2)

    def formwork(self):
        foundation_outer_side = 2 * (self.dw_perimeter_width + self.foundation_width / 2 + self.dw_perimeter_length + self.foundation_width / 2) * self.foundation_depth
        foundation_inner_side = 2 * (self.dw_perimeter_width - self.foundation_width / 2 + self.dw_perimeter_length - self.foundation_width / 2) * self.foundation_depth
        pedestal_underground_outer_side = 2 * (self.dw_perimeter_width + self.foundation_width / 2 + self.dw_perimeter_length + self.foundation_width / 2) * self.pedestal_length
        pedestal_underground_inner_side = 2 * (self.dw_perimeter_width - self.foundation_width / 2 + self.dw_perimeter_length - self.foundation_width / 2) * self.pedestal_length
        formwork = foundation_inner_side + foundation_outer_side + pedestal_underground_outer_side + pedestal_underground_inner_side
        return round(formwork, 2)

    def strconcrete(self):
        return round(self.length * self.foundation_depth * self.foundation_width + self.pedestal_length * self.pedestal_width * self.pedestal_height, 2)  # checked

    def rebar(self):
        concrete = self.length * self.foundation_depth * self.foundation_width + self.pedestal_length * self.pedestal_width * self.pedestal_height
        return round(concrete * 0.12, 2)

    def anchor(self):
        return 0

    def embeddedsteel(self):
        return 0

    def concreteprot(self):
        foundation_outer_side = 2 * (self.dw_perimeter_width + self.foundation_width / 2 + self.dw_perimeter_length + self.foundation_width / 2) * self.foundation_depth
        foundation_inner_side = 2 * (self.dw_perimeter_width - self.foundation_width / 2 + self.dw_perimeter_length - self.foundation_width / 2) * self.foundation_depth
        pedestal_underground_outer_side = 2 * (self.dw_perimeter_width + self.foundation_width / 2 + self.dw_perimeter_length + self.foundation_width / 2) * (self.pedestal_length - self.height_above_ground)
        pedestal_underground_inner_side = 2 * (self.dw_perimeter_width - self.foundation_width / 2 + self.dw_perimeter_length - self.foundation_width / 2) * (self.pedestal_length - self.height_above_ground)
        foundation_base = self.length * self.foundation_width
        foundation_top = self.length * self.foundation_width - self.pedestal_length * self.pedestal_width
        concrete_protection = foundation_outer_side + foundation_inner_side + pedestal_underground_outer_side + pedestal_underground_inner_side + foundation_base + foundation_top
        return round(concrete_protection, 2)

    def grout(self):
        return 0

    def polyethylenesheet(self):
        return round(self.length * self.foundation_width * 2,2)

    def waterStopper(self):
        foundation_outer_side = 2 * (self.dw_perimeter_width + self.foundation_width / 2 + self.dw_perimeter_length + self.foundation_width / 2) * self.foundation_depth
        foundation_inner_side = 2 * (self.dw_perimeter_width - self.foundation_width / 2 + self.dw_perimeter_length - self.foundation_width / 2) * self.foundation_depth
        ws = foundation_outer_side + foundation_inner_side
        return round(ws,2)

    def jointIsolation(self):
        joint = self.length
        return round(joint,2)

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

    def waterStopper(self):
        ws = 2 * (self.width + self.length)
        return ws

    def jointIsolation(self):
        joint = 2 * (self.width + self.length)
        return joint

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

class Matfoundation:
    def __init__(self,width,length,foundation_depth,fill,anchor_type,anchor_qty,es,steel,exc_depth,grout_depth):
        self.width = width
        self.length = length
        self.foundation_depth = foundation_depth
        self.exc_depth = exc_depth
        self.fill = fill
        self.height_above_ground = foundation_depth - (exc_depth - 0.1 - 0.03 - fill)
        self.es = es
        self.steel = steel
        self.grout_depth = grout_depth
        self.anchor_type = anchor_type
        self.anchor_qty = anchor_qty

    def excavation(self):
        self.depth_exc = self.exc_depth
        work_space = 1
        A1 = (self.width + 2 * work_space) * (self.length + 2 * work_space)
        A2 = (self.width + 2 * work_space + 2 * self.depth_exc) * (self.length + 2 * work_space + 2 * self.depth_exc)
        A3 = (self.width + 2 * work_space + self.depth_exc) * (self.length + 2 * work_space + self.depth_exc)
        exc = round((A1 + A2 + 4 * A3) * self.depth_exc / 6, 2)
        print(A1,A2,A3,exc,sep="\n")
        print("Excavation: ",exc)
        return exc

    def strfill(self):
        work_space = 1
        A1 = (self.width + 2 * work_space) * (self.length + 2 * work_space)
        A2 = (self.width + 2 * work_space + 2 * self.fill) * (self.length + 2 * work_space + 2 * self.fill)
        A3 = (self.width + 2 * work_space + self.fill) * (self.length + 2 * work_space + self.fill)
        depth = self.fill
        strfill = round((A1 + A2 + 4 * A3) * depth / 6, 2)
        print(A1,A2,A3,strfill,sep="\n")
        print("Strfill: ",strfill)
        return strfill

    def leanconc(self):
        return round((self.width + 0.5) * (self.length + 0.5) * 0.1, 2)  # checked

    def backfill(self):
        Exc = self.excavation()
        Fill = self.strfill()
        Lc = self.leanconc()
        self.insulation_height = self.exc_depth - 0.1 - self.fill - 0.03
        return round(Exc - Fill - Lc - Lc/3 -self.width * self.length * self.insulation_height,2)  # checked

    def formwork(self):
        return round(2 * (self.width + self.length) * self.foundation_depth ,2)  # checked

    def strconcrete(self):
        return round(self.width * self.length * self.foundation_depth, 2)  # checked

    def rebar(self):
        return round(self.width * self.length * self.foundation_depth * 0.12, 2)  # checked

    def anchor(self):
        anchors  = {"M24":0,
                    "M30":0,
                    "M36":0,
                    "M42":0}
        anchors[f"{self.anchor_type}"] = self.anchor_qty
        return anchors #list(anchor().items[0] = anchor_type

    def embeddedsteel(self):
        return round(self.es, 2)  # checked

    def concreteprot(self):
        return round(self.width * self.length + 2 * (self.width + self.length) * self.insulation_height, 2)  # checked

    def grout(self):
        try:
            grout_area = self.width * self.length / (self.anchor_qty * 1.5)
        except ZeroDivisionError:
            grout_area = 0
        return self.grout_depth *  grout_area# checked

    def polyethylenesheet(self):
        return round(self.width * self.length * 2,2)

    def waterStopper(self):
        ws = 2 * (self.width + self.length)
        return ws

    def jointIsolation(self):
        joint = 2 * (self.width + self.length)
        return joint