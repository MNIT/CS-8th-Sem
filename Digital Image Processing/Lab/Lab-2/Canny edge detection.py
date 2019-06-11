'''
Canny edge detection technique
'''

sys.setrecursionlimit(1000*1000*4)

def apply_filter(kernel, r, c, img):
    value = 0
    k_r, k_c = len(kernel), len(kernel[0])
    i_r, i_c = img.shape
    
    for i in range(k_r):
        for j in range(k_c):
            x = i + r - (k_r//2)
            y = j + c - (k_c//2)

            if(isValid(x, y, i_r, i_c)):
                value += (kernel[i][j] * img[x][y])
    return value


def dfs_visit(suppressed, r, c, visited, i, j):
    if(visited[i][j] == 1):
        return

    if(suppressed[i][j] < th_low):
        visited[i][j] = 1
        return
    
    visited[i][j] = 1

    for p, q in [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]: 
        if(isValid(p, q, r, c)):
            dfs_visit(suppressed, r, c, visited, p, q)
        
    return


sigma = 1.4
img = cv2.imread('house.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#im = gaussian_blur(im, sigma)
img = cv2.GaussianBlur(img, (5, 5), 1.4)

#sobel filters for gradients in x and y directions
filter_x = [[-1,0,1], [-2,0,2], [-1,0,1]]
filter_y = [[-1,-2,-1], [0,0,0], [1,2,1]]

r, c = img.shape

grad_x = np.zeros(img.shape, np.float)
grad_y = np.zeros(img.shape, np.float)

grad_magnitude = np.zeros(img.shape, np.float)
grad_angle = np.zeros(img.shape, np.float)

for i in range(r):
    for j in range(c):
        grad_x[i][j] = apply_filter(filter_x, i, j, img)
        grad_y[i][j] = apply_filter(filter_y, i, j, img)
        
        x, y = grad_x[i][j], grad_y[i][j]
        
        grad_magnitude[i][j] = math.sqrt((x ** 2) + (y ** 2))
        
        t = round(math.degrees(math.atan2(y,x)), 3)
        if(t < 0):
            t += 180
        
        grad_angle[i][j] = t
        

suppressed = np.copy(grad_magnitude)
th_low= 20
th_high= 45

for i in range(r):
    for j in range(c):
        angle = gradient_angle[i][j]
        pixel1 = 0
        pixel2 = 0

        if((angle>=0 and angle<=22.5) or (angle>157.5 and angle<=180)):
            if(j-1>=0):
                pixel1 = grad_magnitude[i][j-1]
            if(j+1<c):
                pixel2 = grad_magnitude[i][j+1]
        
        elif(angle>22.5 and angle<=67.5):
            if(j-1>=0 and i+1<r):
                pixel1 = grad_magnitude[i+1][j-1]
            if(j+1<c and i-1>=0):
                pixel2 = grad_magnitude[i-1][j+1]
        
        elif(angle>67.5 and angle<=112.5):
            if(i-1>=0):
                pixel1 = grad_magnitude[i-1][j]
            if(i+1<r):
                pixel2 = grad_magnitude[i+1][j]
        
        elif(angle>112.5 and angle<=157.5):
            if(i-1>=0 and j-1>=0):
                pixel1 = grad_magnitude[i-1][j-1]
            if(i+1<r and j+1<c):
                pixel2 = grad_magnitude[i+1][j+1]
        
        if(grad_magnitude[i][j] < pixel1 or grad_magnitude[i][j] < pixel2):
            suppressed[i][j] = 0

plt.imshow(suppressed.astype(np.uint8), cmap = "gray")

visited = np.zeros_like(suppressed)
for i in range(r):
    for j in range(c):
        if(suppressed[i][j] > th_high and visited[i][j] == 0):
            dfs_visit(suppressed, r, c, visited, i, j)
            
#pixels which have not been visited represent weak edges , so set them to 0
for i in range(r):
    for j in range(c):
        if(visited[i][j] == 0):
            suppressed[i][j] = 0

print("Sigma =", sigma)
print("Low threshold =", th_low)
print("High threshold =", th_high)

plt.title('Canny Edge Detector')
plt.imshow(suppressed.astype(np.uint8), cmap = "gray")


def get_gaussian_kernel(size, sigma):
    res = []
    for i in range(size):
        res.append([])
        for j in range(size):
            x = j - (size//2)
            y = (size//2) - i
            
            val = (x**2)+(y**2)
            val*=-1
            val/=2
            val/=(sigma**2)
            val1 = math.exp(val)
            val1/=2
            val1/=math.pi
            val1/=(sigma**2)
            
            res[i].append(round(val1, 4))
    return res

        
def apply_filter(kernel, r, c, img):
    value = 0
    k_r, k_c = len(kernel), len(kernel[0])
    i_r, i_c = img.shape
    
    for i in range(k_r):
        for j in range(k_c):
            x = i + r - (k_r//2)
            y = j + c - (k_c//2)

            if(isValid(x, y, i_r, i_c)):
                value += (kernel[i][j] * img[x][y])
    return value


def gaussian_blur(img, sigma):
    kernel = get_gaussian_kernel(5, sigma)
    
    blur_image = np.zeros(img.shape, np.uint8)
    r, c = img.shape
    
    for i in range(r):
        for j in range(c):
            blur_image[i][j] = round(apply_filter(kernel, i, j, img), 4)
    
    return blur_image