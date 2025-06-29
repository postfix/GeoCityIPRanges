# GeoCityIPRanges
A command-line tool to obtain IP address ranges for specified cities using the MaxMind GeoLite2-City database.


## Features

- **Local CSV lookup only**  
  The tool relies on already-downloaded CSV files; no download logic is built in.  
- **City lookup**  
  Maps city names to one or more GeoName IDs.  
- **IPv4 & IPv6**  
  Prints both IPv4 and IPv6 CIDR blocks for each city.  
- **CLI-friendly**  
  Easy to integrate into scripts or pipelines; supports multiple cities per run.

---

## Prerequisites

1. **Download** the GeoLite2-City CSV ZIP from MaxMind:  
   - Log in to your MaxMind account.  
   - Download **GeoLite2-City-CSV_YYYYMMDD.zip**.  
2. **Extract** the following into your working directory:  
   - `GeoLite2-City-Locations-en.csv`  
   - `GeoLite2-City-Blocks-IPv4.csv`  
   - `GeoLite2-City-Blocks-IPv6.csv`

---

## Installation

1. Clone this repository:  
   ```bash
   git clone https://github.com/your-username/GeoCityIPRanges.git
   cd GeoCityIPRanges
   ```
2. (Optional) Create and activate a virtual environment:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Ensure `city_ip_ranges.py` is executable:  
   ```bash
   chmod +x city_ip_ranges.py
   ```

_No external Python packages are required beyond the standard library._

---
# Usage Examples

```bash
# 1) Specify all three paths explicitly:
./city_ip_ranges.py \
  --locations-csv GeoLite2-City-CSV_20250627/GeoLite2-City-Locations-en.csv \
  --blocks4-csv   GeoLite2-City-CSV_20250627/GeoLite2-City-Blocks-IPv4.csv \
  --blocks6-csv   GeoLite2-City-CSV_20250627/GeoLite2-City-Blocks-IPv6.csv \
  Birmingham Bristol London
```
If any required CSV is missing, the script will exit with an error listing which file(s) need to be present.

---

## .gitignore

```gitignore
# MaxMind GeoLite2 ZIP archives
GeoLite2-ASN-CSV_*.zip
GeoLite2-City-CSV_*.zip
GeoLite2-Country-CSV_*.zip

# MaxMind GeoLite2 extracted CSV folders
GeoLite2-ASN-CSV_*/
GeoLite2-City-CSV_*/
GeoLite2-Country-CSV_*/
```
