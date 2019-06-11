plt.figure(figsize = (15,10))

for gamma in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    output = gray.copy()
    
    for i in range(len(output)):
        for j in range(len(output[i])):
            output[i][j] = output[i][j] ** gamma
    
    plt.subplot(2, 4, gamma*10)
    plt.imshow(output, cmap = "gray")