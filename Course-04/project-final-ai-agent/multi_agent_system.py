"""
Multi-Agent Inventory & Sales System for The Beaver's Choice Paper Company
===========================================================================

This system implements a multi-agent architecture with the following components:
- Orchestrator Agent: Coordinates all operations using managed_agents pattern
- Inventory Management Agent: Handles stock queries and reorder decisions
- Quote Generation Agent: Creates competitive quotes with appropriate discounts
- Sales Transaction Agent: Processes orders and manages financial transactions

Framework: smolagents with managed_agents delegation pattern
Database: SQLite (munder_difflin.db)
"""

import pandas as pd
import numpy as np
import os
import time
import dotenv
import ast
import logging
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from typing import Dict, List, Union
from sqlalchemy import create_engine, Engine

# Import smolagents framework
from smolagents import tool, ToolCallingAgent, OpenAIServerModel

# Configure logging to track agent execution
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from parent directory if not found locally
from dotenv import load_dotenv
import sys

# Try loading from current directory first, then parent
if not load_dotenv():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(parent_dir, '.env')
    load_dotenv(env_path)

# Validate environment variables
if not os.getenv("UDACITY_OPENAI_API_KEY"):
    raise ValueError("Missing UDACITY_OPENAI_API_KEY environment variable")
if not os.getenv("OPENAI_BASE_URL"):
    raise ValueError("Missing OPENAI_BASE_URL environment variable")

# ============================================================================
# DATABASE SETUP AND HELPER FUNCTIONS (from project_starter.py)
# ============================================================================

# Create an SQLite database
db_engine = create_engine("sqlite:///munder_difflin.db")

# List containing the different kinds of papers 
paper_supplies = [
    # Paper Types (priced per sheet unless specified)
    {"item_name": "A4 paper",                         "category": "paper",        "unit_price": 0.05},
    {"item_name": "Letter-sized paper",              "category": "paper",        "unit_price": 0.06},
    {"item_name": "Cardstock",                        "category": "paper",        "unit_price": 0.15},
    {"item_name": "Colored paper",                    "category": "paper",        "unit_price": 0.10},
    {"item_name": "Glossy paper",                     "category": "paper",        "unit_price": 0.20},
    {"item_name": "Matte paper",                      "category": "paper",        "unit_price": 0.18},
    {"item_name": "Recycled paper",                   "category": "paper",        "unit_price": 0.08},
    {"item_name": "Eco-friendly paper",               "category": "paper",        "unit_price": 0.12},
    {"item_name": "Poster paper",                     "category": "paper",        "unit_price": 0.25},
    {"item_name": "Banner paper",                     "category": "paper",        "unit_price": 0.30},
    {"item_name": "Kraft paper",                      "category": "paper",        "unit_price": 0.10},
    {"item_name": "Construction paper",               "category": "paper",        "unit_price": 0.07},
    {"item_name": "Wrapping paper",                   "category": "paper",        "unit_price": 0.15},
    {"item_name": "Glitter paper",                    "category": "paper",        "unit_price": 0.22},
    {"item_name": "Decorative paper",                 "category": "paper",        "unit_price": 0.18},
    {"item_name": "Letterhead paper",                 "category": "paper",        "unit_price": 0.12},
    {"item_name": "Legal-size paper",                 "category": "paper",        "unit_price": 0.08},
    {"item_name": "Crepe paper",                      "category": "paper",        "unit_price": 0.05},
    {"item_name": "Photo paper",                      "category": "paper",        "unit_price": 0.25},
    {"item_name": "Uncoated paper",                   "category": "paper",        "unit_price": 0.06},
    {"item_name": "Butcher paper",                    "category": "paper",        "unit_price": 0.10},
    {"item_name": "Heavyweight paper",                "category": "paper",        "unit_price": 0.20},
    {"item_name": "Standard copy paper",              "category": "paper",        "unit_price": 0.04},
    {"item_name": "Bright-colored paper",             "category": "paper",        "unit_price": 0.12},
    {"item_name": "Patterned paper",                  "category": "paper",        "unit_price": 0.15},

    # Product Types (priced per unit)
    {"item_name": "Paper plates",                     "category": "product",      "unit_price": 0.10},
    {"item_name": "Paper cups",                       "category": "product",      "unit_price": 0.08},
    {"item_name": "Paper napkins",                    "category": "product",      "unit_price": 0.02},
    {"item_name": "Disposable cups",                  "category": "product",      "unit_price": 0.10},
    {"item_name": "Table covers",                     "category": "product",      "unit_price": 1.50},
    {"item_name": "Envelopes",                        "category": "product",      "unit_price": 0.05},
    {"item_name": "Sticky notes",                     "category": "product",      "unit_price": 0.03},
    {"item_name": "Notepads",                         "category": "product",      "unit_price": 2.00},
    {"item_name": "Invitation cards",                 "category": "product",      "unit_price": 0.50},
    {"item_name": "Flyers",                           "category": "product",      "unit_price": 0.15},
    {"item_name": "Party streamers",                  "category": "product",      "unit_price": 0.05},
    {"item_name": "Decorative adhesive tape (washi tape)", "category": "product", "unit_price": 0.20},
    {"item_name": "Paper party bags",                 "category": "product",      "unit_price": 0.25},
    {"item_name": "Name tags with lanyards",          "category": "product",      "unit_price": 0.75},
    {"item_name": "Presentation folders",             "category": "product",      "unit_price": 0.50},

    # Large-format items (priced per unit)
    {"item_name": "Large poster paper (24x36 inches)", "category": "large_format", "unit_price": 1.00},
    {"item_name": "Rolls of banner paper (36-inch width)", "category": "large_format", "unit_price": 2.50},

    # Specialty papers
    {"item_name": "100 lb cover stock",               "category": "specialty",    "unit_price": 0.50},
    {"item_name": "80 lb text paper",                 "category": "specialty",    "unit_price": 0.40},
    {"item_name": "250 gsm cardstock",                "category": "specialty",    "unit_price": 0.30},
    {"item_name": "220 gsm poster paper",             "category": "specialty",    "unit_price": 0.35},
]

