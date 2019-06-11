'''
Find  scaling factor and perform nearest neighbour interpolation on ‘scale.png’
'''

def scale_image(img, factor):
    r, c, channels = img.shape
    
    r2 = math.ceil(r * factor)
    c2 = math.ceil(c * factor)
    
    #print(r, c, r2, c2)
    
    new_img = np.zeros((r2, c2, channels), np.uint8)

    for i in range(r2):
        for j in range(c2):
            for ch in range(channels):
                new_img[i][j][ch] = 2
                
    #putting correct pixel values in output image as per the scaling factor
    #first phase
    i=0; x=0
    while(x < r2-r):
        j=0; y=0
        
        while(y < c2-c):
            new_img[i][j][0] = img[x][y][0]
            new_img[i][j][1] = img[x][y][1]
            new_img[i][j][2] = img[x][y][2]
            '''
            as per the scaling factor in this case(870/512)
            each pixel needs to set its 3 neighbours
            1st neighbour => right to it
            2nd neighbour => below it
            3rd neighbour => diagonally down 
            whichever neighbour is valid , it is set appropriately
            '''
            for p, q in [(i, j+1), (i+1, j), (i+1, j+1)]:
                if(isValid(p, q, r2, c2)):
                    new_img[p][q][0] = img[x][y][0]
                    new_img[p][q][1] = img[x][y][1]
                    new_img[p][q][2] = img[x][y][2]
            
            j += math.ceil(factor)
            y += 1
        
        i += math.ceil(factor)
        x += 1
    
    #2nd phase
    i=0; x=0
    while(i < (r2-r)*2 and x < r):
        j = (c2-c)*2
        y = c2-c
        
        while(j < c2 and y < c):
            new_img[i][j][0] = img[x][y][0]
            new_img[i][j][1] = img[x][y][1]
            new_img[i][j][2] = img[x][y][2]
            
            if(isValid(i+1, j, r2, c2)):
                new_img[i+1][j][0] = img[x][y][0]
                new_img[i+1][j][1] = img[x][y][1]
                new_img[i+1][j][2] = img[x][y][2]
            j += 1
            y += 1
        i += math.ceil(factor)
        x += 1
    
    #3rd phase
    i = (r2-r)*2
    x = r2-r
    while(i<r2 and x<r):
        j=0; y=0
        
        while(j < (c2-c)*2 and y<c):
            new_img[i][j][0] = img[x][y][0]
            new_img[i][j][1] = img[x][y][1]
            new_img[i][j][2] = img[x][y][2]
            
            if(isvalid(i, j+1, r2, c2)):
                new_img[i][j+1][0] = img[x][y][0]
                new_img[i][j+1][1] = img[x][y][1]
                new_img[i][j+1][2] = img[x][y][2]
            j += math.ceil(factor)
            y += 1
            
        i += 1
        x += 1
    
    #4th phase
    i = (r2-r)*2
    x = r2-r
    while(i < r2 and x < r):
        j = (c2-c)*2
        y = c2-c
        
        while(j < c2 and y < c):
            new_img[i][j][0] = img[x][y][0]
            new_img[i][j][1] = img[x][y][1]
            new_img[i][j][2] = img[x][y][2]
            j += 1
            y += 1
            
        i += 1
        x += 1

    return new_img


img = cv2.imread('scale.png')
scale_factor = 870/512
print("Scale factor :", scale_factor)
new_img = scale_image(img, scale_factor)

print("Input image shape :", img.shape)
print("Scaled image shape :", new_img.shape)

#plt.figure(figsize = (12, 12))

plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(img)

plt.subplot(1, 2, 2)
plt.title("Scaled Image " + str(scale_factor) + " times)")
plt.imshow(new_img)