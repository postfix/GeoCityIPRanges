#!/usr/bin/env python3
"""
geo_ip_ranges.py

Print IPv4 and IPv6 CIDR ranges for specified cities and/or countries,
using **local** MaxMind GeoLite2 CSV databases.

Supports either --cities or --countries (or both).

Requires that you've already downloaded and unpacked:
  - GeoLite2-City-Locations-en.csv
  - GeoLite2-City-Blocks-IPv4.csv
  - GeoLite2-City-Blocks-IPv6.csv
  - GeoLite2-Country-Locations-en.csv
  - GeoLite2-Country-Blocks-IPv4.csv
  - GeoLite2-Country-Blocks-IPv6.csv
into your working directory (or supply paths).
"""
import csv
import argparse
import sys
import os
from collections import defaultdict

def resolve_path(path, fallback_dir):
    if os.path.isfile(path):
        return path
    alt = os.path.join(fallback_dir, os.path.basename(path))
    return alt if os.path.isfile(alt) else None

def ensure_existing(paths):
    missing = [p for p in paths if not (p and os.path.isfile(p))]
    if missing:
        sys.exit(f"[ERROR] Missing required CSV file(s): {', '.join(missing)}")

def load_mapping(loc_csv):
    m = defaultdict(set)
    with open(loc_csv, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            gid = row.get("geoname_id")
            if not gid:
                continue
            # map city, ISO code, and country name
            for key in (
                row.get("city_name", "").strip().lower(),
                row.get("country_iso_code", "").strip().lower(),
                row.get("country_name", "").strip().lower()
            ):
                if key:
                    m[key].add(gid)
    return m

def find_blocks(blocks_csv, id_field, ids):
    with open(blocks_csv, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            if r.get(id_field) in ids:
                yield r.get("network")

def print_ranges(label, ids, b4, b6, id_field):
    print(f"\n=== {label} ===")
    print("-- IPv4 CIDRs --")
    cnt = 0
    for cidr in find_blocks(b4, id_field, ids):
        print(cidr); cnt += 1
    if cnt == 0:
        print("  (none)")
    print("-- IPv6 CIDRs --")
    cnt = 0
    for cidr in find_blocks(b6, id_field, ids):
        print(cidr); cnt += 1
    if cnt == 0:
        print("  (none)")

def main():
    p = argparse.ArgumentParser(
        description="Print GeoLite2 IP CIDR ranges for cities or countries"
    )
    p.add_argument('--cities', nargs='+', metavar='CITY',
                   help="City names (e.g. Kyiv London)")
    p.add_argument('--countries', nargs='+', metavar='COUNTRY',
                   help="Country codes/names (e.g. US Ukraine)")
    p.add_argument('--city-loc', default='GeoLite2-City-Locations-en.csv')
    p.add_argument('--city-b4',  default='GeoLite2-City-Blocks-IPv4.csv')
    p.add_argument('--city-b6',  default='GeoLite2-City-Blocks-IPv6.csv')
    p.add_argument('--country-loc', default='GeoLite2-Country-Locations-en.csv')
    p.add_argument('--country-b4',  default='GeoLite2-Country-Blocks-IPv4.csv')
    p.add_argument('--country-b6',  default='GeoLite2-Country-Blocks-IPv6.csv')
    args = p.parse_args()

    if not (args.cities or args.countries):
        p.error("Must specify --cities and/or --countries")

    # Process cities
    if args.cities:
        city_files = [args.city_loc, args.city_b4, args.city_b6]
        ensure_existing(city_files)
        city_map = load_mapping(args.city_loc)
        for city in args.cities:
            ids = city_map.get(city.lower())
            if not ids:
                print(f"[!] No geoname_id for city '{city}'", file=sys.stderr)
                continue
            print_ranges(f"City: {city}", ids,
                         args.city_b4, args.city_b6,
                         id_field="geoname_id")

    # Process countries
    if args.countries:
        country_files = [args.country_loc, args.country_b4, args.country_b6]
        ensure_existing(country_files)
        country_map = load_mapping(args.country_loc)
        for country in args.countries:
            ids = country_map.get(country.lower())
            if not ids:
                print(f"[!] No geoname_id for country '{country}'", file=sys.stderr)
                continue
            print_ranges(f"Country: {country}", ids,
                         args.country_b4, args.country_b6,
                         id_field="registered_country_geoname_id")

if __name__ == '__main__':
    main()

