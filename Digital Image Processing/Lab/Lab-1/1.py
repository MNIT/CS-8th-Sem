'''
Write a function that computes the histogram of the given. Do not use specific Python
functions for histogram computation (like hist).
'''

hist = []

for i in range(256):
    hist.append(0)

for i in range(len(gray)):
    for j in range(len(gray[i])):
        hist[gray[i][j]] += 1

plt.axis([0,255,0,max(hist)+300])        
for i in range(256):
    plt.plot([i,i], [0, hist[i]], color = "blue")

plt.show()