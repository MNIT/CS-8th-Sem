output = gray.copy()
max_val = np.max(gray)

c = 255/math.log(1 + max_val)

for i in range(len(output)):
    for j in range(len(output[i])):
        output[i][j] = c * math.log(1 + output[i][j])

plt.imshow(output, cmap = "gray")