# Synonym- und Normalisierungs-Mapping für eingehende Item-Namen
ITEM_SYNONYMS = {
    "a4 glossy paper": "Glossy paper",
    "glossy a4 paper": "Glossy paper",
    "heavy cardstock": "Cardstock",
    "heavy cardstock (white)": "Cardstock",
    "colored paper (assorted colors)": "Colored paper",
    "assorted colored paper": "Colored paper",
    "heavyweight cardstock": "Heavyweight paper",
}

def normalize_item_name(name: str) -> str:
    if not name:
        return name
    key = name.strip().lower()
    if key in ITEM_SYNONYMS:
        return ITEM_SYNONYMS[key]
    for canonical in [p["item_name"] for p in paper_supplies]:
        if canonical.lower() in key or key in canonical.lower():
            return canonical
    return name

# Cache für Lieferzeitberechnungen
_delivery_cache: dict[tuple[str, int], str] = {}

def generate_sample_inventory(paper_supplies: list, coverage: float = 0.4, seed: int = 137) -> pd.DataFrame:
    """
    Generate inventory for exactly a specified percentage of items from the full paper supply list.

    This function randomly selects exactly `coverage` × N items from the `paper_supplies` list,
    and assigns each selected item:
    - a random stock quantity between 200 and 800,
    - a minimum stock level between 50 and 150.

    The random seed ensures reproducibility of selection and stock levels.

    Args:
        paper_supplies (list): A list of dictionaries, each representing a paper item with
                               keys 'item_name', 'category', and 'unit_price'.
        coverage (float, optional): Fraction of items to include in the inventory (default is 0.4, or 40%).
        seed (int, optional): Random seed for reproducibility (default is 137).

    Returns:
        pd.DataFrame: A DataFrame with the selected items and assigned inventory values, including:
                      - item_name
                      - category
                      - unit_price
                      - current_stock
                      - min_stock_level
    """
    np.random.seed(seed)
    num_items = int(len(paper_supplies) * coverage)
    selected_indices = np.random.choice(
        range(len(paper_supplies)),
        size=num_items,
        replace=False
    )
    selected_items = [paper_supplies[i] for i in selected_indices]
    
    inventory = []
    for item in selected_items:
        inventory.append({
            "item_name": item["item_name"],
            "category": item["category"],
            "unit_price": item["unit_price"],
            "current_stock": np.random.randint(200, 800),
            "min_stock_level": np.random.randint(50, 150)
        })
    
    return pd.DataFrame(inventory)

