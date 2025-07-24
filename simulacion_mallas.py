import numpy as np

# Valores de resistencias y voltajes para 3 mallas
R1 = 10  # Entre nodo 1 y 2
R2 = 20  # Entre nodo 2 y 3
R3 = 30  # Entre nodo 3 y 1
R4 = 15  # Entre nodo 1 y tierra
R5 = 25  # Entre nodo 2 y tierra
R6 = 35  # Entre nodo 3 y tierra
V1 = 12  # Fuente en malla 1
V2 = 5   # Fuente en malla 2
V3 = 8   # Fuente en malla 3

# Matriz de coeficientes para 3 mallas
A = np.array([
    [R1 + R3 + R4, -R1, -R3],
    [-R1, R1 + R2 + R5, -R2],
    [-R3, -R2, R2 + R3 + R6]
])

# Vector de voltajes
B = np.array([V1, V2, V3])

# Resolver el sistema de ecuaciones
I = np.linalg.solve(A, B)

print(f"Corriente en la malla 1: {I[0]:.2f} A")
print(f"Corriente en la malla 2: {I[1]:.2f} A")
print(f"Corriente en la malla 3: {I[2]:.2f} A") 