# AI Shopping Assistant

An AI-powered price comparison tool built on top of Google's Computer Use Preview. This assistant can automatically search for products across multiple e-commerce websites, extract prices, and generate comparison reports.

## Features

- **Multi-site Price Comparison**: Automatically searches multiple shopping websites
- **Natural Language Interface**: Just describe what you want to find
- **Automatic Data Extraction**: Extracts product name, price, availability, and URLs
- **Comparison Reports**: Generates both JSON and Markdown reports with sorted prices
- **Flexible Queries**: Use predefined product/site combinations or custom queries

## Setup

Make sure you've completed the main setup from the root README.md:

```bash
# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Install Playwright
playwright install-deps chrome
playwright install chrome

# Set up your API key
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

## Usage

### Basic Usage - Product and Sites

The simplest way to use the shopping assistant is to specify a product and list of sites:

```bash
python shop.py --product "wireless mouse" --sites amazon ebay walmart
```

This will:
1. Search for "wireless mouse" on Amazon, eBay, and Walmart
2. Extract price information from each site
3. Generate a comparison report in `shopping_reports/`

### Custom Query

For more control, you can provide a custom natural language query:

```bash
python shop.py --query "Find me the best price for Sony WH-1000XM5 headphones on Amazon and Best Buy, then generate a report"
```

### Available Options

```
--product PRODUCT        Product name to search for
--sites SITE [SITE ...]  List of websites to check
--query QUERY            Custom natural language query
--env {playwright,browserbase}  Browser environment (default: playwright)
--model MODEL            Gemini model to use
--highlight_mouse        Highlight mouse cursor (useful for debugging)
```

## Examples

### Example 1: Compare Gaming Keyboards

```bash
python shop.py --product "Mechanical Gaming Keyboard RGB" --sites amazon newegg bestbuy
```

### Example 2: Find Best Laptop Deal

```bash
python shop.py --product "Dell XPS 13 laptop" --sites amazon walmart bestbuy
```

### Example 3: Custom Shopping Query

```bash
python shop.py --query "I want to buy AirPods Pro 2nd generation. Check the price on Amazon, Best Buy, and Target. Make sure to get the latest model and save all the information."
```

### Example 4: Specific Product Comparison

```bash
python shop.py --query "Compare prices for 'iPhone 15 Pro 256GB' on amazon.com and bestbuy.com"
```

## Understanding the Output

After the agent completes, you'll find reports in the `shopping_reports/` directory:

### JSON Report (`price_comparison_YYYYMMDD_HHMMSS.json`)

```json
[
  {
    "product_name": "Logitech MX Master 3S Wireless Mouse",
    "price": "$99.99",
    "website": "Amazon",
    "url": "https://amazon.com/...",
    "availability": "In Stock",
    "timestamp": "2025-01-17T10:30:00"
  },
  {
    "product_name": "Logitech MX Master 3S",
    "price": "$104.99",
    "website": "Best Buy",
    "url": "https://bestbuy.com/...",
    "availability": "In Stock",
    "timestamp": "2025-01-17T10:32:00"
  }
]
```

### Markdown Report (`price_comparison_YYYYMMDD_HHMMSS.md`)

A formatted report with:
- Timestamp and product count
- Products sorted by price (lowest to highest)
- Summary with best and highest prices
- Clickable URLs for each product

## How It Works

The Shopping Assistant uses custom functions that the AI can call:

1. **save_product_info()**: Saves product details (name, price, URL, availability)
2. **generate_price_report()**: Creates JSON and Markdown comparison reports

The AI agent:
1. Navigates to each specified website
2. Searches for the product
3. Identifies the product page
4. Extracts relevant information
5. Calls `save_product_info()` to store the data
6. After checking all sites, calls `generate_price_report()` to create the report

## Tips for Best Results

1. **Be Specific**: Use full product names when possible (e.g., "Sony WH-1000XM5" instead of just "headphones")

2. **Common Sites**: The agent works best with popular sites like:
   - amazon.com
   - ebay.com
   - walmart.com
   - bestbuy.com
   - target.com
   - newegg.com

3. **Allow Time**: The agent needs to navigate real websites, so complex searches may take a few minutes

4. **Check Reports**: Always review the generated reports to ensure prices were captured correctly

5. **Product Variations**: Be aware that different sites may have slightly different product variations

## Advanced Usage

### Using with Browserbase

For more stable and scalable usage, use Browserbase:

```bash
export BROWSERBASE_API_KEY="your_key"
export BROWSERBASE_PROJECT_ID="your_project"

python shop.py --product "gaming laptop" --sites amazon newegg --env browserbase
```

### Custom Model

Use a different Gemini model:

```bash
python shop.py --product "webcam" --sites amazon bestbuy --model "gemini-2.5-computer-use-preview-10-2025"
```

## Extending the Shopping Assistant

You can extend the shopping assistant by modifying `shopping_assistant.py`:

### Add New Custom Functions

```python
def calculate_shipping(base_price: str, location: str) -> dict:
    """Calculates estimated shipping costs."""
    # Your logic here
    return {"shipping": "$5.99"}
```

Then add it to the `ShoppingBrowserAgent.__init__`:

```python
shopping_functions = [
    types.FunctionDeclaration.from_callable(
        client=self._client, callable=save_product_info
    ),
    types.FunctionDeclaration.from_callable(
        client=self._client, callable=generate_price_report
    ),
    types.FunctionDeclaration.from_callable(
        client=self._client, callable=calculate_shipping
    ),
]
```

## Troubleshooting

### "No product data available to generate report"

The agent couldn't find or save product information. Try:
- Making your product name more specific
- Using more common shopping sites
- Checking your internet connection

### Agent seems stuck

- Some websites have complex layouts that confuse the agent
- Try using `--highlight_mouse` to see what the agent is doing
- Simplify your query or try different websites

### Prices seem incorrect

- Different sites may show different prices (sales, shipping, etc.)
- The agent extracts visible prices - always verify by clicking the URLs in the report
- Some sites require accounts or show location-based pricing

## Learning Opportunities

This project demonstrates:

1. **Browser Automation**: How AI can control real browsers
2. **Web Scraping**: Extracting structured data from unstructured web pages
3. **Function Calling**: How AI models can use custom tools
4. **Data Processing**: Collecting, sorting, and reporting on data
5. **Natural Language**: Converting human requests into actions

## Next Steps

Try enhancing the shopping assistant:

- Add price history tracking
- Send email notifications for price drops
- Compare shipping costs
- Filter by ratings/reviews
- Add support for international sites
- Create a web dashboard for viewing reports

Happy shopping! 🛍️
