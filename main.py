import numpy as np
import tracker

mtx = [
    [1893.467163759115, 0, 858.5694304386387],
    [0, 1872.633927665982, 363.4403478426465],
    [0, 0, 1]
]

dist = [0.09027454545326657, 0.01970389139323089, \
    -0.009913299829184851, -0.01689213111040934, -0.5511020458301069]

mtx = (np.array(mtx, dtype=np.float32))
dist = (np.array(dist, dtype=np.float32))

s8 = tracker.Tracker(mtx, dist)
s8.run('video', 'trip.mp4')
