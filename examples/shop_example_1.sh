#!/bin/bash
# Example 1: Compare wireless mouse prices across Amazon, eBay, and Walmart

echo "========================================="
echo "Shopping Assistant Example 1"
echo "Product: Wireless Mouse"
echo "Sites: Amazon, eBay, Walmart"
echo "========================================="
echo ""

python ../shop.py \
  --product "Logitech MX Master 3S wireless mouse" \
  --sites amazon ebay walmart \
  --env playwright

echo ""
echo "Done! Check the shopping_reports/ directory for results."
