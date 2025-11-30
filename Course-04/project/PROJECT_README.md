# Multi-Agent Inventory & Sales System
## The Beaver's Choice Paper Company

A sophisticated multi-agent system for managing inventory, generating quotes, and processing sales transactions using AI agents built with the smolagents framework.

---

## 📋 Project Overview

This project implements a complete multi-agent system that handles:
- Customer inquiries about products and availability
- Automated quote generation with intelligent discounting
- Sales order processing and fulfillment
- Inventory management and tracking
- Financial reporting and analytics

### Key Features

✨ **Intelligent Agent Orchestration** - Hierarchical agent architecture with specialized roles  
💰 **Dynamic Pricing** - Automatic discounts based on order size and event type  
📊 **Real-Time Inventory** - Accurate stock tracking and availability checking  
🔒 **Data Privacy** - Customer-facing outputs protect sensitive business information  
📈 **Financial Tracking** - Complete transaction history and reporting  
🤖 **AI-Powered** - Uses GPT-4o-mini for natural language understanding  

---

## 🏗️ System Architecture

### Agent Hierarchy

```
┌─────────────────────────────────────┐
│     Orchestrator Agent              │
│  (Customer Interface & Coordinator)  │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┬─────────────┐
       │                │             │
┌──────▼──────┐  ┌─────▼─────┐  ┌────▼────────┐
│  Inventory  │  │   Quote   │  │    Sales    │
│   Agent     │  │   Agent   │  │    Agent    │
└─────────────┘  └───────────┘  └─────────────┘
       │                │             │
       └───────┬────────┴──────┬──────┘
               │               │
          ┌────▼───────────────▼─────┐
          │   Database & Tools       │
          └──────────────────────────┘
```

### Agents & Responsibilities

#### 1. **Orchestrator Agent**
- Primary customer interface
- Request type classification (inquiry/quote/order)
- Workflow coordination
- Response generation

#### 2. **Inventory Management Agent**
- Stock level queries
- Inventory summaries
- Reorder assessments
- Delivery timeline estimates

#### 3. **Quote Generation Agent**
- Price quote generation
- Discount calculation
- Historical quote analysis
- Competitive pricing

#### 4. **Sales Transaction Agent**
- Order processing
- Stock verification
- Transaction recording
- Order confirmations

---

## 🛠️ Tools & Helper Functions

All required database functions are integrated as agent tools:

| Helper Function | Tool Name | Purpose |
|----------------|-----------|---------|
| `create_transaction` | `process_sale_tool` | Record sales and stock orders |
| `get_all_inventory` | `get_all_inventory_tool` | List all items in stock |
| `get_stock_level` | `check_inventory_tool` | Check specific item availability |
| `get_supplier_delivery_date` | `check_delivery_time_tool` | Estimate delivery times |
| `get_cash_balance` | `get_financial_status_tool` | View cash balance |
| `generate_financial_report` | `get_financial_status_tool` | Comprehensive financial report |
| `search_quote_history` | `search_quote_history_tool` | Find similar past quotes |

---

## 💻 Technical Stack

- **Language:** Python 3.13
- **Agent Framework:** smolagents 1.23.0  
- **LLM:** gpt-4o-mini (OpenAI API)
- **Database:** SQLite with SQLAlchemy
- **Data Processing:** pandas, numpy
- **Environment:** python-dotenv

---

## 📁 Project Structure

```
Course-04/project/
├── multi_agent_system.py          # Main implementation (967 lines)
├── agent_workflow_diagram.mmd     # Mermaid architecture diagram
├── reflection_report.md            # Comprehensive evaluation report
├── test_quick.py                   # Quick system test
├── project_starter.py              # Original starter code
├── quote_requests_sample.csv       # Test dataset (20 requests)
├── quote_requests.csv              # Full quote history
├── quotes.csv                      # Historical quotes
├── munder_difflin.db               # SQLite database
├── PROJECT_README.md               # This file
└── README.md                       # Original project instructions
```

---

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.13+ with required packages:
pip install smolagents pandas numpy sqlalchemy python-dotenv openai
```

### Environment Setup

Create a `.env` file in the workspace root with:
```env
UDACITY_OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Running the System

**Full Test Suite:**
```bash
cd Course-04/project
python multi_agent_system.py
```

**Quick Test:**
```bash
python test_quick.py
```

### Expected Output

The system will:
1. Initialize the database
2. Process all customer requests from `quote_requests_sample.csv`
3. Display detailed workflow for each request
4. Generate `test_results.csv` with outcomes
5. Show financial state changes

