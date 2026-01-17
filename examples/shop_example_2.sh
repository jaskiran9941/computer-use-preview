#!/bin/bash
# Example 2: Compare gaming headset prices with a custom query

echo "========================================="
echo "Shopping Assistant Example 2"
echo "Product: Gaming Headset"
echo "Custom Query Mode"
echo "========================================="
echo ""

python ../shop.py \
  --query "Find the SteelSeries Arctis Nova Pro gaming headset on Amazon and Best Buy. Compare the prices and check if it's in stock. Save the information and generate a report." \
  --env playwright

echo ""
echo "Done! Check the shopping_reports/ directory for results."
