def run(top, bottom, length):
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


top = [0, 3, 6, 11]
bot = [3, 6, 11, 12]

length = 6.3

newtop, newbottom = run(top, bot, length)


print(newtop)
print(newbottom)
