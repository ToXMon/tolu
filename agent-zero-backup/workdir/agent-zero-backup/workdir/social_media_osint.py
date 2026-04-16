#!/usr/bin/env python3
"""
Social Media OSINT Tool
Checks phone number +17328740910 against multiple social media platforms.
Uses direct API calls and web scraping only (no search engines).
"""

import requests
import json
import time
import re
import hashlib
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup

# ============================================================
# Configuration
# ============================================================
TARGET_PHONE = "+17328740910"
PHONE_DASHED = "732-874-0910"
PHONE_DOTTED = "732.874.0910"
PHONE_PAREN = "(732) 874-0910"
PHONE_PLAIN = "7328740910"
PHONE_NOPLUS = "17328740910"
NAMES = ["Catalino B Cheng", "Catalino Cheng", "Walter J Kellert", "Deeksha", "Susheel", "Venna"]
LOCATION = "Edison, NJ"

# Browser-like session
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
})

results = {
    "target_phone": TARGET_PHONE,
    "scan_timestamp": datetime.utcnow().isoformat() + "Z",
    "phone_formats_checked": [TARGET_PHONE, PHONE_DASHED, PHONE_DOTTED, PHONE_PAREN, PHONE_PLAIN, PHONE_NOPLUS],
    "names_checked": NAMES,
    "platforms": {}
}

def safe_get(url, timeout=15, allow_redirects=True, headers=None):
    """Safe GET request with error handling."""
    try:
        h = dict(SESSION.headers)
        if headers:
            h.update(headers)
        resp = SESSION.get(url, timeout=timeout, allow_redirects=allow_redirects, headers=h, verify=False)
        return resp
    except Exception as e:
        return None

def safe_post(url, data=None, json_data=None, timeout=15, headers=None):
    """Safe POST request with error handling."""
    try:
        h = dict(SESSION.headers)
        if headers:
            h.update(headers)
        resp = SESSION.post(url, data=data, json=json_data, timeout=timeout, headers=h, verify=False)
        return resp
    except Exception as e:
        return None

# ============================================================
# 1. WhatsApp Check
# ============================================================
def check_whatsapp():
    print("[*] Checking WhatsApp...")
    platform_result = {"platform": "WhatsApp", "checks": []}
    
    # Check via WhatsApp Web API endpoint / wa.me redirect
    phone_variants = [PHONE_NOPLUS, PHONE_PLAIN]
    for pv in phone_variants:
        # wa.me short link - check if number has WhatsApp
        url = f"https://wa.me/{pv}"
        resp = safe_get(url, allow_redirects=False)
        if resp:
            status = resp.status_code
            location = resp.headers.get("Location", "")
            platform_result["checks"].append({
                "url": url,
                "status_code": status,
                "redirect_location": location,
                "note": "wa.me redirects to WhatsApp Web if number is valid WhatsApp account"
            })
            # If it redirects to web.whatsapp.com, the number likely has WhatsApp
            if status in (301, 302) and "whatsapp" in location.lower():
                platform_result["registered"] = True
                platform_result["confidence"] = "HIGH"
                platform_result["summary"] = f"Number {TARGET_PHONE} appears to be registered on WhatsApp (wa.me redirect confirms)"
            elif status == 200:
                platform_result["registered"] = True
                platform_result["confidence"] = "HIGH"
                platform_result["summary"] = f"Number {TARGET_PHONE} appears to be registered on WhatsApp"
    
    # Check WhatsApp API endpoint for number validation
    api_url = "https://api.whatsapp.com/send/?phone=" + PHONE_NOPLUS
    resp = safe_get(api_url, allow_redirects=False)
    if resp:
        platform_result["checks"].append({
            "url": api_url,
            "status_code": resp.status_code,
            "redirect": resp.headers.get("Location", "")
        })
    
    # Check if profile picture exists via API
    # https://web.whatsapp.com/chat?t= phone check
    profile_url = f"https://pps.whatsapp.net/v/t61.24694-24/{PHONE_NOPLUS}"
    resp = safe_get(profile_url)
    if resp and resp.status_code == 200:
        platform_result["profile_picture_accessible"] = True
    
    if "registered" not in platform_result:
        platform_result["registered"] = "Unknown"
        platform_result["confidence"] = "LOW"
        platform_result["summary"] = "Could not definitively determine WhatsApp registration"
    
    results["platforms"]["whatsapp"] = platform_result
    print(f"    -> {platform_result.get('summary', 'Done')}")

