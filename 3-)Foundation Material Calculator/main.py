class gt:
    def __init__(self,name,width,length,height):
        self.name = name
        self.width = width
        self.length = length
        self.height = height

    #2.4
    def excavation(self,depth_exc):
        self.depth_exc = depth_exc
        work_space = 2
        A1 = (self.width + work_space) * (self.length + work_space)
        A2 = (self.width + work_space + 2 * self.depth_exc) * (self.length + work_space + 2 * self.depth_exc)
        A3 = (self.width + work_space + self.depth_exc) * (self.length + work_space + self.depth_exc)
        exc = round((A1 + A2 + 4 * A3) * self.depth_exc / 6, 2)
        return exc

    #2.7
    def strFill(self,depth_fill):
        self.depth_fill = depth_fill
        work_space = 2
        A1 = (self.width + work_space) * (self.length + work_space)
        A2 = (self.width + work_space + 2 * self.depth_fill) * (self.length + work_space + 2 * self.depth_fill)
        A3 = (self.width + work_space + self.depth_fill) * (self.length + work_space + self.depth_fill)
        depth = self.depth_fill
        strfill = round((A1 + A2 + 4 * A3) * depth / 6, 2)
        return strfill

    def concreteUnderGround(self,depth):
        concrete = self.width * self.length * depth
        return  concrete

    #2.11
    def backFill(self):
        pass

    #3.1
    def leanConcrete(self):
        pass

    #3.2
    def concreteFoundation(self):
        pass

    #3.11
    def grout(self):
        pass

    #3.12
    def screed(self):
        pass

    #4.1
    def formwork(self):
        pass

    #5.1
    def rebar(self):
        pass

    #6.1
    def embeddedSteel(self):
        pass

    #17.1
    def insulationSika(self):
        pass

    #17.4
    def peSheet(self):
        pass



if __name__ == '__main__':
    gt9e = gt("gt9e",6.2,34.524,3)
    gts = [gt9e]
    for gast in gts:
        print(f"Excavation for {gast.name}: {gast.excavation(3)}")
        print(f"Strfill for {gast.name}: {gast.strFill(1.185)}")
        print(f"Concrete under ground for {gast.name}: {gast.concreteUnderGround(1.715)}")
        print()