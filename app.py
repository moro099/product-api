 from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

PRODUCT_CSV = "source_data/products/product_master.csv"

df_products = pd.read_csv(PRODUCT_CSV)
df_products["last_updated"] = pd.to_datetime(df_products["last_updated"])


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Product API is running",
        "endpoints": {
            "health": "/health",
            "full_load": "/products",
            "incremental_load_example": "/products?updated_after=2026-01-10 00:00:00"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "rows": len(df_products)})


@app.route("/products", methods=["GET"])
def get_products():
    updated_after = request.args.get("updated_after")

    filtered_df = df_products.copy()

    if updated_after:
        try:
            updated_after_dt = pd.to_datetime(updated_after)
            filtered_df = filtered_df[filtered_df["last_updated"] > updated_after_dt]
        except Exception:
            return jsonify({"error": "Invalid updated_after format. Use YYYY-MM-DD HH:MM:SS"}), 400

    result_df = filtered_df.copy()
    result_df["last_updated"] = result_df["last_updated"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify(result_df.to_dict(orient="records"))


@app.route("/products/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    result = df_products[df_products["product_id"] == product_id]
    if result.empty:
        return jsonify({"message": "Product not found"}), 404

    row = result.iloc[0].copy()
    row["last_updated"] = pd.to_datetime(row["last_updated"]).strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(row.to_dict())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
