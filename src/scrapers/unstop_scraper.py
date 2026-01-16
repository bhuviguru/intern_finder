from .base_scraper import BaseScraper
from datetime import datetime
import time

class UnstopScraper(BaseScraper):
    def __init__(self, browser_instance=None):
        super().__init__(browser_instance)
        self.base_url = "https://unstop.com/internships"

    async def scrape(self, keywords):
        jobs = []
        if not self.browser:
            self.logger.error("Browser instance not set")
            return jobs

        page = await self.browser.new_page()
        
        try:
            # Unstop search URL pattern: https://unstop.com/internships?term=<keyword>
            for keyword in keywords:
                search_term = keyword.replace(" ", "%20")
                url = f"{self.base_url}?term={search_term}"
                self.logger.info(f"Scraping {url}")
                
                await page.goto(url, timeout=60000)
                await page.wait_for_load_state("networkidle")

                # Parse job cards
                # Selectors need to be verified, using generic structural assumptions or known classes
                # Unstop usually uses specific card classes
                job_cards = await page.query_selector_all(".c-body") # highly variable, needs robust selector

                # Fallback to a broader selector if specific one fails
                if not job_cards:
                     job_cards = await page.query_selector_all("app-opportunity-card")

                for card in job_cards:
                    try:
                        role_elem = await card.query_selector("h2") or await card.query_selector(".job-title")
                        company_elem = await card.query_selector("h3") or await card.query_selector(".org-name")
                        
                        # Location and Stipend logic is trickier on Unstop as it varies
                        # We might need to click or check specific icons
                        
                        if not role_elem: continue

                        role = (await role_elem.inner_text()).strip()
                        company = (await company_elem.inner_text()).strip() if company_elem else "Unknown"
                        
                        link_elem = await card.query_selector("a.card-anchor") or await card.query_selector("a")
                        link = ""
                        if link_elem:
                            href = await link_elem.get_attribute("href")
                            if href.startswith("http"):
                                link = href
                            else:
                                link = "https://unstop.com" + href
                        
                        job = {
                            "site": "Unstop",
                            "company": company,
                            "role": role,
                            "stipend": "See Link",
                            "location": "See Link",
                            "link": link,
                            "deadline": None,
                            "posted_date": datetime.now().strftime("%Y-%m-%d")
                        }
                        jobs.append(job)
                        
                    except Exception as e:
                        self.logger.error(f"Error parsing Unstop job card: {e}")
            
        except Exception as e:
            self.logger.error(f"Error scraping Unstop: {e}")
        finally:
            await page.close()
            
        return jobs
