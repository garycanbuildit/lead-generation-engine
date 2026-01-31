# 📊 Google Sheets Export - Setup Guide

## Quick Start

Export your leads to Google Sheets with one command:

```bash
python3 execution/export_to_sheets.py \
  --input .tmp/houston_landscapers_complete.json \
  --title "Houston Landscapers - Leads"
```

---

## 🔧 Setup (One-Time)

### Step 1: Install Google Sheets API Libraries

```bash
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 2: Get Google API Credentials

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/

2. **Create a New Project:**
   - Click "Select a project" → "New Project"
   - Name it: "Lead Generation Engine"
   - Click "Create"

3. **Enable Google Sheets API:**
   - In the search bar, type "Google Sheets API"
   - Click on it and click "Enable"

4. **Create OAuth 2.0 Credentials:**
   - Go to "Credentials" (left sidebar)
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure the OAuth consent screen:
     - User Type: External
     - App name: "Lead Generation Engine"
     - User support email: your email
     - Developer contact: your email
     - Click "Save and Continue" through the rest
   - Back to "Create OAuth client ID":
     - Application type: "Desktop app"
     - Name: "Lead Export"
     - Click "Create"

5. **Download Credentials:**
   - Click the download icon (⬇️) next to your new OAuth 2.0 Client ID
   - Save the file as `credentials.json`
   - Move it to your project directory: `/Users/garymills/antigravity001/`

### Step 3: First Run (Authorization)

```bash
python3 execution/export_to_sheets.py \
  --input .tmp/houston_landscapers_complete.json
```

- A browser window will open
- Sign in with your Google account
- Click "Allow" to grant permissions
- The script will save a `token.json` file for future use

---

## 📊 What Gets Exported

Your Google Sheet will have these columns:

| Column | Description |
|--------|-------------|
| **Name** | Business name |
| **Website** | Business website URL |
| **Phone** | Phone number |
| **Email** | Email address(es) |
| **Score** | Lead score (1-5) |
| **Facebook Link** | Facebook profile/page |
| **Instagram Link** | Instagram handle |
| **TikTok Link** | TikTok profile |
| **X Link** | X/Twitter handle |
| **LinkedIn Link** | LinkedIn company page |
| **Address** | Full address |
| **Rating** | Star rating |
| **Reviews** | Number of reviews |
| **Category** | Business category |
| **Hours** | Business hours |
| **Price Level** | Price level ($, $$, $$$) |

---

## 🚀 Usage Examples

### Basic Export
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/houston_landscapers_complete.json
```

### With Custom Title
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/houston_landscapers_complete.json \
  --title "Houston Landscapers - Jan 2026"
```

### Export Different Industries
```bash
# Plumbers
python3 execution/export_to_sheets.py \
  --input .tmp/dallas_plumbers.json \
  --title "Dallas Plumbers"

# HVAC
python3 execution/export_to_sheets.py \
  --input .tmp/austin_hvac.json \
  --title "Austin HVAC Companies"

# Dentists
python3 execution/export_to_sheets.py \
  --input .tmp/miami_dentists.json \
  --title "Miami Dentists"
```

---

## 🔄 Complete Workflow

### 1. Scrape GMB Listings
```bash
python3 execution/scrape_gmb_free.py \
  --query "landscapers" \
  --location "Houston, TX" \
  --max-results 10 \
  --output-format json \
  --output .tmp/leads.json
```

### 2. Enrich with Contact Data
```bash
python3 execution/enrich_leads.py \
  --input .tmp/leads.json \
  --output .tmp/leads_enriched.txt
```

### 3. Export to Google Sheets
```bash
python3 execution/export_to_sheets.py \
  --input .tmp/leads.json \
  --title "My Leads"
```

**Note:** The export script reads from the JSON file, which already contains enriched data (emails, social media, scores).

---

## ✨ Features

### Automatic Formatting
- ✅ Header row is frozen (stays visible when scrolling)
- ✅ Header row is bold with gray background
- ✅ Columns are auto-resized to fit content
- ✅ Clean, professional appearance

### Smart Data Handling
- ✅ Multiple emails are comma-separated
- ✅ Missing data shows as empty cells
- ✅ Social media links are clickable
- ✅ Website URLs are clickable

### Easy Sharing
- ✅ Get a shareable Google Sheets URL
- ✅ Share with your team
- ✅ Edit online collaboratively
- ✅ Export to Excel/CSV from Google Sheets

---

## 📋 Sample Output

After running the script, you'll get:

```
================================================================================
EXPORTING LEADS TO GOOGLE SHEETS
================================================================================
Total leads: 10
================================================================================

🔐 Authenticating with Google...
✓ Authenticated successfully

📊 Creating Google Sheet: 'Houston Landscapers - Leads'...
✓ Spreadsheet created: 1a2b3c4d5e6f7g8h9i0j

📝 Preparing data...
✓ Prepared 10 rows (+ header)

📤 Writing data to Google Sheet...
✓ Data written successfully

🎨 Formatting sheet...
✓ Formatting complete

================================================================================
✅ EXPORT COMPLETE!
================================================================================

📊 Google Sheet URL:
https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j/edit

📋 Columns exported:
  1. Name
  2. Website
  3. Phone
  4. Email
  5. Score
  6. Facebook Link
  7. Instagram Link
  8. TikTok Link
  9. X Link
  10. LinkedIn Link
  11. Address
  12. Rating
  13. Reviews
  14. Category
  15. Hours
  16. Price Level

📊 Total leads exported: 10

🔗 Open in browser: https://docs.google.com/spreadsheets/d/1a2b3c4d5e6f7g8h9i0j/edit
```

---

## 🔒 Security & Privacy

### Files Created
- `credentials.json` - Your OAuth credentials (keep private!)
- `token.json` - Your access token (keep private!)

### .gitignore
Both files are automatically excluded from git:
```
credentials.json
token.json
```

### Permissions
The script only requests access to:
- ✅ Create and edit Google Sheets
- ❌ No access to other files
- ❌ No access to Gmail
- ❌ No access to Drive files

---

## 🐛 Troubleshooting

### "credentials.json not found"
**Solution:** Follow Step 2 above to download credentials from Google Cloud Console.

### "Authentication failed"
**Solution:** Delete `token.json` and run the script again to re-authenticate.

### "Permission denied"
**Solution:** Make sure you clicked "Allow" during the OAuth flow.

### "Module not found"
**Solution:** Install the required libraries:
```bash
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

## 📚 Additional Resources

- **Google Sheets API Docs:** https://developers.google.com/sheets/api
- **Python Quickstart:** https://developers.google.com/sheets/api/quickstart/python
- **OAuth 2.0 Guide:** https://developers.google.com/identity/protocols/oauth2

---

## 🎯 Tips

### Organize Your Sheets
Create separate sheets for different:
- Industries (landscapers, plumbers, HVAC)
- Cities (Houston, Dallas, Austin)
- Dates (Jan 2026, Feb 2026)

### Use Google Sheets Features
- ✅ Sort by score (highest first)
- ✅ Filter by rating (4+ stars)
- ✅ Color-code by lead quality
- ✅ Add notes and follow-up dates
- ✅ Share with your sales team

### Export Options
From Google Sheets, you can:
- Download as Excel (.xlsx)
- Download as CSV
- Download as PDF
- Import into CRM

---

**🎉 You're ready to export leads to Google Sheets!**
