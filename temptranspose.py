import numpy

# a = [[1,2,3],[11, 12, 13]]
# b = [4,5,6]
# c = [7,8,9]

# arr = numpy.array(a)

# arr = numpy.append([a[1]], [b, c], axis=0)

# print(arr)
# arrtranspose = numpy.transpose(arr)
# print(arrtranspose)

# print(arrtranspose.tolist())

# print(arrtranspose)

lst = [1,2,3]
lst2 = [[4,5,6], [7,8,9]]


arr = numpy.append([lst], lst2, axis=0)

print(arr)

