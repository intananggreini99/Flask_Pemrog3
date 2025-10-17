# matriks/validators/is_symmetric.py

def is_symmetric(matrix):
    """Memeriksa apakah matriks bersifat simetris."""
    if matrix.rows != matrix.cols:
        return False

    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if matrix.data[i][j] != matrix.data[j][i]:
                return False
    return True