# ============================================================
# 2. Telegram Check
# ============================================================
def check_telegram():
    print("[*] Checking Telegram...")
    platform_result = {"platform": "Telegram", "checks": []}
    
    # Check via Telegram's public resolve endpoint
    # Try phone-based username lookup
    phone_username_variants = [
        f"+{PHONE_NOPLUS}",
        PHONE_PLAIN,
        PHONE_NOPLUS,
    ]
    
    for pv in phone_username_variants:
        encoded = urllib.parse.quote(pv)
        url = f"https://t.me/+{encoded.lstrip('+')}"
        resp = safe_get(url, allow_redirects=False)
        if resp:
            platform_result["checks"].append({
                "url": url,
                "status_code": resp.status_code,
                "redirect": resp.headers.get("Location", "")
            })
    
    # Check Telegram API for contact resolution
    # This checks if a phone number has an associated Telegram account
    api_check_url = f"https://api.telegram.org/"
    resp = safe_get(api_check_url)
    if resp:
        platform_result["api_accessible"] = resp.status_code == 200
    
    # Check for common username patterns based on names
    name_usernames = []
    for name in NAMES:
        parts = name.lower().split()
        if len(parts) >= 2:
            name_usernames.append(parts[0] + parts[-1])  # e.g., catalinocheng
            name_usernames.append(parts[0] + "_" + parts[-1])
            if len(parts) > 2:
                name_usernames.append(parts[0] + parts[1][0] + parts[-1])  # catalinobcheng
        else:
            name_usernames.append(parts[0])
    
    name_usernames = list(set(name_usernames))
    platform_result["username_checks"] = []
    
    for uname in name_usernames:
        url = f"https://t.me/{uname}"
        resp = safe_get(url)
        if resp and resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # Check if the page shows a real Telegram user
            title_tag = soup.find("title")
            meta_desc = soup.find("meta", {"property": "og:description"})
            if title_tag:
                title_text = title_tag.text.strip()
                if "Telegram" in title_text and name.lower() not in title_text.lower():
                    # Generic page, user doesn't exist
                    pass
                else:
                    platform_result["username_checks"].append({
                        "username": uname,
                        "url": url,
                        "title": title_text,
                        "description": meta_desc.get("content", "") if meta_desc else "",
                        "possible_match": True
                    })
    
    if not platform_result["username_checks"]:
        platform_result["summary"] = "No Telegram profiles found for name-based username patterns"
    else:
        platform_result["summary"] = f"Found {len(platform_result['username_checks'])} potential Telegram profiles via username patterns"
    
    results["platforms"]["telegram"] = platform_result
    print(f"    -> {platform_result.get('summary', 'Done')}")

# ============================================================
# 3. Facebook Check
# ============================================================
def check_facebook():
    print("[*] Checking Facebook...")
    platform_result = {"platform": "Facebook", "checks": []}
    
    # Facebook phone search URLs
    search_queries = [
        TARGET_PHONE,
        PHONE_PAREN,
        PHONE_DASHED,
        PHONE_PLAIN,
    ]
    
    for q in search_queries:
        encoded = urllib.parse.quote(q)
        # Facebook search endpoint
        url = f"https://www.facebook.com/search/people/?q={encoded}"
        resp = safe_get(url, allow_redirects=False)
        if resp:
            platform_result["checks"].append({
                "url": url,
                "status_code": resp.status_code,
                "redirect": resp.headers.get("Location", ""),
                "note": "Facebook requires login for search; redirects indicate auth requirement"
            })
    
    # Check Facebook's public directory approach
    # Try accessing phone-linked profile if any
    phone_profile_urls = [
        f"https://www.facebook.com/{PHONE_PLAIN}",
        f"https://www.facebook.com/{PHONE_NOPLUS}",
        f"https://www.facebook.com/search/top/?q={urllib.parse.quote(TARGET_PHONE)}",
    ]
    
    for url in phone_profile_urls:
        resp = safe_get(url, allow_redirects=False)
        if resp:
            platform_result["checks"].append({
                "url": url,
                "status_code": resp.status_code,
                "redirect": resp.headers.get("Location", "")
            })
    
    # Search by name + location
    name_search_results = []
    for name in NAMES:
        encoded_name = urllib.parse.quote(f"{name} {LOCATION}")
        url = f"https://www.facebook.com/search/people/?q={encoded_name}"
        resp = safe_get(url, allow_redirects=False)
        if resp:
            name_search_results.append({
                "name": name,
                "url": url,
                "status_code": resp.status_code,
            })
    
    platform_result["name_searches"] = name_search_results
    
    # Check Facebook account recovery - leaks whether phone has account
    recovery_url = "https://www.facebook.com/login/identify/"
    resp = safe_get(recovery_url)
    if resp and resp.status_code == 200:
        # Try to submit phone number for recovery check
        platform_result["recovery_page_accessible"] = True
        platform_result["checks"].append({
            "url": recovery_url,
            "status_code": resp.status_code,
            "note": "Recovery page accessible; phone submission requires JavaScript/CSRF token"
        })
    
    platform_result["summary"] = "Facebook requires authentication for detailed search; public endpoints redirect to login"
    platform_result["limitations"] = "Most Facebook searches require authenticated session; scraping is blocked by login wall"
    
    results["platforms"]["facebook"] = platform_result
    print(f"    -> {platform_result.get('summary', 'Done')}")

