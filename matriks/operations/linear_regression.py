# matriks/operations/linear_regression_numpy.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matriks.matrix import Matrix
from matriks.operations.multiplier import multiply_matrices
from matriks.operations.subtractor import subtract_matrices


class LinearRegressionApp:
    """
    Implementasi Regresi Linear dengan operasi matriks internal.
    Bisa digunakan untuk training, prediksi, dan evaluasi.
    """

    def __init__(self, lr=0.01, n_iters=1000, normalize=True):
        self.lr = lr
        self.n_iters = n_iters
        self.normalize = normalize
        self.weights = None
        self.bias = None
        self.loss_history = []
        self.feature_names = []
        self.target_name = None
        self._mean = None
        self._std = None
        self.is_trained = False

    # -------------------------------------------------------
    # 📘 Persiapan data
    # -------------------------------------------------------
    def prepare_data(self, df_or_array, feature_cols=None, target_col=None):
        """
        Mempersiapkan data X dan y dari DataFrame atau array.
        Jika target_col tidak diberikan, hanya mengembalikan X (untuk prediksi).
        """
        if isinstance(df_or_array, pd.DataFrame):
            df = df_or_array
            if feature_cols is None:
                # jika tidak ditentukan, gunakan semua kolom kecuali target
                feature_cols = df.columns.tolist()
                if target_col and target_col in feature_cols:
                    feature_cols.remove(target_col)
            X = df[feature_cols].values

            # jika kolom target ada, ambil y
            y = df[target_col].values if target_col and target_col in df.columns else None

            self.feature_names = feature_cols
            self.target_name = target_col
        else:
            X = np.array(df_or_array)
            y = None

        # normalisasi
        if self.normalize:
            if self._mean is None or self._std is None or y is not None:
                # hitung ulang mean/std hanya pada data training
                self._mean = X.mean(axis=0)
                self._std = X.std(axis=0)
                self._std[self._std == 0] = 1.0
            X = (X - self._mean) / self._std

        return X, y

    def prepare_test(self, X):
        """Normalisasi X test berdasarkan mean/std training."""
        X = np.array(X, dtype=float)
        if self.normalize:
            if self._mean is None or self._std is None:
                raise RuntimeError("Model belum dilatih: tidak ada mean/std.")
            X = (X - self._mean) / self._std
        return X

    # -------------------------------------------------------
    # ⚙️ Training model
    # -------------------------------------------------------
    def fit(self, X, y):
        """Melatih model regresi linear menggunakan gradient descent."""
        X = np.array(X, dtype=float)
        y = np.array(y, dtype=float).reshape(-1, 1)
        n_samples, n_features = X.shape

        self.weights = np.zeros((n_features, 1))
        self.bias = 0.0

        X_mat = Matrix(X.tolist())
        y_mat = Matrix(y.tolist())
        theta_mat = Matrix(self.weights.tolist())

        for _ in range(self.n_iters):
            # h(x) = Xθ + b
            h_mat = multiply_matrices(X_mat, theta_mat)
            h_x = np.array(h_mat.data) + self.bias

            # error = h(x) - y
            error_mat = subtract_matrices(Matrix(h_x.tolist()), y_mat)

            # gradien
            X_T = Matrix(np.transpose(X).tolist())
            grad_mat = multiply_matrices(X_T, error_mat)
            grad_np = np.array(grad_mat.data) / n_samples

            self.weights -= self.lr * grad_np
            self.bias -= self.lr * np.mean(error_mat.data)

            # hitung loss
            loss = np.mean((h_x - y) ** 2)
            self.loss_history.append(float(loss))
            theta_mat = Matrix(self.weights.tolist())

        self.is_trained = True

    # -------------------------------------------------------
    # 🔮 Prediksi
    # -------------------------------------------------------
    def predict(self, X):
        """Melakukan prediksi, baik pada data training atau testing."""
        if self.weights is None:
            raise RuntimeError("Model belum dilatih. Jalankan fit() terlebih dahulu.")
        X = np.array(X, dtype=float)
        return np.dot(X, self.weights) + self.bias

    # -------------------------------------------------------
    # 📊 Evaluasi
    # -------------------------------------------------------
    def evaluate(self, X, y, visualize=True, save_path=None):
        """
        Menghitung metrik evaluasi (R2, MSE, RMSE, MAE).
        Dapat digunakan setelah prediksi dilakukan.
        """
        if y is None:
            raise ValueError("Kolom target (y) tidak ditemukan untuk evaluasi.")

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
    # 🎨 Visualisasi
    # -------------------------------------------------------
    def _plot_evaluation(self, y_true, y_pred, save_path=None):
        """Plot prediksi vs nilai aktual + loss curve."""
        plt.figure(figsize=(10, 4))

        # Subplot 1: Predicted vs True
        plt.subplot(1, 2, 1)
        plt.scatter(y_true, y_pred, color="blue", s=10)
        plt.plot([min(y_true), max(y_true)],
                 [min(y_true), max(y_true)],
                 color="red", linewidth=2)
        plt.xlabel("True Values")
        plt.ylabel("Predicted Values")
        plt.title("Predicted vs True Values")
        plt.grid(True, linestyle="--", alpha=0.6)

        # Subplot 2: Loss Curve
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
    # 🧾 Info model
    # -------------------------------------------------------
    def summary(self):
        """Menampilkan ringkasan model."""
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
