import numpy as np

# 生成随机矩阵
matrix_A = np.random.randint(low=0, high=100, size=(800, 500))
matrix_B = np.random.randint(low=0, high=100, size=(500, 800))

# 保存矩阵到 CSV 文件
np.savetxt('matrix_A.csv', matrix_A, delimiter=',')
np.savetxt('matrix_B.csv', matrix_B, delimiter=',')