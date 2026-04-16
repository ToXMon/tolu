#!/usr/bin/env python3
"""
Phone OSINT Tool - Reverse Phone Number Lookup
Performs reverse phone lookup using multiple public APIs and techniques.
"""

import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import json
import sys
import time
import re
from datetime import datetime


class PhoneOSINT:
    def __init__(self, phone_number):
        self.original_input = phone_number
        self.results = {
            "target_number": phone_number,
            "timestamp": datetime.utcnow().isoformat(),
            "parsing": {},
            "carrier_info": {},
            "location_info": {},
            "cnam_lookups": [],
            "api_lookups": [],
            "identity_analysis": {},
            "summary": {}
        }
        self.parsed_number = None
        self.e164_format = None
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def parse_number(self):
        """Parse and validate the phone number using phonenumbers library."""
        print("\n[*] Parsing phone number...")
        try:
            self.parsed_number = phonenumbers.parse(self.original_input, "US")
            self.e164_format = phonenumbers.format_number(
                self.parsed_number, phonenumbers.PhoneNumberFormat.E164
            )

            self.results["parsing"] = {
                "valid": phonenumbers.is_valid_number(self.parsed_number),
                "possible": phonenumbers.is_possible_number(self.parsed_number),
                "e164_format": self.e164_format,
                "international_format": phonenumbers.format_number(
                    self.parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                ),
                "national_format": phonenumbers.format_number(
                    self.parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL
                ),
                "country_code": self.parsed_number.country_code,
                "national_number": str(self.parsed_number.national_number),
                "region": phonenumbers.region_code_for_number(self.parsed_number),
                "number_type": phonenumbers.number_type(self.parsed_number).__str__(),
            }

            type_map = {
                "0": "FIXED_LINE",
                "1": "MOBILE",
                "2": "FIXED_LINE_OR_MOBILE",
                "3": "TOLL_FREE",
                "4": "PREMIUM_RATE",
                "5": "SHARED_COST",
                "6": "VOIP",
                "7": "PERSONAL_NUMBER",
                "8": "PAGER",
                "9": "UAN",
                "10": "VOICEMAIL",
                "-1": "UNKNOWN"
            }
            self.results["parsing"]["number_type_name"] = type_map.get(
                self.results["parsing"]["number_type"], "UNKNOWN"
            )

            print(f"  [+] Valid: {self.results['parsing']['valid']}")
            print(f"  [+] E164: {self.e164_format}")
            print(f"  [+] Region: {self.results['parsing']['region']}")
            print(f"  [+] Type: {self.results['parsing']['number_type_name']}")

        except Exception as e:
            print(f"  [-] Error parsing number: {e}")
            self.results["parsing"]["error"] = str(e)

    def get_carrier_info(self):
        """Get carrier information from phonenumbers library."""
        print("\n[*] Getting carrier information...")
        try:
            carrier_name = carrier.name_for_number(self.parsed_number, "en")
            self.results["carrier_info"]["phonenumbers_carrier"] = carrier_name or "Unknown"
            print(f"  [+] Carrier: {carrier_name or 'Unknown'}")
        except Exception as e:
            print(f"  [-] Error getting carrier: {e}")

    def get_location_info(self):
        """Get geographic location information."""
        print("\n[*] Getting location information...")
        try:
            location = geocoder.description_for_number(self.parsed_number, "en")
            timezones = timezone.time_zones_for_number(self.parsed_number)

            self.results["location_info"] = {
                "geocoder_location": location or "Unknown",
                "timezones": list(timezones),
            }
            print(f"  [+] Location: {location or 'Unknown'}")
            print(f"  [+] Timezones: {timezones}")
        except Exception as e:
            print(f"  [-] Error getting location: {e}")

    def lookup_numverify(self):
        """Lookup using Numverify API."""
        print("\n[*] Attempting Numverify-style lookup...")
        try:
            url = "http://apilayer.net/api/validate"
            params = {
                "access_key": "",
                "number": self.e164_format,
                "country_code": "US",
                "format": 1
            }
            resp = self.session.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                self.results["api_lookups"].append({
                    "source": "numverify",
                    "data": data
                })
                print(f"  [+] Numverify response received")
                if data.get("valid"):
                    print(f"      Carrier: {data.get('carrier', 'N/A')}")
                    print(f"      Location: {data.get('location', 'N/A')}")
                    print(f"      Type: {data.get('line_type', 'N/A')}")
            else:
                print(f"  [-] Numverify returned status {resp.status_code}")
        except Exception as e:
            print(f"  [-] Numverify error: {e}")

    def lookup_opencnam(self):
        """Lookup using OpenCNAM for caller ID name."""
        print("\n[*] Attempting OpenCNAM lookup...")
        try:
            national = self.results["parsing"]["national_number"].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            url = f"https://api.opencnam.com/v3/phone/{national}"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                self.results["cnam_lookups"].append({
                    "source": "opencnam",
                    "data": data
                })
                print(f"  [+] OpenCNAM: {data}")
            elif resp.status_code == 404:
                print(f"  [-] OpenCNAM: No caller ID data found")
            else:
                print(f"  [-] OpenCNAM returned status {resp.status_code}")
        except Exception as e:
            print(f"  [-] OpenCNAM error: {e}")

    def lookup_telnyx(self):
        """Lookup using Telnyx public number lookup API."""
        print("\n[*] Attempting Telnyx lookup...")
        try:
            url = f"https://lookup.telnyx.com/v1/phone_number/{self.e164_format}"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                self.results["api_lookups"].append({
                    "source": "telnyx",
                    "data": data
                })
                print(f"  [+] Telnyx response received")
                if "carrier" in data:
                    print(f"      Carrier: {data['carrier']}")
            else:
                print(f"  [-] Telnyx returned status {resp.status_code}")
        except Exception as e:
            print(f"  [-] Telnyx error: {e}")

    def lookup_fcc_area_code(self):
        """Look up area code information."""
        print("\n[*] Looking up area code information...")
        area_code = str(self.parsed_number.national_number)[:3]
        area_code_map = {
            "732": "New Jersey (Central: New Brunswick, Toms River, Lakewood, Freehold)",
            "201": "New Jersey (Northeast: Jersey City, Hackensack)",
            "973": "New Jersey (Northern: Newark, Paterson)",
            "609": "New Jersey (Southern/Central: Trenton, Atlantic City)",
            "856": "New Jersey (Southern: Camden, Vineland)",
            "908": "New Jersey (Central: Elizabeth, Somerville)",
        }
        if area_code in area_code_map:
            self.results["location_info"]["area_code_detail"] = area_code_map[area_code]
            print(f"  [+] Area code {area_code}: {area_code_map[area_code]}")
        else:
            print(f"  [*] Area code {area_code}: not in local database")

    def lookup_callercomplaints(self):
        """Check caller complaints databases."""
        print("\n[*] Checking complaint/spam databases...")
        try:
            national = self.results["parsing"]["national_number"].replace(" ", "-")
            url = f"https://www.callercomplaints.com/Phone-Number/{national}"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                complaints = re.findall(r"complaint[^<]*<[^>]*>([^<]+)", resp.text, re.IGNORECASE)
                self.results["api_lookups"].append({
                    "source": "callercomplaints",
                    "status": "checked",
                    "complaints_found": len(complaints)
                })
                print(f"  [+] CallerComplaints checked - {len(complaints)} mentions")
            else:
                print(f"  [-] CallerComplaints status {resp.status_code}")
        except Exception as e:
            print(f"  [-] CallerComplaints error: {e}")

    def lookup_truecallermode(self):
        """Check Truecaller-style public data endpoints."""
        print("\n[*] Attempting Truecaller public data lookup...")
        try:
            national = self.results["parsing"]["national_number"].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            url = f"https://search5-noneu.truecaller.com/v2/search?q={national}&countryCode=us&type=4&locAddr=&placement=SEARCHRESULTS%3AHISTORY&adId=&clientId=1&myNumber=1"
            headers = {
                "User-Agent": "Truecaller/11.0 (Android; 11)",
            }
            resp = self.session.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                self.results["api_lookups"].append({
                    "source": "truecaller",
                    "data": data
                })
                print(f"  [+] Truecaller data received")
            else:
                print(f"  [-] Truecaller returned {resp.status_code}")
        except Exception as e:
            print(f"  [-] Truecaller error: {e}")

    def lookup_spydialer(self):
        """Check SpyDialer public endpoint pattern."""
        print("\n[*] Attempting SpyDialer-style lookup...")
        try:
            national = self.results["parsing"]["national_number"].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            url = "https://spydialer.com/api/Default/LookupPhone"
            data = {"phone": national, "countryCode": "US"}
            resp = self.session.post(url, json=data, timeout=10)
            if resp.status_code == 200:
                result = resp.json()
                self.results["api_lookups"].append({
                    "source": "spydialer",
                    "data": result
                })
                print(f"  [+] SpyDialer data received: {result}")
            else:
                print(f"  [-] SpyDialer returned {resp.status_code}")
        except Exception as e:
            print(f"  [-] SpyDialer error: {e}")

    def lookup_national_cell_registry(self):
        """Check national cellular directory."""
        print("\n[*] Attempting National Cellular Directory lookup...")
        try:
            national = self.results["parsing"]["national_number"].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            url = f"https://www.nationalcellulardirectory.com/search/results.cfm?phone={national}"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                names = re.findall(r'class="owner-name"[^>]*>([^<]+)<', resp.text)
                self.results["api_lookups"].append({
                    "source": "national_cellular_directory",
                    "names_found": names[:5] if names else []
                })
                if names:
                    print(f"  [+] Names found: {names[:5]}")
                else:
                    print(f"  [*] No names extracted from page")
            else:
                print(f"  [-] NCD returned {resp.status_code}")
        except Exception as e:
            print(f"  [-] NCD error: {e}")

    def lookup_syncme(self):
        """Check SyncMe directory."""
        print("\n[*] Attempting SyncMe lookup...")
        try:
            national = self.results["parsing"]["national_number"].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            url = f"https://sync.me/phone/?number={national}&search=Search"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                name_matches = re.findall(r'<div class="name"[^>]*>([^<]+)</div>', resp.text)
                comment_matches = re.findall(r'<div class="comment"[^>]*>([^<]+)</div>', resp.text)
                self.results["api_lookups"].append({
                    "source": "syncme",
                    "names": name_matches[:5] if name_matches else [],
                    "comments": comment_matches[:5] if comment_matches else []
                })
                if name_matches:
                    print(f"  [+] SyncMe names found: {name_matches[:5]}")
                if comment_matches:
                    print(f"  [+] SyncMe comments: {comment_matches[:5]}")
                if not name_matches and not comment_matches:
                    print(f"  [*] SyncMe page loaded, no structured data extracted")
            else:
                print(f"  [-] SyncMe returned {resp.status_code}")
        except Exception as e:
            print(f"  [-] SyncMe error: {e}")

    def lookup_usphonebook(self):
        """Check USPhoneBook public lookup."""
        print("\n[*] Attempting USPhoneBook lookup...")
        try:
            national = self.results["parsing"]["national_number"].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            url = f"https://www.usphonebook.com/{national[:3]}-{national[3:6]}-{national[6:]}"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                name_matches = re.findall(r'itemprop="name"[^>]*>([^<]+)</span>', resp.text)
                addr_matches = re.findall(r'itemprop="address"[^>]*>([^<]+)<', resp.text)
                alt_names = re.findall(r'class="name[^"]*"[^>]*>([^<]+)', resp.text)
                self.results["api_lookups"].append({
                    "source": "usphonebook",
                    "names": name_matches[:5] if name_matches else [],
                    "addresses": addr_matches[:3] if addr_matches else [],
                    "alt_names": alt_names[:5] if alt_names else []
                })
                if name_matches:
                    print(f"  [+] USPhoneBook names: {name_matches[:5]}")
                if addr_matches:
                    print(f"  [+] USPhoneBook addresses: {addr_matches[:3]}")
                if alt_names:
                    print(f"  [+] USPhoneBook alt names: {alt_names[:5]}")
                if not name_matches and not addr_matches and not alt_names:
                    print(f"  [*] USPhoneBook page loaded, no structured data extracted")
            else:
                print(f"  [-] USPhoneBook returned {resp.status_code}")
        except Exception as e:
            print(f"  [-] USPhoneBook error: {e}")

    def lookup_thatsthem(self):
        """Check ThatsThem public directory."""
        print("\n[*] Attempting ThatsThem lookup...")
        try:
            national = self.results["parsing"]["national_number"].replace(" ", "-")
            url = f"https://thatsthem.com/phone/{national}"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                name_matches = re.findall(r'class="name[^"]*"[^>]*>([^<]+)', resp.text)
                addr_matches = re.findall(r'class="address[^"]*"[^>]*>([^<]+)', resp.text)
                self.results["api_lookups"].append({
                    "source": "thatsthem",
                    "names": name_matches[:5] if name_matches else [],
                    "addresses": addr_matches[:3] if addr_matches else []
                })
                if name_matches:
                    print(f"  [+] ThatsThem names: {name_matches[:5]}")
                else:
                    print(f"  [*] ThatsThem page loaded")
            else:
                print(f"  [-] ThatsThem returned {resp.status_code}")
        except Exception as e:
            print(f"  [-] ThatsThem error: {e}")

    def lookup_caller_id_api(self):
        """Check caller ID APIs."""
        print("\n[*] Attempting caller.id.com lookup...")
        try:
            national = self.results["parsing"]["national_number"].replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            url = f"https://calleridtest.com/lookup/{national}"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                print(f"  [+] CallerID page loaded")
                self.results["api_lookups"].append({
                    "source": "callerid_lookup",
                    "status": "page_loaded",
                    "response_length": len(resp.text)
                })
            else:
                print(f"  [-] CallerID returned {resp.status_code}")
        except Exception as e:
            print(f"  [-] CallerID error: {e}")

    def cross_reference_identity(self, family_names):
        """Cross-reference all found names with known family names."""
        print("\n[*] Cross-referencing with known family names...")
        found_names = set()

        # Collect all names from all sources
        for lookup in self.results.get("api_lookups", []):
            if isinstance(lookup.get("data"), dict) and "names" in lookup["data"]:
                for name in lookup["data"]["names"]:
                    found_names.add(name)
            if "names_found" in lookup:
                for name in lookup["names_found"]:
                    found_names.add(name)
            if "names" in lookup:
                for name in lookup["names"]:
                    found_names.add(name)
            if "alt_names" in lookup:
                for name in lookup["alt_names"]:
                    found_names.add(name)

        for cnam in self.results.get("cnam_lookups", []):
            if "data" in cnam and isinstance(cnam["data"], dict):
                if "cnam" in cnam["data"]:
                    found_names.add(cnam["data"]["cnam"])
                if "name" in cnam["data"]:
                    found_names.add(cnam["data"]["name"])

        # Clean up names
        clean_names = set()
        for name in found_names:
            name = str(name).strip()
            if name and len(name) > 1:
                clean_names.add(name)

        self.results["identity_analysis"]["all_found_names"] = list(clean_names)

        # Check for matches with known family names
        matches = {}
        for identifier, search_name in family_names.items():
            matches[identifier] = {
                "search_name": search_name,
                "found": False,
                "matched_entries": []
            }
            for found_name in clean_names:
                if search_name.lower() in found_name.lower():
                    matches[identifier]["found"] = True
                    matches[identifier]["matched_entries"].append(found_name)

        any_match = any(m["found"] for m in matches.values())
        self.results["identity_analysis"]["family_name_matches"] = matches
        self.results["identity_analysis"]["identity_confidence"] = "HIGH" if any_match else "LOW"

        print(f"  [*] All found names: {list(clean_names)}")
        for key, match in matches.items():
            status = "MATCH" if match["found"] else "NO MATCH"
            print(f"  [{'+' if match['found'] else '-'}] {identifier} '{match['search_name']}': {status}")

        print(f"  [*] Identity confidence: {self.results['identity_analysis']['identity_confidence']}")

    def generate_summary(self):
        """Generate a final summary of all findings."""
        print("\n" + "="*60)
        print("SUMMARY OF FINDINGS")
        print("="*60)

        parsing = self.results.get("parsing", {})
        print(f"\nPhone Number: {parsing.get('international_format', 'N/A')}")
        print(f"Valid: {parsing.get('valid', 'N/A')}")
        print(f"Region: {parsing.get('region', 'N/A')}")
        print(f"Type: {parsing.get('number_type_name', 'N/A')}")

        carrier_info = self.results.get("carrier_info", {})
        print(f"\nCarrier: {carrier_info.get('phonenumbers_carrier', 'N/A')}")

        location = self.results.get("location_info", {})
        print(f"Location: {location.get('geocoder_location', 'N/A')}")
        print(f"Timezone: {location.get('timezones', 'N/A')}")
        if "area_code_detail" in location:
            print(f"Area Code Detail: {location['area_code_detail']}")

        print(f"\nAPI Lookups Performed: {len(self.results.get('api_lookups', []))}")
        for lookup in self.results.get("api_lookups", []):
            src = lookup.get('source', 'unknown')
            summary = json.dumps(lookup)[:120]
            print(f"  - {src}: {summary}")

        print(f"\nCNAM Lookups: {len(self.results.get('cnam_lookups', []))}")
        for cnam in self.results.get("cnam_lookups", []):
            src = cnam.get('source', 'unknown')
            summary = json.dumps(cnam)[:120]
            print(f"  - {src}: {summary}")

        identity = self.results.get("identity_analysis", {})
        print(f"\nIdentity Confidence: {identity.get('identity_confidence', 'N/A')}")
        if identity.get("all_found_names"):
            print(f"All Names Found: {identity['all_found_names']}")

        for key, match in identity.get("family_name_matches", {}).items():
            m_str = 'MATCH - ' + str(match.get('matched_entries', [])) if match.get('found') else 'No match found'
            print(f"  {key} ({match.get('search_name', '')}): {m_str}")

    def run(self, family_names=None):
        """Execute all lookups."""
        print("="*60)
        print("PHONE OSINT TOOL - Reverse Phone Lookup")
        print("="*60)
        print(f"Target: {self.original_input}")
        if family_names:
            print(f"Family names for cross-ref: {family_names}")

        # Step 1: Parse and validate
        self.parse_number()

        if not self.results["parsing"].get("valid", False):
            print("\n[!] WARNING: Phone number may not be valid!")

        # Step 2: Get carrier and location info
        self.get_carrier_info()
        self.get_location_info()

        # Step 3: API lookups
        self.lookup_telnyx()
        self.lookup_opencnam()
        self.lookup_numverify()
        self.lookup_truecallermode()
        self.lookup_spydialer()
        self.lookup_fcc_area_code()
        self.lookup_usphonebook()
        self.lookup_thatsthem()
        self.lookup_syncme()
        self.lookup_callercomplaints()
        self.lookup_national_cell_registry()
        self.lookup_caller_id_api()

        # Step 4: Cross-reference with known names
        if family_names:
            self.cross_reference_identity(family_names)

        # Step 5: Generate summary
        self.generate_summary()

        # Save results
        output_file = "/a0/usr/workdir/phone_osint_results.json"
        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n[*] Full results saved to {output_file}")

        return self.results


if __name__ == "__main__":
    target_phone = "(732) 874-0910"

    family_names = {
        "possible_person": "Deeksha",
        "father": "Susheel",
        "mother": "Venna"
    }

    osint = PhoneOSINT(target_phone)
    results = osint.run(family_names=family_names)
