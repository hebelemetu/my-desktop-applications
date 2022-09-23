class Matfoundation:
    def __init__(self,width,length,pedestal_length,pedestal_width,foundation_depth,pedestal_height,height_above_ground,fill,bolt,es,steel):
        self.width = width
        self.length = length
        self.pedestal_length = pedestal_length
        self.pedestal_width = pedestal_width
        self.foundation_depth = foundation_depth
        self.pedestal_height = pedestal_height
        self.height_above_ground = height_above_ground
        self.fill = fill
        self.bolt = bolt
        self.pedestal = 1
        self.es = es
        self.steel = steel

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
        return round(self.pedestal * self.bolt, 0)  # checked

    def embeddedsteel(self):
        return round(self.pedestal * self.es, 2)  # checked

    def concreteprot(self):
        return round(self.width * self.length + (self.width * self.length - self.pedestal * self.pedestal_length * self.pedestal_width) + (2 * (self.pedestal_length + self.pedestal_width) * (self.pedestal_height - self.height_above_ground) * self.pedestal), 2)  # checked

    def grout(self):
        return round(self.pedestal_length * self.pedestal_width * self.pedestal * 0.05, 3)  # checked

    def polyethylenesheet(self):
        return round(self.width * self.length,2)