# ============================================================
# 4. Twitter/X Check
# ============================================================
def check_twitter():
    print("[*] Checking Twitter/X...")
    platform_result = {"platform": "Twitter/X", "checks": []}
    
    # Twitter search URLs
    search_queries = [
        TARGET_PHONE,
        PHONE_PAREN,
        PHONE_DASHED,
        PHONE_PLAIN,
    ] + [f"{name} {LOCATION}" for name in NAMES[:3]]  # Top 3 names
    
    for q in search_queries:
        encoded = urllib.parse.quote(q)
        url = f"https://twitter.com/search?q={encoded}&f=user"
        resp = safe_get(url, allow_redirects=False)
        if resp:
            platform_result["checks"].append({
                "query": q,
                "url": url,
                "status_code": resp.status_code,
                "redirect": resp.headers.get("Location", "")
            })
    
    # Check X.com variant
    for q in [TARGET_PHONE, PHONE_PLAIN]:
        encoded = urllib.parse.quote(q)
        url = f"https://x.com/search?q={encoded}&f=user"
        resp = safe_get(url, allow_redirects=False)
        if resp:
            platform_result["checks"].append({
                "query": q,
                "url": url,
                "status_code": resp.status_code,
            })
    
    # Check common username patterns
    username_patterns = []
    for name in NAMES:
        parts = name.lower().split()
        if len(parts) >= 2:
            username_patterns.extend([
                parts[0] + parts[-1],
                parts[0] + "_" + parts[-1],
                parts[0][0] + parts[-1],
                parts[0] + parts[-1][0],
            ])
        else:
            username_patterns.append(parts[0])
    
    username_patterns = list(set(username_patterns))
    platform_result["username_checks"] = []
    
    for uname in username_patterns:
        url = f"https://twitter.com/{uname}"
        resp = safe_get(url, allow_redirects=False)
        if resp:
            if resp.status_code == 200:
                platform_result["username_checks"].append({
                    "username": uname,
                    "url": url,
                    "status_code": 200,
                    "possible_account": True
                })
    
    platform_result["summary"] = "Twitter/X requires authentication for user search; username pattern checks performed"
    results["platforms"]["twitter"] = platform_result
    print(f"    -> {platform_result.get('summary', 'Done')}")

# ============================================================
# 5. Instagram Check
# ============================================================
def check_instagram():
    print("[*] Checking Instagram...")
    platform_result = {"platform": "Instagram", "checks": []}
    
    # Instagram username lookup
    username_patterns = []
    for name in NAMES:
        parts = name.lower().split()
        if len(parts) >= 2:
            username_patterns.extend([
                parts[0] + parts[-1],
                parts[0] + "_" + parts[-1],
                parts[0] + "." + parts[-1],
                parts[0][0] + parts[-1],
                parts[0] + parts[1][0] + parts[-1] if len(parts) > 2 else "",
            ])
        else:
            username_patterns.append(parts[0])
    
    username_patterns = list(set([p for p in username_patterns if p]))
    platform_result["username_checks"] = []
    
    for uname in username_patterns:
        url = f"https://www.instagram.com/{uname}/"
        resp = safe_get(url)
        if resp:
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                # Look for user data in page source
                scripts = soup.find_all("script", type="application/ld+json")
                meta_desc = soup.find("meta", {"property": "og:description"})
                meta_title = soup.find("meta", {"property": "og:title"})
                
                user_data = {}
                if meta_title:
                    user_data["title"] = meta_title.get("content", "")
                if meta_desc:
                    desc = meta_desc.get("content", "")
                    user_data["description"] = desc
                    # Extract follower/following counts
                    followers = re.findall(r'(\d+)\s*Followers', desc)
                    following = re.findall(r'(\d+)\s*Following', desc)
                    posts = re.findall(r'(\d+)\s*Posts', desc)
                    if followers:
                        user_data["followers"] = followers[0]
                    if following:
                        user_data["following"] = following[0]
                    if posts:
                        user_data["posts"] = posts[0]
                
                for script in scripts:
                    try:
                        data = json.loads(script.string)
                        user_data["structured_data"] = data
                    except:
                        pass
                
                platform_result["username_checks"].append({
                    "username": uname,
                    "url": url,
                    "status_code": 200,
                    "data": user_data,
                    "possible_match": True
                })
            elif resp.status_code == 404:
                pass  # Username doesn't exist
    
    # Check Instagram's phone login/recovery
    # This would reveal if phone is linked to an account
    recovery_url = "https://www.instagram.com/accounts/password/reset/"
    resp = safe_get(recovery_url)
    if resp:
        platform_result["recovery_page_accessible"] = resp.status_code == 200
    
    if platform_result["username_checks"]:
        platform_result["summary"] = f"Found {len(platform_result['username_checks'])} potential Instagram profiles"
    else:
        platform_result["summary"] = "No Instagram profiles found for name-based username patterns"
    
    results["platforms"]["instagram"] = platform_result
    print(f"    -> {platform_result.get('summary', 'Done')}")

