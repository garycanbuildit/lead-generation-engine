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
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
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
            if any(x in email for x in ['.png', '.jpg', '.gif', '.css', '.js']):
                continue
            if email.startswith(('example@', 'user@', 'email@')):
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
            
            # Facebook
            if 'facebook.com/' in href or 'fb.com/' in href or 'fb.me/' in href:
                social['facebook'] = href
            
            # Instagram
            elif 'instagram.com/' in href or 'instagr.am/' in href:
                social['instagram'] = href
            
            # TikTok
            elif 'tiktok.com/' in href:
                social['tiktok'] = href
            
            # LinkedIn
            elif 'linkedin.com/' in href:
                social['linkedin'] = href
            
            # Twitter/X
            elif 'twitter.com/' in href or 'x.com/' in href:
                social['twitter'] = href
        
        return social
    
    def scrape_website(self, url: str) -> Tuple[List[str], Dict[str, str]]:
        """
        Scrape a website for email and social media.
        
        Returns:
            Tuple of (emails, social_media_dict)
        """
        if not url or url == 'N/A':
            return [], {}
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"  📡 Scraping: {url}")
            
            # Get homepage
            response = self.session.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            html = response.text
            domain = urlparse(url).netloc
            
            # Extract emails and social media
            emails = self.extract_emails(html, domain)
            social = self.extract_social_media(html, url)
            
            # Try to find contact page for more emails
            soup = BeautifulSoup(html, 'html.parser')
            contact_links = soup.find_all('a', href=True, string=re.compile(r'contact|email|reach', re.I))
            
            if contact_links and len(emails) == 0:
                try:
                    contact_url = urljoin(url, contact_links[0]['href'])
                    print(f"    → Checking contact page: {contact_url}")
                    contact_response = self.session.get(contact_url, timeout=10)
                    contact_emails = self.extract_emails(contact_response.text, domain)
                    emails.extend(contact_emails)
                    emails = list(set(emails))  # Deduplicate
                except:
                    pass
            
            return emails, social
            
        except requests.exceptions.Timeout:
            print(f"    ⚠️  Timeout accessing {url}")
            return [], {}
        except requests.exceptions.RequestException as e:
            print(f"    ⚠️  Error accessing {url}: {str(e)[:50]}")
            return [], {}
        except Exception as e:
            print(f"    ⚠️  Unexpected error: {str(e)[:50]}")
            return [], {}
    
    def calculate_score(self, lead: Dict, emails: List[str], social: Dict[str, str]) -> int:
        """
        Calculate lead score based on criteria:
        - 1 point: Service business
        - 3 points: Has email
        - 1 point: Has social media
        """
        score = 0
        
        # 1 point for service business (always true for our leads)
        score += 1
        
        # 3 points for email
        if emails:
            score += 3
        
        # 1 point for social media
        has_social = any(v for v in social.values() if v)
        if has_social:
            score += 1
        
        return score
    
    def generate_cold_email(self, lead: Dict) -> str:
        """Generate personalized cold email for SEO services."""
        business_name = lead.get('name', 'Your Business')
        category = lead.get('category', 'service business')
        location = lead.get('address', 'your area')
        
        # Extract city from address
        city = "your area"
        if location and ',' in location:
            parts = location.split(',')
            if len(parts) >= 2:
                city = parts[-2].strip()
        
        email = f"""Subject: Quick question about {business_name}'s online presence

Hi {business_name} team,

I came across your business while researching {category.lower()} in {city}, and I noticed a few opportunities to help you get more customers online.

Many service businesses in {city} are missing out on 40-60% of potential customers because they're not showing up on Google when people search for "{category.lower()} near me."

I specialize in helping local service businesses like yours:
• Rank #1 on Google Maps
• Get more 5-star reviews  
• Show up when customers search for your services
• Increase website traffic by 200-300%

Would you be open to a quick 15-minute call to see if we can help you get more customers?

I'd be happy to do a free audit of your online presence and show you exactly where you're losing potential customers.

Best regards,
[Your Name]
[Your Company]
[Your Phone]
[Your Email]

P.S. I noticed you have {lead.get('reviews', '0')} reviews with a {lead.get('rating', 'N/A')} star rating - that's great! Let me show you how to turn those reviews into more customers.
"""
        return email


def enrich_lead(enricher: LeadEnricher, lead: Dict, delay: float = 2.0) -> Dict:
    """Enrich a single lead with contact data."""
    print(f"\n{'='*80}")
    print(f"Enriching: {lead.get('name', 'Unknown')}")
    print(f"{'='*80}")
    
    website = lead.get('website', 'N/A')
    
    if website == 'N/A' or not website:
        print("  ⚠️  No website - skipping enrichment")
        emails = []
        social = {}
    else:
        emails, social = enricher.scrape_website(website)
        time.sleep(delay)  # Rate limiting
    
    # Calculate score
    score = enricher.calculate_score(lead, emails, social)
    
    # Generate cold email
    cold_email = enricher.generate_cold_email(lead)
    
    # Create enriched lead
    enriched = lead.copy()
    enriched['emails'] = emails
    enriched['social_media'] = social
    enriched['lead_score'] = score
    enriched['cold_email'] = cold_email
    
    # Print summary
    print(f"  ✓ Emails found: {len(emails)}")
    if emails:
        for email in emails[:3]:  # Show first 3
            print(f"    - {email}")
    
    social_count = sum(1 for v in social.values() if v)
    print(f"  ✓ Social media: {social_count} platform(s)")
    for platform, url in social.items():
        if url:
            print(f"    - {platform.title()}: {url[:50]}...")
    
    print(f"  ✓ Lead Score: {score}/5")
    
    return enriched


