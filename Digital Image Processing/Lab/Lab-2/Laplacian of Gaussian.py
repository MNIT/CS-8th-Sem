'''
Laplacian of Gaussian edge detection technique
'''

#function to find value of gaussian kernel for given (x,y) and given sigma value
def calculate_gauss(x,y,sigma):
    val = (x**2)+(y**2)
    val*=-1
    val/=2
    val/=(sigma**2)
    val1 = math.exp(val)
    val1/=2
    val1/=math.pi
    val1/=(sigma**2)
    return val1
    
#function to apply convolution operation
def apply_filter(laplace_kernel,kernel_size_x,kernel_size_y,r,c,gaussian_filter,filter_size_x,filter_size_y):
    value=0
    #for each pixel of filter
    for i in range(kernel_size_x):
        for j in range(kernel_size_y):
            #coordinates of image pixel as per standard coordinate system
            x=i+r-(kernel_size_x//2)
            y=j+c-(kernel_size_y//2)
            #if coordinates are valid then apply operation (assuming padding of 0)
            if(isValid(x,y,filter_size_x,filter_size_y)):
                value+=(laplace_kernel[i][j]*gaussian_filter[x][y])
    return value
    
#function to get log filter
def get_filter(laplace_kernel,size,sigma):
    #new matrix for filter
    mat=[]
    #for each value in output filter
    for i in range(size):
        mat.append([])
        for j in range(size):
            #find coordinates of the cell as per standard coordinate system
            x=j-(size//2)
            y=(size//2)-i
            mat[i].append(round(laplace_kernel[i][j]*calculate_gauss(x,y,sigma),5))
    #returning the output filter
    return mat
    
#function to convert a matrix into numpy matrix
def get_numpy(im):
    im2=np.zeros((len(im),len(im[0])),np.uint8)
    for i in range(len(im)):
        for j in range(len(im[0])):
            im2[i][j]=im[i][j]
    return im2
    
#function to check if zero crossing slope is in threshold(positive) or not
def above_threshold(a,b):
    global threshold
    if(abs(a-b) > threshold):
        return 1
    else:
        return 0


img = cv2.imread('house.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

laplace_kernel1 = [[1,1,1], [1,-8,1], [1,1,1]]
laplace_kernel2 = [[-1,2,-1], [2,-4,2], [-1,2,-1]]

laplace_kernels = [laplace_kernel1, laplace_kernel2]

gaussian_filter_size = 5
threshold = 15
sigmas = [1, 2, 3]

c = 0

for laplace_kernel in laplace_kernels:
    filtered_images = []
    crossing_images = []
    
    c+=1
    s=0
    
    for sigma in sigmas:
        s+=1

        log = get_filter(laplace_kernel, 3, sigma)

        im2 = []
        
        #for each pixel in image apply the filter
        for i in range(len(gray)):
            im2.append([])
            for j in range(len(gray[i])):
                im2[i].append(math.floor(apply_filter(log,len(log),len(log[0]),i,j,gray,len(gray),len(gray[0]))))
        
        #matrix for zero crossings
        crossing = np.zeros((len(im2),len(im2[0])),np.uint8)
        i=0
        #counting total number of zero crossings found
        count=0
        
        #for each pixel
        while(i<len(im2)):
            j=0
            
            while(j<len(im2[i])):
                if(im2[i][j]==0):
                    if(j-1>=0 and j+1<len(im2[i]) and im2[i][j-1]<0 and im2[i][j+1]>0 and above_threshold(im2[i][j-1],im2[i][j+1])):
                        crossing[i][j]=255
                        count+=1
                    if(j-1>=0 and j+1<len(im2[i]) and im2[i][j-1]>0 and im2[i][j+1]<0 and above_threshold(im2[i][j-1],im2[i][j+1])):
                        crossing[i][j]=255
                        count+=1
                    if(i-1>=0 and i+1<len(im2) and im2[i-1][j]<0 and im2[i+1][j]>0 and above_threshold(im2[i-1][j],im2[i+1][j])):
                        crossing[i][j]=255
                        count+=1
                    if(i-1>=0 and i+1<len(im2) and im2[i-1][j]>0 and im2[i+1][j]<0 and above_threshold(im2[i-1][j],im2[i+1][j])):
                        crossing[i][j]=255
                        count+=1
                else:
                    if(j-1>=0 and j+1<len(im2[i]) and im2[i][j-1]<0 and im2[i][j]>0 and above_threshold(im2[i][j-1],im2[i][j])):
                        crossing[i][j]=255
                        count+=1
                    if(j-1>=0 and j+1<len(im2[i]) and im2[i][j-1]>0 and im2[i][j]<0 and above_threshold(im2[i][j-1],im2[i][j])):
                        crossing[i][j]=255
                        count+=1
                    if(i-1>=0 and i+1<len(im2) and im2[i-1][j]<0 and im2[i][j]>0 and above_threshold(im2[i-1][j],im2[i][j])):
                        crossing[i][j]=255
                        count+=1
                    if(i-1>=0 and i+1<len(im2) and im2[i-1][j]>0 and im2[i][j]<0 and above_threshold(im2[i-1][j],im2[i][j])):
                        crossing[i][j]=255
                        count+=1
                j+=1
            i+=1

        print("Number of zero crossings for kernel ",c," and sigma = ",s," are ",count)
        filtered_images.append(get_numpy(im2))
        crossing_images.append(crossing)
    
    val1 = np.concatenate((filtered_images[0],filtered_images[1],filtered_images[2]),axis=1) 
    val2 = np.concatenate((crossing_images[0],crossing_images[1],crossing_images[2]),axis=1) 
    val3 = np.concatenate((val1,val2),axis=0) 
    
    plt.title("Kernel " + str(c) + "(filtered and zero crossing images)")
    plt.imshow(val3)
    print()
    print()
    
'''
observations:
    kernel 1 gives better result for sigma = 2,3
    kernel 2 gives better result for sigma = 1
    for all three sigma values , results of kernel 1 are better than kernel 2
    as we increase sigma value , number of zero crossings first increase and then decrease for given laplace kernels
'''


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