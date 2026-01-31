# GMB Lead Scraper - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r execution/requirements.txt
```

### 2. Get Your SerpAPI Key (Recommended Method)

1. Go to [https://serpapi.com/](https://serpapi.com/)
2. Sign up for a free account (100 searches/month free)
3. Copy your API key from the dashboard

### 3. Configure Environment

```bash
# Copy the template
cp .env.template .env

# Edit .env and add your SerpAPI key
# SERPAPI_KEY=your_actual_key_here
```

### 4. Run Your First Scrape

```bash
python3 execution/scrape_gmb.py \
  --query "coffee shops" \
  --location "San Francisco, CA" \
  --max-results 10
```

## Usage Examples

### Basic Search
```bash
python3 execution/scrape_gmb.py \
  --query "restaurants" \
  --location "New York, NY"
```

### Export to JSON
```bash
python3 execution/scrape_gmb.py \
  --query "plumbers" \
  --location "Austin, TX" \
  --output-format json
```

### Export to CSV
```bash
python3 execution/scrape_gmb.py \
  --query "dentists" \
  --location "Los Angeles, CA" \
  --output-format csv \
  --max-results 50
```

### Custom Output Path
```bash
python3 execution/scrape_gmb.py \
  --query "gyms" \
  --location "Miami, FL" \
  --output my_leads.txt
```

## Output Formats

### Text Format (Default)
Clean, readable text file with all business details:
```
================================================================================
LEAD #1
================================================================================
Business Name: Blue Bottle Coffee
Category: Coffee Shop
Address: 66 Mint St, San Francisco, CA 94103
Phone: (510) 653-3394
Website: https://bluebottlecoffee.com
Rating: 4.5 stars (1,234 reviews)
...
```

### JSON Format
Structured data for programmatic use:
```json
{
  "generated": "2026-01-31T11:38:00",
  "total_leads": 10,
  "leads": [
    {
      "name": "Blue Bottle Coffee",
      "address": "66 Mint St, San Francisco, CA 94103",
      ...
    }
  ]
}
```

### CSV Format
Spreadsheet-compatible format for Excel/Google Sheets:
```csv
name,address,phone,website,rating,reviews,...
Blue Bottle Coffee,"66 Mint St, San Francisco, CA 94103",(510) 653-3394,...
```

## Data Fields Extracted

- ✅ Business Name
- ✅ Full Address
- ✅ Phone Number
- ✅ Website URL
- ✅ Star Rating
- ✅ Number of Reviews
- ✅ Business Category
- ✅ Google Maps URL
- ✅ Price Level (when available)
- ✅ Business Hours (when available)
- ✅ Description (when available)

## Scraping Methods

### Method 1: SerpAPI (Default - Recommended)
- **Pros**: Most reliable, handles anti-bot measures, structured data
- **Cons**: Requires API key, limited free tier (100/month)
- **Setup**: Get key at https://serpapi.com/

```bash
python3 execution/scrape_gmb.py --method serpapi --query "..." --location "..."
```

### Method 2: Google Places API (Coming Soon)
- **Pros**: Official Google API, reliable
- **Cons**: Requires Google Cloud account, costs money after free tier
- **Setup**: Enable Places API in Google Cloud Console

```bash
python3 execution/scrape_gmb.py --method places --query "..." --location "..."
```

### Method 3: Browser Automation (Coming Soon)
- **Pros**: Free, no API keys needed
- **Cons**: Slower, more fragile, may hit CAPTCHAs
- **Setup**: Install Playwright or Selenium

```bash
python3 execution/scrape_gmb.py --method browser --query "..." --location "..."
```

## Rate Limits & Best Practices

### SerpAPI Free Tier
- 100 searches per month
- No rate limiting within the quota
- Upgrade for more searches

### Recommendations
- Start with small batches (10-20 results) to test
- Use specific search queries for better results
- Include city/state in location for accuracy
- Export to CSV for easy import into CRM systems

## Troubleshooting

### "SERPAPI_KEY not found in .env file"
- Make sure you copied `.env.template` to `.env`
- Add your actual API key to the `.env` file
- Don't use quotes around the key

### "No leads found"
- Try a different search query
- Make the location more specific
- Check if the business type exists in that area

### "requests library not installed"
```bash
pip install -r execution/requirements.txt
```

### Rate limit exceeded
- Wait until next month (free tier resets)
- Upgrade your SerpAPI plan
- Use a different scraping method

## Next Steps

1. **Test the scraper** with a small query
2. **Review the output** in `.tmp/` directory
3. **Import leads** into your CRM or spreadsheet
4. **Automate** by creating a workflow for regular scraping
5. **Enrich data** by visiting websites to find emails

## Advanced Usage

### Batch Processing Multiple Locations
Create a script to loop through multiple cities:

```bash
for city in "New York, NY" "Los Angeles, CA" "Chicago, IL"; do
  python3 execution/scrape_gmb.py \
    --query "restaurants" \
    --location "$city" \
    --output-format csv \
    --output "leads_${city// /_}.csv"
done
```

### Scheduled Scraping
Use cron to run weekly:

```bash
# Add to crontab (crontab -e)
0 9 * * 1 cd /path/to/antigravity001 && python3 execution/scrape_gmb.py --query "..." --location "..."
```

## Legal & Ethical Considerations

⚠️ **Important**: 
- Review Google's Terms of Service
- Use data responsibly and comply with privacy laws (GDPR, CCPA)
- Don't spam or harass businesses
- Respect opt-out requests
- Use for legitimate business purposes only

## Support

For issues or questions:
1. Check the directive: `directives/scrape_gmb_leads.md`
2. Review error messages carefully
3. Verify your API key is correct
4. Check SerpAPI dashboard for quota/usage

---

**Ready to generate leads?** Run your first scrape and watch the magic happen! ✨
