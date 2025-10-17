# matriks/validators/is_identity.py

def is_identity(matrix):
    """Memeriksa apakah matriks merupakan matriks identitas."""
    if matrix.rows != matrix.cols:
        return False

    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if i == j:
                if matrix.data[i][j] != 1:
                    return False
            else:
                if matrix.data[i][j] != 0:
                    return False
    return True
