#!/usr/bin/env python3
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

"""
Shopping Assistant CLI - AI-powered price comparison tool.

This script allows you to compare prices across multiple shopping websites
using natural language commands.

Examples:
    python shop.py --product "wireless mouse" --sites "amazon ebay walmart"
    python shop.py --product "gaming keyboard" --sites "amazon newegg"
    python shop.py --query "Find me the best price for AirPods Pro on Amazon and Best Buy"
"""

import argparse
import sys
from shopping_assistant import ShoppingBrowserAgent
from computers import PlaywrightComputer, BrowserbaseComputer

PLAYWRIGHT_SCREEN_SIZE = (1440, 900)


def build_shopping_query(product_name: str, sites: list[str]) -> str:
    """Builds a natural language query for the shopping agent."""

    query = f"""You are a shopping assistant. Your task is to compare prices for '{product_name}' across multiple websites.

For each website listed below, please:
1. Navigate to the website
2. Search for '{product_name}'
3. Find the product and extract:
   - Exact product name
   - Price (including currency symbol)
   - Availability status (in stock, out of stock, etc.)
   - Product page URL
4. Use the save_product_info function to save this information

Websites to check:
{chr(10).join(f'- {site}' for site in sites)}

After checking all websites, use the generate_price_report function to create a comparison report.

Important tips:
- Make sure to get the EXACT price displayed on each site
- If a product is not available or not found, note that in availability
- Try to find the same or very similar product on each site for accurate comparison
- Save information for each site before moving to the next one
"""

    return query


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AI Shopping Assistant - Compare prices across multiple websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python shop.py --product "wireless mouse" --sites amazon ebay walmart
  python shop.py --product "Sony WH-1000XM5" --sites amazon bestbuy
  python shop.py --query "Find AirPods Pro 2 on Amazon and compare with Best Buy"
        """
    )

    parser.add_argument(
        "--product",
        type=str,
        help="The product name to search for (e.g., 'wireless mouse', 'laptop')",
    )

    parser.add_argument(
        "--sites",
        type=str,
        nargs="+",
        help="List of websites to check (e.g., amazon ebay walmart bestbuy)",
    )

    parser.add_argument(
        "--query",
        type=str,
        help="Custom natural language query for the shopping agent",
    )

    parser.add_argument(
        "--env",
        type=str,
        choices=("playwright", "browserbase"),
        default="playwright",
        help="The browser environment to use (default: playwright)",
    )

    parser.add_argument(
        "--initial_url",
        type=str,
        default="https://www.google.com",
        help="The initial URL to load (default: https://www.google.com)",
    )

    parser.add_argument(
        "--highlight_mouse",
        action="store_true",
        default=False,
        help="Highlight the mouse cursor position (playwright only)",
    )

    parser.add_argument(
        "--model",
        default='gemini-2.5-computer-use-preview-10-2025',
        help="The Gemini model to use (default: gemini-2.5-computer-use-preview-10-2025)",
    )

    args = parser.parse_args()

    # Build or validate query
    if args.query:
        query = args.query
    elif args.product and args.sites:
        query = build_shopping_query(args.product, args.sites)
    else:
        parser.error("You must provide either --query OR both --product and --sites")
        return 1

    print("\n" + "="*80)
    print("AI SHOPPING ASSISTANT")
    print("="*80)

    if args.product:
        print(f"\nProduct: {args.product}")
        print(f"Sites to check: {', '.join(args.sites)}")
    else:
        print(f"\nCustom Query: {args.query}")

    print("\nStarting shopping assistant...\n")

    # Set up browser environment
    if args.env == "playwright":
        env = PlaywrightComputer(
            screen_size=PLAYWRIGHT_SCREEN_SIZE,
            initial_url=args.initial_url,
            highlight_mouse=args.highlight_mouse,
        )
    elif args.env == "browserbase":
        env = BrowserbaseComputer(
            screen_size=PLAYWRIGHT_SCREEN_SIZE,
            initial_url=args.initial_url
        )
    else:
        raise ValueError(f"Unknown environment: {args.env}")

    # Run the shopping agent
    with env as browser_computer:
        agent = ShoppingBrowserAgent(
            browser_computer=browser_computer,
            query=query,
            model_name=args.model,
        )
        agent.agent_loop()

    print("\n" + "="*80)
    print("SHOPPING ASSISTANT COMPLETE")
    print("="*80)
    print("\nCheck the 'shopping_reports' directory for your price comparison report!")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
