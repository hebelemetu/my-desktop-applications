class foundation:
    def __init__(self,a,b,c,d,e,f,h,fill,bolt,pedestal,es,steel):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.h = h
        self.fill = fill
        self.bolt = bolt
        self.pedestal = pedestal
        self.es = es
        self.steel = steel

    def excavation_old(self):
        depth = (self.f - self.h + self.e + 0.1 + self.fill)
        A1 = (self.a + 2) * (self.b + 2)
        A2 = (self.a + 2 + 2 * depth) * (self.b + 2 + 2 * depth)
        A3 = (A1 + A2) / 2
        return round((A1 + A2 + 4 * A3) * depth / 6, 2)  # checked

    def excavation(self,min_depth):
        print(f"min depth = {min_depth}")
        depth = (self.f - self.h + self.e + 0.1 + self.fill)
        if depth >= min_depth:
            depth = depth - min_depth
            print(f"new depth = {depth}")
            A1 = (self.a + 2) * (self.b + 2)
            excavation = A1 * depth
            return  round(excavation,2)
        else:
            return 0


    def strfill(self):
        A1 = (self.a + 2) * (self.b + 2)
        A2 = (self.a + 2 + 2 * self.fill) * (self.b + 2 + 2 * self.fill)
        A3 = (A1 + A2) / 2
        depth = self.fill
        return round((A1 + A2 + 4 * A3) * depth / 6, 2)  # checked

    def leanconc(self):
        return round((self.a + 0.1) * (self.b + 0.1) * 0.1, 2)  # checked

    def backfill(self):
        depth = (self.f - self.h + self.e + 0.1 + self.fill)
        A1 = (self.a + 2) * (self.b + 2)
        A2 = (self.a + 2 + 2 * depth) * (self.b + 2 + 2 * depth)
        A3 = (A1 + A2) / 2
        Exc = (A1 + A2 + 4 * A3) * depth / 6
        A1_2 = (self.a + 2) * (self.b + 2)
        A2_2 = (self.a + 2 + 2 * self.fill) * (self.b + 2 + 2 * self.fill)
        A3_2 = (A1_2 + A2_2) / 2
        depth_2 = self.fill
        Fill = (A1_2 + A2_2 + 4 * A3_2) * depth_2 / 6
        Lc = round((self.a + 0.1) * (self.b + 0.1) * 0.1, 2)
        return round(Exc - Fill - Lc - self.pedestal * self.c * self.d * (self.f - self.h) - self.a * self.b * self.e,2)  # checked

    def formwork(self):
        return round(
            2 * (self.a + self.b) * self.e + self.pedestal * 2 * (self.c + self.d) * self.f + self.pedestal * 2 * (self.c + self.d) * 0.15, 2)  # checked

    def strconcrete(self):
        return round(self.a * self.b * self.e + self.pedestal * self.c * self.d * self.f, 2)  # checked

    def rebar(self):
        return round((self.a * self.b * self.e + self.pedestal * self.c * self.d * self.f) * 0.1, 2)  # checked

    def anchor(self):
        return round(self.pedestal * self.bolt, 0)  # checked

    def embeddedsteel(self):
        return round(self.pedestal * self.es, 2)  # checked

    def concreteprot(self):
        return round(self.a * self.b + (self.a * self.b - self.pedestal * self.c * self.d) + (
                    2 * (self.c + self.d) * (self.f - self.h) * self.pedestal), 2)  # checked

    def secondconcrete(self):
        return round(self.c * self.d * self.pedestal * 0.15, 2)  # checked

    def steelqty(self):
        return self.steel  # checked


class cable:
    def __init__(self,d,e,f,g,fill,divisionwall,length,coverlength):
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.fill = fill
        self.divisionwall = divisionwall
        self.length = length
        self.coverlength = coverlength
        self.a = self.f + self.divisionwall * self.f + 2 * self.d + self.divisionwall * self.d
        self.b = self.e + self.d + 0.1
        self.c = self.e + self.d

    def Area(self):
        return self.a * self.b

    def cablelength(self):
        return self.length

    def cableexcavation(self,min_depth):
        depth = self.b + self.fill
        if depth >= min_depth:
            depth = depth - min_depth
            return round((self.a + 2) * depth, 2)
        else:
            return 0

    def cablestrfill(self):
        return round((self.a + 2) * self.fill, 2)

    def cableleanconc(self):
        return round((self.a + 0.4) * 0.1, 2)

    def cablebackfill(self):
        return round(self.a * (self.b + self.fill) - self.a * self.fill - (self.a + 0.4) * 0.1 - (self.c * self.a), 2)

    def cableformwork(self):
        return round((self.c * 2 + self.e * 2 + self.divisionwall * self.e * 2), 2)

    def cableformworkcover(self):
        return round((2 * self.a + 2 * self.coverlength) * self.g / self.coverlength + self.a, 2)

    def cablestrconcrete(self):
        return round(self.d * self.a + self.a * self.g + 2 * self.d * self.e + self.divisionwall * self.e * self.d, 2)

    def cablerebar(self):
        return round(
            (self.d * self.a + self.a * self.g + 2 * self.d * self.e + self.divisionwall * self.e * self.d) * 0.1, 2)

    def cableembeddedsteel(self):
        return round((2 + 4 + self.a * 4) * 2.7 / 1000, 2)

    def cableconcreteprot(self):
        return round(self.a + self.c * 2, 2)

    def cablewaterstopper(self):
        return round(self.d * 2 / self.d, 2)

    def cablejointiso(self):
        return round(self.a / self.coverlength + ((2 * self.c + self.a) / 16), 2)

class fence_road:
    def __init__(self,fence_length,road,road_width):
        self.fence_length = fence_length
        self.road = road
        self.road_width = road_width

    def fence_length_perfeeder(self):
        return self.fence_length * 2

    def road_length_perfeeder(self):
        return self.road * 3

    def pit_manhole(self):
        return self.road * 3 / 25

    def kerbstone(self):
        return self.road * 3 * 2

    def road_joint(self):
        return self.road * 3 / 6 * 4

    def electric_conduit(self):
        return self.road * 3

    def pipe_150mm(self):
        return self.road * 3

    def excavation_site(self,depth,width,length):
        A1 = (width + 2) * (length + 2)
        A2 = (width + 2 + 2 * depth) * (length + 2 + 2 * depth)
        A3 = (A1 + A2) / 2
        return round((A1 + A2 + 4 * A3) * depth / 6, 2)

if __name__ == '__main__':
    a = fence_road(15.5,15.5,4)
    print(a.excavation_site(2.4,31,80))
    pylon = foundation(8.8,7.5,2.4,4.8,0.6,1.85,0.15,1,16,1,0,2.312)
    exc_pylon = pylon.excavation_old()
    fill_pylon = pylon.strfill()
    lc = pylon.leanconc()
    backfill = pylon.backfill()
    fw = pylon.formwork()
    strconc = pylon.strconcrete()
    rebar=pylon.rebar()
    anchor = pylon.anchor()
    embedded_steel = pylon.embeddedsteel()
    concreteprot = pylon.concreteprot()
    secondconc = pylon.secondconcrete()
    steelqty = pylon.steelqty()
    print(f"exc = {exc_pylon} fill = {fill_pylon} lc = {lc} backfill = {backfill} fw = {fw} strconc = {strconc} rebar = {rebar} anchor = {anchor} embed = {embedded_steel} concreteprot = {concreteprot} secondconc = {secondconc} steel = {steelqty}")
