# Quick Start Guide - Shopping Assistant

Get started with the AI Shopping Assistant in 5 minutes!

## Prerequisites

Make sure you have:
- Python 3.10 or higher
- A Google Gemini API key (get one at https://aistudio.google.com/apikey)

## Step 1: Setup (One Time)

```bash
# Clone and navigate to the repo (if you haven't already)
cd computer-use-preview

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install-deps chrome
playwright install chrome

# Set your API key
export GEMINI_API_KEY="your-api-key-here"
```

## Step 2: Run Your First Price Comparison

Try this simple example:

```bash
python shop.py --product "wireless mouse" --sites amazon walmart
```

The AI will:
1. Open a browser
2. Search for "wireless mouse" on Amazon
3. Extract the price and product info
4. Do the same for Walmart
5. Generate a comparison report

## Step 3: View Your Results

Check the `shopping_reports/` directory:

```bash
ls -la shopping_reports/

# View the markdown report
cat shopping_reports/price_comparison_*.md
```

## More Examples

### Example 1: Gaming Keyboard

```bash
python shop.py --product "Mechanical Gaming Keyboard RGB" --sites amazon newegg
```

### Example 2: Headphones (Custom Query)

```bash
python shop.py --query "Find Sony WH-1000XM5 headphones on Amazon and Best Buy, compare prices"
```

### Example 3: Use Pre-made Examples

```bash
cd examples
./shop_example_1.sh
```

## What's Happening?

When you run the shopping assistant:

1. **Browser Opens**: A Chrome browser window opens (you'll see it!)
2. **AI Navigation**: The Gemini AI navigates to each website
3. **Smart Search**: It searches for your product
4. **Data Extraction**: Extracts prices, names, and availability
5. **Report Generation**: Creates JSON and Markdown reports

## Understanding the Output

You'll see real-time output like:

```
========================================
AI SHOPPING ASSISTANT
========================================

Product: wireless mouse
Sites to check: amazon, walmart

Starting shopping assistant...

[AI thinks and navigates...]

SHOPPING ASSISTANT COMPLETE
========================================

Check the 'shopping_reports' directory for your price comparison report!
```

## Tips for Best Results

1. **Be Specific**: "Logitech MX Master 3S" works better than "mouse"
2. **Patience**: Real websites take time to load and navigate
3. **Verify**: Always check the generated URLs to confirm prices
4. **Popular Sites**: Stick to well-known sites for best results

## Common Sites That Work Well

- amazon.com (or amazon.co.uk, amazon.ca, etc.)
- walmart.com
- bestbuy.com
- target.com
- ebay.com
- newegg.com

## Troubleshooting

### "No module named 'google'"

Run: `pip install -r requirements.txt`

### "API key not found"

Make sure you set: `export GEMINI_API_KEY="your-key"`

### Browser doesn't open

Try: `playwright install chrome`

### Reports directory doesn't exist

It will be created automatically on first run

## Next Steps

Now that you've tried the basic shopping assistant:

1. Read the full documentation: `SHOPPING_ASSISTANT.md`
2. Try different products and websites
3. Modify the code to add new features
4. Experiment with custom queries

## Learning Resources

- **Browser Automation**: Watch how the AI navigates websites
- **Function Calling**: Check `shopping_assistant.py` to see custom functions
- **Data Extraction**: See how prices are extracted from different sites
- **Report Generation**: Learn how data is formatted in reports

## Fun Challenges

Try to:
1. Add a new shopping site to your search
2. Compare 5+ different products at once
3. Track prices over time (run multiple times)
4. Add a new custom function (e.g., calculate total with tax)
5. Create a "deal finder" that only reports items under $X

Happy shopping and happy learning! 🎓🛍️

---

For detailed documentation, see `SHOPPING_ASSISTANT.md`
