'''
Convert scale.png to grayscale and rotate by 30 and 180 degrees
'''

def isValid(x, y, r, c):
    if(x>=0 and x<r and y>=0 and y<c):
        return 1
    else:
        return 0

def rotate_by_180(image):
    r = len(image)
    c = len(image[0])
    new_image = np.zeros((r,c), np.uint8)
    
    for i in range(r):
        for j in range(c):
            new_image[i][j] = image[r-1-i][j]    
    return new_image


def rotate_by_30(image):
    r = len(image)
    c = len(image[0])
    new_image = np.zeros((2*r, 2*c), np.uint8)
    
    for i in range(2*r):
        for j in range(2*c):
            new_image[i][j] = 1

    a = math.cos(math.radians(30))
    b = math.sin(math.radians(30))

    for i in range(r):
        for j in range(c):
            x = ((i-r//2)*a) - ((j-c//2)*b)
            y = ((i-r//2)*b) + ((j-c//2)*a)
            
            x += r//math.sqrt(2)
            y += c//math.sqrt(2)
            
            x = abs(int(round(x)))
            y = abs(int(round(y)))
            
            if(isValid(x, y, 2*r, 2*c)):
                new_image[x][y] = image[i][j]
    return new_image

def alias(image30):
    r = len(image30)
    c = len(image30[0])

    for i in range(r):
        for j in range(c):
            #if pixel is a hole(same intensity as background)
            if(image30[i][j] == 1):
                temp = 0
                #taking values from valid 4 neighbours and taking mean
                if(isValid(i-1, j, r, c)):
                    temp += image30[i-1][j]
                if(isValid(i+1, j, r, c)):
                    temp += image30[i+1][j]
                if(isValid(i, j-1, r, c)):
                    temp += image30[i][j-1]
                if(isValid(i, j+1, r, c)):
                    temp += image30[i][j+1]
                
                image30[i][j] = temp//4
    return image30


image = cv2.imread('scale.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.subplot(1, 3, 1)
plt.title("Gray scale image")
plt.imshow(gray, cmap = "gray")

gray30 = rotate_by_30(gray)
gray30 = alias(gray30)
plt.subplot(1, 3, 2)
plt.title("30 degrees anticlockwise rotated")
plt.imshow(gray30, cmap = "gray")

gray180 = rotate_by_180(gray)
plt.subplot(1, 3, 3)
plt.title("180 degrees rotated")
plt.imshow(gray180, cmap = "gray")