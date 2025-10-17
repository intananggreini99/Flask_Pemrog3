# matriks/main.py

import time
from matriks.matrix import Matrix
from matriks.operations.adder import add_matrices
from matriks.operations.multiplier import multiply_matrices
from matriks.operations.determinant import determinant
from matriks.utilities import print_matrix
from matriks.validators.is_identity import is_identity
from matriks.validators.is_square import is_square
from matriks.validators.is_symmetric import is_symmetric
from matriks.exporters.csv_exporter import export_to_csv
from matriks.structures.sparsematrix import SparseMatrix

def create_sparse_data(size):
    data = [[0] * size for _ in range(size)]
    data[0][0] = 1
    data[size-1][size-1] = 1
    return data

if __name__ == "__main__":

    print("\n--- Menguji Solusi dengan SparseMatrix ---")
    sparse_data_1000 = create_sparse_data(1000)
    
    # Perhatikan: kita instansiasi SparseMatrix
    mat_a = SparseMatrix(sparse_data_1000)
    mat_b = SparseMatrix(sparse_data_1000)
    
    start_time = time.time()
    
    # Perhatikan: fungsi multiply_matrices() tidak berubah sama sekali
    product_mat = multiply_matrices(mat_a, mat_b)
    end_time = time.time()

    print(f"Waktu yang dibutuhkan untuk perkalian: {end_time - start_time:.2f} detik")

    print("\n--- Pembuktian OCP dengan Penjumlahan ---")
    # Matriks padat (dense)
    matriks_padat = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # Matriks jarang (sparse) yang memiliki nilai yang sama
    matriks_jarang = SparseMatrix([[1, 0, 0], [0, 5, 0], [7, 0, 9]])

    # Lakukan penjumlahan matriks padat + matriks jarang
    # Perhatikan: fungsi 'add_matrices()' tidak diubah sama sekali
    hasil_penjumlahan = add_matrices(matriks_padat, matriks_jarang)

    print("Hasil Penjumlahan Matriks Biasa dan Sparse:")
    print(hasil_penjumlahan)
