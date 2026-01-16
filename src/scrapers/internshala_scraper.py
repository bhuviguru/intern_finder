from .base_scraper import BaseScraper
from datetime import datetime
import time

class InternshalaScraper(BaseScraper):
    def __init__(self, browser_instance=None):
        super().__init__(browser_instance)
        self.base_url = "https://internshala.com/internships"

    async def scrape(self, keywords):
        jobs = []
        if not self.browser:
            self.logger.error("Browser instance not set")
            return jobs

        page = await self.browser.new_page()
        
        try:
            # Construct search URL (simple version, can be enhanced with filters)
            # Internshala URL structure: /internships/keywords-internship
            # For multiple keywords, it's tricky, so we might need multiple passes or broad search
            
            # Let's try to search for the first keyword or construct a search query
            # For simplicity, we loop through keywords or join them if supported. 
            # Internshala supports format: https://internshala.com/internships/<keyword>-internship
            
            for keyword in keywords:
                search_term = keyword.lower().replace(" ", "-")
                url = f"{self.base_url}/{search_term}-internship"
                self.logger.info(f"Scraping {url}")
                
                await page.goto(url, timeout=60000)
                await page.wait_for_load_state("networkidle")
                
                # Check for popup and close if necessary
                try:
                     await page.click(".login-modal .close_action", timeout=2000)
                except:
                    pass

                job_cards = await page.query_selector_all(".individual_internship")
                
                for card in job_cards:
                    try:
                        role_elem = await card.query_selector(".job-title-href")
                        company_elem = await card.query_selector(".company-name")
                        location_elem = await card.query_selector(".locations")
                        stipend_elem = await card.query_selector(".stipend_container .stipend")
                        link_elem = await card.query_selector(".job-title-href")
                        
                        if not role_elem: continue # Ad or invalid card

                        role = (await role_elem.inner_text()).strip()
                        company = (await company_elem.inner_text()).strip() if company_elem else "Unknown"
                        location = (await location_elem.inner_text()).strip() if location_elem else "Remote" # Default or parse
                        stipend = (await stipend_elem.inner_text()).strip() if stipend_elem else "Not disclosed"
                        link = "https://internshala.com" + await link_elem.get_attribute("href")
                        
                        # Posted info is sometimes hidden or relative text
                        # We'll use current date for scraped date
                        
                        # Deadline is available in .supply_demand_detal_container .other_detail_item (order varies)
                        # Skipping detailed deadline parsing for speed, can add later
                        
                        job = {
                            "site": "Internshala",
                            "company": company,
                            "role": role,
                            "stipend": stipend,
                            "location": location,
                            "link": link,
                            "deadline": None, # Needs deeper parsing
                            "posted_date": datetime.now().strftime("%Y-%m-%d")
                        }
                        jobs.append(job)
                        
                    except Exception as e:
                        self.logger.error(f"Error parsing job card: {e}")
            
        except Exception as e:
            self.logger.error(f"Error scraping Internshala: {e}")
        finally:
            await page.close()
            
        return jobs
