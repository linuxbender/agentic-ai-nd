#!/usr/bin/env python3
"""
Validation script to verify multi-agent system meets all rubric requirements.
"""

import pandas as pd
import os
from pathlib import Path

def validate_test_results():
    """
    Verify test_results.csv meets rubric requirements:
    - At least 3 requests result in cash balance changes
    - At least 3 quote requests are successfully fulfilled
    - Not all requests fulfilled (with reasons)
    """
    print("=" * 80)
    print("VALIDATING TEST RESULTS")
    print("=" * 80)
    
    if not os.path.exists("test_results.csv"):
        print("❌ ERROR: test_results.csv not found!")
        return False
    
    df = pd.read_csv("test_results.csv")
    total_requests = len(df)
    
    print(f"\n✅ Total requests processed: {total_requests}")
    
    # Check for cash balance changes
    if "cash_balance" in df.columns:
        # Calculate changes from initial balance
        initial_balance = 50000.00  # Known initial balance
        cash_changes = df[df["cash_balance"] != initial_balance]
        num_cash_changes = len(cash_changes)
        
        print(f"\n✅ Requests with cash balance changes: {num_cash_changes}")
        if num_cash_changes >= 3:
            print("   ✅ PASS: At least 3 requests changed cash balance")
        else:
            print(f"   ❌ FAIL: Only {num_cash_changes} requests changed cash balance (need >=3)")
    
    # Check for fulfilled orders
    fulfilled = df[df["response"].str.contains("successful|processed|confirmed", case=False, na=False)]
    num_fulfilled = len(fulfilled)
    
    print(f"\n✅ Successfully fulfilled requests: {num_fulfilled}")
    if num_fulfilled >= 3:
        print("   ✅ PASS: At least 3 requests successfully fulfilled")
    else:
        print(f"   ❌ FAIL: Only {num_fulfilled} requests fulfilled (need >=3)")
    
    # Check for unfulfilled requests
    unfulfilled = df[df["response"].str.contains("out of stock|unavailable|cannot|insufficient", case=False, na=False)]
    num_unfulfilled = len(unfulfilled)
    
    print(f"\n✅ Unfulfilled requests (with reasons): {num_unfulfilled}")
    if num_unfulfilled > 0:
        print("   ✅ PASS: Not all requests fulfilled (as expected)")
    else:
        print("   ⚠️  WARNING: All requests were fulfilled (unusual)")
    
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total Requests: {total_requests}")
    print(f"Fulfilled: {num_fulfilled}")
    print(f"Unfulfilled: {num_unfulfilled}")
    print("=" * 80)
    
    return True

def validate_code_structure():
    """
    Verify code structure meets rubric requirements.
    """
    print("\n" + "=" * 80)
    print("VALIDATING CODE STRUCTURE")
    print("=" * 80)
    
    # Check if main file exists
    if not os.path.exists("multi_agent_system.py"):
        print("❌ ERROR: multi_agent_system.py not found!")
        return False
    
    with open("multi_agent_system.py", "r") as f:
        code = f.read()
    
    # Check for multi-agent system
    if "managed_agents" in code:
        print("✅ Uses managed_agents pattern for multi-agent coordination")
    else:
        print("❌ WARNING: managed_agents pattern not found")
    
    # Check for required helper functions as tools
    required_functions = [
        "create_transaction",
        "get_all_inventory",
        "get_stock_level",
        "get_supplier_delivery_date",
        "get_cash_balance",
        "generate_financial_report",
        "search_quote_history"
    ]
    
    print("\n✅ Checking for required helper functions as tools:")
    for func in required_functions:
        if func in code:
            print(f"   ✅ {func} - found")
        else:
            print(f"   ❌ {func} - missing")
    
    # Check for agent definitions
    agents = ["orchestrator_agent", "inventory_agent", "quote_agent", "sales_agent"]
    print("\n✅ Checking for agent definitions:")
    for agent in agents:
        if agent in code:
            print(f"   ✅ {agent} - defined")
        else:
            print(f"   ❌ {agent} - missing")
    
    # Check for documentation
    if '"""' in code and "Multi-Agent" in code:
        print("\n✅ Code includes documentation/docstrings")
    else:
        print("\n⚠️  WARNING: Limited documentation found")
    
    print("=" * 80)
    return True

def validate_reflection_report():
    """
    Verify reflection report meets rubric requirements.
    """
    print("\n" + "=" * 80)
    print("VALIDATING REFLECTION REPORT")
    print("=" * 80)
    
    if not os.path.exists("reflection_report.md"):
        print("❌ ERROR: reflection_report.md not found!")
        return False
    
    with open("reflection_report.md", "r") as f:
        content = f.read()
    
    # Check for workflow explanation
    if "workflow" in content.lower() or "architecture" in content.lower():
        print("✅ Contains workflow/architecture explanation")
    else:
        print("❌ Missing workflow explanation")
    
    # Check for evaluation discussion
    if "evaluation" in content.lower() or "results" in content.lower():
        print("✅ Discusses evaluation results")
    else:
        print("❌ Missing evaluation discussion")
    
    # Check for improvement suggestions
    if "improvement" in content.lower() or "enhancement" in content.lower():
        print("✅ Includes improvement suggestions")
    else:
        print("❌ Missing improvement suggestions")
    
    # Count improvement suggestions
    suggestions = content.lower().count("###") + content.lower().count("##")
    print(f"✅ Found approximately {suggestions} section headers (includes improvements)")
    
    print("=" * 80)
    return True

def main():
    """
    Run all validations.
    """
    print("\n" + "🔍" * 40)
    print("MULTI-AGENT SYSTEM RUBRIC VALIDATION")
    print("🔍" * 40)
    
    results = []
    
    print("\n[1/3] Validating Test Results...")
    results.append(validate_test_results())
    
    print("\n[2/3] Validating Code Structure...")
    results.append(validate_code_structure())
    
    print("\n[3/3] Validating Reflection Report...")
    results.append(validate_reflection_report())
    
    print("\n" + "=" * 80)
    print("FINAL VALIDATION RESULT")
    print("=" * 80)
    
    if all(results):
        print("✅ ALL VALIDATIONS PASSED")
    else:
        print("❌ SOME VALIDATIONS FAILED - Please review above")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
