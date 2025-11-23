"""
Main entry point for the refinery optimization system.
"""
from workflow import RefineryOptimizationWorkflow
from utils import save_results_to_json


def main():
    """Main function to execute the refinery optimization workflow."""
    feedstocks = [
        "West Texas Intermediate Crude",
        # Alternative feedstocks for testing:
        # "Brent Crude Oil",
        # "Light Sweet Crude",
        # "Heavy Sour Crude",
    ]
    
    workflow = RefineryOptimizationWorkflow()
    
    current_feedstock = feedstocks[0]
    results = workflow.run(current_feedstock)
    
    # Optional: Save results to JSON
    # save_results_to_json(results, "refinery_optimization_results.json")


if __name__ == "__main__":
    main()