# ============================================================
# 6. LinkedIn Check
# ============================================================
def check_linkedin():
    print("[*] Checking LinkedIn...")
    platform_result = {"platform": "LinkedIn", "checks": []}
    
    # LinkedIn search URLs
    for name in NAMES:
        encoded_name = urllib.parse.quote(name)
        url = f"https://www.linkedin.com/pub/dir?firstName=&lastName={encoded_name}&trk=people-guest_people-search-bar_search-submit"
        resp = safe_get(url, allow_redirects=False)
        if resp:
            platform_result["checks"].append({
                "name": name,
                "url": url,
                "status_code": resp.status_code,
                "redirect": resp.headers.get("Location", ""),
            })
    
    # Check LinkedIn public profiles for names
    for name in NAMES[:3]:
        parts = name.lower().split()
        if len(parts) >= 2:
            # Public profile URL pattern: linkedin.com/in/firstname-lastname
            slug = "-".join(parts)
            url = f"https://www.linkedin.com/in/{slug}"
            resp = safe_get(url, allow_redirects=False)
            if resp:
                if resp.status_code == 200:
                    platform_result["checks"].append({
                        "profile_url": url,
                        "status_code": 200,
                        "possible_match": True,
                        "note": f"LinkedIn profile page found for {name}"
                    })
    
    # Try LinkedIn's schooner/ved API for people search
    api_url = f"https://www.linkedin.com/sales/gig/profile/lookup?firstName=Catalino&lastName=Cheng"
    resp = safe_get(api_url, allow_redirects=False)
    if resp:
        platform_result["checks"].append({
            "api_url": api_url,
            "status_code": resp.status_code,
        })
    
    platform_result["summary"] = "LinkedIn requires authentication; public profile checks attempted for name-based URLs"
    results["platforms"]["linkedin"] = platform_result
    print(f"    -> {platform_result.get('summary', 'Done')}")

# ============================================================
# 7. TikTok Check
# ============================================================
def check_tiktok():
    print("[*] Checking TikTok...")
    platform_result = {"platform": "TikTok", "checks": []}
    
    # TikTok username patterns
    username_patterns = []
    for name in NAMES:
        parts = name.lower().split()
        if len(parts) >= 2:
            username_patterns.extend([
                parts[0] + parts[-1],
                parts[0] + "_" + parts[-1],
                parts[0] + "." + parts[-1],
                parts[0][0] + parts[-1],
            ])
        else:
            username_patterns.append(parts[0])
    
    username_patterns = list(set(username_patterns))
    platform_result["username_checks"] = []
    
    tiktok_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://www.tiktok.com/",
    }
    
    for uname in username_patterns:
        url = f"https://www.tiktok.com/@{uname}"
        resp = safe_get(url, headers=tiktok_headers)
        if resp and resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.find("title")
            meta_desc = soup.find("meta", {"property": "og:description"})
            
            profile_data = {}
            if title:
                profile_data["title"] = title.text.strip()
            if meta_desc:
                profile_data["description"] = meta_desc.get("content", "")
            
            # Check if it's a real profile vs error page
            if title and uname.lower() in title.text.lower():
                platform_result["username_checks"].append({
                    "username": uname,
                    "url": url,
                    "data": profile_data,
                    "possible_match": True
                })
    
    # TikTok search by phone (SMS login check)
    sms_url = "https://www.tiktok.com/login/phone"
    resp = safe_get(sms_url, headers=tiktok_headers)
    if resp:
        platform_result["login_page_accessible"] = resp.status_code == 200
    
    if platform_result["username_checks"]:
        platform_result["summary"] = f"Found {len(platform_result['username_checks'])} potential TikTok profiles"
    else:
        platform_result["summary"] = "No TikTok profiles found for name-based username patterns"
    
    results["platforms"]["tiktok"] = platform_result
    print(f"    -> {platform_result.get('summary', 'Done')}")

