import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from database import create_document, get_documents, db
from schemas import Income, Expense, Item

app = FastAPI(title="Small Business Manager API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Small Business Manager API"}

# Simple dashboard summary
class Summary(BaseModel):
    total_income: float
    total_expense: float
    inventory_value: float

@app.get("/api/summary", response_model=Summary)
def get_summary():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")

    # Aggregate totals
    incomes = get_documents("income")
    expenses = get_documents("expense")
    items = get_documents("item")

    total_income = float(sum(i.get("amount", 0) for i in incomes))
    total_expense = float(sum(e.get("amount", 0) for e in expenses))
    inventory_value = float(sum((it.get("quantity", 0) or 0) * (it.get("unit_cost", 0) or 0) for it in items))

    return Summary(total_income=total_income, total_expense=total_expense, inventory_value=inventory_value)

# Create endpoints (create only; read is via list)
@app.post("/api/incomes")
def create_income(payload: Income):
    _id = create_document("income", payload)
    return {"id": _id}

@app.get("/api/incomes")
def list_incomes():
    docs = get_documents("income", limit=500)
    return docs

@app.post("/api/expenses")
def create_expense(payload: Expense):
    _id = create_document("expense", payload)
    return {"id": _id}

@app.get("/api/expenses")
def list_expenses():
    docs = get_documents("expense", limit=500)
    return docs

@app.post("/api/items")
def create_item(payload: Item):
    _id = create_document("item", payload)
    return {"id": _id}

@app.get("/api/items")
def list_items():
    docs = get_documents("item", limit=500)
    return docs

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
