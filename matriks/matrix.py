class Matrix:
    """
    Kelas untuk merepresentasikan objek matriks.
    """
    def __init__(self, data):
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            raise TypeError("Data harus berupa list of lists.")

        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

        if not all(len(row) == self.cols for row in data):
            raise ValueError("Semua baris harus memiliki jumlah kolom yang sama.")
