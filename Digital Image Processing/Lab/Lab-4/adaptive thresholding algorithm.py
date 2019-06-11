def global_thresholding(img, r, c, t):
    #two matrices for two segments of image (one with pixels value>t and other with <t)
    g1 = np.zeros((r,c), np.uint8)
    g2 = np.zeros_like(g1)
    
    #print(img.shape)
    
    count1=0
    count2=0
    mu1=0
    mu2=0

    for i in range(r):
        for j in range(c):
            if(img[i][j] >= t):
                g1[i][j] = img[i][j]
                count1 += 1
                mu1 += g1[i][j]
            
            else:
                g2[i][j] = img[i][j]
                count2 += 1
                mu2 += g2[i][j]
    
    if(count1 != 0):
        mu1 /= count1
    
    if(count2 != 0):
        mu2 /= count2

    tnew = (mu1 + mu2)/2
    return math.floor(tnew + 0.5)


def adaptive_thresholding(img, patch_size):
    t = 200
    t0 = 0
    
    r, c = img.shape
    thresh_img = np.zeros(img.shape)
    
    for i in range(0, r-patch_size, patch_size):
        for j in range(0, c-patch_size, patch_size):
            
            t = 200
            t0 = 0
    
            #print("Initial Threshold = 200")
            #show_thresh_image(img, t, "Initial Threshold = 200")

            iteration = 1
            img_patch = img[i:i+patch_size, j:j+patch_size]
    
            while(1):
                tnew = global_thresholding(img_patch, patch_size, patch_size, t)
                if(abs(t-tnew) <= t0):
                        break
                t = tnew
                iteration += 1
            
            for p in range(i, i+patch_size):
                for q in range(j, j+patch_size):
                    if(img[p][q] > t):
                        thresh_img[p][q] = 255
    
            #print("Thresholding stopped after", iteration, "iterations")
            #print("Final Threshold = ", t)
    
    plt.title("Adaptive Threshold with patch size = ({0} X {0})". format(patch_size))
    plt.imshow(thresh_img)
    plt.show()
    

def show_thresh_image(img, t, title):
    img2 = np.zeros_like(img)
    img2[img>t] = 255
    
    plt.title(title)
    plt.imshow(img2)
    return


img = cv2.imread('threshold.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

r, c = img.shape

hist = []

for i in range(256):
    hist.append(0)

for i in range(len(img)):
    for j in range(len(img[i])):
        hist[img[i][j]] += 1

plt.axis([0, 256, 0, max(hist)+300])        
for i in range(256):
    plt.plot([i,i], [0, hist[i]], color = "blue")

plt.show()

adaptive_thresholding(img, 5)
adaptive_thresholding(img, 7)
adaptive_thresholding(img, 9)