# GeoCityIPRanges

A command-line tool to obtain IP address ranges for specified **cities** or **countries** using the local MaxMind GeoLite2 CSV databases.

## Features

- **Local CSV lookup only**  
  Relies on already-downloaded CSV files; no download or network logic built in.  
- **City & Country lookup**  
  Supports `--cities` (maps city names → GeoName IDs) and `--countries` (maps ISO codes or country names → GeoName IDs).  
- **IPv4 & IPv6**  
  Prints both IPv4 and IPv6 CIDR blocks for each lookup.  
- **Selective validation**  
  Only checks for the required CSVs for the mode you use (`--cities` or `--countries`).  
- **CLI-friendly**  
  Easy to integrate into scripts or pipelines; supports multiple values per run.

---

## Prerequisites

1. **Download** the GeoLite2-CSV ZIPs from MaxMind:  
   - Log in to your MaxMind account.  
   - Download **GeoLite2-City-CSV_YYYYMMDD.zip** and **GeoLite2-Country-CSV_YYYYMMDD.zip**.  
2. **Extract** the following into your working directory (or supply paths):  
   - `GeoLite2-City-Locations-en.csv`  
   - `GeoLite2-City-Blocks-IPv4.csv`  
   - `GeoLite2-City-Blocks-IPv6.csv`  
   - `GeoLite2-Country-Locations-en.csv`  
   - `GeoLite2-Country-Blocks-IPv4.csv`  
   - `GeoLite2-Country-Blocks-IPv6.csv`

---

## Installation

```bash
git clone https://github.com/your-username/GeoCityIPRanges.git
cd GeoCityIPRanges

# (Optional) Virtual environment
python3 -m venv venv
source venv/bin/activate

# Make the script executable
chmod +x geo_ip_ranges.py
```

_No external Python packages are required beyond the standard library._

---

## Usage

### By City

```bash
./geo_ip_ranges.py   --cities Kyiv London   --city-loc GeoLite2-City-CSV_20250627/GeoLite2-City-Locations-en.csv   --city-b4  GeoLite2-City-CSV_20250627/GeoLite2-City-Blocks-IPv4.csv   --city-b6  GeoLite2-City-CSV_20250627/GeoLite2-City-Blocks-IPv6.csv
```

### By Country

```bash
./geo_ip_ranges.py   --countries US Ukraine   --country-loc GeoLite2-Country-CSV_20250627/GeoLite2-Country-Locations-en.csv   --country-b4 GeoLite2-Country-CSV_20250627/GeoLite2-Country-Blocks-IPv4.csv   --country-b6 GeoLite2-Country-CSV_20250627/GeoLite2-Country-Blocks-IPv6.csv
```

### Mixed (Cities + Countries)

```bash
./geo_ip_ranges.py   --cities Paris   --countries FR   --city-loc    GeoLite2-City-Locations-en.csv   --city-b4     GeoLite2-City-Blocks-IPv4.csv   --city-b6     GeoLite2-City-Blocks-IPv6.csv   --country-loc GeoLite2-Country-Locations-en.csv   --country-b4  GeoLite2-Country-Blocks-IPv4.csv   --country-b6  GeoLite2-Country-Blocks-IPv6.csv
```

If any required CSV for your chosen mode is missing, the script will exit with an error listing which file(s) need to be present.

---

## .gitignore

```gitignore
# MaxMind GeoLite2 ZIP archives
GeoLite2-ASN-CSV_*.zip
GeoLite2-City-CSV_*.zip
GeoLite2-Country-CSV_*.zip

# Extracted CSV folders (optional)
GeoLite2-ASN-CSV_*/
GeoLite2-City-CSV_*/
GeoLite2-Country-CSV_*/
```

---

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.
