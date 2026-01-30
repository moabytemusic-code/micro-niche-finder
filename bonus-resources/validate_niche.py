#!/usr/bin/env python3
"""
Niche Validation Script
Quick check if your side hustle idea has potential
"""

import requests
import json
from datetime import datetime

def validate_niche(keyword):
    """
    Validates a niche idea using free APIs
    Returns a simple score and recommendations
    """
    print(f"\n🔍 Analyzing: '{keyword}'...")
    
    # 1. Check Google Trends interest (simulated - would use pytrends in production)
    trend_score = len(keyword) * 5  # Simplified scoring
    
    # 2. Check Reddit mentions
    reddit_url = f"https://www.reddit.com/search.json?q={keyword}&limit=10"
    headers = {'User-Agent': 'NicheValidator/1.0'}
    
    try:
        response = requests.get(reddit_url, headers=headers)
        reddit_data = response.json()
        reddit_mentions = len(reddit_data.get('data', {}).get('children', []))
    except:
        reddit_mentions = 0
    
    # 3. Calculate profit potential score (0-100)
    base_score = min(trend_score, 50)
    social_score = min(reddit_mentions * 5, 30)
    keyword_quality = 20 if len(keyword.split()) >= 2 else 10
    
    total_score = base_score + social_score + keyword_quality
    
    # Generate report
    report = {
        "keyword": keyword,
        "score": min(total_score, 100),
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "search_interest": "Medium" if base_score > 25 else "Low",
            "social_mentions": reddit_mentions,
            "competition": "Low" if total_score < 50 else "Medium"
        },
        "recommendation": get_recommendation(total_score)
    }
    
    return report

def get_recommendation(score):
    if score >= 70:
        return "✅ STRONG POTENTIAL - Start building immediately"
    elif score >= 50:
        return "⚠️ MODERATE POTENTIAL - Validate with a landing page first"
    else:
        return "❌ LOW POTENTIAL - Consider pivoting to a related niche"

def main():
    print("=" * 50)
    print("NICHE VALIDATOR - Signal Engines")
    print("=" * 50)
    
    keyword = input("\nEnter your niche idea: ").strip()
    
    if not keyword:
        print("❌ Please enter a valid keyword")
        return
    
    result = validate_niche(keyword)
    
    print(f"\n📊 VALIDATION REPORT")
    print("-" * 50)
    print(f"Niche: {result['keyword']}")
    print(f"Profit Score: {result['score']}/100")
    print(f"Search Interest: {result['metrics']['search_interest']}")
    print(f"Social Mentions: {result['metrics']['social_mentions']}")
    print(f"Competition Level: {result['metrics']['competition']}")
    print(f"\n{result['recommendation']}")
    print("-" * 50)
    
    # Save to file
    filename = f"validation_{keyword.replace(' ', '_')}.json"
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n💾 Report saved to: {filename}")

if __name__ == "__main__":
    main()
