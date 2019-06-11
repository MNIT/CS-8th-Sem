'''
Perform contrast stretching on the given and display original image as well as resultant
image in the same frame.
'''

freq = []

for i in range(256):
    freq.append(0)

for i in range(len(gray)):
    for j in range(len(gray[i])):
        freq[gray[i][j]] += 1

new_img = np.zeros((len(gray),len(gray[0])), np.uint8)
    
xmin = 256
xmax = -1
    
for i in range(256):
    if(freq[i] != 0 and i < xmin):
        xmin = i
        
    if(freq[i] != 0 and i > xmax):
        xmax = i
            
min_freq = min(freq)
max_freq = max(freq)
    
for i in range(256):
    if(freq[i] == min_freq):
        ymin = i
        
    if(freq[i] == max_freq):
        ymax = i
    
denom = ymax - ymin
num = xmax - xmin
factor = num/denom

for i in range(len(gray)):
    for j in range(len(gray[i])):
        new_img[i][j] = factor * (gray[i][j]-ymin) + xmin
            
plt.subplot(1, 2, 1)
plt.imshow(gray, cmap = "gray")

plt.subplot(1, 2, 2)
plt.imshow(new_img, cmap = "gray")