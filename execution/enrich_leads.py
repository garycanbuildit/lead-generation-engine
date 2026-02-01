#!/usr/bin/env python3
"""
Lead Enrichment Script

Scrapes business websites to extract:
- Email addresses
- Social media handles (Facebook, Instagram, TikTok, LinkedIn, X)
- Generates personalized cold emails
- Scores leads based on qualification criteria
"""

import argparse
import json
import re
import sys
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required libraries not installed.")
    print("Run: pip3 install requests beautifulsoup4")
    sys.exit(1)


class LeadEnricher:
    """Enriches leads with contact data from websites."""
    
    def __init__(self):
        self.session = requests.Session()
        # List of rotating user agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
        ]
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def extract_emails(self, html: str, domain: str) -> List[str]:
        """Extract email addresses from HTML."""
        # Email regex pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html, re.IGNORECASE)
        
        # Filter and deduplicate
        valid_emails = []
        seen = set()
        
        for email in emails:
            email = email.lower().strip()
            # Skip common false positives
            if email in seen:
                continue
            if any(x in email for x in ['.png', '.jpg', '.gif', '.css', '.js', '.svg', '.webp']):
                continue
            if email.startswith(('example@', 'user@', 'email@', 'support@example', 'info@example')):
                continue
            
            seen.add(email)
            valid_emails.append(email)
        
        return valid_emails
    
    def extract_social_media(self, html: str, base_url: str) -> Dict[str, str]:
        """Extract social media handles from HTML."""
        social = {
            'facebook': None,
            'instagram': None,
            'tiktok': None,
            'linkedin': None,
            'twitter': None
        }
        
        # Find all links
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '').lower()
            
            # Ensure it's not a relative link that happens to contain the name
            if not any(x in href for x in ['facebook.com', 'fb.com', 'instagram.com', 'tiktok.com', 'linkedin.com', 'twitter.com', 'x.com']):
                continue

            # Facebook
            if 'facebook.com/' in href or 'fb.com/' in href or 'fb.me/' in href:
                if not social['facebook'] or len(href) < len(social['facebook']):
                    social['facebook'] = href
            
            # Instagram
            elif 'instagram.com/' in href or 'instagr.am/' in href:
                if not social['instagram'] or len(href) < len(social['instagram']):
                    social['instagram'] = href
            
            # TikTok
            elif 'tiktok.com/' in href:
                if not social['tiktok'] or len(href) < len(social['tiktok']):
                    social['tiktok'] = href
            
            # LinkedIn
            elif 'linkedin.com/' in href:
                if not social['linkedin'] or len(href) < len(social['linkedin']):
                    social['linkedin'] = href
            
            # Twitter/X
            elif 'twitter.com/' in href or 'x.com/' in href:
                if not social['twitter'] or len(href) < len(social['twitter']):
                    social['twitter'] = href
        
        return social
    
    def scrape_website(self, url: str) -> Tuple[List[str], Dict[str, str]]:
        """
        Scrape a website for email and social media.
        """
        if not url or url == 'N/A':
            return [], {}
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"  📡 Scraping: {url}")
            
            # Update user agent for this request
            self.session.headers.update({'User-Agent': random.choice(self.user_agents)})
            
            # Get homepage with retry and longer timeout
            response = None
            for attempt in range(2):
                try:
                    response = self.session.get(url, timeout=15, allow_redirects=True)
                    response.raise_for_status()
                    break
                except Exception as e:
                    if attempt == 0:
                        print(f"    ⚠️  Retry 1 for {url}...")
                        time.sleep(1)
                        # Try with http if https failed
                        if url.startswith('https://'):
                            url = url.replace('https://', 'http://')
                        continue
                    raise e
            
            if not response:
                return [], {}

            html = response.text
            domain = urlparse(url).netloc
            
            # Extract emails and social media
            emails = self.extract_emails(html, domain)
            social = self.extract_social_media(html, url)
            
            # Try to find more pages (contact, about)
            soup = BeautifulSoup(html, 'html.parser')
            extra_urls = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text().lower()
                if any(x in href.lower() or x in text for x in ['contact', 'about', 'email', 'reach', 'info']):
                    full_url = urljoin(url, href)
                    if urlparse(full_url).netloc == domain and full_url != url:
                        extra_urls.append(full_url)
            
            # Scraping up to 2 extra pages if needed
            for extra_url in list(set(extra_urls))[:2]:
                if len(emails) > 5 and all(social.values()):
                    break # Already found enough
                    
                try:
                    print(f"    → Checking extra page: {extra_url}")
                    self.session.headers.update({'User-Agent': random.choice(self.user_agents)})
                    res = self.session.get(extra_url, timeout=10)
                    if res.status_code == 200:
                        emails.extend(self.extract_emails(res.text, domain))
                        new_social = self.extract_social_media(res.text, extra_url)
                        for k, v in new_social.items():
                            if v and not social.get(k):
                                social[k] = v
                except:
                    pass
            
            emails = list(set(emails))
            return emails, social
            
        except Exception as e:
            print(f"    ⚠️  Error accessing {url}: {str(e)[:100]}")
            return [], {}

    def calculate_score(self, lead: Dict, emails: List[str], social: Dict[str, str]) -> int:
        """Calculate lead score (1-5)."""
        score = 1 # Base point for being a business
        if emails:
            score += 3
        if any(social.values()):
            score += 1
        return score

    def generate_cold_email(self, lead: Dict) -> str:
        """Generate personalized cold email."""
        business_name = lead.get('name', 'Your Business')
        category = lead.get('category', 'service business')
        location = lead.get('address', 'your area')
        
        city = "your area"
        if location and ',' in location:
            parts = location.split(',')
            if len(parts) >= 2:
                city = parts[-2].strip()
        
        email = f"""Subject: Question for the {business_name} team 

Hi {business_name} team,

I came across your business while researching {category.lower()} in {city}, and I noticed a few opportunities to help you get more customers.

I specialize in helping local service businesses like yours rank higher on Google and convert more visitors into calls.

Would you be open to a quick 10-minute chat about how we can help you grow in {city}?

Best regards,
[Your Name]
"""
        return email


