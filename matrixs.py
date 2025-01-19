import numpy as np

# 生成随机矩阵
matrix_A = np.random.rand(2000, 2000)
matrix_B = np.random.rand(2000, 2000)

# 保存矩阵到 CSV 文件
np.savetxt('matrix_A.csv', matrix_A, delimiter=',')
np.savetxt('matrix_B.csv', matrix_B, delimiter=',')