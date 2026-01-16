from .base_scraper import BaseScraper
from datetime import datetime
import time

class NaukriScraper(BaseScraper):
    def __init__(self, browser_instance=None):
        super().__init__(browser_instance)
        self.base_url = "https://www.naukri.com"

    async def scrape(self, keywords):
        jobs = []
        if not self.browser:
            self.logger.error("Browser instance not set")
            return jobs

        page = await self.browser.new_page()
        
        try:
            # Naukri search URL: https://www.naukri.com/<keyword>-internship-jobs
            for keyword in keywords:
                search_term = keyword.lower().replace(" ", "-")
                url = f"{self.base_url}/{search_term}-internship-jobs"
                self.logger.info(f"Scraping {url}")
                
                await page.goto(url, timeout=60000)
                await page.wait_for_load_state("domcontentloaded")

                title = await page.title()
                if "Access Denied" in title or "Security Check" in title:
                    self.logger.warning(f"Access Denied by Naukri for {url}. functionality might be limited.")
                    continue
                
                # Naukri classes are often obfuscated or standard
                job_cards = await page.query_selector_all(".srp-jobtuple-wrapper")
                
                for card in job_cards:
                    try:
                        role_elem = await card.query_selector(".title")
                        company_elem = await card.query_selector(".comp-name")
                        location_elem = await card.query_selector(".locWdth")
                        stipend_elem = await card.query_selector(".sal-wrap")
                        link_elem = await card.query_selector(".title")
                        
                        if not role_elem: continue

                        role = (await role_elem.inner_text()).strip()
                        company = (await company_elem.inner_text()).strip() if company_elem else "Unknown"
                        location = (await location_elem.inner_text()).strip() if location_elem else "Not specified"
                        stipend = (await stipend_elem.inner_text()).strip() if stipend_elem else "Not disclosed"
                        link = await link_elem.get_attribute("href")
                        
                        job = {
                            "site": "Naukri",
                            "company": company,
                            "role": role,
                            "stipend": stipend,
                            "location": location,
                            "link": link,
                            "deadline": None,
                            "posted_date": datetime.now().strftime("%Y-%m-%d")
                        }
                        jobs.append(job)
                        
                    except Exception as e:
                        self.logger.error(f"Error parsing Naukri job card: {e}")
            
        except Exception as e:
            self.logger.error(f"Error scraping Naukri: {e}")
        finally:
            await page.close()
            
        return jobs