# ============================================================
# 8. Snapchat Check
# ============================================================
def check_snapchat():
    print("[*] Checking Snapchat...")
    platform_result = {"platform": "Snapchat", "checks": []}
    
    # Snapchat username lookup
    username_patterns = []
    for name in NAMES:
        parts = name.lower().split()
        if len(parts) >= 2:
            username_patterns.extend([
                parts[0] + parts[-1],
                parts[0] + "_" + parts[-1],
                parts[0][0] + parts[-1],
            ])
        else:
            username_patterns.append(parts[0])
    
    username_patterns = list(set(username_patterns))
    platform_result["username_checks"] = []
    
    for uname in username_patterns:
        # Snapchat add URL - shows if user exists
        url = f"https://www.snapchat.com/add/{uname}"
        resp = safe_get(url)
        if resp:
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                title = soup.find("title")
                meta = soup.find("meta", {"property": "og:title"})
                
                profile_data = {}
                if title:
                    profile_data["title"] = title.text.strip()
                if meta:
                    profile_data["og_title"] = meta.get("content", "")
                
                platform_result["username_checks"].append({
                    "username": uname,
                    "url": url,
                    "status_code": 200,
                    "data": profile_data,
                    "possible_match": True
                })
    
    # Snapchat phone number search via API
    snap_api = "https://www.snapchat.com/add/by_phone"
    resp = safe_get(snap_api)
    if resp:
        platform_result["phone_api_accessible"] = resp.status_code == 200
    
    if platform_result["username_checks"]:
        platform_result["summary"] = f"Found {len(platform_result['username_checks'])} potential Snapchat profiles"
    else:
        platform_result["summary"] = "No Snapchat profiles found for name-based username patterns"
    
    results["platforms"]["snapchat"] = platform_result
    print(f"    -> {platform_result.get('summary', 'Done')}")

# ============================================================
# 9. Signal Check
# ============================================================
def check_signal():
    print("[*] Checking Signal...")
    platform_result = {"platform": "Signal", "checks": []}
    
    # Signal does not expose registration status publicly
    # But we can check the Signal server API
    signal_urls = [
        "https://signal.org/",
        "https://updates.signal.org/",
        f"https://signal.me/#p/{PHONE_NOPLUS}",  # Signal invite link
    ]
    
    for url in signal_urls:
        resp = safe_get(url)
        if resp:
            platform_result["checks"].append({
                "url": url,
                "status_code": resp.status_code,
            })
    
    # Check if Signal link format works
    signal_link = f"https://signal.me/#p/+{PHONE_NOPLUS}"
    resp = safe_get(signal_link)
    if resp and resp.status_code == 200:
        platform_result["checks"].append({
            "url": signal_link,
            "status_code": 200,
            "note": "Signal.me link accessible (all numbers get a link, doesn't confirm registration)"
        })
    
    platform_result["summary"] = "Signal does not publicly expose registration status; signal.me links exist for all phone numbers"
    platform_result["limitations"] = "Signal's privacy-first design prevents external registration checks"
    
    results["platforms"]["signal"] = platform_result
    print(f"    -> {platform_result.get('summary', 'Done')}")

# ============================================================
# 10. Google/Gmail Check
# ============================================================
def check_google():
    print("[*] Checking Google/Gmail...")
    platform_result = {"platform": "Google/Gmail", "checks": []}
    
    # Check if Gmail accounts exist for likely email patterns
    email_patterns = []
    for name in NAMES:
        parts = name.lower().split()
        if len(parts) >= 2:
            email_patterns.extend([
                f"{parts[0]}.{parts[-1]}@gmail.com",
                f"{parts[0]}{parts[-1]}@gmail.com",
                f"{parts[0]}{parts[1][0]}{parts[-1]}@gmail.com" if len(parts) > 2 else f"{parts[0]}{parts[-1]}@gmail.com",
                f"{parts[0][0]}{parts[-1]}@gmail.com",
                f"{parts[0]}_{parts[-1]}@gmail.com",
            ])
            # Also try with numbers
            email_patterns.append(f"{parts[0]}{parts[-1]}732@gmail.com")
            email_patterns.append(f"{parts[0]}{parts[-1]}874@gmail.com")
        else:
            email_patterns.append(f"{parts[0]}@gmail.com")
    
    email_patterns = list(set(email_patterns))
    platform_result["email_patterns_checked"] = email_patterns
    
    # Google account recovery check
    for email in email_patterns[:5]:  # Check first 5 patterns
        recovery_url = f"https://accounts.google.com/signin/v2/usernamelookup"
        # This doesn't directly work without JS but we can check the endpoint
        platform_result["checks"].append({
            "email": email,
            "recovery_url": recovery_url,
            "note": "Google account recovery requires JavaScript; cannot verify existence via scraping alone"
        })
    
    # Check Google Voice number lookup
    gv_url = "https://voice.google.com/about"
    resp = safe_get(gv_url)
    if resp:
        platform_result["voice_page_accessible"] = resp.status_code == 200
    
    platform_result["summary"] = "Google account existence cannot be verified via scraping; recovery requires JS"
    platform_result["limitations"] = "Google uses robust anti-scraping measures; account enumeration is prevented"
    
    results["platforms"]["google"] = platform_result
    print(f"    -> {platform_result.get('summary', 'Done')}")

