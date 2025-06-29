#!/usr/bin/env python3
"""
city_ip_ranges.py

Given a list of city names, print all IPv4 and IPv6 CIDR ranges
from a local MaxMind GeoLite2-City CSV database.

Requires that you've already downloaded and unpacked:
  - GeoLite2-City-Locations-en.csv
  - GeoLite2-City-Blocks-IPv4.csv
  - GeoLite2-City-Blocks-IPv6.csv

This version will auto-detect the Blocks CSVs in the same folder
as your Locations CSV if you only specify --locations-csv.
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
    if os.path.isfile(alt):
        return alt
    return None

def ensure_csvs(loc_csv, blocks4_csv, blocks6_csv):
    loc_dir = os.path.dirname(os.path.abspath(loc_csv))
    loc_path = resolve_path(loc_csv, loc_dir) or loc_csv
    b4_path  = resolve_path(blocks4_csv, loc_dir) or blocks4_csv
    b6_path  = resolve_path(blocks6_csv, loc_dir) or blocks6_csv

    missing = [p for p in (loc_path, b4_path, b6_path) if not os.path.isfile(p)]
    if missing:
        sys.exit(f"[ERROR] Missing required CSV file(s): {', '.join(missing)}\n"
                 "Please ensure the paths are correct.")
    return loc_path, b4_path, b6_path

def load_city_ids(loc_csv):
    city_map = defaultdict(set)
    with open(loc_csv, newline='', encoding='utf-8') as fh:
        for row in csv.DictReader(fh):
            name = (row.get("city_name") or "").strip()
            gid  = row.get("geoname_id")
            if name and gid:
                city_map[name.lower()].add(gid)
    return city_map

def find_blocks(blocks_csv, ids):
    with open(blocks_csv, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        id_field = ("geoname_id"
                    if "geoname_id" in reader.fieldnames
                    else "registered_country_geoname_id")
        for r in reader:
            if r.get(id_field) in ids:
                yield r.get("network")

def main():
    p = argparse.ArgumentParser(
        description="Print GeoLite2-City IP CIDR ranges for specified cities"
    )
    p.add_argument('cities', nargs='+',
                   help="City name(s), e.g. Kyiv New York")
    p.add_argument('--locations-csv', default='GeoLite2-City-Locations-en.csv',
                   help="Path to Locations CSV")
    p.add_argument('--blocks4-csv',    default='GeoLite2-City-Blocks-IPv4.csv',
                   help="Path to IPv4 Blocks CSV")
    p.add_argument('--blocks6-csv',    default='GeoLite2-City-Blocks-IPv6.csv',
                   help="Path to IPv6 Blocks CSV")
    args = p.parse_args()

    loc_csv, b4_csv, b6_csv = ensure_csvs(
        args.locations_csv, args.blocks4_csv, args.blocks6_csv
    )

    city_map = load_city_ids(loc_csv)

    for city in args.cities:
        ids = city_map.get(city.lower())
        if not ids:
            print(f"[!] No geoname_id for '{city}'", file=sys.stderr)
            continue

        print(f"\n=== {city} (geoname_id: {', '.join(sorted(ids))}) ===")
        print("-- IPv4 CIDRs --")
        count = 0
        for cidr in find_blocks(b4_csv, ids):
            print(cidr)
            count += 1
        if count == 0:
            print("  (none)")

        print("-- IPv6 CIDRs --")
        count = 0
        for cidr in find_blocks(b6_csv, ids):
            print(cidr)
            count += 1
        if count == 0:
            print("  (none)")

if __name__ == '__main__':
    main()

