class Duck:
    def __init__(self, length, top, bottom):
        self.__length = length
        # self.__top = top
        # self.__bottom = bottom
        self.__top = (self.layer(length, top, bottom))[0]
        self.__bottom = (self.layer(length, top, bottom))[1]
    
    @property
    def length(self):
        return self.__length
    
    @length.setter
    def length(self, value):
        self.__length = value
    
    @property
    def top(self):
        return self.__top
    
    @top.setter
    def top(self, value):
        self.__top = value
    
    @property
    def bottom(self):
        return self.__bottom
    
    @bottom.setter
    def bottom(self, value):
        self.__bottom = value
    

    def layer(self, length, top, bottom):
        newbottom = []
        for i in range(len(bottom)):
            if bottom[i] < length:
                newbottom.append(bottom[i])
            else:
                break
        newbottom.append(length)
        newtop = []
        for i in range(len(newbottom)):
            newtop.append(top[i])
        
        return (newtop, newbottom)

    def cetak(self):
        return (self.bottom)[-1]

    def kuadrat(self):
        def f(x): return x*x
        
        return list(map(f, self.bottom)) 

    kembali = lambda self: self.bottom[-1]

    datang = lambda self: 2 * self.kembali()


length = 6.5
datop = [0, 3, 6, 9]
datbot = [3, 6, 9, 12]
a = Duck(length, datop, datbot)

atr = vars(a)

print(atr)

print(a.cetak())
print(a.kuadrat())
print(a.kembali())
print(a.datang())