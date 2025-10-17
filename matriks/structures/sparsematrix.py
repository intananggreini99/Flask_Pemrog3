# matriks/sparsematrix.py
from matriks.matrix import Matrix

class SparseMatrix(Matrix):
    """
    Representasi matriks jarang (sparse) yang lebih efisien.
    Mematuhi LSP karena dapat menggantikan Matrix biasa.
    """
    def __init__(self, data):
        # Baris ini memanggil konstruktor kelas induk (Matrix)
        super().__init__(data)
        self._sparse_data = {}
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                if val != 0:
                    self._sparse_data[(r, c)] = val

    def get_value(self, row, col):
        return self._sparse_data.get((row, col), 0)
    
    def __str__(self):
        output = ""
        for r in range(self.rows):
            row_str = []
            for c in range(self.cols):
                row_str.append(str(self.get_value(r, c)))
            output += " ".join(row_str) + "\n"
        return output.strip()
