import numpy as np

# Método de Gauss-Seidel para sistemas de ecuaciones lineales
def G_seidel(A, b, xo, tol):
    D = np.diag(np.diag(A))
    U = D - np.triu(A)
    L = D - np.tril(A)

    tg = np.dot(np.linalg.inv((D - L)), U)
    cg = np.dot(np.linalg.inv((D - L)), b)

    lam, v = np.linalg.eig(tg)

    if (max(abs(lam)) < 1):
        x1 = np.dot(tg, xo) + cg
        i = 1
        lista = []
        while(max(abs(x1 - xo)) > tol):
            lista.append([x1, max(abs(x1 - xo))])
            xo = x1
            x1 = np.dot(tg, xo) + cg
            i += 1
        lista.append([x1, max(abs(x1 - xo))])
        return x1, lista
    else:
        print(f'El sistema iterativo con vector inicial en {xo} no converge')
    return None, None

# Eliminación Gaussiana para sistemas de ecuaciones lineales
def Eliminacion_Gaussiana(A, b):
    n = len(b)
    x = np.zeros(n)
    for k in range(0, n - 1):
        for i in range(k + 1, n):
            lam = A[i, k] / (A[k, k])
            A[i, k:n] = A[i, k:n] - lam * A[k, k:n]
            b[i] = b[i] - lam * b[k]
    for k in range(n - 1, -1, -1):
        x[k] = (b[k] - np.dot(A[k, k + 1:n], x[k + 1:n])) / (A[k, k])
    return x

# Gauss-Seidel Matricial para sistemas de ecuaciones lineales
def Gauss_sum(A, B, X0, tol):
    n = len(B)
    norm = 2
    cont = 0
    M = 50
    X1 = np.zeros(n)
    while(norm >= tol or cont > M):
        for i in range(n):
            aux = 0
            for j in range(n):
                if (i != j):
                    aux = aux - A[i, j] * X0[j]
            X1[i] = (B[i] + aux) / A[i, i]
            norm = np.max(np.abs(X1 - X0))
            X0 = X1
        cont += 1
    return X1

# Función de pivoteo
def pivoteo(A, b):
    n = len(b)
    for i in range(n):
        max_index = abs(A[i:, i]).argmax() + i
        A[[i, max_index]] = A[[max_index, i]]
        b[[i, max_index]] = b[[max_index, i]]
    return A, b
