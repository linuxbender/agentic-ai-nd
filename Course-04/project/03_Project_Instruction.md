# Project Instructions: Multi-Agent Inventory & Sales System

## Overview

This guide will walk you through building a multi-agent system for The Beaver's Choice Paper Company. Follow these steps carefully to create a robust, efficient solution.

---

## Step 1: Draft Your Agent Workflow

### 1.1 Create a System Diagram

Begin by drafting a diagram illustrating the interactions and data flows between the agents in your multi-agent system. Your diagram should demonstrate the sequence of operations for:

- Handling customer inquiries
- Inventory management
- Quote generation
- Order fulfillment

### 1.2 Recommended Agent Architecture

Consider implementing the following agents:

1. **Orchestrator Agent**
   - Handles customer inquiries
   - Delegates tasks to specialized agents
   - Coordinates workflow between agents

2. **Inventory Management Agent**
   - Answers inventory queries accurately
   - Decides when to reorder supplies
   - Monitors stock levels

3. **Quote Generation Agent**
   - Generates quotes efficiently
   - Applies bulk discounts strategically
   - Encourages sales through competitive pricing

4. **Sales Transaction Agent**
   - Finalizes sales transactions
   - Considers inventory levels
   - Manages delivery timelines

### 1.3 Recommended Tools

Your agents should have access to tools that interact with the system database and external resources:

| Tool | Purpose |
|------|---------|
| **Inventory Checker** | Checks inventory for different paper types |
| **Quote History Tool** | Retrieves quote history related to customer requests |
| **Delivery Timeline Tool** | Checks timeline for delivery from supplier |
| **Order Fulfillment Tool** | Fulfills orders by updating system database |

> **Note**: These recommendations are starting points. Feel free to design your architecture differently based on your understanding of inventory and sales management.

### 1.4 Diagramming Tools

Use one of these tools to create your workflow diagram:

- [Diagrams.net](https://www.diagrams.net/) (formerly Draw.io)
- [Mermaid](https://mermaid.js.org/) (code-based diagrams)

---

## Step 2: Review the Starter Code

### 2.1 Examine the Provided Code

Carefully review `project_starter.py` in your workspace. This file includes:

- **Database Management**: SQLite initialization and operations
- **Inventory Management**: Stock level tracking and updates
- **Financial Tracking**: Transaction generation and monitoring
- **Utility Functions**: 
  - Supplier delivery date estimation
  - Current cash balance calculations

### 2.2 Study Time Requirement

**Spend at least 30 minutes** reviewing the starter file.

### 2.3 Documentation Exercise

Write brief descriptions for each function provided to ensure you understand:
- Function purpose
- Input parameters
- Return values
- Usage within your system

### 2.4 Update Your Workflow

Once you complete your review:

1. Revisit your agent flow draft from Step 1
2. Update the tools you initially outlined
3. Replace hypothetical tools with actual functions from the starter code
4. Refine your architecture based on available functionality

---

## Step 3: Select Your Agent Framework

### 3.1 Framework Options

Choose one of the following agent orchestration frameworks:

| Framework | Documentation | Best For |
|-----------|--------------|----------|
| **smolagents** | [Documentation](https://github.com/huggingface/smolagents) | Simple, straightforward agent systems |
| **pydantic-ai** | [Documentation](https://ai.pydantic.dev/) | Type-safe, validated agent interactions |
| **npcsh** | [Documentation](https://github.com/anthropics/npcsh) | Shell-based agent workflows |

### 3.2 Selection Criteria

Ensure your chosen framework:
- ✅ Aligns with project requirements
- ✅ Supports your intended agent interactions
- ✅ You are comfortable working with it

---

## Step 4: Implement Your System

### 4.1 Implementation Steps

1. **Create Worker Agents**
   - Implement each specialized agent (inventory, quotes, sales)
   - Use helper functions from starter file to define tools
   - Ensure each agent has clear responsibilities

2. **Create Orchestration Agent**
   - Implement the main coordinator
   - Define workflow logic
   - Handle agent-to-agent communication

3. **Follow Your Diagram**
   - Implement based on your workflow from Step 1
   - Update diagram if implementation reveals better approaches
   - Maintain consistency between diagram and code

### 4.2 Implementation Guidelines

- Use the helper functions from `project_starter.py` for tool definitions
- Refer to the **project rubric** for success criteria
- Keep your code modular and well-documented
- Test each agent individually before integration

---

## Step 5: Test and Evaluate Your Implementation

### 5.1 Testing Dataset

Test your multi-agent system thoroughly using the provided dataset: **`quote_requests_sample.csv`**

### 5.2 Validation Criteria

Ensure your system:

| Criteria | Description |
|----------|-------------|
| **✓ Inquiry Handling** | Agents correctly handle various customer inquiries and orders |
| **✓ Inventory Optimization** | Orders are accommodated effectively to optimize inventory use and profitability |
| **✓ Competitive Pricing** | The quoting agent consistently provides competitive and attractive pricing |

### 5.3 Evaluation Process

1. Run the provided evaluation code
2. Review the generated `test_results.csv` file
3. Compare results against the project rubric
4. Identify areas for improvement

---

## Step 6: Reflect and Document

### 6.1 Prepare Your Report

Create a clear and concise report containing:

#### Section 1: System Explanation
- Comprehensive description of your multi-agent system
- Agent roles and responsibilities
- Tool implementations
- Workflow logic

#### Section 2: Evaluation Results
- Analysis of `test_results.csv`
- Highlighting system strengths
- Identifying areas for improvement
- Performance metrics

#### Section 3: Improvement Suggestions
- Recommendations based on evaluation
- Potential enhancements
- Scalability considerations

### 6.2 Final Submission Checklist

Your submission must include:

- [ ] **Updated agent flow diagram** (image file)
- [ ] **Completed implementation script** (single Python file)
- [ ] **Reflective report** with evaluations and recommendations
- [ ] **Test results** (`test_results.csv`)

### 6.3 Quality Check

Before submitting:

1. ✅ Review the project rubric thoroughly
2. ✅ Ensure all requirements are met
3. ✅ Verify code runs without errors
4. ✅ Check that documentation is complete
5. ✅ Test with the sample dataset

---

## Additional Resources

### Understanding the Business Context

To better understand this project, research:
- Inventory management systems
- Sales management processes
- Pricing strategies for physical products
- Supply chain coordination

### Support and Troubleshooting

If you encounter issues:
1. Review the starter code documentation
2. Check framework-specific documentation
3. Verify environment variables are set correctly
4. Test individual components before integration

---

**Good luck with your implementation! Build a system that The Beaver's Choice Paper Company will be proud to use!** 🦫📄
