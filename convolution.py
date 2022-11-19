import struct
from copy import deepcopy

def keepinrange(x):
    if x > 255:
        return 255
    if x < 0:
        return 0
    else :
        return x    

Inp_file = open ("lana.bmp","rb")
Out_file = open("lana2.bmp","rb+")
Inp_file.seek(18,0)
w = Inp_file.read(4)
width=struct.unpack("i",w)
# print ("Image width = ", width[0])
h = Inp_file.read(4)
height=struct.unpack("i",h)
# print ("Image height = ", height[0]) 
Inp_file.seek(10,0)
o = Inp_file.read(4)
offset = struct.unpack("i",o)
Inp_file.seek(offset[0],0)
Out_file.seek(offset[0],0)

HeadMatrix = [[],[],[]]

for y in range(height[0]):

    Stdnt_Matrix = [[],[],[]]

    for x in range(width[0]):
        for i in range(3):

            Pixel = Inp_file.read(1)[0]
            Stdnt_Matrix[i].append(Pixel)

    for i in range(3):

        HeadMatrix[i].append(Stdnt_Matrix[i])

def ConvoK(HeadMatrix1):

#Kernel = [[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]] # blur
#Kernel = [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]] #edge detection corner diagonal counted
#Kernel = [[0,-1,0],[-1,4,-1],[0,-1,0]] #edge detection 
#Kernel = [[1/16,2/16,1/16],[2/16,4/16,2/16],[1/16,2/16,1/16]] guassian blur
#Kernel = [[0,0,0],[0,1,0],[0,0,0]] identity
#Kernel = [[0,-1,0],[-1,5,-1],[0,-1,0]] #sharp
#Kernel = [[-1,0,0],[0,0,0],[0,0,1]] embossing

    Kernel = [[0,-1,0],[-1,5,-1],[0,-1,0]]
    CopyMatrix = deepcopy(HeadMatrix1)
    for y in range(height[0]):
        for x in range(width[0]):
            sum = 0
            for i in range(3):
                for j in range(3):
                    if ((y+i-1) < 0) or ((y+i-1) > height[0]-1) or ((x+j-1) < 0) or ((x+j-1) > width[0] -1 ):
                        sum += 0
                    else :
                        sum += CopyMatrix[y+i-1][x+j-1]*Kernel[i][j]
            HeadMatrix1[y][x]= keepinrange(sum)
    return HeadMatrix1

def grey(x):
    x = x//3
    return x

def bright(x):
    x = keepinrange(int(x+50))
    return x

def changeContrast(x):
    cont = 22
    x = ((((x/255)-0.5)*cont)+0.5)*255
    return keepinrange(int(x))

def grey(x):
    return(x//3)

def negative(x):
    return(255-x)

for i in range(1):

    BlueMatrix =ConvoK(HeadMatrix[0])
    GreenMatrix= ConvoK(HeadMatrix[1])
    RedMatrix= ConvoK(HeadMatrix[2])

for y in range(height[0]):
    for x in range(width[0]):

        BlueElements = BlueMatrix[y][x]
        GreenElements = GreenMatrix[y][x]
        RedElements = RedMatrix[y][x]

        # BlueElements = grey(BlueMatrix[y][x])
        # GreenElements = grey(GreenMatrix[y][x])
        # RedElements = grey(RedMatrix[y][x])

        # BlueElements = bright(BlueMatrix[y][x])
        # GreenElements = bright(GreenMatrix[y][x])
        # RedElements = bright(RedMatrix[y][x])
    
        # BlueElements = changeContrast(BlueMatrix[y][x])
        # GreenElements = changeContrast(GreenMatrix[y][x])
        # RedElements = changeContrast(RedMatrix[y][x])

        # BlueElements = negative(BlueMatrix[y][x])
        # GreenElements = negative(GreenMatrix[y][x])
        # RedElements = negative(RedMatrix[y][x])

        BlueBytes = int(BlueElements).to_bytes(1,'little')
        GreenBytes = int(GreenElements).to_bytes(1,"little")
        RedBytes = int(RedElements).to_bytes(1,"little")

        Out_file.write(BlueBytes)
        Out_file.write(GreenBytes)
        Out_file.write(RedBytes)
print("IMAGE HAS BEEN FILTERED....")
Inp_file.close()
Out_file.close()