def init_database(db_engine: Engine = db_engine, seed: int = 137) -> Engine:    
    """
    Set up the Munder Difflin database with all required tables and initial records.

    This function performs the following tasks:
    - Creates the 'transactions' table for logging stock orders and sales
    - Loads customer inquiries from 'quote_requests.csv' into a 'quote_requests' table
    - Loads previous quotes from 'quotes.csv' into a 'quotes' table, extracting useful metadata
    - Generates a random subset of paper inventory using `generate_sample_inventory`
    - Inserts initial financial records including available cash and starting stock levels

    Args:
        db_engine (Engine): A SQLAlchemy engine connected to the SQLite database.
        seed (int, optional): A random seed used to control reproducibility of inventory stock levels.
                              Default is 137.

    Returns:
        Engine: The same SQLAlchemy engine, after initializing all necessary tables and records.

    Raises:
        Exception: If an error occurs during setup, the exception is printed and raised.
    """
    try:
        # Create an empty 'transactions' table schema
        transactions_schema = pd.DataFrame({
            "id": [],
            "item_name": [],
            "transaction_type": [],
            "units": [],
            "price": [],
            "transaction_date": [],
        })
        transactions_schema.to_sql("transactions", db_engine, if_exists="replace", index=False)

        initial_date = datetime(2025, 1, 1).isoformat()

        # Load and initialize 'quote_requests' table
        quote_requests_df = pd.read_csv("quote_requests.csv")
        quote_requests_df["id"] = range(1, len(quote_requests_df) + 1)
        quote_requests_df.to_sql("quote_requests", db_engine, if_exists="replace", index=False)

        # Load and transform 'quotes' table
        quotes_df = pd.read_csv("quotes.csv")
        quotes_df["request_id"] = range(1, len(quotes_df) + 1)
        quotes_df["order_date"] = initial_date

        if "request_metadata" in quotes_df.columns:
            quotes_df["request_metadata"] = quotes_df["request_metadata"].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )
            quotes_df["job_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("job_type", ""))
            quotes_df["order_size"] = quotes_df["request_metadata"].apply(lambda x: x.get("order_size", ""))
            quotes_df["event_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("event_type", ""))

        quotes_df = quotes_df[[
            "request_id",
            "total_amount",
            "quote_explanation",
            "order_date",
            "job_type",
            "order_size",
            "event_type"
        ]]
        quotes_df.to_sql("quotes", db_engine, if_exists="replace", index=False)

        # Generate inventory and seed stock
        inventory_df = generate_sample_inventory(paper_supplies, seed=seed)
        initial_transactions = []

        # Add a starting cash balance
        initial_transactions.append({
            "item_name": None,
            "transaction_type": "sales",
            "units": None,
            "price": 50000.0,
            "transaction_date": initial_date,
        })

        # Add stock order transactions
        for _, item in inventory_df.iterrows():
            initial_transactions.append({
                "item_name": item["item_name"],
                "transaction_type": "stock_orders",
                "units": item["current_stock"],
                "price": item["current_stock"] * item["unit_price"],
                "transaction_date": initial_date,
            })

        pd.DataFrame(initial_transactions).to_sql("transactions", db_engine, if_exists="append", index=False)
        inventory_df.to_sql("inventory", db_engine, if_exists="replace", index=False)

        return db_engine

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def create_transaction(
    item_name: str,
    transaction_type: str,
    quantity: int,
    price: float,
    date: Union[str, datetime],
) -> int:
    """
    Record a transaction in the database.

    Args:
        item_name (str): The name of the item involved in the transaction.
        transaction_type (str): Either 'stock_orders' or 'sales'.
        quantity (int): Number of units involved in the transaction.
        price (float): Total price of the transaction.
        date (str or datetime): Date of the transaction in ISO 8601 format.

    Returns:
        int: The ID of the newly inserted transaction.
    """
    try:
        date_str = date.isoformat() if isinstance(date, datetime) else date

        if transaction_type not in {"stock_orders", "sales"}:
            raise ValueError("Transaction type must be 'stock_orders' or 'sales'")

        transaction = pd.DataFrame([{
            "item_name": item_name,
            "transaction_type": transaction_type,
            "units": quantity,
            "price": price,
            "transaction_date": date_str,
        }])

        transaction.to_sql("transactions", db_engine, if_exists="append", index=False)
        result = pd.read_sql("SELECT last_insert_rowid() as id", db_engine)
        return int(result.iloc[0]["id"])

    except Exception as e:
        print(f"Error creating transaction: {e}")
        raise

def get_all_inventory(as_of_date: str) -> Dict[str, int]:
    """
    Retrieve a snapshot of available inventory as of a specific date.

    Args:
        as_of_date (str): ISO-formatted date string (YYYY-MM-DD).

    Returns:
        Dict[str, int]: A dictionary mapping item names to their current stock levels.
    """
    query = """
        SELECT
            item_name,
            SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END) as stock
        FROM transactions
        WHERE item_name IS NOT NULL
        AND transaction_date <= :as_of_date
        GROUP BY item_name
        HAVING stock > 0
    """
    result = pd.read_sql(query, db_engine, params={"as_of_date": as_of_date})
    return dict(zip(result["item_name"], result["stock"]))

def get_stock_level(item_name: str, as_of_date: Union[str, datetime]) -> pd.DataFrame:
    """
    Retrieve the stock level of a specific item as of a given date.

    Args:
        item_name (str): The name of the item to look up.
        as_of_date (str or datetime): The cutoff date (inclusive).

    Returns:
        pd.DataFrame: A single-row DataFrame with columns 'item_name' and 'current_stock'.
    """
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    stock_query = """
        SELECT
            item_name,
            COALESCE(SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END), 0) AS current_stock
        FROM transactions
        WHERE item_name = :item_name
        AND transaction_date <= :as_of_date
    """
    return pd.read_sql(
        stock_query,
        db_engine,
        params={"item_name": item_name, "as_of_date": as_of_date},
    )

def get_supplier_delivery_date(input_date_str: str, quantity: int) -> str:
    """
    Estimate the supplier delivery date based on order quantity.

    Args:
        input_date_str (str): The starting date in ISO format (YYYY-MM-DD).
        quantity (int): The number of units in the order.

    Returns:
        str: Estimated delivery date in ISO format (YYYY-MM-DD).
    """
    try:
        input_date_dt = datetime.fromisoformat(input_date_str.split("T")[0])
    except (ValueError, TypeError):
        input_date_dt = datetime.now()

    if quantity <= 10:
        days = 0
    elif quantity <= 100:
        days = 1
    elif quantity <= 1000:
        days = 4
    else:
        days = 7

    delivery_date_dt = input_date_dt + timedelta(days=days)
    return delivery_date_dt.strftime("%Y-%m-%d")

def get_cash_balance(as_of_date: Union[str, datetime]) -> float:
    """
    Calculate the current cash balance as of a specified date.

    Args:
        as_of_date (str or datetime): The cutoff date (inclusive).

    Returns:
        float: Net cash balance as of the given date.
    """
    try:
        if isinstance(as_of_date, datetime):
            as_of_date = as_of_date.isoformat()

        transactions = pd.read_sql(
            "SELECT * FROM transactions WHERE transaction_date <= :as_of_date",
            db_engine,
            params={"as_of_date": as_of_date},
        )

        if not transactions.empty:
            total_sales = transactions.loc[transactions["transaction_type"] == "sales", "price"].sum()
            total_purchases = transactions.loc[transactions["transaction_type"] == "stock_orders", "price"].sum()
            return float(total_sales - total_purchases)

        return 0.0

    except Exception as e:
        print(f"Error getting cash balance: {e}")
        return 0.0

def generate_financial_report(as_of_date: Union[str, datetime]) -> Dict:
    """
    Generate a complete financial report for the company as of a specific date.

    Args:
        as_of_date (str or datetime): The date for the report.

    Returns:
        Dict: Financial report with cash balance, inventory value, and other details.
    """
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    cash = get_cash_balance(as_of_date)
    inventory_df = pd.read_sql("SELECT * FROM inventory", db_engine)
    inventory_value = 0.0
    inventory_summary = []

    for _, item in inventory_df.iterrows():
        stock_info = get_stock_level(item["item_name"], as_of_date)
        stock = stock_info["current_stock"].iloc[0]
        item_value = stock * item["unit_price"]
        inventory_value += item_value

        inventory_summary.append({
            "item_name": item["item_name"],
            "stock": stock,
            "unit_price": item["unit_price"],
            "value": item_value,
        })

    top_sales_query = """
        SELECT item_name, SUM(units) as total_units, SUM(price) as total_revenue
        FROM transactions
        WHERE transaction_type = 'sales' AND transaction_date <= :date
        GROUP BY item_name
        ORDER BY total_revenue DESC
        LIMIT 5
    """
    top_sales = pd.read_sql(top_sales_query, db_engine, params={"date": as_of_date})
    top_selling_products = top_sales.to_dict(orient="records")

    return {
        "as_of_date": as_of_date,
        "cash_balance": cash,
        "inventory_value": inventory_value,
        "total_assets": cash + inventory_value,
        "inventory_summary": inventory_summary,
        "top_selling_products": top_selling_products,
    }

def search_quote_history(search_terms: List[str], limit: int = 5) -> List[Dict]:
    """
    Retrieve historical quotes matching the provided search terms.

    Args:
        search_terms (List[str]): List of terms to search for.
        limit (int, optional): Maximum number of results. Default is 5.

    Returns:
        List[Dict]: List of matching quotes.
    """
    conditions = []
    params = {}

    for i, term in enumerate(search_terms):
        param_name = f"term_{i}"
        conditions.append(
            f"(LOWER(qr.response) LIKE :{param_name} OR "
            f"LOWER(q.quote_explanation) LIKE :{param_name})"
        )
        params[param_name] = f"%{term.lower()}%"

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT
            qr.response AS original_request,
            q.total_amount,
            q.quote_explanation,
            q.job_type,
            q.order_size,
            q.event_type,
            q.order_date
        FROM quotes q
        JOIN quote_requests qr ON q.request_id = qr.id
        WHERE {where_clause}
        ORDER BY q.order_date DESC
        LIMIT {limit}
    """

    with db_engine.connect() as conn:
        result = conn.execute(text(query), params)
        return [dict(row) for row in result]

# ============================================================================
# MULTI-AGENT SYSTEM TOOLS
# ============================================================================

@tool
def check_inventory_tool(item_name: str, date: str) -> str:
    """
    Check the current stock level for a specific item.
    
    Args:
        item_name: Name of the item to check (e.g., 'A4 paper', 'Paper cups'). 
                   Use EXACT names from similar items suggestions if initial search fails.
        date: Date in YYYY-MM-DD format (use the request date from the customer's message)
    
    Returns:
        String with stock information or suggestions for similar items
    """
    try:
        original_name = item_name
        item_name = normalize_item_name(item_name)
        stock_df = get_stock_level(item_name, date)
        if stock_df.empty or stock_df["current_stock"].iloc[0] == 0:
            # Vorschläge suchen
            suggestions = []
            tokens = [t for t in original_name.lower().replace('(', ' ').replace(')', ' ').split() if len(t) > 2]
            for canonical in [p["item_name"] for p in paper_supplies]:
                if any(t in canonical.lower() for t in tokens):
                    suggestions.append(canonical)
            suggestion_text = f" Similar items: {', '.join(sorted(set(suggestions)))}`" if suggestions else ""
            return f"Item '{original_name}' not found or out of stock.{suggestion_text}"

        stock = int(stock_df["current_stock"].iloc[0])
        
        # Get unit price from inventory table
        inventory_df = pd.read_sql(
            "SELECT unit_price FROM inventory WHERE item_name = :item_name",
            db_engine,
            params={"item_name": item_name}
        )
        
        if inventory_df.empty:
            return f"Item '{item_name}' has {stock} units in stock but pricing information is unavailable."
        
        unit_price = float(inventory_df["unit_price"].iloc[0])
        
        return f"Item: {item_name}\nCurrent stock: {stock} units\nUnit price: ${unit_price:.2f}"
    except Exception as e:
        return f"Error checking inventory: {str(e)}"

@tool
def get_all_inventory_tool(date: str) -> str:
    """
    Get a summary of all items currently in stock.
    
    Args:
        date: Date in YYYY-MM-DD format
    
    Returns:
        String with inventory summary
    """
    try:
        inventory = get_all_inventory(date)
        if not inventory:
            return "No items currently in stock."
        
        result = "Current Inventory Summary:\n"
        result += "-" * 50 + "\n"
        
        # Get pricing information
        for item_name, stock in sorted(inventory.items()):
            inventory_df = pd.read_sql(
                "SELECT unit_price, category FROM inventory WHERE item_name = :item_name",
                db_engine,
                params={"item_name": item_name}
            )
            if not inventory_df.empty:
                unit_price = float(inventory_df["unit_price"].iloc[0])
                category = inventory_df["category"].iloc[0]
                result += f"{item_name} ({category}): {stock} units @ ${unit_price:.2f}\n"
        
        return result
    
    except Exception as e:
        return f"Error retrieving inventory: {str(e)}"

@tool
def check_delivery_time_tool(date: str, quantity: int) -> str:
    """
    Check estimated delivery time from supplier for an order.
    
    Args:
        date: Order date in YYYY-MM-DD format
        quantity: Number of units to order
    
    Returns:
        String with delivery date information
    """
    try:
        cache_key = (date, int(quantity))
        if cache_key in _delivery_cache:
            return f"Cached delivery estimate for {quantity} units on {date}: {_delivery_cache[cache_key]} (reuse to avoid repetition)."
        delivery_date = get_supplier_delivery_date(date, quantity)
        
        # Calculate days
        order_date = datetime.fromisoformat(date)
        delivery_dt = datetime.fromisoformat(delivery_date)
        days = (delivery_dt - order_date).days
        
        if days == 0:
            time_desc = "same day"
        elif days == 1:
            time_desc = "1 day"
        else:
            time_desc = f"{days} days"
        
        result = f"For an order of {quantity} units placed on {date}:\nEstimated delivery: {delivery_date} ({time_desc})"
        _delivery_cache[cache_key] = result
        return result
    except Exception as e:
        return f"Error checking delivery time: {str(e)}"

@tool
def search_quote_history_tool(search_terms: str) -> str:
    """
    Search historical quotes for similar requests.
    
    Args:
        search_terms: Comma-separated search terms (e.g., 'wedding,invitations')
    
    Returns:
        String with relevant quote history
    """
    try:
        terms = [term.strip() for term in search_terms.split(",")]
        quotes = search_quote_history(terms, limit=3)
        
        if not quotes:
            return "No matching quotes found in history."
        
        result = "Relevant Quote History:\n"
        result += "=" * 60 + "\n"
        
        for i, quote in enumerate(quotes, 1):
            result += f"\nQuote {i}:\n"
            result += f"Request: {quote['original_request'][:100]}...\n"
            result += f"Amount: ${quote['total_amount']:.2f}\n"
            result += f"Type: {quote['job_type']} - {quote['event_type']}\n"
            result += f"Size: {quote['order_size']}\n"
            result += f"Explanation: {quote['quote_explanation'][:150]}...\n"
            result += "-" * 60 + "\n"
        
        return result
    
    except Exception as e:
        return f"Error searching quote history: {str(e)}"

@tool
def get_financial_status_tool(date: str) -> str:
    """
    Get current financial status including cash balance and inventory value.
    
    Args:
        date: Date in YYYY-MM-DD format
    
    Returns:
        String with financial summary
    """
    try:
        cash = get_cash_balance(date)
        report = generate_financial_report(date)
        
        result = "Financial Status Report\n"
        result += "=" * 60 + "\n"
        result += f"Date: {date}\n"
        result += f"Cash Balance: ${cash:,.2f}\n"
        result += f"Inventory Value: ${report['inventory_value']:,.2f}\n"
        result += f"Total Assets: ${report['total_assets']:,.2f}\n"
        
        if report['top_selling_products']:
            result += "\nTop Selling Products:\n"
            for product in report['top_selling_products'][:3]:
                result += f"  - {product['item_name']}: ${product['total_revenue']:.2f} revenue\n"
        
        return result
    
    except Exception as e:
        return f"Error getting financial status: {str(e)}"

@tool
def process_sale_tool(item_name: str, quantity: int, unit_price: float, date: str) -> str:
    """
    Process a sale transaction and update inventory.
    
    Args:
        item_name: Name of the item being sold
        quantity: Number of units sold
        unit_price: Price per unit
        date: Transaction date in YYYY-MM-DD format
    
    Returns:
        String confirming the transaction
    """
    try:
        original_name = item_name
        item_name = normalize_item_name(item_name)
        stock_df = get_stock_level(item_name, date)
        if stock_df.empty:
            return f"ERROR: Item '{original_name}' not found in inventory after normalization to '{item_name}'."

        current_stock = int(stock_df["current_stock"].iloc[0])
        
        if current_stock < quantity:
            return f"ERROR: Insufficient stock. Requested: {quantity} units, Available: {current_stock} units."
        
        # Calculate total price
        total_price = quantity * unit_price
        
        # Create transaction
        transaction_id = create_transaction(
            item_name=item_name,
            transaction_type="sales",
            quantity=quantity,
            price=total_price,
            date=date
        )
        
        new_stock = current_stock - quantity
        
        result = f"Sale Processed Successfully!\n"
        result += f"Transaction ID: {transaction_id}\n"
        result += f"Item: {item_name}\n"
        result += f"Quantity Sold: {quantity} units\n"
        result += f"Unit Price: ${unit_price:.2f}\n"
        result += f"Total Amount: ${total_price:.2f}\n"
        result += f"Remaining Stock: {new_stock} units\n"
        
        return result
    except Exception as e:
        return f"Error processing sale: {str(e)}"

@tool
def calculate_discount_tool(base_price: float, quantity: int, event_type: str = "") -> str:
    """
    Calculate appropriate discount based on quantity and event type.
    
    Args:
        base_price: Base price before discount
        quantity: Number of units
        event_type: Type of event (e.g., 'wedding', 'conference', 'corporate'), empty string if not provided
    
    Returns:
        String with discount calculation details
    """
    try:
        # Handle None or empty event_type
        if not event_type:
            event_type = ""
            
        discount_percentage = 0.0
        discount_reason = ""
        
        # Quantity-based discounts
        if quantity >= 1000:
            discount_percentage = 15.0
            discount_reason = "Bulk order (1000+ units)"
        elif quantity >= 500:
            discount_percentage = 10.0
            discount_reason = "Large order (500-999 units)"
        elif quantity >= 200:
            discount_percentage = 5.0
            discount_reason = "Medium order (200-499 units)"
        
        # Event-based additional discount
        event_discount = 0.0
        if event_type and event_type.lower() in ['wedding', 'corporate', 'conference']:
            event_discount = 3.0
            discount_reason += f" + Special event ({event_type})"
        
        total_discount = discount_percentage + event_discount
        discount_amount = base_price * (total_discount / 100)
        final_price = base_price - discount_amount
        
        result = f"Discount Calculation:\n"
        result += f"Base Price: ${base_price:.2f}\n"
        result += f"Quantity: {quantity} units\n"
        result += f"Discount: {total_discount}% ({discount_reason})\n"
        result += f"Discount Amount: ${discount_amount:.2f}\n"
        result += f"Final Price: ${final_price:.2f}\n"
        
        return result
    
    except Exception as e:
        return f"Error calculating discount: {str(e)}"

# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

# Initialize the OpenAI model
model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.getenv("UDACITY_OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_BASE_URL")
)

# Inventory Management Agent
# Handles stock queries, inventory summaries, and delivery time estimates
inventory_agent = ToolCallingAgent(
    name="inventory_agent",
    tools=[
        check_inventory_tool,
        get_all_inventory_tool,
        check_delivery_time_tool
    ],
    model=model,
    description="""Checks inventory availability and delivery times. 
    IMPORTANT: Extract the date from your task (format YYYY-MM-DD) and pass it to tools.
    If an item is not found, check the 'Similar items' suggestions and try those EXACT names."""
)

# Quote Generation Agent
# Handles pricing, discounts, and quote generation
quote_agent = ToolCallingAgent(
    name="quote_agent",
    tools=[
        check_inventory_tool,
        search_quote_history_tool,
        calculate_discount_tool,
        get_financial_status_tool
    ],
    model=model,
    description="""Generates quotes with pricing and discounts.
    IMPORTANT: Extract the date from your task (format YYYY-MM-DD) and pass it to tools.
    If items not found, use 'Similar items' suggestions with EXACT names."""
)

# Sales Transaction Agent
# Handles order processing and transaction recording
sales_agent = ToolCallingAgent(
    name="sales_agent",
    tools=[
        process_sale_tool,
        check_inventory_tool,
        get_financial_status_tool,
        check_delivery_time_tool
    ],
    model=model,
    description="""Processes sales transactions.
    IMPORTANT: Extract the date from your task (format YYYY-MM-DD) and pass it to tools.
    Use EXACT item names when processing sales."""
)

# Orchestrator Agent
# Coordinates all operations and delegates to specialized worker agents
# Uses managed_agents pattern with ToolCallingAgent
# Note: While CodeAgent is shown in smolagents examples, ToolCallingAgent provides
# better control and avoids infinite loops for this use case
orchestrator_agent = ToolCallingAgent(
    name="orchestrator_agent",
    tools=[],  # No tools - delegates to worker agents
    model=model,
    managed_agents=[inventory_agent, quote_agent, sales_agent],
    description="""You coordinate between specialized worker agents: inventory_agent, quote_agent, and sales_agent.
For each customer request, call the appropriate agents in sequence to fulfill the request."""
)

# ============================================================================
# TEST SCENARIO RUNNER
# ============================================================================

def run_test_scenarios(max_requests: int | None = None):
    """
    Run the multi-agent system through test scenarios from quote_requests_sample.csv.
    max_requests: Optional Begrenzung für Smoke-Tests.
    """
    logger.info("=" * 80)
    logger.info("INITIALIZING MULTI-AGENT INVENTORY & SALES SYSTEM")
    logger.info("=" * 80)
    
    print("=" * 80)
    print("INITIALIZING MULTI-AGENT INVENTORY & SALES SYSTEM")
    print("=" * 80)
    print("\nInitializing Database...")
    init_database(db_engine)
    
    try:
        quote_requests_sample = pd.read_csv("quote_requests_sample.csv")
        quote_requests_sample["request_date"] = pd.to_datetime(
            quote_requests_sample["request_date"], format="%m/%d/%y", errors="coerce"
        )
        quote_requests_sample.dropna(subset=["request_date"], inplace=True)
        quote_requests_sample = quote_requests_sample.sort_values("request_date")
    except Exception as e:
        logger.error(f"FATAL: Error loading test data: {e}")
        print(f"FATAL: Error loading test data: {e}")
        return

    # Get initial state
    initial_date = quote_requests_sample["request_date"].min().strftime("%Y-%m-%d")
    report = generate_financial_report(initial_date)
    current_cash = report["cash_balance"]
    current_inventory = report["inventory_value"]

    logger.info(f"Initial Financial State: Cash=${current_cash:,.2f}, Inventory=${current_inventory:,.2f}")
    
    print(f"\nInitial Financial State:")
    print(f"  Cash Balance: ${current_cash:,.2f}")
    print(f"  Inventory Value: ${current_inventory:,.2f}")
    print(f"  Total Assets: ${report['total_assets']:,.2f}")
    print("\n" + "=" * 80)

    results = []
    
    for idx, row in quote_requests_sample.iterrows():
        if max_requests is not None and idx >= max_requests:
            break
        # Cache pro Request zurücksetzen
        _delivery_cache.clear()
        request_date = row["request_date"].strftime("%Y-%m-%d")

        logger.info(f"\n{'=' * 80}")
        logger.info(f"REQUEST {idx+1} OF {len(quote_requests_sample)}")
        logger.info(f"Date: {request_date}, Context: {row['job']} - {row['event']}")
        logger.info(f"Customer Request: {row['request'][:100]}...")
        
        print(f"\n{'=' * 80}")
        print(f"REQUEST {idx+1} OF {len(quote_requests_sample)}")
        print(f"{'=' * 80}")
        print(f"Context: {row['job']} organizing {row['event']}")
        print(f"Request Date: {request_date}")
        print(f"Cash Balance: ${current_cash:,.2f}")
        print(f"Inventory Value: ${current_inventory:,.2f}")
        print(f"\nCustomer Request: {row['request']}")
        print("-" * 80)

        # Process request with orchestrator
        request_with_context = f"""
Date: {request_date}
Context: {row['job']} organizing {row['event']}
Customer Request: {row['request']}

Please analyze this request and coordinate with the appropriate worker agents to:
1. Check inventory availability (inventory_agent)
2. Generate quotes if needed (quote_agent)  
3. Process sales transactions if this is an order (sales_agent)

Provide a professional customer response explaining the outcome.
"""

        try:
            logger.info(f"Delegating request to orchestrator_agent...")
            response = orchestrator_agent.run(request_with_context, max_steps=15)
            response_text = str(response)
            logger.info(f"Request processed successfully")
        except Exception as e:
            response_text = f"ERROR: Failed to process request - {str(e)}"
            logger.error(f"ERROR processing request: {e}")
            print(f"ERROR processing request: {e}")

        # Update state
        report = generate_financial_report(request_date)
        new_cash = report["cash_balance"]
        new_inventory = report["inventory_value"]
        
        cash_change = new_cash - current_cash
        inventory_change = new_inventory - current_inventory

        logger.info(f"Financial Update: Cash ${current_cash:,.2f} → ${new_cash:,.2f} (Change: ${cash_change:+,.2f})")

        print("\n" + "-" * 80)
        print("SYSTEM RESPONSE:")
        print("-" * 80)
        print(response_text)
        print("\n" + "-" * 80)
        print("FINANCIAL UPDATE:")
        print("-" * 80)
        print(f"Cash Balance: ${current_cash:,.2f} → ${new_cash:,.2f} (Change: ${cash_change:+,.2f})")
        print(f"Inventory Value: ${current_inventory:,.2f} → ${new_inventory:,.2f} (Change: ${inventory_change:+,.2f})")

        current_cash = new_cash
        current_inventory = new_inventory

        results.append({
            "request_id": idx + 1,
            "request_date": request_date,
            "context": f"{row['job']} - {row['event']}",
            "request": row['request'],
            "response": response_text,
            "cash_balance": current_cash,
            "inventory_value": current_inventory,
        })

        time.sleep(1)  # Rate limiting

    # Final report
    logger.info("\n" + "=" * 80)
    logger.info("FINAL FINANCIAL REPORT")
    logger.info("=" * 80)
    
    print("\n" + "=" * 80)
    print("FINAL FINANCIAL REPORT")
    print("=" * 80)
    final_date = quote_requests_sample["request_date"].max().strftime("%Y-%m-%d")
    final_report = generate_financial_report(final_date)
    
    logger.info(f"Final Cash Balance: ${final_report['cash_balance']:,.2f}")
    logger.info(f"Final Inventory Value: ${final_report['inventory_value']:,.2f}")
    
    print(f"Final Cash Balance: ${final_report['cash_balance']:,.2f}")
    print(f"Final Inventory Value: ${final_report['inventory_value']:,.2f}")
    print(f"Total Assets: ${final_report['total_assets']:,.2f}")
    
    if final_report['top_selling_products']:
        print("\nTop Selling Products:")
        for i, product in enumerate(final_report['top_selling_products'][:5], 1):
            print(f"  {i}. {product['item_name']}: ${product['total_revenue']:.2f} revenue ({product['total_units']} units)")

    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv("test_results.csv", index=False)
    logger.info(f"Results saved to test_results.csv")
    print(f"\nResults saved to test_results.csv")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    max_req = 1 if os.getenv("USE_SMOKE") == "1" else None
    results = run_test_scenarios(max_requests=max_req)
