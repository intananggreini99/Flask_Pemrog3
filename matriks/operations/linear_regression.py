import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matriks.matrix import Matrix
from matriks.operations.multiplier import multiply_matrices
from matriks.operations.subtractor import subtract_matrices

class LinearRegressionApp:
    """
    Model Regresi Linear manual berbasis operasi matriks sendiri.
    Bisa training, prediksi, evaluasi, dan visualisasi.
    """

    # -------------------------------------------------------
    # 🏁 INIT - Setting Awal Model
    # -------------------------------------------------------
    def _init_(self, lr=0.01, n_iters=1000, normalize=True):
        self.lr = lr                      # Learning rate - ukuran langkah perubahan bobot
        self.n_iters = n_iters            # Berapa kali proses update bobot (training)
        self.normalize = normalize        # Apakah fitur X dinormalisasi?
        self.weights = None               # Bobot (koefisien) untuk setiap fitur X
        self.bias = None                  # Intercept (offset) model
        self.loss_history = []            # Menyimpan nilai loss di tiap iterasi training
        self.feature_names = []           # Nama-nama fitur X (jika DataFrame)
        self.target_name = None           # Nama target (kolom y)
        self._mean = None                 # Rata-rata masing-masing fitur X (untuk normalisasi)
        self._std = None                  # Deviasi standar fitur X (untuk normalisasi)
        self.is_trained = False           # Status: model sudah dilatih?

    # -------------------------------------------------------
    # 📘 Persiapan Data
    # -------------------------------------------------------
    def prepare_data(self, df_or_array, feature_cols=None, target_col=None):
        """
        Proses input data, pilih fitur X & target y, normalisasi jika perlu.
        """
        if isinstance(df_or_array, pd.DataFrame):
            df = df_or_array.copy()
            if feature_cols is None:
                feature_cols = df.columns.tolist()
                if target_col and target_col in feature_cols:
                    feature_cols.remove(target_col)
            X = df[feature_cols].values
            y = df[target_col].values if target_col and target_col in df.columns else None
            self.feature_names = feature_cols
            self.target_name = target_col
        else:
            X = np.array(df_or_array)
            y = None

        # Normalisasi fitur jika dipilih
        if self.normalize:
            if self._mean is None or self._std is None or y is not None:
                self._mean = X.mean(axis=0)
                self._std = X.std(axis=0)
                self._std[self._std == 0] = 1.0  # Cegah pembagian nol
            X = (X - self._mean) / self._std

        return X, y

    # -------------------------------------------------------
    # 📑 Persiapan Data Test
    # -------------------------------------------------------
    def prepare_test(self, X):
        """
        Proses data uji: normalisasi X berdasarkan mean & std hasil training.
        """
        X = np.array(X, dtype=float)
        if self.normalize:
            if self._mean is None or self._std is None:
                raise RuntimeError("Model harus sudah di-training agar ada mean/std.")
            X = (X - self._mean) / self._std
        return X

    # -------------------------------------------------------
    # ⚙ Training Model
    # -------------------------------------------------------
    def fit(self, X, y):
        """
        Training model linear regression dengan gradient descent manual.
        """
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float).reshape(-1, 1)
        n_samples, n_features = X.shape

        self.weights = np.zeros((n_features, 1))
        self.bias = 0.0

        X_mat = Matrix(X.tolist())
        y_mat = Matrix(y.tolist())
        theta_mat = Matrix(self.weights.tolist())

        for _ in range(self.n_iters):
            # a. Hitung prediksi: h(x)=Xθ + b (X kali bobot, tambah bias)
            h_mat = multiply_matrices(X_mat, theta_mat)
            h_x = np.array(h_mat.data) + self.bias

            # b. Hitung error prediksi (hasil prediksi - nilai asli)
            error_mat = subtract_matrices(Matrix(h_x.tolist()), y_mat)

            # c. Transpose X dan hitung gradien agar tahu perubahan bobot yang optimal
            X_T = Matrix(np.transpose(X).tolist())
            grad_mat = multiply_matrices(X_T, error_mat)
            grad_np = np.array(grad_mat.data) / n_samples

            # d. Update bobot dan bias model (gradient descent step)
            self.weights -= self.lr * grad_np
            self.bias -= self.lr * np.mean(error_mat.data)

            # e. Simpan nilai loss (MSE) di riwayat training
            loss = np.mean((h_x - y) ** 2)
            self.loss_history.append(float(loss))

            # f. Perbarui theta buat iterasi selanjutnya
            theta_mat = Matrix(self.weights.tolist())

        self.is_trained = True

    # -------------------------------------------------------
    # 🔮 Prediksi
    # -------------------------------------------------------
    def predict(self, X):
        """
        Melakukan prediksi menggunakan bobot dan bias hasil training.
        """
        if self.weights is None:
            raise RuntimeError("Model belum dilatih, jalankan fit() dulu.")
        X = np.array(X, dtype=float)
        return np.dot(X, self.weights) + self.bias

    # -------------------------------------------------------
    # 📊 Evaluasi Model
    # -------------------------------------------------------
    def evaluate(self, X, y, visualize=True, save_path=None):
        """
        Hitung nilai evaluasi model (R2, MSE, RMSE, MAE) dan bisa tampilkan grafik.
        """
        if y is None:
            raise ValueError("Target y harus diisi untuk evaluasi.")

        y = np.array(y, dtype=float).reshape(-1, 1)
        y_pred = self.predict(X)

        mse = float(np.mean((y - y_pred) ** 2))
        rmse = float(np.sqrt(mse))
        mae = float(np.mean(np.abs(y - y_pred)))
        ss_res = float(np.sum((y - y_pred) ** 2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2))
        r2 = float(1 - (ss_res / ss_tot)) if ss_tot != 0 else 0.0

        metrics = {"R2": r2, "MSE": mse, "RMSE": rmse, "MAE": mae}

        if visualize:
            self._plot_evaluation(y, y_pred, save_path)

        return metrics

    # -------------------------------------------------------
    # 🎨 Visualisasi Hasil
    # -------------------------------------------------------
    def _plot_evaluation(self, y_true, y_pred, save_path=None):
        """
        Buat grafik: Prediksi vs Asli (kiri), Training Loss (kanan).
        """
        plt.figure(figsize=(10, 4))

        # Plot kiri: tiap titik (harga asli vs harga prediksi)
        plt.subplot(1, 2, 1)
        plt.scatter(y_true, y_pred, color="blue", s=10)
        plt.plot([min(y_true), max(y_true)],
                 [min(y_true), max(y_true)],
                 color="red", linewidth=2)
        plt.xlabel("True Values")
        plt.ylabel("Predicted Values")
        plt.title("Predicted vs True Values")
        plt.grid(True, linestyle="--", alpha=0.6)

        # Plot kanan: Riwayat nilai loss/MSE selama training
        plt.subplot(1, 2, 2)
        plt.plot(range(len(self.loss_history)), self.loss_history, color="green", linewidth=2)
        plt.xlabel("Iterations")
        plt.ylabel("Loss (MSE)")
        plt.title("Training Loss Curve")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            plt.close()

    # -------------------------------------------------------
    # 🧾 Ringkasan Model
    # -------------------------------------------------------
    def summary(self):
        """
        Print ringkasan model (parameter, bobot setiap fitur, dan bias).
        """
        if self.weights is None:
            print("Model belum dilatih.")
            return
        print("\n📘 Model Summary")
        print(f"Learning rate: {self.lr}")
        print(f"Iterations: {self.n_iters}")
        print(f"Normalize: {self.normalize}")
        for i, name in enumerate(self.feature_names):
            print(f"  {name}: {self.weights[i, 0]:.6f}")
        print(f"Intercept (bias): {self.bias:.6f}")
