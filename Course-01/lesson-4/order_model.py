from pydantic import BaseModel
from typing import List, Optional


class OrderItem(BaseModel):
    """Represents a single item within an order."""
    sku: str  # Stock Keeping Unit (required)
    quantity: int  # Required quantity
    item_name: Optional[str] = None  # Optional item name


class Order(BaseModel):
    """Represents the structure for an incoming order."""
    order_id: int  # Required order identifier
    customer_email: Optional[str] = None  # Optional customer email
    items: List[OrderItem]  # Required list of OrderItem objects
    total_amount: float  # Required total amount
