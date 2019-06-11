plt.figure(figsize = (18, 12))

binary = []

def decimalToBinary(x):
    ans = ""
    for i in range(8):
        ans += str(x%2)
        x //= 2
    return ans[::-1]

for i in range(len(gray)):
    binary.append([])
    for j in range(len(gray[i])):
        binary[i].append(decimalToBinary(gray[i][j]))
    
for bit in range(7,-1,-1):
    new_img = np.zeros((len(gray), len(gray[0])), np.uint8)
        
    for i in range(len(gray)):
        for j in range(len(gray[i])):
            if(binary[i][j][bit] == '1'):
                new_img[i][j] = 255
            else:
                new_img[i][j] = 0
        
    plt.subplot(2, 4, 8-bit)
    plt.imshow(new_img, cmap = "gray")