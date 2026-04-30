import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pandas as pd
import io
import json

app = FastAPI(title="GeM Catalogue Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents), header=None)

    # Find the header row (row with "Item Number")
    header_row = None
    for i, row in df.iterrows():
        if any(str(v).strip().lower() in ["item number", "item no"] for v in row.values if pd.notna(v)):
            header_row = i
            break

    if header_row is None:
        return {"error": "Could not find header row in Excel"}

    df.columns = df.iloc[header_row]
    df = df.iloc[header_row + 1:].reset_index(drop=True)

    # Normalize column names
    col_map = {}
    for col in df.columns:
        if pd.isna(col):
            continue
        c = str(col).strip().lower()
        if "item number" in c or "item no" in c:
            col_map[col] = "item_number"
        elif "item title" in c:
            col_map[col] = "item_title"
        elif "item description" in c:
            col_map[col] = "item_description"
        elif "item quantity" in c or "quantity" in c:
            col_map[col] = "quantity"
        elif "hsn" in c:
            col_map[col] = "hsn_code"
        elif col_map.get(col) is None and "item" in c:
            col_map[col] = "make"

    df = df.rename(columns=col_map)

    # Keep only needed columns
    needed = ["item_number", "item_title", "make", "item_description", "quantity", "hsn_code"]
    existing = [c for c in needed if c in df.columns]
    df = df[existing].dropna(subset=["item_number"])

    items = []
    for _, row in df.iterrows():
        item = {}
        for col in existing:
            val = row.get(col)
            item[col] = "" if pd.isna(val) else str(val).strip()
        # item_number as integer string
        try:
            item["item_number"] = str(int(float(item["item_number"])))
        except:
            pass
        items.append(item)

    return {"items": items, "total": len(items)}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join(STATIC_DIR, "index.html"), encoding="utf-8") as f:
        return f.read()
 
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