def format_enriched_lead(lead: Dict, index: int) -> str:
    """Format enriched lead as text."""
    sep = "=" * 80
    line = "-" * 80
    
    text = f"\n{sep}\n"
    text += f"LEAD #{index} - SCORE: {lead.get('lead_score', 0)}/5\n"
    text += f"{sep}\n"
    text += f"Business Name: {lead.get('name', 'N/A')}\n"
    text += f"Category: {lead.get('category', 'N/A')}\n"
    text += f"Address: {lead.get('address', 'N/A')}\n"
    text += f"Phone: {lead.get('phone', 'N/A')}\n"
    
    # Website
    website = lead.get('website', 'N/A')
    if website != 'N/A' and website:
        text += f"Website: [{website}]({website})\n"
    
    text += f"Rating: {lead.get('rating', 'N/A')} stars ({lead.get('reviews', 'N/A')} reviews)\n"
    
    # Email addresses
    emails = lead.get('emails', [])
    if emails:
        text += f"\n📧 EMAIL ADDRESSES ({len(emails)}):\n"
        for email in emails:
            text += f"  - {email}\n"
    else:
        text += f"\n📧 EMAIL: Not found\n"
    
    # Social media
    social = lead.get('social_media', {})
    has_social = any(v for v in social.values() if v)
    
    if has_social:
        text += f"\n📱 SOCIAL MEDIA:\n"
        for platform, url in social.items():
            if url:
                text += f"  - {platform.title()}: {url}\n"
    else:
        text += f"\n📱 SOCIAL MEDIA: Not found\n"
    
    # Lead score breakdown
    text += f"\n⭐ LEAD SCORE: {lead.get('lead_score', 0)}/5\n"
    text += f"  - Service Business: 1 point ✓\n"
    text += f"  - Email Address: {3 if emails else 0} points {'✓' if emails else '✗'}\n"
    text += f"  - Social Media: {1 if has_social else 0} point {'✓' if has_social else '✗'}\n"
    
    # Cold email
    text += f"\n📨 COLD EMAIL TEMPLATE:\n"
    text += f"{line}\n"
    text += lead.get('cold_email', 'N/A')
    text += f"{line}\n"
    
    return text


def save_enriched_leads(leads: List[Dict], output_path: Path):
    """Save enriched leads to text file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("ENRICHED GMB LEADS - WITH CONTACT DATA\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Leads: {len(leads)}\n")
        f.write("=" * 80 + "\n")
        
        # Sort by score (highest first)
        sorted_leads = sorted(leads, key=lambda x: x.get('lead_score', 0), reverse=True)
        
        for i, lead in enumerate(sorted_leads, 1):
            f.write(format_enriched_lead(lead, i))
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")
        
        # Summary
        f.write("\n\nSUMMARY:\n")
        f.write(f"Total Leads: {len(leads)}\n")
        f.write(f"Leads with Email: {sum(1 for l in leads if l.get('emails'))}\n")
        f.write(f"Leads with Social Media: {sum(1 for l in leads if any(l.get('social_media', {}).values()))}\n")
        f.write(f"\nScore Distribution:\n")
        for score in range(5, 0, -1):
            count = sum(1 for l in leads if l.get('lead_score') == score)
            f.write(f"  {score}/5: {count} leads\n")
    
    print(f"\n✓ Enriched leads saved to: {output_path}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Enrich GMB leads with contact data and cold emails"
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='Input JSON file with leads'
    )
    parser.add_argument(
        '--output',
        help='Output text file (default: .tmp/enriched_leads.txt)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=2.0,
        help='Delay between requests in seconds (default: 2.0)'
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
    print(f"LEAD ENRICHMENT - EXTRACTING CONTACT DATA")
    print(f"{'='*80}")
    print(f"Total leads to enrich: {len(leads)}")
    print(f"Delay between requests: {args.delay}s")
    print(f"{'='*80}\n")
    
    # Enrich leads
    enricher = LeadEnricher()
    enriched_leads = []
    
    for i, lead in enumerate(leads, 1):
        print(f"\nProgress: {i}/{len(leads)}")
        enriched = enrich_lead(enricher, lead, args.delay)
        enriched_leads.append(enriched)
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = Path('.tmp') / f'enriched_leads_{timestamp}.txt'
    
    # Save results
    save_enriched_leads(enriched_leads, output_path)
    
    # Print summary
    print(f"\n{'='*80}")
    print("ENRICHMENT COMPLETE!")
    print(f"{'='*80}")
    print(f"Total leads processed: {len(enriched_leads)}")
    print(f"Leads with email: {sum(1 for l in enriched_leads if l.get('emails'))}")
    print(f"Leads with social media: {sum(1 for l in enriched_leads if any(l.get('social_media', {}).values()))}")
    print(f"\nScore distribution:")
    for score in range(5, 0, -1):
        count = sum(1 for l in enriched_leads if l.get('lead_score') == score)
        if count > 0:
            print(f"  {score}/5 points: {count} leads")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
