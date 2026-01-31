# 🚀 Quick Start: Lead Generation Engine

## Complete Workflow

### 1️⃣ Scrape GMB Listings

```bash
python3 execution/scrape_gmb_free.py \
  --query "appliance repair" \
  --location "Houston, TX" \
  --max-results 10 \
  --output-format json \
  --output .tmp/leads.json
```

**Output**: JSON file with 10 GMB listings

---

### 2️⃣ Enrich with Contact Data

```bash
python3 execution/enrich_leads.py \
  --input .tmp/leads.json \
  --output .tmp/enriched_leads.txt
```

**Output**: Text file with:
- ✅ Email addresses
- ✅ Social media handles
- ✅ Lead scores (1-5)
- ✅ Personalized cold emails

---

## What You Get

### For Each Lead:

```
Business Name: Houston Appliance Repair Pros
Phone: (713) 555-0101
Website: https://www.houstonappliancepros.com

📧 EMAILS:
  - info@houstonappliancepros.com
  - contact@houstonappliancepros.com

📱 SOCIAL MEDIA:
  - Facebook: https://facebook.com/houstonappliancepros
  - Instagram: https://instagram.com/houstonappliancepros

⭐ LEAD SCORE: 5/5
  - Service Business: 1 point ✓
  - Email Address: 3 points ✓
  - Social Media: 1 point ✓

📨 COLD EMAIL:
[Personalized email template ready to send]
```

---

## Lead Scoring

| Score | Quality | What It Means |
|-------|---------|---------------|
| 5/5 | 🔥 Hot | Service + Email + Social |
| 4/5 | 🌡️ Warm | Service + Email OR Social |
| 3/5 | ❄️ Cold | Email only |
| 1-2/5 | 📋 Low | Limited contact info |

---

## Installation

```bash
# Install dependencies
pip3 install -r execution/requirements.txt

# Or manually
pip3 install requests beautifulsoup4 python-dotenv
```

---

## Files Structure

```
antigravity001/
├── directives/
│   ├── scrape_gmb_leads.md      # GMB scraping directive
│   └── enrich_leads.md          # Lead enrichment directive
│
├── execution/
│   ├── scrape_gmb_free.py       # GMB scraper (free, no API)
│   ├── enrich_leads.py          # Lead enrichment
│   └── requirements.txt         # Dependencies
│
└── .tmp/
    ├── leads.json               # Raw GMB data
    └── enriched_leads.txt       # Final output
```

---

## Example: Different Industries

### HVAC Companies
```bash
python3 execution/scrape_gmb_free.py \
  --query "HVAC repair" \
  --location "Dallas, TX" \
  --max-results 20 \
  --output-format json \
  --output .tmp/hvac_dallas.json

python3 execution/enrich_leads.py \
  --input .tmp/hvac_dallas.json \
  --output .tmp/hvac_dallas_enriched.txt
```

### Plumbers
```bash
python3 execution/scrape_gmb_free.py \
  --query "plumbers" \
  --location "Austin, TX" \
  --max-results 15 \
  --output-format json \
  --output .tmp/plumbers_austin.json

python3 execution/enrich_leads.py \
  --input .tmp/plumbers_austin.json \
  --output .tmp/plumbers_austin_enriched.txt
```

### Electricians
```bash
python3 execution/scrape_gmb_free.py \
  --query "electricians" \
  --location "San Antonio, TX" \
  --max-results 25 \
  --output-format json \
  --output .tmp/electricians_sa.json

python3 execution/enrich_leads.py \
  --input .tmp/electricians_sa.json \
  --output .tmp/electricians_sa_enriched.txt
```

---

## Tips for Best Results

### 1. Use Specific Queries
✅ Good: "appliance repair", "HVAC repair", "emergency plumber"
❌ Bad: "repair", "services", "business"

### 2. Include Location
✅ Good: "Houston, TX", "Dallas, TX", "Austin, TX"
❌ Bad: "Texas", "USA"

### 3. Adjust Delay for Politeness
```bash
# Slower, more polite (recommended)
python3 execution/enrich_leads.py \
  --input .tmp/leads.json \
  --output .tmp/enriched.txt \
  --delay 3.0

# Faster (use with caution)
python3 execution/enrich_leads.py \
  --input .tmp/leads.json \
  --output .tmp/enriched.txt \
  --delay 1.0
```

### 4. Filter by Score
```bash
# View only hot leads (5/5)
grep -A 50 "SCORE: 5/5" .tmp/enriched_leads.txt

# View warm and hot leads (4-5/5)
grep -A 50 "SCORE: [45]/5" .tmp/enriched_leads.txt
```

---

## Current Status: Sample Data

⚠️ **Note**: The current system uses **sample data** with fake websites.

To get **real data**, you need to:
1. Set up SerpAPI (100 free searches/month)
2. Or use browser automation (Playwright/Selenium)

See `directives/scrape_gmb_leads.md` for details.

---

## Next Steps

1. ✅ Review sample output in `.tmp/enriched_leads_demo.txt`
2. ✅ Set up real GMB scraping (SerpAPI recommended)
3. ✅ Run on real data
4. ✅ Verify email addresses
5. ✅ Customize cold emails
6. ✅ Start outreach!

---

## Support

- **Directives**: See `directives/` for detailed instructions
- **Documentation**: See `LEAD_ENRICHMENT_COMPLETE.md`
- **Examples**: See `.tmp/` for sample outputs

---

**🎯 You're ready to generate leads!**
