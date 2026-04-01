from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

df_products = pd.read_csv("source_data/products/product_master.csv")

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(df_products.to_dict(orient="records"))

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "rows": len(df_products)})
