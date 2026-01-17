# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shopping Assistant Functions - Price comparison utilities."""

import os
import json
from datetime import datetime
from typing import Optional

# Global storage for product data
PRODUCT_DATA = []


def save_product_info(
    product_name: str,
    price: str,
    website: str,
    url: str,
    availability: str = "Unknown"
) -> dict:
    """
    Saves product information for comparison.

    Args:
        product_name: Name of the product
        price: Price as a string (e.g., "$29.99", "£45.00")
        website: Name of the website (e.g., "Amazon", "eBay")
        url: URL of the product page
        availability: Stock availability status

    Returns:
        A confirmation dictionary with the saved product info
    """
    product_info = {
        "product_name": product_name,
        "price": price,
        "website": website,
        "url": url,
        "availability": availability,
        "timestamp": datetime.now().isoformat()
    }

    PRODUCT_DATA.append(product_info)

    return {
        "status": "success",
        "message": f"Saved product info from {website}",
        "total_products_saved": len(PRODUCT_DATA)
    }


def generate_price_report(filename: Optional[str] = None) -> dict:
    """
    Generates a price comparison report from all saved product data.

    Args:
        filename: Optional custom filename for the report (without extension)

    Returns:
        A dictionary with report details and file path
    """
    if not PRODUCT_DATA:
        return {
            "status": "error",
            "message": "No product data available to generate report"
        }

    # Generate filename
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"price_comparison_{timestamp}"

    # Create reports directory if it doesn't exist
    os.makedirs("shopping_reports", exist_ok=True)

    # Generate JSON report
    json_path = f"shopping_reports/{filename}.json"
    with open(json_path, 'w') as f:
        json.dump(PRODUCT_DATA, f, indent=2)

    # Generate Markdown report
    md_path = f"shopping_reports/{filename}.md"
    with open(md_path, 'w') as f:
        f.write("# Price Comparison Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total Products Compared:** {len(PRODUCT_DATA)}\n\n")
        f.write("---\n\n")

        # Sort by price (try to extract numeric value)
        def extract_price(item):
            price_str = item['price']
            # Remove currency symbols and convert to float
            import re
            numbers = re.findall(r'\d+\.?\d*', price_str.replace(',', ''))
            return float(numbers[0]) if numbers else float('inf')

        try:
            sorted_products = sorted(PRODUCT_DATA, key=extract_price)
        except:
            sorted_products = PRODUCT_DATA

        for idx, product in enumerate(sorted_products, 1):
            f.write(f"## {idx}. {product['website']}\n\n")
            f.write(f"**Product:** {product['product_name']}\n\n")
            f.write(f"**Price:** {product['price']}\n\n")
            f.write(f"**Availability:** {product['availability']}\n\n")
            f.write(f"**URL:** [{product['url']}]({product['url']})\n\n")
            f.write("---\n\n")

        # Add summary
        f.write("## Summary\n\n")
        if sorted_products:
            f.write(f"**Best Price:** {sorted_products[0]['price']} at {sorted_products[0]['website']}\n\n")
            if len(sorted_products) > 1:
                f.write(f"**Highest Price:** {sorted_products[-1]['price']} at {sorted_products[-1]['website']}\n\n")

    return {
        "status": "success",
        "message": f"Generated price comparison report",
        "products_compared": len(PRODUCT_DATA),
        "json_report": json_path,
        "markdown_report": md_path,
        "best_price": PRODUCT_DATA[0]['price'] if PRODUCT_DATA else None
    }


def clear_product_data():
    """Clears all saved product data."""
    global PRODUCT_DATA
    PRODUCT_DATA = []
