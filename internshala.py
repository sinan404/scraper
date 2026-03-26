import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://internshala.com/internships/"
HEADERS = {
    # Using a more modern User-Agent to avoid immediate blocks
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

jobs_data = []

def scrape_page(job_cards):
    for job in job_cards:

        # Job Title
        try:
            # Internshala uses 'job-title-href' or 'view_detail_button'
            title_tag = job.find("a", class_=["job-title-href", "view_detail_button"])
            title = title_tag.text.strip() if title_tag else ""
        except Exception:
            title = ""

        # Location (Drilling down to the anchor tag)
        try:
            # Find the p tag, then the span, then the 'a' tag specifically
            location = job.find("p", class_="locations").find("span").find("a").get_text(strip=True)
        except Exception:
            location = "Work from home"
        
        # Experience
        try:
            experience_div = job.find("div", class_="job-experience-item")
            experience = experience_div.find("div", class_="item_body").get_text(strip=True) if experience_div else "Not Specified"
        except Exception:
            experience = "Not Specified"

        # Skills Required
        try:
            skills_section = job.find("div", class_="job_skill")
            skills = skills_section.text.strip() if skills_section else ""
        except Exception:
            skills = ""

        # Salary / Stipend
        try:
            salary = job.find("span", class_="stipend").text.strip()
        except Exception:
            salary = ""

        # Job URL
        try:
            title_tag = job.find("a", class_=["job-title-href", "view_detail_button"])
            link = title_tag["href"] if title_tag else ""
            job_url = ("https://internshala.com" + link) if link else ""
        except Exception:
            job_url = ""

        # Description Summary
        description = ""

        if job_url:
            try:
                job_page = requests.get(job_url, headers=HEADERS, timeout=10)
                job_page.raise_for_status()
                job_soup = BeautifulSoup(job_page.text, "html.parser")

                desc_block = job_soup.find("div", class_="text-container")

                if desc_block:
                    description = desc_block.text.strip()[:250]
            except Exception:
                description = ""

        jobs_data.append({
            "JobTitle": title,
            "Location": location,
            "ExperienceRequired": experience,
            "SkillsRequired": skills,
            "Salary": salary,
            "JobURL": job_url,
            "JobDescriptionSummary": description
        })


def scrape_all_pages():

    page_number = 1

    while page_number <= 1:

        if page_number == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}page-{page_number}/"

        print(f"Scraping: {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                print(f"Stopping: Received status code {response.status_code}")
                break
        except Exception as e:
            print(f"Stopping due to request error: {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        job_cards = soup.find_all("div", class_="individual_internship")

        if not job_cards:
            print("No more job cards found. Ending scrape.")
            break

        scrape_page(job_cards)

        # FIXED: Uncommented the page increment to prevent infinite loops
        page_number += 1

        time.sleep(2)


# Run scraper
if __name__ == "__main__":
    scrape_all_pages()

    # Convert to DataFrame
    df = pd.DataFrame(jobs_data)

    # Save Excel file
    if not df.empty:
        try:
            df.to_excel("Internshala_Jobs.xlsx", index=False)
            print("✅ Data saved to Internshala_Jobs.xlsx")
        except ImportError:
            # Fallback to CSV if openpyxl is not installed
            df.to_csv("Internshala_Jobs.csv", index=False)
            print("✅ `openpyxl` not found. Fallback: Data saved to Internshala_Jobs.csv")
        except Exception as e:
            print(f"❌ Failed to save data: {e}")
    else:
        print("⚠️ No data was scraped.")
        