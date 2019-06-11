'''
Apply weighted mean filter on filter.jpg
'''

def apply_filter(img):
    r, c, channel = img.shape
    
    new_img = np.zeros(img.shape, np.uint8)

    for i in range(r):
        for j in range(c):
            t = [0,0,0]
            t[0] += img[i][j][0] * 4
            t[1] += img[i][j][1] * 4
            t[2] += img[i][j][2] * 4
            
            for p, q in [(i-1, j), (i, j-1), (i+1, j), (i, j+1)]:
                if(isValid(p, q, r, c)):
                    t[0] += img[p][q][0]
                    t[1] += img[p][q][1]
                    t[2] += img[p][q][2]
            
            new_img[i][j][0] = t[0]//8
            new_img[i][j][1] = t[1]//8
            new_img[i][j][2] = t[2]//8
    
    return new_img


image = cv2.imread('filter.jpg')
new_image = apply_filter(image)

plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

plt.subplot(1, 2, 2)
plt.title("Filtered Image")
plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
