class Pit:
    def __init__(self,width, length, height, bottom_thickness, mid_height, top_thickness, wall_thickness, mid_width, mid_length, strfill):
        self.bottom_thickness = bottom_thickness #d
        self.wall_thickness = wall_thickness #g
        self.mid_height =  mid_height#e
        self.top_thickness = top_thickness#f
        self.mid_width = mid_width#h
        self.mid_length= mid_length#k
        self.strfill = strfill
        self.width = width
        self.length = length
        self.height = height
        #self.width = self.mid_width + 2 * self.wall_thickness #a
        #self.length= self.mid_length + 2 * self.wall_thickness #b
        #self.height = self.mid_height + self.bottom_thickness + self.top_thickness #c


    def excavation(self):
        exc = (self.width + 2) * (self.length + 2) * (self.height - self.top_thickness + 0.15 + self.strfill)
        return exc

    def strFill(self):
        fill = (self.width + 2) * (self.length + 2) * self.strfill
        return fill

    def backFilling(self):
        bf = self.excavation() - self.width * self.length * (self.height - self.top_thickness) - self.strFill() - self.leanConcrete()
        return bf

    def leanConcrete(self):
        lc = (self.width + 0.4) * (self.length + 0.4) * 0.1
        return lc

    def formwork(self):
        fw = 2 * (self.width + self.length) * self.height + 2 * (self.mid_width + self.mid_height) * self.mid_height
        return fw

    def strconcrete(self):
        conc = self.width * self.length * self.bottom_thickness + 2 * (self.width + self.mid_length) * self.wall_thickness * self.mid_height + self.width * self.length * self.top_thickness
        return conc

    def rebar(self):
        rb = self.strconcrete() * 0.12
        return rb

    def embeddedSteel(self):
        es = self.width * self.length * 30
        return es

    def concreteProtection(self):
        insulation = self.width * self.length + (2 * (self.width + self.length) * (self.height - self.top_thickness))
        return insulation

    def waterStopper(self):
        ws = 2 * (self.width + self.length)
        return ws

    def jointIsolation(self):
        joint = 2 * (self.width + self.length)
        return joint

    def polyethylenesheet(self):
        return round(self.width * self.length,2)




