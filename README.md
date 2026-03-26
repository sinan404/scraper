# Internshala Job Scraper 🕷️

A robust Python script to automatically scrape internship and job listings directly from Internshala.

## 🚀 Features
* **Automated Pagination:** Seamlessly navigates through Internshala's pages to collect job cards (currently optimized to scrape the first 5 pages).
* **Data Points Extracted:** 
  * Job Title
  * Location
  * Required Skills
  * Salary / Stipend
  * Direct Application URL
  * Brief Job Description
* **Safe Exporting:** Automatically saves the scraped data to an Excel file (`Internshala_Jobs.xlsx`). Includes a safe fallback mechanism to save as `Internshala_Jobs.csv` if Excel dependencies are missing.
* **Anti-Blocking:** Uses standard browser User-Agents and respects basic rate limits via timeouts/sleeps.

## 🛠️ Prerequisites

Make sure you have Python installed. You will need the following libraries to run the script:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```
*(Note: `openpyxl` is recommended to support `.xlsx` Excel exports, but the scraper will work and fallback to `.csv` without it).*

## 💻 Usage

Run the scraper using Python in your terminal:

```bash
python internshala.py
```

The script will begin printing logs to the terminal as it navigates each page:
```text
Scraping: https://internshala.com/internships/
Scraping: https://internshala.com/internships/page-2/
...
✅ Data saved to Internshala_Jobs.xlsx
```

Once completed, check the folder for your newly generated dataset!

## ⚠️ Notes on Scraping
Please use this responsibly! Sending too many requests too quickly can temporarily block your IP address from accessing Internshala. The script includes a `time.sleep(2)` pause to help mitigate this.
