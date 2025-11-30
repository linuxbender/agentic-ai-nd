import os
import unittest
from datetime import datetime
import pandas as pd

# Ensure we import from project path
from multi_agent_system import (
    normalize_item_name,
    get_supplier_delivery_date,
    calculate_discount_tool,
    process_sale_tool,
    init_database,
    db_engine,
    get_stock_level,
    create_transaction,
)

class TestCoreFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize fresh database for tests
        init_database(db_engine)
        cls.test_date = '2025-04-01'

    def test_normalize_item_name(self):
        self.assertEqual(normalize_item_name('heavy cardstock (white)'), 'Cardstock')
        self.assertEqual(normalize_item_name('Glossy A4 Paper'), 'Glossy paper')
        # Unmapped should return original or closest match
        self.assertIn('paper', normalize_item_name('eco friendly paper'))

    def test_supplier_delivery_date_thresholds(self):
        base = '2025-04-01'
        self.assertEqual(get_supplier_delivery_date(base, 5), '2025-04-01')  # same day
        self.assertEqual(get_supplier_delivery_date(base, 50), '2025-04-02') # +1 day
        self.assertEqual(get_supplier_delivery_date(base, 500), '2025-04-05') # +4 days
        self.assertEqual(get_supplier_delivery_date(base, 1500), '2025-04-08') # +7 days

    def test_discount_calculation(self):
        result = calculate_discount_tool(1000.0, 600, 'wedding')
        self.assertIn('Discount:', result)
        self.assertIn('Large order', result)
        self.assertIn('Special event', result)

    def test_process_sale_and_stock_update(self):
        # Find an item with stock
        stock_df = get_stock_level('Glossy paper', self.test_date)
        initial_stock = int(stock_df['current_stock'].iloc[0])
        response = process_sale_tool('Glossy paper', 10, 0.20, self.test_date)
        self.assertIn('Sale Processed Successfully', response)
        new_stock_df = get_stock_level('Glossy paper', self.test_date)
        # Stock does not change retroactively for same date selection (as query is <= date)
        # Create a later transaction and verify change
        later_date = '2025-04-02'
        create_transaction('Glossy paper', 'sales', 5, 1.0, later_date)
        later_stock_df = get_stock_level('Glossy paper', later_date)
        self.assertEqual(int(later_stock_df['current_stock'].iloc[0]), initial_stock - 10 - 5)

if __name__ == '__main__':
    unittest.main()

