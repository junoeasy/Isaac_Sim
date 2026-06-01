import numpy as np
A=np.array([2,1],
           [5,3])
A_inv=np.linalg.inv(A)

result_at=A @ A_inv
result_star= A*A_inv
print("--- A @ A_inv 결과 ---")
print(np.round(result_at))
print("--- A * A_inv 결과 ---")
print(result_star)