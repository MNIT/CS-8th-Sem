'''
Write a function that performs histogram equalization (see lecture notes or course book).
Use your own function, but do not use functions like cv2.equalizeHist();
'''

def get_frequencies(gray):
    hist = []

    for i in range(256):
        hist.append(0)

    for i in range(len(gray)):
        for j in range(len(gray[i])):
            hist[gray[i][j]] += 1
    
    return hist
  

freq = get_frequencies(gray)

total_pixels = sum(freq)
norm = []
for i in range(0, 256):
    norm.append(freq[i]/total_pixels)

    
new_img = np.zeros((len(image),len(image[0]),3), np.uint8)

for i in range(len(gray)):
    for j in range(len(gray[i])):
        pixel_val = 0
            
        for k in range(0, gray[i][j]+1):
            pixel_val += norm[k]
            
        pixel_val *= 255
        new_img[i][j] = pixel_val
            
cv2.imwrite('histogram-equalization.png', new_img)
plt.imshow(cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB))
plt.show()
freq = get_frequencies(cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY))

plt.axis([0, 256, 0, 1.5*max(freq)])
    
for i in range(256):
    plt.plot([i, i], [0, freq[i]], color = "blue")
    
plt.show()