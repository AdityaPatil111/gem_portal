# GeM Catalogue Offering Portal

A web UI that mirrors the GeM portal's Catalogue Offering screen.  
Upload your parts Excel file → view all items → click "Change Catalogue" → fill Make / Model / HSN Code → Save.

## Folder structure
```
gem_portal/
├── main.py            # FastAPI backend
├── requirements.txt
├── README.md
└── static/
    └── index.html     # Frontend UI
```

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 3. Open browser
http://localhost:8000
```

## How it works

1. Open `http://localhost:8000` in your browser.
2. Upload the Excel file (supports drag & drop).
3. All items appear in the table (Item No, Category, Quantity).
4. Click **CHANGE CATALOGUE** on any row → expands fields:
   - **Make** = Item (3rd column in Excel)
   - **Model** = Item Description (4th column)
   - **HSN Code** = last column
5. Click **Save and Continue** — row is marked ✓ Saved, next unsaved item auto-opens.

## Excel Format Expected

| Item Number | Item Title | Item | Item Description | Item Quantity | HSN code |
|-------------|------------|------|-----------------|--------------|----------|
| 1 | EK3000B-3627695 | 3627695 | SEAL O RING | 142 | 40169320 |
