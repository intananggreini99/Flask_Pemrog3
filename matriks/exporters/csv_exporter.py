import csv
def export_to_csv(matrix, filename):
    
    """Mengekspor data matriks ke file CSV."""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(matrix.data)
    print(f"Matriks berhasil diekspor ke {filename}")