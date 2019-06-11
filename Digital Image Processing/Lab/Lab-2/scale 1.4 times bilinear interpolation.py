'''
Scale 'scale.png' to 1.4 times (use bilinear interpolation)
'''

def bilinear_interpolation(img, x, y):
    r, c, channels = img.shape
    #finding neighbours of the pixel to be calculated
    left_x = math.floor(x)
    left_y = math.floor(y)
    right_x = left_x+1
    right_y = left_y+1
    
    #if right neighbour is out of boundary then make it as pixel at the boundary
    if(right_x >= r):
        right_x -= 1
    if(right_y >= c):
        right_y -= 1
    
    pixel_value = []
    
    for c in range(channels):
        #2 interpolations in x direction and final interpolation in y direction
        ipx1 = ((right_y - y) * img[left_x][left_y][c]) + ((y - left_y) * img[left_x][right_y][c])
        ipx2 = ((right_y - y) * img[right_x][left_y][c]) + ((y - left_y) * img[right_x][right_y][c])
        
        ipy1 = ((right_x - x) * ipx1) + ((x - left_x) * ipx2)
        pixel_value.append(int(round(ipy1)))

    return pixel_value


def scale_image(img, factor):
    r, c , channels = img.shape
    
    r_scale = math.ceil(r*factor)
    c_scale = math.ceil(c*factor)

    new_img = np.zeros((r_scale, c_scale, 3), np.uint8)

    for i in range(r_scale):
        for j in range(c_scale):
            #finding pixel from original image corresponding to (i,j) pixel in new image
            x = i/factor
            y = j/factor
            new_img[i][j] = bilinear_interpolation(img, x, y)
    return new_img


img = cv2.imread('scale.png')
new_img = scale_image(img, 1.4)

print("Input image shape :", img.shape)
print("Scaled image shape :", new_img.shape)

plt.figure(figsize = (12, 12))

plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(img)

plt.subplot(1, 2, 2)
plt.title("Scaled Image (1.4 times)")
plt.imshow(new_img)