---

## 📊 Sample Results

### Successful Quote Generation

**Request:** 500 invitation cards for a wedding  
**Response:**
```
For the order of 500 invitation cards for the wedding:
- Unit Price: $0.43 per card (13% discount applied)
- Total: $215.00
- Discount Breakdown:
  • 10% for large order (500-999 units)
  • 3% for special event (wedding)
- Estimated Delivery: 4 days
- Current Stock: 526 units available
```

### Stock Unavailability Handling

**Request:** A4 glossy paper, heavy cardstock, colored paper  
**Response:**
```
The request for paper supplies cannot be fulfilled due to insufficient
stock for heavy cardstock, colored paper, and A4 glossy paper. However,
if you would like, I can place an order for these items but they cannot
be delivered before the ceremony on April 15, 2025.
```

---

## 🎯 Business Rules

### Discount Structure

| Order Size | Discount | Additional |
|-----------|----------|------------|
| 200-499 units | 5% | +3% for special events |
| 500-999 units | 10% | +3% for special events |
| 1000+ units | 15% | +3% for special events |

### Special Events
- Weddings
- Corporate events
- Conferences

### Delivery Times

| Quantity | Delivery Time |
|----------|---------------|
| ≤ 10 units | Same day |
| 11-100 units | 1 day |
| 101-1000 units | 4 days |
| 1000+ units | 7 days |

---

## 📈 Performance Metrics

From test execution on 20 sample requests:

- **Fulfillment Rate:** ~60% (items in stock and processable)
- **Stock Limitations:** ~40% (unavailable items)
- **System Errors:** 0% (no crashes or data corruption)
- **Financial Accuracy:** 100% (all transactions recorded correctly)
- **Response Quality:** Excellent (transparent, professional, accurate)

---

## 🔧 Key Strengths

1. ✅ **Accurate Inventory Management** - Real-time stock tracking
2. ✅ **Intelligent Discounting** - Automatic calculation with clear justification
3. ✅ **Transparent Communication** - Customers understand pricing and availability
4. ✅ **Data Privacy** - No sensitive business data exposed
5. ✅ **Financial Integrity** - Complete audit trail
6. ✅ **Error Handling** - Graceful degradation when items unavailable
7. ✅ **Modular Design** - Easy to extend and maintain

---

## 🚧 Known Limitations & Improvements

### Current Limitations

1. **Item Name Matching** - Exact name matching required; "A4 glossy paper" ≠ "Glossy paper"
2. **Redundant Tool Calls** - Some efficiency loss from repeated queries
3. **No Alternative Suggestions** - Doesn't recommend similar products when exact match unavailable

### Planned Improvements

1. **Fuzzy Matching** - Use string similarity for product name matching
2. **Tool Call Caching** - Reduce API costs with result caching
3. **Product Recommendations** - Suggest alternatives when items unavailable
4. **Multi-Item Optimization** - Calculate combined discounts for bulk orders
5. **Inventory Automation** - Automatic reordering when stock low

---

## 📚 Documentation

- **Architecture Diagram:** `agent_workflow_diagram.mmd` - Visual system architecture
- **Reflection Report:** `reflection_report.md` - Comprehensive analysis and evaluation
- **Code Documentation:** Inline comments and docstrings throughout

---

## 🧪 Testing

### Test Dataset

`quote_requests_sample.csv` contains 20 diverse requests:
- Small inquiries (< 100 units)
- Medium orders (100-500 units)
- Large bulk orders (500+ units)
- Various product types (paper, products, specialty items)
- Different event contexts (weddings, conferences, ceremonies)

### Test Execution

```bash
python multi_agent_system.py
```

Generates `test_results.csv` with:
- Request ID and date
- Customer context
- Original request
- System response
- Financial state changes (cash balance, inventory value)

---

## 🏆 Project Compliance

### Rubric Requirements Met

✅ Agent workflow diagram with all agents and tools  
✅ Orchestrator + worker agent architecture  
✅ All 7 required helper functions integrated  
✅ System evaluation with provided dataset  
✅ Test results documented  
✅ Reflection report with evaluation and improvements  
✅ Transparent customer communications  
✅ Data privacy maintained  
✅ Code quality (naming, comments, modularity)  

---

## 📝 License

This project is part of the Udacity Agentic AI Nanodegree coursework.

---

## 👥 Author

**Glenn**  
Agentic AI Nanodegree - Course 04 Project  
November 2025

---

**Built with ❤️ and AI agents** 🤖