def enrich_lead(enricher: LeadEnricher, lead: Dict, delay: float = 1.0) -> Dict:
    """Enrich a single lead."""
    print(f"\n--- Enriching: {lead.get('name', 'Unknown')} ---")
    
    website = lead.get('website', 'N/A')
    emails = []
    social = {}
    
    if website != 'N/A' and website:
        emails, social = enricher.scrape_website(website)
        if delay > 0:
            time.sleep(delay)
    
    score = enricher.calculate_score(lead, emails, social)
    cold_email = enricher.generate_cold_email(lead)
    
    enriched = lead.copy()
    enriched['emails'] = emails
    enriched['social_media'] = social
    enriched['lead_score'] = score
    enriched['cold_email'] = cold_email
    
    print(f"  ✓ Found {len(emails)} emails and {sum(1 for v in social.values() if v)} social links. Score: {score}/5")
    return enriched


def save_enriched_leads_text(leads: List[Dict], output_path: Path):
    """Save to text report."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("ENRICHED LEADS REPORT\n" + "="*80 + "\n")
        for i, lead in enumerate(leads, 1):
            f.write(f"\nLEAD #{i}: {lead.get('name')}\n")
            f.write(f"Score: {lead.get('lead_score')}/5\n")
            f.write(f"Emails: {', '.join(lead.get('emails', [])) if lead.get('emails') else 'None'}\n")
            f.write(f"Social: {json.dumps(lead.get('social_media'))}\n")
            f.write("-"*40 + "\n")


def save_leads_json(leads: List[Dict], output_path: Path):
    """Save to JSON file."""
    data = {
        'generated': datetime.now().isoformat(),
        'total_leads': len(leads),
        'leads': leads
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', help='Output file (.txt or .json)')
    parser.add_argument('--delay', type=float, default=1.0)
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        return 1
        
    with open(input_path, 'r') as f:
        data = json.load(f)
        leads = data.get('leads', [])
        
    enricher = LeadEnricher()
    enriched_leads = []
    
    for lead in leads:
        enriched_leads.append(enrich_lead(enricher, lead, args.delay))
        
    if args.output:
        out_path = Path(args.output)
        if out_path.suffix == '.json':
            save_leads_json(enriched_leads, out_path)
        else:
            save_enriched_leads_text(enriched_leads, out_path)
            # Also save JSON companion
            save_leads_json(enriched_leads, out_path.with_suffix('.json'))
    else:
        # Default behavior: update input JSON if no output specified
        save_leads_json(enriched_leads, input_path)
        
    print(f"\n✅ Enrichment complete. Processed {len(leads)} leads.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
