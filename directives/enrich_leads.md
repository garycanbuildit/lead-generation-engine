# Enrich GMB Leads with Contact Data

## Goal
Enhance GMB leads by scraping business websites to extract:
- Email addresses
- Social media handles (Facebook, Instagram, TikTok, LinkedIn, X/Twitter)
- Generate personalized cold email for SEO services
- Score leads based on qualification criteria

## Inputs
- **Leads File** (JSON): Output from `scrape_gmb.py` or `scrape_gmb_free.py`
- **Service Type** (string): Type of service to offer (default: "SEO services")

## Execution

### Primary Script
`execution/enrich_leads.py` - Website scraper and lead enrichment

```bash
python3 execution/enrich_leads.py \
  --input .tmp/houston_appliance_repair.json \
  --output .tmp/enriched_leads.txt
```

## Outputs

### Primary Deliverable
Text file with enriched lead data including:
- All original GMB data
- Email address (if found)
- Social media handles (Facebook, Instagram, TikTok, LinkedIn, X)
- Lead score (1-5 points)
- Personalized cold email template

### Lead Scoring System

**Total: 5 points maximum**

1. **Service Business** (1 point)
   - Is this a service-based business? (Yes = 1 point)

2. **Email Address** (3 points)
   - Email found on website = 3 points
   - No email found = 0 points

3. **Social Media Presence** (1 point)
   - Has at least one social media handle = 1 point
   - No social media = 0 points

**Score Interpretation:**
- 5 points = Hot lead (service business + email + social)
- 4 points = Warm lead (service business + email OR social)
- 3 points = Cold lead (email only)
- 1-2 points = Low priority

## Technical Approach

### Email Extraction
- Regex pattern: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
- Common locations: Contact page, footer, about page
- Filter out generic emails (info@, contact@, etc.) - keep them but note

### Social Media Detection
- **Facebook**: Look for `facebook.com/`, `fb.com/`, `fb.me/`
- **Instagram**: Look for `instagram.com/`, `instagr.am/`
- **TikTok**: Look for `tiktok.com/@`
- **LinkedIn**: Look for `linkedin.com/company/`, `linkedin.com/in/`
- **X/Twitter**: Look for `twitter.com/`, `x.com/`

### Cold Email Template
Personalized with:
- Business name
- Location
- Service category
- Specific pain point for their industry

## Data Fields to Extract

**From Website:**
- Email address(es)
- Facebook URL
- Instagram handle
- TikTok handle
- LinkedIn URL
- X/Twitter handle

**Generated:**
- Lead score (1-5)
- Cold email template
- Qualification notes

## Edge Cases & Constraints

### Website Accessibility
- Some websites may block scraping
- Use proper User-Agent headers
- Respect robots.txt
- Handle timeouts gracefully (5-10 second timeout per site)

### Email Validation
- Check email format is valid
- Flag suspicious emails (noreply@, spam@, etc.)
- Prioritize business-specific emails over generic ones

### Social Media Links
- May be in footer, header, or contact page
- Could be icons without text
- May use shortened URLs (bit.ly, etc.)

### Missing Data
- Not all businesses have websites
- Not all websites have email addresses
- Social media may not be linked

### Rate Limiting
- Add 2-3 second delay between website requests
- Don't overwhelm servers
- Consider using async requests for speed

## Error Handling

- **No website**: Skip enrichment, score = 1 (service business only)
- **Website timeout**: Log error, continue with next lead
- **Invalid HTML**: Try to parse anyway, log warning
- **No email found**: Score without email points
- **No social media**: Score without social points

## Performance Considerations

- **Speed**: ~5-10 seconds per website (with delays)
- **Batch size**: Process all leads in one run
- **Memory**: Keep data in memory, write at end
- **Resumability**: Save progress every 10 leads

## Cold Email Template Structure

```
Subject: Quick question about [Business Name]'s online presence

Hi [Business Name] team,

I came across your business while researching appliance repair services 
in Houston, and I noticed a few opportunities to help you get more 
customers online.

Many service businesses in Houston are missing out on 40-60% of potential 
customers because they're not showing up on Google when people search for 
"[service] near me."

I specialize in helping local service businesses like yours:
- Rank #1 on Google Maps
- Get more 5-star reviews
- Show up when customers search for your services

Would you be open to a quick 15-minute call to see if we can help you 
get more customers?

Best regards,
[Your Name]
```

## Learnings & Updates

### 2026-01-31
- Initial directive created
- Need to handle websites without contact pages
- Consider scraping multiple pages (home, contact, about)
- May need to handle JavaScript-heavy sites

### Future Improvements
- Add phone number extraction from website
- Extract business hours from website
- Check if website is mobile-friendly
- Analyze website speed/performance
- Check for existing SEO optimization
- Add sentiment analysis of reviews
