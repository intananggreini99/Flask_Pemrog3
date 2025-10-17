from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import certifi
from bson.objectid import ObjectId
from dotenv import load_dotenv
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
from matriks.operations.linear_regression import LinearRegressionApp

# --------------------------------------------------------
# Konfigurasi Awal
# --------------------------------------------------------
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secret_regression_app")

UPLOAD_FOLDER = "uploads"
PLOT_FOLDER = "static/plots"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

# --------------------------------------------------------
# Koneksi MongoDB
# --------------------------------------------------------
MONGO_URI = os.getenv(
    "MONGO_URI",
    "MONGO_URI=mongodb://intanchris:sdt25@mongo:27017/appdb?authSource=appdb"
)
MONGO_DB = os.getenv("MONGO_DB", "appdb")

client = MongoClient(
    MONGO_URI,
    tls=False,
    retryWrites=False,
    tlsCAFile=certifi.where() if "mongodb+srv" in MONGO_URI else None
)
db = client[MONGO_DB]

# --------------------------------------------------------
# 🧩 Halaman 1 — Upload Data
# --------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def page1_upload():
    if request.method == "POST":
        nama_user = request.form["nama_user"]
        train_file = request.files["train_file"]
        test_file = request.files["test_file"]

        # Simpan file ke folder uploads/
        train_path = os.path.join(UPLOAD_FOLDER, "training", train_file.filename)
        test_path = os.path.join(UPLOAD_FOLDER, "testing", test_file.filename)
        os.makedirs(os.path.dirname(train_path), exist_ok=True)
        os.makedirs(os.path.dirname(test_path), exist_ok=True)
        train_file.save(train_path)
        test_file.save(test_path)

        # Simpan metadata ke MongoDB
        result = db.submissions.insert_one({
            "nama_user": nama_user,
            "file_train": train_path,
            "file_test": test_path,
            "created_at": datetime.now()
        })

        # Simpan ID ke session untuk halaman berikutnya
        session["submission_id"] = str(result.inserted_id)
        return redirect(url_for("page2_variables"))

    return render_template("page1_upload.html")


# --------------------------------------------------------
# 🧩 Halaman 2 — Pilih Variabel dan Jalankan Model Custom
# --------------------------------------------------------
@app.route("/variables", methods=["GET", "POST"])
def page2_variables():
    submission_id = session.get("submission_id")
    if not submission_id:
        return redirect(url_for("page1_upload"))

    submission = db.submissions.find_one({"_id": ObjectId(submission_id)})
    df = pd.read_csv(submission["file_train"])

    if request.method == "POST":
        x_columns = request.form.getlist("x_columns")
        y_column = request.form["y_column"]

        # Gunakan model custom dari matriks/
        model = LinearRegressionApp()
        X = df[x_columns].values
        y = df[y_column].values

        model.fit(X, y)
        metrics = model.evaluate(X, y, visualize=False)

        # Simpan plot hasil regresi
        nama_user = submission["nama_user"].replace(" ", "_")
        plot_filename = f"result_{nama_user}.png"
        plot_path = os.path.join(PLOT_FOLDER, plot_filename)

        model._plot_evaluation(y, model.predict(X))
        plt.savefig(plot_path, bbox_inches="tight")
        plt.close()

        # Simpan ke MongoDB
        db.submissions.update_one(
            {"_id": ObjectId(submission_id)},
            {"$set": {
                "x_columns": x_columns,
                "y_column": y_column,
                "evaluasi": metrics,
                "visualisasi_path": plot_filename
            }}
        )
        return redirect(url_for("page3_result"))

    columns = df.columns.tolist()
    return render_template("page2_variables.html", columns=columns)


# --------------------------------------------------------
# 🧩 Halaman 3 — Menampilkan Hasil Regresi
# --------------------------------------------------------
@app.route("/result")
def page3_result():
    submission_id = session.get("submission_id")
    if not submission_id:
        return redirect(url_for("page1_upload"))

    data = db.submissions.find_one({"_id": ObjectId(submission_id)})
    df_preview = pd.read_csv(data["file_train"]).head(7)

    return render_template(
        "page3_result.html",
        data=data,
        table=df_preview.to_html(classes="table table-striped table-sm text-white", border=0)
    )


# --------------------------------------------------------
# Endpoint Healthcheck (untuk Docker)
# --------------------------------------------------------
@app.route("/healthz")
def healthz():
    try:
        client.admin.command("ping")
        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "fail", "error": str(e)}, 500


# --------------------------------------------------------
# Entry Point
# --------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)