from Pile import Pile

length = 10
diameter = 0.5
top = [0., 3., 6., 11.]
bot = [3., 6., 11., 12.]
gam = [10., 10., 10., 10.]
strength = [25., 25., 25., 25.]

pile1 = Pile(length, diameter, top, bot, gam, strength)
pile1.load = 100

attr = vars(pile1)
print(attr)

print(pile1.run())
# print(pile1.numNodal())


# print(pile1.numNodal())
# print(pile1.numIndexB())

# a = pile1.nDepth()
# print(a)

# b = pile1.strengthNodal()
# print(b)


# pile1.numSegmen = 100
# print(pile1.nDepth())
# c = pile1.strengthLayer()
# print(c)

# print(pile1.cetakpu())