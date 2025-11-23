from Agent import FactCheckerAgent

if __name__ == "__main__":
    print("\n=== TESTING ENHANCED FactCheckerAgent ===")
    test_fact_checker = FactCheckerAgent("Test Enhanced FactChecker")
    text1 = "This report is clear and all facts are confirmed."
    result1 = test_fact_checker.run(text1)
    print(f"Input: '{text1}'\nOutput Flags: {result1['flags']}\n")
    text2 = "The findings suggest a positive trend, but the outcome is still debated and uncertain due to limited data."
    result2 = test_fact_checker.run(text2)
    print(f"Input: '{text2}'\nOutput Flags: {result2['flags']}\n")
    text3 = "An error was found in the preliminary report, making some conclusions uncertain."
    result3 = test_fact_checker.run(text3)
    print(f"Input: '{text3}'\nOutput Flags: {result3['flags']}\n")