"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional
import datetime as dt

# Example schemas (you can keep or remove as needed):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# --------------------------------------------------
# Business management app schemas (used by the app)
# --------------------------------------------------

class Income(BaseModel):
    """Incomes collection schema (collection name: income)"""
    title: str = Field(..., description="Short title for the income")
    amount: float = Field(..., gt=0, description="Income amount")
    date: dt.date = Field(..., description="Date of income")
    note: Optional[str] = Field(None, description="Optional note")
    category: Optional[str] = Field(None, description="Income category")

class Expense(BaseModel):
    """Expenses collection schema (collection name: expense)"""
    title: str = Field(..., description="Short title for the expense")
    amount: float = Field(..., gt=0, description="Expense amount")
    date: dt.date = Field(..., description="Date of expense")
    note: Optional[str] = Field(None, description="Optional note")
    category: Optional[str] = Field(None, description="Expense category")

class Item(BaseModel):
    """Inventory items collection schema (collection name: item)"""
    name: str = Field(..., description="Item name")
    sku: Optional[str] = Field(None, description="Stock keeping unit")
    quantity: int = Field(0, ge=0, description="Quantity on hand")
    unit_cost: float = Field(0, ge=0, description="Unit cost")
    note: Optional[str] = Field(None, description="Optional note")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
