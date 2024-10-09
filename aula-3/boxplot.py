import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(10)
data1 = np.random.normal(100, 10, 200)
data2 = np.random.normal(90, 20, 200)
data3 = np.random.normal(110, 5, 200)


plt.boxplot([data1, data2, data3], vert=False, patch_artist=True, boxprops=dict(facecolor='blue'))

plt.title('Boxplot')
plt.ylabel('Valores')
plt.yticks([1,2,3])

plt.show()
