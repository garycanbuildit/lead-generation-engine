# GMB Lead Scraper - README

## What This Does

This intelligent lead generation engine scrapes Google My Business (GMB) profiles and extracts business listing details into clean, usable formats.

## Features

✅ **Multiple Output Formats**: Text, JSON, CSV  
✅ **Rich Data Extraction**: Name, address, phone, website, ratings, hours, and more  
✅ **Flexible Scraping Methods**: SerpAPI (recommended), Google Places API, Browser automation  
✅ **Clean Text Output**: Human-readable format perfect for sales teams  
✅ **Structured Data**: JSON/CSV for CRM imports and automation  
✅ **Error Handling**: Graceful handling of missing data and API errors  

## Quick Start

### 1. Setup
```bash
# Install dependencies
pip3 install -r execution/requirements.txt

# Configure API key
cp .env.template .env
# Edit .env and add your SERPAPI_KEY
```

### 2. Get SerpAPI Key
- Sign up at [https://serpapi.com/](https://serpapi.com/)
- Free tier: 100 searches/month
- Copy your API key to `.env`

### 3. Run Your First Scrape
```bash
python3 execution/scrape_gmb.py \
  --query "coffee shops" \
  --location "San Francisco, CA" \
  --max-results 10
```

## Usage Examples

### Basic Text Output
```bash
python3 execution/scrape_gmb.py \
  --query "restaurants" \
  --location "New York, NY"
```

### Export to CSV (for Excel/CRM)
```bash
python3 execution/scrape_gmb.py \
  --query "plumbers" \
  --location "Austin, TX" \
  --output-format csv \
  --max-results 50
```

### Export to JSON (for automation)
```bash
python3 execution/scrape_gmb.py \
  --query "dentists" \
  --location "Los Angeles, CA" \
  --output-format json
```

## Output Example

See `.tmp/sample_leads_output.txt` for a sample of what the text output looks like.

Each lead includes:
- Business Name
- Category/Type
- Full Address
- Phone Number
- Website URL
- Star Rating & Review Count
- Business Hours
- Google Maps Link
- Description (when available)

## Documentation

- **Setup Guide**: See `GMB_SETUP.md` for detailed installation and configuration
- **Directive**: See `directives/scrape_gmb_leads.md` for technical details and edge cases
- **Main Script**: `execution/scrape_gmb.py`

## Architecture (DOE System)

This follows the Directive → Observation → Experiment pattern:

1. **Directive** (`directives/scrape_gmb_leads.md`): Defines what to scrape and how
2. **Execution** (`execution/scrape_gmb.py`): Deterministic script that does the work
3. **Output** (`.tmp/leads_*.txt`): Clean, usable lead data

## Scraping Methods

### SerpAPI (Default - Recommended)
- Most reliable and easy to use
- Handles anti-bot measures automatically
- 100 free searches/month
- **Status**: ✅ Implemented

### Google Places API
- Official Google API
- Requires Google Cloud account
- **Status**: 🚧 Coming soon

### Browser Automation
- Free, no API keys needed
- Slower and more fragile
- **Status**: 🚧 Coming soon

## Data Fields Extracted

| Field | Description | Always Available |
|-------|-------------|------------------|
| Business Name | Official business name | ✅ |
| Address | Full street address | ✅ |
| Phone | Contact phone number | ⚠️ Usually |
| Website | Business website URL | ⚠️ Usually |
| Rating | Star rating (1-5) | ⚠️ Usually |
| Reviews | Number of reviews | ⚠️ Usually |
| Category | Business type/category | ✅ |
| Maps URL | Google Maps link | ✅ |
| Hours | Operating hours | ⚠️ Sometimes |
| Price Level | Price range ($-$$$$) | ⚠️ Sometimes |
| Description | Business description | ⚠️ Sometimes |

## Best Practices

1. **Start Small**: Test with 10-20 results first
2. **Be Specific**: Use detailed search queries ("italian restaurants" vs "restaurants")
3. **Include Location**: Always specify city and state
4. **Export to CSV**: Easiest for importing into CRM systems
5. **Respect Limits**: Don't exceed your API quota

## Troubleshooting

### No API Key Error
```bash
# Make sure .env exists and contains:
SERPAPI_KEY=your_actual_key_here
```

### No Results Found
- Try a more specific or different query
- Make sure the location is valid
- Check if businesses of that type exist in the area

### Import Error
```bash
pip3 install -r execution/requirements.txt
```

## Legal & Ethical Use

⚠️ **Important**:
- Use for legitimate business purposes only
- Respect privacy laws (GDPR, CCPA)
- Don't spam or harass businesses
- Review Google's Terms of Service
- Use data responsibly

## Next Steps

1. ✅ Read `GMB_SETUP.md` for detailed setup
2. ✅ Get your SerpAPI key
3. ✅ Run a test scrape
4. ✅ Import leads into your CRM
5. ✅ Start generating business!

## Support

- **Directive**: `directives/scrape_gmb_leads.md`
- **Setup Guide**: `GMB_SETUP.md`
- **Script**: `execution/scrape_gmb.py`

---

**Ready to generate leads?** Follow the Quick Start guide above! 🚀