# ============================================================
# 11. Additional Platforms
# ============================================================
def check_additional_platforms():
    print("[*] Checking additional platforms...")
    
    # --- GitHub ---
    print("    -> Checking GitHub...")
    github_result = {"platform": "GitHub", "checks": []}
    username_patterns = []
    for name in NAMES:
        parts = name.lower().split()
        if len(parts) >= 2:
            username_patterns.extend([
                parts[0] + parts[-1],
                parts[0] + "-" + parts[-1],
                parts[0][0] + parts[-1],
            ])
        else:
            username_patterns.append(parts[0])
    
    username_patterns = list(set(username_patterns))
    github_result["username_checks"] = []
    
    for uname in username_patterns:
        url = f"https://api.github.com/users/{uname}"
        resp = safe_get(url)
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                github_result["username_checks"].append({
                    "username": uname,
                    "url": data.get("html_url", ""),
                    "name": data.get("name", ""),
                    "bio": data.get("bio", ""),
                    "location": data.get("location", ""),
                    "company": data.get("company", ""),
                    "public_repos": data.get("public_repos", 0),
                    "followers": data.get("followers", 0),
                    "created_at": data.get("created_at", ""),
                    "possible_match": True
                })
            except:
                pass
    
    # Also search GitHub for phone number in code/commits
    for q in [PHONE_PLAIN, PHONE_DASHED, PHONE_NOPLUS]:
        url = f"https://api.github.com/search/code?q={q}"
        resp = safe_get(url)
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("total_count", 0) > 0:
                    github_result["phone_in_code"] = data["total_count"]
            except:
                pass
    
    if github_result["username_checks"]:
        github_result["summary"] = f"Found {len(github_result['username_checks'])} GitHub profiles"
    else:
        github_result["summary"] = "No GitHub profiles found for name-based username patterns"
    
    results["platforms"]["github"] = github_result
    
    # --- Pinterest ---
    print("    -> Checking Pinterest...")
    pinterest_result = {"platform": "Pinterest", "checks": []}
    for uname in username_patterns[:6]:
        url = f"https://www.pinterest.com/{uname}/"
        resp = safe_get(url)
        if resp and resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.find("title")
            if title and uname.lower() in title.text.lower():
                pinterest_result["checks"].append({
                    "username": uname,
                    "url": url,
                    "title": title.text.strip(),
                    "possible_match": True
                })
    
    pinterest_result["summary"] = f"Found {len(pinterest_result['checks'])} potential Pinterest profiles" if pinterest_result["checks"] else "No Pinterest profiles found"
    results["platforms"]["pinterest"] = pinterest_result
    
    # --- Reddit ---
    print("    -> Checking Reddit...")
    reddit_result = {"platform": "Reddit", "checks": []}
    reddit_headers = {
        "User-Agent": "Mozilla/5.0 (compatible; research-bot)",
    }
    for uname in username_patterns:
        url = f"https://www.reddit.com/user/{uname}/about.json"
        resp = safe_get(url, headers=reddit_headers)
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("data") and not data["data"].get("is_suspended"):
                    user_data = data["data"]
                    reddit_result["checks"].append({
                        "username": uname,
                        "url": f"https://www.reddit.com/user/{uname}",
                        "link_karma": user_data.get("link_karma", 0),
                        "comment_karma": user_data.get("comment_karma", 0),
                        "account_age": user_data.get("created_utc", ""),
                        "possible_match": True
                    })
            except:
                pass
    
    reddit_result["summary"] = f"Found {len(reddit_result['checks'])} Reddit profiles" if reddit_result["checks"] else "No Reddit profiles found"
    results["platforms"]["reddit"] = reddit_result
    
    # --- YouTube ---
    print("    -> Checking YouTube...")
    youtube_result = {"platform": "YouTube", "checks": []}
    for name in NAMES[:3]:
        encoded = urllib.parse.quote(name)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        resp = safe_get(url)
        if resp and resp.status_code == 200:
            youtube_result["checks"].append({
                "search_name": name,
                "url": url,
                "status_code": 200,
                "note": "YouTube search requires JS for results; page fetched but channel data in JS bundle"
            })
    
    youtube_result["summary"] = "YouTube search requires JavaScript; limited scraping possible"
    results["platforms"]["youtube"] = youtube_result
    
    # --- About.me ---
    print("    -> Checking About.me...")
    aboutme_result = {"platform": "About.me", "checks": []}
    for uname in username_patterns[:6]:
        url = f"https://about.me/{uname}"
        resp = safe_get(url)
        if resp and resp.status_code == 200:
            aboutme_result["checks"].append({
                "username": uname,
                "url": url,
                "possible_match": True
            })
    aboutme_result["summary"] = f"Found {len(aboutme_result['checks'])} potential About.me profiles" if aboutme_result["checks"] else "No About.me profiles found"
    results["platforms"]["aboutme"] = aboutme_result
    
    # --- Skype ---
    print("    -> Checking Skype...")
    skype_result = {"platform": "Skype", "checks": []}
    # Skype Web search API (limited)
    skype_api_url = "https://api.skype.com/users/self/contacts"
    resp = safe_get(skype_api_url)
    if resp:
        skype_result["checks"].append({
            "api_url": skype_api_url,
            "status_code": resp.status_code,
            "note": "Skype API requires authentication"
        })
    skype_result["summary"] = "Skype contact search requires authenticated API access"
    results["platforms"]["skype"] = skype_result
    
    # --- Gravatar ---
    print("    -> Checking Gravatar...")
    gravatar_result = {"platform": "Gravatar", "checks": []}
    for email in [f"{name.lower().replace(' ', '')}@gmail.com" for name in NAMES[:3]]:
        email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
        url = f"https://en.gravatar.com/{email_hash}.json"
        resp = safe_get(url)
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                if data.get("entry"):
                    entry = data["entry"][0]
                    gravatar_result["checks"].append({
                        "email": email,
                        "hash": email_hash,
                        "username": entry.get("preferredUsername", ""),
                        "display_name": entry.get("displayName", ""),
                        "location": entry.get("currentLocation", ""),
                        "url": f"https://en.gravatar.com/{email_hash}",
                        "possible_match": True
                    })
            except:
                pass
    gravatar_result["summary"] = f"Found {len(gravatar_result['checks'])} Gravatar profiles" if gravatar_result["checks"] else "No Gravatar profiles found for guessed email patterns"
    results["platforms"]["gravatar"] = gravatar_result

