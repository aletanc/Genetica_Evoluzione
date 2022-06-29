import numpy as np

def nw(x, y, match = 1, mismatch = 1, gap = 1):
    nx = len(x)
    ny = len(y)
    # Optimal score at each possible pair of characters.
    F = np.zeros((nx + 1, ny + 1))
    F[:,0] = np.linspace(0, -nx * gap, nx + 1)
    F[0,:] = np.linspace(0, -ny * gap, ny + 1)
    # Pointers to trace through an optimal aligment.
    P = np.zeros((nx + 1, ny + 1))
    P[:,0] = 3
    P[0,:] = 4
    # Temporary scores.
    t = np.zeros(3)
    for i in range(nx):
        for j in range(ny):
            if x[i] == y[j]:
                t[0] = F[i,j] + match
            else:
                t[0] = F[i,j] - mismatch
            t[1] = F[i,j+1] - gap
            t[2] = F[i+1,j] - gap
            tmax = np.max(t)
            F[i+1,j+1] = tmax
            if t[0] == tmax:
                P[i+1,j+1] += 2
            if t[1] == tmax:
                P[i+1,j+1] += 3
            if t[2] == tmax:
                P[i+1,j+1] += 4
    # Trace through an optimal alignment.
    i = nx
    j = ny
    rx = []
    ry = []
    while i > 0 or j > 0:
        if P[i,j] in [2, 5, 6, 9]:
            rx.append(x[i-1])
            ry.append(y[j-1])
            i -= 1
            j -= 1
        elif P[i,j] in [3, 5, 7, 9]:
            rx.append(x[i-1])
            ry.append('-')
            i -= 1
        elif P[i,j] in [4, 6, 7, 9]:
            rx.append('-')
            ry.append(y[j-1])
            j -= 1
    # Reverse the strings.
    rx = ''.join(rx)[::-1]
    ry = ''.join(ry)[::-1]
    return '\n'.join([rx, ry])

np.random.seed(1234)

n = []
t = []

x = np.random.choice(['A', 'T', 'G', 'C'], 10)
y = np.random.choice(['A', 'T', 'G', 'C'], 10)
print("".join(x))
print("".join(y))
print("migliori allineamenti: ")
print(nw(x, y))

verbose = False
for i in range(1000 - 1):

    i+=1
    
    x = np.random.choice(['A', 'T', 'G', 'C'], i)
    y = np.random.choice(['A', 'T', 'G', 'C'], i)

    if verbose:
        print("".join(x))
        print("".join(y))
        print("migliori allineamenti: ")

    import time

    start = time.time()
    
    nww = nw(x, y)
    if verbose:
        print(nww)

    stop = time.time()
    if verbose:
        print("lunghezza ",len(x))
    print(i)
    print("tempo: %0.4f sec" % (stop-start))

    n.append(i)
    t.append(stop-start)

#esporto i dati sui calcoli temporali per non doverli rifare
import pandas as pd
df = pd.DataFrame()
df["lenght"] = n
df["time"] = t

df.to_csv(r'NeedlemanWunschTimeComplexity.csv', index=False)

# import i dati sui calcoli temporali

read_df = pd.read_csv('NeedlemanWunschTimeComplexity.csv')
x = read_df["lenght"]
y = read_df["time"]

import matplotlib.pyplot as plt

plt.plot(x, y, '.')
plt.xlabel("lunghezza sequenza")
plt.ylabel("tempo (s)")
plt.title("Programmazione dinamica")
plt.show()