from Pile import Pile

length = 13.5
diameter = 0.5

top = [0., 3., 6., 11.]
bot = [3., 6., 11., 18.]
gam = [10., 10., 10., 10.]
strength = [25., 25., 25., 25.]

pile1 = Pile(length, diameter, top, bot, gam, strength)
pile1.load = 100
pile1.numStage = 20
pile1.numSegmen = 10

pile1.show()

attr = vars(pile1)
print(attr)




# a = pile1.run()


# pile2 = Pile(length, diameter, top, bot, gam, strength)
# pile2.load = 100
# pile2.numStage = 20
# pile2.numSegmen = 20
# pile2.show()


# pile3 = Pile(length, diameter, top, bot, gam, strength)
# pile3.load = 100
# pile3.numStage = 20
# pile3.numSegmen = 30
# pile3.show()


# pile4 = Pile(length, diameter, top, bot, gam, strength)
# pile4.load = 100
# pile4.numStage = 100
# pile4.numSegmen = 20
# pile4.show()


# pile5 = Pile(length, diameter, top, bot, gam, strength)
# pile5.load = 100
# pile5.numStage = 100
# pile5.numSegmen = 50
# pile5.show()




# depth, deflection, moment, shear, soil = pile1.show()

# print(depth)
# print(deflection)
# print(moment)
# print(shear)
# print(soil)



# print('load 10', a[0])
# print('load 20', a[1])
# print('load 30', a[2])
# print('load 40', a[3])
# print('load 50', a[4])
# print('load 60', a[5])
# print('load 70', a[6])
# print('load 80', a[7])
# print('load 90', a[8])
# print('load 100', a[9])

# pile2 = Pile(length, diameter, top, bot, gam, strength)
# pile2.load = 100
# pile2.numSegmen = 50

# attr2 = vars(pile2)
# print(attr2)

# pile2.run()
# print('sukses2')

