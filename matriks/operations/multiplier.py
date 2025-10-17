from ..matrix import Matrix

def multiply_matrices(matrix1, matrix2):
    """
    Melakukan operasi perkalian pada dua objek matriks.
    """
    if matrix1.cols != matrix2.rows:
        raise ValueError("Jumlah kolom matriks pertama harus sama dengan jumlah baris matriks kedua untuk perkalian.")

    result_data = [[0 for _ in range(matrix2.cols)] for _ in range(matrix1.rows)]
    
    for i in range(matrix1.rows):
        for j in range(matrix2.cols):
            for k in range(matrix1.cols):
                result_data[i][j] += matrix1.data[i][k] * matrix2.data[k][j]
    
    return Matrix(result_data)
