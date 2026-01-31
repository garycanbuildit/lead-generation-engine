# 📊 Export to Google Sheets - Quick Reference

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. Get Google Credentials
1. Go to https://console.cloud.google.com/
2. Create a project → Enable "Google Sheets API"
3. Create "OAuth 2.0 Client ID" (Desktop app)
4. Download as `credentials.json` → Save to project root

### 3. Export Your Leads
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/houston_landscapers_complete.json \
  --title "Houston Landscapers"
```

**First time:** Browser will open for authorization → Click "Allow"  
**After that:** Automatic (uses saved token.json)

---

## 📋 What Gets Exported

Your Google Sheet will have these columns:

1. **Name** - Business name
2. **Website** - Business website URL
3. **Phone** - Phone number
4. **Email** - Email address(es)
5. **Score** - Lead score (1-5)
6. **Facebook Link** - Facebook profile
7. **Instagram Link** - Instagram handle
8. **TikTok Link** - TikTok profile
9. **X Link** - X/Twitter handle
10. **LinkedIn Link** - LinkedIn page
11. **Address** - Full address
12. **Rating** - Star rating
13. **Reviews** - Number of reviews
14. **Category** - Business category
15. **Hours** - Business hours
16. **Price Level** - Price level ($, $$, $$$)

---

## 🔄 Complete Workflow

```bash
# Step 1: Scrape GMB listings
python3 execution/scrape_gmb_free.py \
  --query "landscapers" \
  --location "Houston, TX" \
  --max-results 10 \
  --output-format json \
  --output .tmp/leads.json

# Step 2: Enrich with contact data
python3 execution/enrich_leads.py \
  --input .tmp/leads.json \
  --output .tmp/leads_enriched.txt

# Step 3: Export to Google Sheets
python3 execution/export_to_sheets.py \
  --input .tmp/leads.json \
  --title "My Leads"
```

---

## 💡 Examples

### Houston Landscapers
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/houston_landscapers_complete.json \
  --title "Houston Landscapers - Jan 2026"
```

### Dallas Plumbers
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/dallas_plumbers.json \
  --title "Dallas Plumbers"
```

### Austin HVAC
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/austin_hvac.json \
  --title "Austin HVAC Companies"
```

---

## 🎯 Output

After export, you'll get a Google Sheets URL like:
```
https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j/edit
```

**Features:**
- ✅ Header row frozen (stays visible when scrolling)
- ✅ Header row bold with gray background
- ✅ Columns auto-resized
- ✅ Clickable links (website, social media)
- ✅ Ready to share with your team

---

## 🔧 Troubleshooting

**"credentials.json not found"**
→ Download from Google Cloud Console (see GOOGLE_SHEETS_SETUP.md)

**"Module not found"**
→ Run: `pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`

**"Authentication failed"**
→ Delete `token.json` and run again

---

## 📚 Full Documentation

See `GOOGLE_SHEETS_SETUP.md` for:
- Detailed setup instructions
- Google Cloud Console walkthrough
- Security & privacy info
- Advanced usage examples

---

**🎉 Export your leads to Google Sheets in seconds!**