# ============================================================
# 12. Phone Number Scraping Check
# ============================================================
def check_phone_number_exposure():
    print("[*] Checking phone number exposure across sites...")
    exposure_result = {"platform": "Phone Number Exposure", "checks": []}
    
    # Check phone number on various public directories
    sites_to_check = [
        f"https://www.spokeo.com/{TARGET_PHONE}",
        f"https://www.spokeo.com/phone/{PHONE_NOPLUS}",
        f"https://www.unmask.com/phone/{PHONE_NOPLUS}",
        f"https://www.truepeoplesearch.com/results?phoneno={PHONE_DASHED}",
        f"https://www.fastpeoplesearch.com/{PHONE_DASHED}",
        f"https://www.usphonebook.com/{PHONE_NOPLUS}",
        f"https://www.whitepages.com/phone/{PHONE_DASHED}",
        f"https://calleridtest.com/{PHONE_NOPLUS}",
        f"https://www.sync.me/search/?phone={PHONE_NOPLUS}",
        f"https://www.callercomplaints.com/Phone-Number/{PHONE_NOPLUS}",
        f"https://www.shouldianswer.com/phone-number/{PHONE_NOPLUS}",
        f"https://www.callercomplaints.com/Phone-Number/{PHONE_DASHED}",
        f"https://800notes.com/Phone.aspx/{PHONE_DASHED}",
        f"https://www.whocalled.us/lookup/{PHONE_NOPLUS}",
        f"https://numverify.com/",
    ]
    
    for url in sites_to_check:
        resp = safe_get(url)
        if resp:
            status = resp.status_code
            data_snippet = ""
            if status == 200:
                # Try to extract relevant text
                soup = BeautifulSoup(resp.text, "html.parser")
                # Remove script and style elements
                for s in soup(["script", "style"]):
                    s.decompose()
                text = soup.get_text(separator=" ", strip=True)
                # Look for name references in the text
                name_found = []
                for name in NAMES:
                    if name.lower() in text.lower():
                        name_found.append(name)
                if name_found:
                    data_snippet = f"Names found on page: {', '.join(name_found)}"
                else:
                    # Get first 200 chars of text
                    data_snippet = text[:300] if len(text) > 300 else text
            
            exposure_result["checks"].append({
                "url": url,
                "status_code": status,
                "data_snippet": data_snippet[:500] if data_snippet else "",
                "names_found": name_found if status == 200 else []
            })
    
    # Check for phone number in data breach databases via public APIs
    breach_apis = [
        f"https://haveibeenpwned.com/unifiedsearch/{TARGET_PHONE}",
    ]
    for url in breach_apis:
        resp = safe_get(url, headers={"hibp-api-key": ""})
        if resp:
            exposure_result["checks"].append({
                "url": url,
                "status_code": resp.status_code,
                "note": "HIBP requires API key for phone lookups"
            })
    
    exposure_result["summary"] = f"Checked {len(exposure_result['checks'])} phone directory sites"
    results["platforms"]["phone_exposure"] = exposure_result
    print(f"    -> Checked {len(exposure_result['checks'])} sites")

