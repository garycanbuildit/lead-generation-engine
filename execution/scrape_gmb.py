#!/usr/bin/env python3
"""
Google My Business Lead Scraper

Scrapes GMB profiles and extracts business information for lead generation.
Supports multiple scraping methods: SerpAPI, Google Places API, and web scraping.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Lead:
    """Represents a business lead with contact information."""
    
    def __init__(self, data: Dict):
        self.name = data.get('name', 'N/A')
        self.address = data.get('address', 'N/A')
        self.phone = data.get('phone', 'N/A')
        self.website = data.get('website', 'N/A')
        self.rating = data.get('rating', 'N/A')
        self.reviews = data.get('reviews', 'N/A')
        self.hours = data.get('hours', 'N/A')
        self.category = data.get('category', 'N/A')
        self.maps_url = data.get('maps_url', 'N/A')
        self.price_level = data.get('price_level', 'N/A')
        self.description = data.get('description', 'N/A')
    
    def to_dict(self) -> Dict:
        """Convert lead to dictionary."""
        return {
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'website': self.website,
            'rating': self.rating,
            'reviews': self.reviews,
            'hours': self.hours,
            'category': self.category,
            'maps_url': self.maps_url,
            'price_level': self.price_level,
            'description': self.description
        }
    
    def to_text(self, index: int) -> str:
        """Format lead as text."""
        separator = "=" * 80
        line = "-" * 80
        
        text = f"\n{separator}\n"
        text += f"LEAD #{index}\n"
        text += f"{separator}\n"
        text += f"Business Name: {self.name}\n"
        text += f"Category: {self.category}\n"
        text += f"Address: {self.address}\n"
        text += f"Phone: {self.phone}\n"
        text += f"Website: {self.website}\n"
        
        if self.rating != 'N/A':
            text += f"Rating: {self.rating} stars ({self.reviews} reviews)\n"
        
        if self.hours != 'N/A':
            text += f"Hours: {self.hours}\n"
        
        if self.price_level != 'N/A':
            text += f"Price Level: {self.price_level}\n"
        
        text += f"Google Maps: {self.maps_url}\n"
        
        if self.description != 'N/A':
            text += f"\nDescription: {self.description}\n"
        
        text += f"\n{line}\n"
        
        return text


class GMBScraper:
    """Main scraper class with multiple scraping methods."""
    
    def __init__(self, method: str = 'serpapi'):
        self.method = method
        self.leads: List[Lead] = []
    
    def scrape_with_serpapi(self, query: str, location: str, max_results: int) -> List[Lead]:
        """Scrape using SerpAPI (recommended method)."""
        try:
            import requests
        except ImportError:
            print("Error: 'requests' library not installed. Run: pip install requests")
            return []
        
        api_key = os.environ.get('SERPAPI_KEY') or os.getenv('SERPAPI_KEY')
        if not api_key:
            print("Error: SERPAPI_KEY not found in environment")
            return []
        
        print(f"🔍 Searching for '{query}' in '{location}' using SerpAPI...")
        
        leads = []
        params = {
            'engine': 'google_maps',
            'q': query,
            'location': location,
            'api_key': api_key
        }
        
        try:
            response = requests.get('https://serpapi.com/search', params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Check for SerpAPI errors in the JSON response
            if 'error' in data:
                print(f"❌ SerpAPI Error: {data['error']}")
                return []
            
            # SerpAPI Google Maps results are usually in 'local_results'
            # But sometimes if only one result is found, it looks different
            results = data.get('local_results', [])
            
            if not results and 'place_results' in data:
                # If searching for a specific place, it might be in place_results
                results = [data['place_results']]
            
            if not results:
                print(f"⚠️  No results found for '{query}' in '{location}'")
                # Log a snippet of the response for debugging if no results found
                print(f"DEBUG: Response keys: {list(data.keys())}")
                return []
            
            for result in results[:max_results]:
                lead_data = {
                    'name': result.get('title', 'N/A'),
                    'address': result.get('address', 'N/A'),
                    'phone': result.get('phone', 'N/A'),
                    'website': result.get('website', 'N/A'),
                    'rating': result.get('rating', 'N/A'),
                    'reviews': result.get('reviews', 'N/A'),
                    'category': result.get('type', 'N/A'),
                    'maps_url': result.get('link', 'N/A'),
                    'price_level': result.get('price', 'N/A'),
                    'hours': result.get('hours', 'N/A'),
                    'description': result.get('description', 'N/A')
                }
                
                leads.append(Lead(lead_data))
                print(f"  ✓ Found: {lead_data['name']}")
            
            print(f"\n✅ Successfully scraped {len(leads)} leads")
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e.response.status_code} - {e.response.text}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Network Error: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return []
        
        return leads
    
    def scrape_with_places_api(self, query: str, location: str, max_results: int) -> List[Lead]:
        """Scrape using Google Places API."""
        print("Google Places API method not yet implemented.")
        print("This requires a Google Cloud API key with Places API enabled.")
        return []
    
    def scrape_with_browser(self, query: str, location: str, max_results: int) -> List[Lead]:
        """Scrape using browser automation (Playwright/Selenium)."""
        print("Browser automation method not yet implemented.")
        print("This method is more complex and requires Playwright or Selenium.")
        return []
    
    def scrape(self, query: str, location: str, max_results: int = 20) -> List[Lead]:
        """Main scraping method - routes to appropriate scraper."""
        if self.method == 'serpapi':
            return self.scrape_with_serpapi(query, location, max_results)
        elif self.method == 'places':
            return self.scrape_with_places_api(query, location, max_results)
        elif self.method == 'browser':
            return self.scrape_with_browser(query, location, max_results)
        else:
            print(f"Error: Unknown scraping method '{self.method}'")
            return []


def save_leads_as_text(leads: List[Lead], output_path: Path) -> None:
    """Save leads to a text file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("GOOGLE MY BUSINESS LEADS\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Leads: {len(leads)}\n")
        f.write("=" * 80 + "\n")
        
        for i, lead in enumerate(leads, 1):
            f.write(lead.to_text(i))
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")
    
    print(f"✓ Leads saved to: {output_path}")


