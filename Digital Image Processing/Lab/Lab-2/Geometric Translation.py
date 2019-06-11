img = cv2.imread("filter.jpg")

d_x = 40
d_y = -80

print(img.shape)
new_img = np.zeros(img.shape, np.uint8)

r, c, channels = img.shape

for i in range(r):
    for j in range(c):
        for k in range(channels):
            if(isValid(i + d_y, j + d_x, r, c)):
                new_img[i + d_y][j + d_x][k] = img[i][j][k]

plt.subplot(121)
plt.title("Original Image")
plt.imshow(img)

plt.subplot(122)
plt.title("Geometric Translation")
plt.imshow(new_img)