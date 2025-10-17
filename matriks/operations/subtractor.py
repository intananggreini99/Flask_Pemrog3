from ..matrix import Matrix

def subtract_matrices(matrix1, matrix2):
    """
    Melakukan operasi pengurangan pada dua objek matriks.
    """
    if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
        raise ValueError("Matriks harus memiliki dimensi yang sama untuk pengurangan.")

    result_data = [[0 for _ in range(matrix1.cols)] for _ in range(matrix1.rows)]
    for i in range(matrix1.rows):
        for j in range(matrix1.cols):
            result_data[i][j] = matrix1.data[i][j] - matrix2.data[i][j]

    return Matrix(result_data)
