#!/usr/bin/env python3
"""
DeepPhoneIntel - Professional OSINT Tool
Author: hyper-a11
License: MIT
"""

import argparse
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
import webbrowser
from colorama import Fore, Style, init

# ==== Initialize Colorama ====
init(autoreset=True)

# ==== API Config ====
NUMVERIFY_API_KEY = "YOUR_NUMVERIFY_API_KEY"  # Optional
NUMVERIFY_URL = "http://apilayer.net/api/validate"
IP_API_URL = "http://ip-api.com/json/"

# ==== Helper Functions (Colored Output) ====
def info(msg): print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + msg)
def success(msg): print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + msg)
def warning(msg): print(Fore.YELLOW + "[WARNING] " + Style.RESET_ALL + msg)
def error(msg): print(Fore.RED + "[ERROR] " + Style.RESET_ALL + msg)

# ==== Phone Lookup ====
def phone_lookup(phone):
    try:
        num = phonenumbers.parse(phone, None)
        success("\n=== Phone Info ===")
        print(f"Country      : {phonenumbers.region_code_for_number(num)}")
        print(f"Valid        : {phonenumbers.is_valid_number(num)}")
        print(f"Possible     : {phonenumbers.is_possible_number(num)}")
        print(f"Carrier      : {carrier.name_for_number(num, 'en')}")
        print(f"Time Zones   : {timezone.time_zones_for_number(num)}")
        print(f"Geo (approx) : {geocoder.description_for_number(num, 'en')}")
    except phonenumbers.NumberParseException:
        error("Invalid phone number format.")

# ==== NumVerify Lookup ====
def numverify_lookup(phone):
    success("\n=== NumVerify Lookup ===")
    if NUMVERIFY_API_KEY == "YOUR_NUMVERIFY_API_KEY":
        warning("NumVerify API key missing. Skipping lookup.")
        return
    try:
        r = requests.get(NUMVERIFY_URL, params={"access_key": NUMVERIFY_API_KEY, "number": phone})
        data = r.json()
        if data.get("valid"):
            print(f"Location : {data.get('location')} ({data.get('country_name')})")
            print(f"Carrier  : {data.get('carrier')}")
        else:
            warning("NumVerify lookup failed.")
    except:
        error("NumVerify API not accessible.")

# ==== Open or Print URLs ====
def open_or_print(url, open_browser):
    if open_browser:
        webbrowser.open(url)
    else:
        print(url)

# ==== Social Media Search ====
def social_media_search(phone, open_browser):
    success("\n=== Social Media Search ===")
    sites = ["facebook.com", "linkedin.com", "instagram.com", "twitter.com"]
    for site in sites:
        url = f"https://www.google.com/search?q=\"{phone}\" site:{site}"
        info(f"Searching {site}")
        open_or_print(url, open_browser)

# ==== Telegram Search ====
def telegram_search(phone, open_browser):
    success("\n=== Telegram Search ===")
    url = f"https://www.google.com/search?q=\"{phone}\" site:t.me OR site:telegram.me"
    open_or_print(url, open_browser)

# ==== Breach Lookup ====
def breach_lookup(phone, open_browser):
    success("\n=== Breach DB Lookup ===")
    urls = [
        f"https://scylla.sh/search?q={phone}",
        f"https://dehashed.com/search?query={phone}"
    ]
    for u in urls:
        open_or_print(u, open_browser)

# ==== Email Lookup ====
def email_username_search(email, open_browser):
    success("\n=== Email / Username OSINT ===")
    sites = ["facebook.com", "linkedin.com", "instagram.com", "github.com", "twitter.com"]
    for site in sites:
        url = f"https://www.google.com/search?q=\"{email}\" site:{site}"
        info(f"Searching {site}")
        open_or_print(url, open_browser)

# ==== IP Lookup ====
def ip_lookup(ip):
    success("\n=== IP Lookup ===")
    try:
        r = requests.get(f"{IP_API_URL}{ip}")
        data = r.json()
        if data.get("status") == "success":
            print(f"IP        : {ip}")
            print(f"ISP       : {data.get('isp')}")
            print(f"City      : {data.get('city')}, {data.get('regionName')}, {data.get('country')}")
            print(f"Lat / Lon : {data.get('lat')}, {data.get('lon')}")
        else:
            warning("IP lookup failed.")
    except:
        error("Could not fetch IP details.")

# ==== Main ====
def main():
    parser = argparse.ArgumentParser(description="DeepPhoneIntel - Professional OSINT Tool by hyper-a11")
    parser.add_argument("phone", help="Phone number with country code (e.g. +919876543210)")
    parser.add_argument("--email", help="Email/username for OSINT search")
    parser.add_argument("--ip", help="IP address for lookup")
    parser.add_argument("--no-browser", action="store_true", help="Print URLs instead of opening browser tabs")
    args = parser.parse_args()

    open_browser = not args.no_browser

    phone_lookup(args.phone)
    numverify_lookup(args.phone)
    social_media_search(args.phone, open_browser)
    telegram_search(args.phone, open_browser)
    breach_lookup(args.phone, open_browser)

    if args.email:
        email_username_search(args.email, open_browser)

    if args.ip:
        ip_lookup(args.ip)

if __name__ == "__main__":
    main()
