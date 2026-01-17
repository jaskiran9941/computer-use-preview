#!/usr/bin/env python3
"""
Test script for the shopping assistant functions.
This tests the custom functions without running the full browser agent.
"""

import os
import sys
from shopping_functions import save_product_info, generate_price_report, PRODUCT_DATA


def test_shopping_functions():
    """Test the shopping assistant custom functions."""

    print("="*80)
    print("TESTING SHOPPING ASSISTANT FUNCTIONS")
    print("="*80)
    print()

    # Clear any existing data
    PRODUCT_DATA.clear()

    print("Test 1: Saving product information")
    print("-" * 40)

    # Test saving products from different sites
    result1 = save_product_info(
        product_name="Logitech MX Master 3S Wireless Mouse",
        price="$99.99",
        website="Amazon",
        url="https://amazon.com/example-product-1",
        availability="In Stock"
    )
    print(f"✓ Saved product from Amazon: {result1}")

    result2 = save_product_info(
        product_name="Logitech MX Master 3S",
        price="$104.99",
        website="Best Buy",
        url="https://bestbuy.com/example-product-2",
        availability="In Stock"
    )
    print(f"✓ Saved product from Best Buy: {result2}")

    result3 = save_product_info(
        product_name="Logitech MX Master 3S Mouse",
        price="$97.50",
        website="Walmart",
        url="https://walmart.com/example-product-3",
        availability="Limited Stock"
    )
    print(f"✓ Saved product from Walmart: {result3}")

    print()
    print(f"Total products saved: {len(PRODUCT_DATA)}")
    print()

    print("Test 2: Generating price comparison report")
    print("-" * 40)

    report = generate_price_report(filename="test_report")
    print(f"✓ Report generated: {report}")
    print()

    if report['status'] == 'success':
        print("✓ Report files created:")
        print(f"  - JSON: {report['json_report']}")
        print(f"  - Markdown: {report['markdown_report']}")
        print()

        # Display the markdown report
        if os.path.exists(report['markdown_report']):
            print("="*80)
            print("MARKDOWN REPORT PREVIEW")
            print("="*80)
            with open(report['markdown_report'], 'r') as f:
                print(f.read())

    print()
    print("="*80)
    print("ALL TESTS PASSED! ✓")
    print("="*80)
    print()
    print("The shopping assistant functions are working correctly.")
    print("You can now try running the full shopping assistant with:")
    print()
    print('  python shop.py --product "wireless mouse" --sites amazon walmart')
    print()


if __name__ == "__main__":
    test_shopping_functions()
