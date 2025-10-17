from matriks.matrix import Matrix

def print_matrix(matrix):
    """
    Mencetak isi dari objek matriks.
    """
    for row in matrix.data:
        print(row)

def find_determinant(matrix):
    """Menghitung determinan dari matriks persegi."""
    if matrix.rows != matrix.cols:
        raise ValueError("Matriks harus persegi untuk menghitung determinan.")

    if matrix.rows == 1:
        return matrix.data[0][0]

    if matrix.rows == 2:
        return matrix.data[0][0]*matrix.data[1][1] - matrix.data[0][1]*matrix.data[1][0]

    det = 0
    for c in range(matrix.cols):
        minor = [
            [matrix.data[i][j] for j in range(matrix.cols) if j != c]
            for i in range(1, matrix.rows)
        ]
        sign = (-1) ** c
        det += sign * matrix.data[0][c] * find_determinant(Matrix(minor))
    return det

def is_square(matrix):
    """Memeriksa apakah matriks berbentuk persegi."""
    return matrix.rows == matrix.cols