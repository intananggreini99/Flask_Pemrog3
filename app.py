from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import certifi
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
from matriks.operations.linear_regression import LinearRegressionApp

load_dotenv()

app = Flask(__name__)
app.secret_key = "secret_regression_app"

PLOT_FOLDER = "static/plots"
os.makedirs(PLOT_FOLDER, exist_ok=True)

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "regression_app")
client = MongoClient(
    MONGO_URI,
    tls=True,
    retryWrites=False,
    tlsCAFile=certifi.where())
db = client[MONGO_DB]

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------------------
# 🧩 Halaman 1 — Upload data dan simpan user
# ---------------------------------------------
@app.route("/", methods=["GET", "POST"])
def page1_upload():
    if request.method == "POST":
        nama_user = request.form["nama_user"]
        train_file = request.files["train_file"]
        test_file = request.files["test_file"]

        # simpan file
        train_path = os.path.join(UPLOAD_FOLDER, "training", train_file.filename)
        test_path = os.path.join(UPLOAD_FOLDER, "testing", test_file.filename)
        os.makedirs(os.path.dirname(train_path), exist_ok=True)
        os.makedirs(os.path.dirname(test_path), exist_ok=True)
        train_file.save(train_path)
        test_file.save(test_path)

        # simpan ke MongoDB
        result = db.submissions.insert_one({
            "nama_user": nama_user,
            "file_train": train_path,
            "file_test": test_path,
            "created_at": datetime.now()
        })

        # simpan id ke session
        session["submission_id"] = str(result.inserted_id)
        return redirect(url_for("page2_variables"))
    return render_template("page1_upload.html")


# ------------------------------------------------
# 🧩 Halaman 2 — Pilih variabel dan jalankan regresi
# ------------------------------------------------
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

        # Jalankan regresi linear
        model = LinearRegressionApp()
        X = df[x_columns].values
        y = df[y_column].values
        model.fit(X, y)
        metrics = model.evaluate(X, y, visualize=False)

        # Simpan visualisasi
        nama_user = submission["nama_user"].replace(" ", "_")
        plot_filename = f"result_{nama_user}.png"
        plot_path = os.path.join("static", "plots", plot_filename)
        os.makedirs(os.path.dirname(plot_path), exist_ok=True)

        # Simpan visualisasi tanpa GUI
        model._plot_evaluation(y, model.predict(X))
        plt.savefig(plot_path, bbox_inches="tight")
        plt.close()

        # Simpan hanya nama file ke MongoDB
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


# ------------------------------------------
# 🧩 Halaman 3 — Menampilkan hasil regresi
# ------------------------------------------
@app.route("/result")
def page3_result():
    submission_id = session.get("submission_id")
    if not submission_id:
        return redirect(url_for("page1_upload"))

    data = db.submissions.find_one({"_id": ObjectId(submission_id)})
    df = pd.read_csv(data["file_train"]).head(7)
    return render_template("page3_result.html", data=data, table=df.to_html(classes="table table-striped"))


if __name__ == "__main__":
    app.run(debug=True)
