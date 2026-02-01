#!/usr/bin/env python3
"""
Lead Generation Engine - Web Server

Flask backend that handles:
- Lead generation requests
- Data enrichment
- Google Sheets export
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import json
import os
from pathlib import Path
import tempfile
import uuid

app = Flask(__name__, static_folder='../web')
CORS(app)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
EXECUTION_DIR = PROJECT_ROOT / 'execution'
TMP_DIR = PROJECT_ROOT / '.tmp'

@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/generate-leads', methods=['POST'])
def generate_leads():
    """
    Generate leads based on query parameters.
    
    Request body:
    {
        "query": "landscapers",
        "location": "Houston, TX",
        "maxResults": 10,
        "enrichData": true
    }
    """
    try:
        data = request.json
        query = data.get('query')
        location = data.get('location')
        max_results = data.get('maxResults', 10)
        enrich_data = data.get('enrichData', True)
        
        if not query or not location:
            return jsonify({'error': 'Query and location are required'}), 400
        
        # Generate unique filename
        session_id = str(uuid.uuid4())[:8]
        output_file = TMP_DIR / f'leads_{session_id}.json'
        
        # Step 1: Scrape GMB listings
        # Check if SerpAPI key is available for real data
        serpapi_key = os.environ.get('SERPAPI_KEY')
        if serpapi_key:
            print(f"🚀 Using SerpAPI for REAL data: {max_results} {query} in {location}...")
            scrape_script = 'scrape_gmb.py'
        else:
            print(f"💡 No SerpAPI key found. Using DEMO mode: {max_results} {query} in {location}...")
            scrape_script = 'scrape_gmb_free.py'

        scrape_cmd = [
            'python3',
            str(EXECUTION_DIR / scrape_script),
            '--query', query,
            '--location', location,
            '--max-results', str(max_results),
            '--output-format', 'json',
            '--output', str(output_file)
        ]
        
        result = subprocess.run(scrape_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown scraping error"
            print(f"Scraping error: {error_msg}")
            return jsonify({'error': f'Scraping failed: {error_msg}'}), 500
        
        # Load scraped data
        with open(output_file, 'r') as f:
            leads_data = json.load(f)
        
        # Step 2: Enrich data if requested
        if enrich_data:
            print(f"Enriching {len(leads_data['leads'])} leads...")
            enriched_file = TMP_DIR / f'enriched_{session_id}.txt'
            
            enrich_cmd = [
                'python3',
                str(EXECUTION_DIR / 'enrich_leads.py'),
                '--input', str(output_file),
                '--output', str(enriched_file),
                '--delay', '1.0'
            ]
            
            result = subprocess.run(enrich_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Warning: Enrichment failed: {result.stderr}")
            
            # Reload data (enrichment updates the JSON file in place)
            with open(output_file, 'r') as f:
                leads_data = json.load(f)
        
        # Return results
        return jsonify(leads_data)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export-to-sheets', methods=['POST'])
def export_to_sheets():
    """
    Export leads to Google Sheets with read-only sharing.
    
    Request body: Same format as generate-leads response
    """
    try:
        data = request.json
        
        # Save data to temp file
        session_id = str(uuid.uuid4())[:8]
        temp_file = TMP_DIR / f'export_{session_id}.json'
        
        with open(temp_file, 'w') as f:
            json.dump(data, f)
        
        # Run export script
        print(f"Exporting {len(data.get('leads', []))} leads to Google Sheets...")
        export_cmd = [
            'python3',
            str(EXECUTION_DIR / 'export_to_sheets.py'),
            '--input', str(temp_file),
            '--title', f"Gary's Leads - {data.get('leads', [{}])[0].get('category', 'Unknown')}"
        ]
        
        result = subprocess.run(export_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return jsonify({'error': f'Export failed: {result.stderr}'}), 500
        
        # Extract Google Sheets URL and ID from output
        output = result.stdout
        url = None
        sheet_id = None
        
        for line in output.split('\n'):
            if 'docs.google.com/spreadsheets' in line:
                url = line.strip()
                # Extract sheet ID from URL
                if '/d/' in url:
                    sheet_id = url.split('/d/')[1].split('/')[0]
                break
        
        if not url or not sheet_id:
            return jsonify({'error': 'Failed to get Google Sheets URL'}), 500
        
        # Set sharing permissions to read-only (anyone with link can view)
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            
            # Load credentials
            creds = None
            token_path = PROJECT_ROOT / 'token.json'
            if token_path.exists():
                creds = Credentials.from_authorized_user_file(str(token_path))
            
            if creds:
                service = build('drive', 'v3', credentials=creds)
                
                # Set permission: anyone with link can view (read-only)
                permission = {
                    'type': 'anyone',
                    'role': 'reader'  # Read-only access
                }
                
                service.permissions().create(
                    fileId=sheet_id,
                    body=permission,
                    fields='id'
                ).execute()
                
                print(f"✓ Sheet set to read-only (anyone with link can view)")
        except Exception as e:
            print(f"Warning: Could not set sharing permissions: {e}")
            # Continue anyway - sheet is still created
        
        return jsonify({
            'url': url,
            'message': 'Export successful - Read-only link created'
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'message': 'Lead Generation Engine is running'})


if __name__ == '__main__':
    # Ensure tmp directory exists
    TMP_DIR.mkdir(exist_ok=True)
    
    # Get port from environment variable (for deployment) or use 8080
    port = int(os.environ.get('PORT', 8080))
    
    print("="*80)
    print("🚀 LEAD GENERATION ENGINE - WEB SERVER")
    print("="*80)
    print(f"\n📂 Project root: {PROJECT_ROOT}")
    print(f"📂 Execution dir: {EXECUTION_DIR}")
    print(f"📂 Temp dir: {TMP_DIR}")
    print(f"\n🌐 Starting server on port: {port}")
    print(f"\n✅ Ready to generate leads!")
    print("="*80)
    print()
    
    app.run(debug=False, host='0.0.0.0', port=port)
