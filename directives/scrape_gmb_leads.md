# Scrape Google My Business Leads

## Goal
Extract business listing details from Google My Business (GMB) profiles to generate leads. Output the data in a clean text format for easy consumption and follow-up.

## Inputs
- **Search Query** (string): The type of business to search for (e.g., "restaurants", "plumbers", "dentists")
- **Location** (string): Geographic area to search (e.g., "New York, NY", "Los Angeles, CA")
- **Max Results** (integer, optional): Maximum number of results to scrape (default: 20)
- **Output Format** (string, optional): Format for output ("txt", "csv", "json", default: "txt")

## Execution

### Primary Script
`execution/scrape_gmb.py` - Main scraping engine

```bash
python3 execution/scrape_gmb.py \
  --query "coffee shops" \
  --location "San Francisco, CA" \
  --max-results 20 \
  --output-format txt
```

### Supporting Scripts
- `execution/gmb_parser.py` - Parses GMB HTML/JSON data
- `execution/format_leads.py` - Formats extracted data into various output formats

## Outputs

### Primary Deliverable
Text file in `.tmp/leads_[timestamp].txt` containing:
- Business Name
- Address
- Phone Number
- Website
- Rating & Review Count
- Business Hours
- Category/Type
- Google Maps URL

### Example Output Format
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
Hours: Mon-Fri 7AM-7PM, Sat-Sun 8AM-6PM
Google Maps: https://maps.google.com/?cid=12345...

--------------------------------------------------------------------------------
```

## Technical Approach

### Method 1: Google Maps API (Recommended if available)
- Use Google Places API for structured data
- Requires API key in `.env`
- Most reliable and terms-compliant

### Method 2: Web Scraping (Fallback)
- Use Playwright/Selenium for dynamic content
- Parse Google Maps search results
- More fragile, requires maintenance
- **Note**: Respect robots.txt and rate limits

### Method 3: Third-party APIs
- Use services like SerpAPI, ScraperAPI
- Requires API key and credits
- Most reliable for production use

## Data Fields to Extract

**Required:**
- Business name
- Address (full)
- Phone number
- Google Maps URL

**Optional (if available):**
- Website URL
- Email address
- Rating (stars)
- Number of reviews
- Business hours
- Category/business type
- Price level
- Photos URLs
- Description

## Edge Cases & Constraints

### Rate Limiting
- Google may block excessive requests
- Implement delays between requests (2-5 seconds recommended)
- Use rotating user agents
- Consider proxy rotation for large-scale scraping

### Missing Data
- Not all businesses have websites or phone numbers
- Handle missing fields gracefully
- Mark incomplete profiles in output

### Anti-Scraping Measures
- Google uses CAPTCHA and bot detection
- May need to use authenticated browser sessions
- Consider using official APIs when possible

### Legal & Ethical Considerations
- Review Google's Terms of Service
- Respect robots.txt
- Don't overload servers
- Use data responsibly (GDPR, privacy laws)

### Data Quality
- Validate phone numbers (format check)
- Validate URLs (check if reachable)
- Deduplicate results
- Handle special characters in business names

## Error Handling

- **No results found**: Log warning, return empty dataset
- **Network timeout**: Retry with exponential backoff (max 3 attempts)
- **CAPTCHA detected**: Pause execution, log error, notify user
- **Invalid location**: Validate location before scraping
- **Parsing errors**: Log failed entries, continue with next result

## Performance Considerations

- **Speed**: ~2-5 seconds per business (with rate limiting)
- **Batch size**: Process in chunks of 20-50 to avoid timeouts
- **Memory**: Keep data in memory until batch complete, then write to file
- **Resumability**: Save progress periodically for large jobs

## Learnings & Updates

### 2026-01-31
- Initial directive created
- Need to determine which scraping method to use based on available resources
- Consider SerpAPI as primary method for reliability

### Future Improvements
- Add email extraction from websites
- Implement duplicate detection across runs
- Add export to Google Sheets
- Create scheduling capability for regular scraping
- Add data enrichment (social media profiles, etc.)