def save_leads_as_json(leads: List[Lead], output_path: Path) -> None:
    """Save leads to a JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        'generated': datetime.now().isoformat(),
        'total_leads': len(leads),
        'leads': [lead.to_dict() for lead in leads]
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Leads saved to: {output_path}")


def save_leads_as_csv(leads: List[Lead], output_path: Path) -> None:
    """Save leads to a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    import csv
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if not leads:
            return
        
        fieldnames = leads[0].to_dict().keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for lead in leads:
            writer.writerow(lead.to_dict())
    
    print(f"✓ Leads saved to: {output_path}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Scrape Google My Business profiles for lead generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 execution/scrape_gmb.py --query "coffee shops" --location "San Francisco, CA"
  python3 execution/scrape_gmb.py --query "plumbers" --location "Austin, TX" --max-results 50
  python3 execution/scrape_gmb.py --query "dentists" --location "NYC" --output-format json

Scraping Methods:
  serpapi  - Uses SerpAPI (requires SERPAPI_KEY in .env) [RECOMMENDED]
  places   - Uses Google Places API (requires GOOGLE_PLACES_KEY in .env)
  browser  - Uses browser automation (requires Playwright/Selenium)
        """
    )
    
    parser.add_argument(
        '--query',
        required=True,
        help='Search query (e.g., "restaurants", "plumbers")'
    )
    parser.add_argument(
        '--location',
        required=True,
        help='Location to search (e.g., "New York, NY", "Los Angeles, CA")'
    )
    parser.add_argument(
        '--max-results',
        type=int,
        default=20,
        help='Maximum number of results to scrape (default: 20)'
    )
    parser.add_argument(
        '--output-format',
        choices=['txt', 'json', 'csv'],
        default='txt',
        help='Output format (default: txt)'
    )
    parser.add_argument(
        '--method',
        choices=['serpapi', 'places', 'browser'],
        default='serpapi',
        help='Scraping method to use (default: serpapi)'
    )
    parser.add_argument(
        '--output',
        help='Custom output file path (optional)'
    )
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = GMBScraper(method=args.method)
    
    # Scrape leads
    leads = scraper.scrape(args.query, args.location, args.max_results)
    
    if not leads:
        print("\n⚠️  No leads found or scraping failed.")
        return 1
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"leads_{timestamp}.{args.output_format}"
        output_path = Path('.tmp') / filename
    
    # Save leads in requested format
    print(f"\n💾 Saving {len(leads)} leads...")
    
    if args.output_format == 'txt':
        save_leads_as_text(leads, output_path)
    elif args.output_format == 'json':
        save_leads_as_json(leads, output_path)
    elif args.output_format == 'csv':
        save_leads_as_csv(leads, output_path)
    
    print(f"\n🎉 Done! {len(leads)} leads extracted successfully.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
