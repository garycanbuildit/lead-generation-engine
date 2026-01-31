#!/usr/bin/env python3
"""
Export Leads to Google Sheets

Exports enriched lead data to a Google Sheet with columns:
- Name
- Website
- Phone
- Email
- Score
- Facebook Link
- Instagram Link
- TikTok Link
- X Link
- LinkedIn Link
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    import os
except ImportError:
    print("Error: Google Sheets API libraries not installed.")
    print("Run: pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def get_credentials():
    """Get Google Sheets API credentials."""
    creds = None
    token_path = Path('token.json')
    credentials_path = Path('credentials.json')
    
    # The file token.json stores the user's access and refresh tokens
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                print("\n❌ Error: credentials.json not found!")
                print("\nTo use Google Sheets export, you need to:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project (or select existing)")
                print("3. Enable Google Sheets API")
                print("4. Create OAuth 2.0 credentials (Desktop app)")
                print("5. Download credentials.json to this directory")
                print("\nFor detailed instructions, see:")
                print("https://developers.google.com/sheets/api/quickstart/python")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds


def create_spreadsheet(service, title):
    """Create a new Google Spreadsheet."""
    spreadsheet = {
        'properties': {
            'title': title
        }
    }
    
    spreadsheet = service.spreadsheets().create(
        body=spreadsheet,
        fields='spreadsheetId,spreadsheetUrl'
    ).execute()
    
    return spreadsheet


def prepare_sheet_data(leads):
    """Prepare lead data for Google Sheets."""
    # Header row
    headers = [
        'Name',
        'Website',
        'Phone',
        'Email',
        'Score',
        'Facebook Link',
        'Instagram Link',
        'TikTok Link',
        'X Link',
        'LinkedIn Link',
        'Address',
        'Rating',
        'Reviews',
        'Category',
        'Hours',
        'Price Level'
    ]
    
    # Data rows
    rows = [headers]
    
    for lead in leads:
        # Get social media links
        social = lead.get('social_media', {})
        
        # Get emails (join multiple emails with comma)
        emails = lead.get('emails', [])
        email_str = ', '.join(emails) if emails else ''
        
        row = [
            lead.get('name', ''),
            lead.get('website', ''),
            lead.get('phone', ''),
            email_str,
            str(lead.get('lead_score', '')),
            social.get('facebook', ''),
            social.get('instagram', ''),
            social.get('tiktok', ''),
            social.get('twitter', ''),  # X/Twitter
            social.get('linkedin', ''),
            lead.get('address', ''),
            lead.get('rating', ''),
            lead.get('reviews', ''),
            lead.get('category', ''),
            lead.get('hours', ''),
            lead.get('price_level', '')
        ]
        
        rows.append(row)
    
    return rows


def write_to_sheet(service, spreadsheet_id, data):
    """Write data to Google Sheet."""
    body = {
        'values': data
    }
    
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='A1',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    return result


def format_sheet(service, spreadsheet_id):
    """Format the Google Sheet (header row, column widths, etc.)."""
    requests = [
        # Freeze header row
        {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': 0,
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        },
        # Bold header row
        {
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {
                            'bold': True
                        },
                        'backgroundColor': {
                            'red': 0.9,
                            'green': 0.9,
                            'blue': 0.9
                        }
                    }
                },
                'fields': 'userEnteredFormat(textFormat,backgroundColor)'
            }
        },
        # Auto-resize columns
        {
            'autoResizeDimensions': {
                'dimensions': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': 16
                }
            }
        }
    ]
    
    body = {
        'requests': requests
    }
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Export enriched leads to Google Sheets"
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='Input JSON file with enriched leads'
    )
    parser.add_argument(
        '--title',
        help='Google Sheet title (default: auto-generated)'
    )
    
    args = parser.parse_args()
    
    # Load leads
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    with open(input_path, 'r') as f:
        data = json.load(f)
        leads = data.get('leads', [])
    
    if not leads:
        print("Error: No leads found in input file")
        return 1
    
    print(f"\n{'='*80}")
    print("EXPORTING LEADS TO GOOGLE SHEETS")
    print(f"{'='*80}")
    print(f"Total leads: {len(leads)}")
    print(f"{'='*80}\n")
    
    # Get credentials
    print("🔐 Authenticating with Google...")
    try:
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return 1
    
    print("✓ Authenticated successfully\n")
    
    # Create spreadsheet
    if args.title:
        sheet_title = args.title
    else:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        sheet_title = f"Leads Export - {timestamp}"
    
    print(f"📊 Creating Google Sheet: '{sheet_title}'...")
    try:
        spreadsheet = create_spreadsheet(service, sheet_title)
        spreadsheet_id = spreadsheet['spreadsheetId']
        spreadsheet_url = spreadsheet['spreadsheetUrl']
    except HttpError as e:
        print(f"❌ Failed to create spreadsheet: {e}")
        return 1
    
    print(f"✓ Spreadsheet created: {spreadsheet_id}\n")
    
    # Prepare data
    print("📝 Preparing data...")
    sheet_data = prepare_sheet_data(leads)
    print(f"✓ Prepared {len(sheet_data)-1} rows (+ header)\n")
    
    # Write data
    print("📤 Writing data to Google Sheet...")
    try:
        write_to_sheet(service, spreadsheet_id, sheet_data)
    except HttpError as e:
        print(f"❌ Failed to write data: {e}")
        return 1
    
    print("✓ Data written successfully\n")
    
    # Format sheet
    print("🎨 Formatting sheet...")
    try:
        format_sheet(service, spreadsheet_id)
    except HttpError as e:
        print(f"⚠️  Warning: Formatting failed: {e}")
    
    print("✓ Formatting complete\n")
    
    # Success!
    print(f"{'='*80}")
    print("✅ EXPORT COMPLETE!")
    print(f"{'='*80}")
    print(f"\n📊 Google Sheet URL:")
    print(f"{spreadsheet_url}")
    print(f"\n📋 Columns exported:")
    print("  1. Name")
    print("  2. Website")
    print("  3. Phone")
    print("  4. Email")
    print("  5. Score")
    print("  6. Facebook Link")
    print("  7. Instagram Link")
    print("  8. TikTok Link")
    print("  9. X Link")
    print(" 10. LinkedIn Link")
    print(" 11. Address")
    print(" 12. Rating")
    print(" 13. Reviews")
    print(" 14. Category")
    print(" 15. Hours")
    print(" 16. Price Level")
    print(f"\n📊 Total leads exported: {len(leads)}")
    print(f"\n🔗 Open in browser: {spreadsheet_url}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