# ============================================================
# 13. Name + Location Social Profile Search
# ============================================================
def check_name_social_searches():
    print("[*] Checking name + location across social platforms...")
    name_result = {"platform": "Name-Based Social Search", "searches": []}
    
    # Check various platforms for name + Edison NJ
    name_search_urls = []
    for name in NAMES:
        parts = name.lower().split()
        name_search_urls.extend([
            {
                "name": name,
                "url": f"https://www.facebook.com/search/people/?q={urllib.parse.quote(name + ' Edison NJ')}",
                "platform": "Facebook"
            },
            {
                "name": name,
                "url": f"https://twitter.com/search?q={urllib.parse.quote(name + ' Edison NJ')}&f=user",
                "platform": "Twitter"
            },
            {
                "name": name,
                "url": f"https://www.linkedin.com/pub/dir?firstName={urllib.parse.quote(parts[0])}&lastName={urllib.parse.quote(parts[-1] if len(parts) > 1 else '')}",
                "platform": "LinkedIn"
            },
        ])
    
    for search in name_search_urls:
        resp = safe_get(search["url"], allow_redirects=False)
        if resp:
            search["status_code"] = resp.status_code
            search["redirect"] = resp.headers.get("Location", "")
            name_result["searches"].append(search)
    
    name_result["summary"] = f"Performed {len(name_result['searches'])} name-based social platform searches"
    results["platforms"]["name_social_search"] = name_result
    print(f"    -> {name_result['summary']}")

# ============================================================
# 14. Discord Check
# ============================================================
def check_discord():
    print("[*] Checking Discord...")
    discord_result = {"platform": "Discord", "checks": []}
    
    # Discord doesn't allow phone-based user lookup
    # But we can check if phone is linked to Discord
    discord_urls = [
        "https://discord.com/",
        "https://discord.com/api/v9/users/@me",
    ]
    
    for url in discord_urls:
        resp = safe_get(url)
        if resp:
            discord_result["checks"].append({
                "url": url,
                "status_code": resp.status_code,
            })
    
    discord_result["summary"] = "Discord does not expose phone-number linked accounts; API requires auth token"
    discord_result["limitations"] = "Discord phone verification is internal; no public phone-to-user mapping"
    results["platforms"]["discord"] = discord_result
    print(f"    -> {discord_result['summary']}")

# ============================================================
# Main Execution
# ============================================================
if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    print("="*60)
    print("Social Media OSINT Scanner")
    print(f"Target: {TARGET_PHONE}")
    print(f"Names: {', '.join(NAMES)}")
    print(f"Location: {LOCATION}")
    print("="*60)
    print()
    
    checks = [
        check_whatsapp,
        check_telegram,
        check_facebook,
        check_twitter,
        check_instagram,
        check_linkedin,
        check_tiktok,
        check_snapchat,
        check_signal,
        check_google,
        check_discord,
        check_additional_platforms,
        check_phone_number_exposure,
        check_name_social_searches,
    ]
    
    for check_fn in checks:
        try:
            check_fn()
        except Exception as e:
            platform_name = check_fn.__name__.replace("check_", "")
            print(f"    [!] Error in {platform_name}: {e}")
            results["platforms"][platform_name] = {
                "error": str(e),
                "summary": f"Check failed: {e}"
            }
        time.sleep(1)  # Rate limiting
    
    # Summary
    print()
    print("="*60)
    print("SCAN COMPLETE")
    print("="*60)
    
    results["summary"] = {
        "platforms_checked": len(results["platforms"]),
        "findings": []
    }
    
    for platform, data in results["platforms"].items():
        summary = data.get("summary", "No summary")
        has_findings = bool(data.get("username_checks") or data.get("checks"))
        print(f"  {platform}: {summary}")
        if has_findings:
            # Check for actual positive findings
            positive = data.get("username_checks", []) + [c for c in data.get("checks", []) if c.get("possible_match")]
            if positive:
                results["summary"]["findings"].append({
                    "platform": platform,
                    "details": summary,
                    "positive_hits": len(positive)
                })
    
    # Save results
    output_path = "/a0/usr/workdir/social_media_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to {output_path}")
