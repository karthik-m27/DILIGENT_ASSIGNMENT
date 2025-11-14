# 🚀 E-Commerce Data Pipeline (Cursor A-SDLC Exercise)

This project implements the complete 30-minute exercise using **Cursor IDE**, covering:

- Generating **synthetic e-commerce data** (5 CSV files)
- Ingesting data into a **SQLite database**
- Running **multi-table SQL JOIN queries**
- Pushing the entire project to **GitHub**

---

## 📂 Project Structure

| File | Description |
|------|-------------|
| `generate_data.py` | Generates all synthetic CSV datasets |
| `ingest_sqlite.py` | Creates `ecom.db` and imports CSVs |
| `sample_query.sql` | Advanced SQL JOIN-based analytics |
| `products.csv` | Products dataset |
| `customers.csv` | Customer dataset |
| `orders.csv` | Orders dataset |
| `order_items.csv` | Order line-items |
| `reviews.csv` | Product reviews |
| `README.md` | Documentation |

---

## 🛠️ 1. Generate Synthetic Data

Run the script:

```bash
python generate_data.py
