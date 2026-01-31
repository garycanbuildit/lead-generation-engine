# 🌐 Lead Generation Engine - Web UI

## Quick Start

### 1. Install Web Server Dependencies
```bash
pip3 install flask flask-cors
```

### 2. Start the Server
```bash
python3 web/server.py
```

### 3. Open in Browser
Visit: http://localhost:5000

---

## What You Get

A beautiful web interface where users can:

1. **Enter Search Criteria:**
   - Business type (e.g., "landscapers", "plumbers")
   - Location (e.g., "Houston, TX")
   - Number of leads (5-50)
   - Enrich data (yes/no)

2. **View Results:**
   - Lead cards with all data
   - Stats (total leads, with email, avg rating)
   - Clickable links (website, social media)

3. **Export to Google Sheets:**
   - One-click export button
   - Opens Google Sheet in new tab

---

## Features

### Beautiful UI
- ✅ Modern gradient design
- ✅ Responsive (works on mobile)
- ✅ Smooth animations
- ✅ Loading states
- ✅ Error handling

### Lead Display
- ✅ Lead cards with all info
- ✅ Score badges (1-5)
- ✅ Clickable links
- ✅ Social media buttons
- ✅ Stats dashboard

### Functionality
- ✅ Real-time lead generation
- ✅ Data enrichment
- ✅ Google Sheets export
- ✅ Error handling
- ✅ Loading indicators

---

## API Endpoints

### POST /api/generate-leads
Generate leads based on search criteria.

**Request:**
```json
{
  "query": "landscapers",
  "location": "Houston, TX",
  "maxResults": 10,
  "enrichData": true
}
```

**Response:**
```json
{
  "generated": "2026-01-31T12:00:00",
  "total_leads": 10,
  "leads": [...]
}
```

### POST /api/export-to-sheets
Export leads to Google Sheets.

**Request:** Same as generate-leads response

**Response:**
```json
{
  "url": "https://docs.google.com/spreadsheets/d/...",
  "message": "Export successful"
}
```

### GET /health
Health check endpoint.

---

## How It Works

1. **User fills form** → Enters business type, location, etc.
2. **Frontend sends request** → POST to `/api/generate-leads`
3. **Backend runs scripts:**
   - `scrape_gmb_free.py` - Scrapes GMB listings
   - `enrich_leads.py` - Enriches with emails/social (if enabled)
4. **Results displayed** → Beautiful lead cards with all data
5. **User clicks export** → POST to `/api/export-to-sheets`
6. **Google Sheet created** → Opens in new tab

---

## Usage Examples

### Start Server
```bash
python3 web/server.py
```

Output:
```
================================================================================
🚀 LEAD GENERATION ENGINE - WEB SERVER
================================================================================

📂 Project root: /Users/garymills/antigravity001
📂 Execution dir: /Users/garymills/antigravity001/execution
📂 Temp dir: /Users/garymills/antigravity001/.tmp

🌐 Starting server at: http://localhost:5000

✅ Ready to generate leads!
================================================================================
```

### Access Web UI
Open browser: http://localhost:5000

### Generate Leads
1. Enter "landscapers" in Business Type
2. Enter "Houston, TX" in Location
3. Select "10 leads"
4. Select "Yes - Get emails & social media"
5. Click "Generate Leads"
6. Wait ~30 seconds
7. View results!

### Export to Sheets
1. Click "Export to Google Sheets" button
2. Wait ~5 seconds
3. Google Sheet opens in new tab
4. Done!

---

## File Structure

```
web/
├── index.html          # Frontend UI
├── server.py           # Flask backend
└── requirements.txt    # Dependencies
```

---

## Customization

### Change Port
Edit `server.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change 5000 to 8080
```

### Change UI Colors
Edit `index.html` CSS:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Change to your colors */
```

### Add More Fields
Edit `index.html` form:
```html
<div class="form-group">
    <label for="newField">New Field</label>
    <input type="text" id="newField" name="newField">
</div>
```

---

## Deployment

### Local Network Access
```bash
# Server is already accessible on local network
# Find your IP: ifconfig | grep "inet "
# Access from other devices: http://YOUR_IP:5000
```

### Deploy to Cloud

#### Option 1: Heroku
```bash
# Create Procfile
echo "web: python3 web/server.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

#### Option 2: DigitalOcean
```bash
# Create droplet
# SSH into server
# Clone repo
# Install dependencies
# Run server with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web.server:app
```

#### Option 3: Vercel/Netlify
- Frontend (index.html) → Deploy to Vercel/Netlify
- Backend (server.py) → Deploy to Heroku/Railway

---

## Security Notes

### For Production:
1. **Add authentication** - Require login
2. **Rate limiting** - Prevent abuse
3. **API keys** - Protect endpoints
4. **HTTPS** - Use SSL certificate
5. **Environment variables** - Store credentials securely

### Example with Auth:
```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username == 'admin' and password == 'secret':
        return username

@app.route('/api/generate-leads', methods=['POST'])
@auth.login_required
def generate_leads():
    # ... existing code
```

---

## Troubleshooting

### "Module not found: flask"
```bash
pip3 install flask flask-cors
```

### "Port 5000 already in use"
Change port in `server.py` or kill existing process:
```bash
lsof -ti:5000 | xargs kill -9
```

### "Permission denied"
```bash
chmod +x web/server.py
```

### "Google Sheets export fails"
Make sure `credentials.json` and `token.json` exist in project root.

---

## Next Steps

1. ✅ Install Flask: `pip3 install flask flask-cors`
2. ✅ Start server: `python3 web/server.py`
3. ✅ Open browser: http://localhost:5000
4. ✅ Generate leads!
5. ✅ Export to Google Sheets!

---

**🎉 Your lead generation engine now has a beautiful web interface!**
