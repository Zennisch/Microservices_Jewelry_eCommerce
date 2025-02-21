import asyncio
import json
import os

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from zns_logging import get_logger


class PNJScraper:
    def __init__(self, item_type: str, max_concurrent_requests: int = 10):
        self.base_url = f"https://www.pnj.com.vn/{item_type}"
        self.item_type = item_type
        self.logger = get_logger(__name__)
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        os.makedirs(f"data/{item_type}", exist_ok=True)

    async def fetch(self, url: str, return_bytes: bool = False):
        """Fetch HTML content or binary content (for images) asynchronously"""
        async with self.semaphore:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    return await response.read() if return_bytes else await response.text()

    async def scrape_product_links(self, page: int) -> list:
        """Extracts product URLs from a given page"""
        url = f"{self.base_url}/page-{page}/"
        self.logger.info(f"Fetching product list from {url}")
        try:
            html = await self.fetch(url)
            soup = BeautifulSoup(html, "html.parser")
            container = soup.find("div", {"id": "ajax_pagination_contents"})
            return [
                item.find("a")["href"]
                for item in container.find_all("div", class_="product-image")
            ]
        except Exception as e:
            self.logger.error(f"Error fetching product links from {url}: {e}")
            return []

    async def scrape_product_details(self, url: str):
        """Fetch product details (ID, code, image links) from product page"""
        self.logger.info(f"Fetching product details from {url}")
        try:
            html = await self.fetch(url)
            soup = BeautifulSoup(html, "html.parser")
            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            if not script_tag:
                return None

            data = json.loads(script_tag.string)
            product_data = data["props"]["pageProps"]["dataServerSide"]
            return {
                "product_id": str(product_data["product_id"]).zfill(6),
                "product_code": product_data["product_code"],
                "images": product_data.get("images", []),
            }
        except Exception as e:
            self.logger.error(f"Error fetching product data from {url}: {e}")
            return None

    async def download_image(self, image_url: str, product_id: str, product_code: str):
        """Download image and save to disk"""
        try:
            image_name = image_url.split("/")[-1]
            file_name = (
                f"data/{self.item_type}/{product_id}_{product_code}_{image_name}"
            )
            self.logger.info(f"Downloading {file_name}")
            image_data = await self.fetch(image_url, return_bytes=True)
            with open(file_name, "wb") as f:
                f.write(image_data)
        except Exception as e:
            self.logger.error(f"Failed to download image {image_url}: {e}")

    async def run(self, start_page: int = 1, end_page: int = 8):
        """Orchestrates the scraping process"""
        self.logger.info("Starting PNJ Scraper")

        # Step 1: Get all product URLs
        product_urls = sum(
            await asyncio.gather(*[self.scrape_product_links(i) for i in range(start_page, end_page + 1)]),
            [],
        )

        # Step 2: Get product details
        product_details = await asyncio.gather(*[self.scrape_product_details(url) for url in product_urls])
        product_details = [data for data in product_details if data]

        # Step 3: Download images
        download_tasks = [
            self.download_image(img, product["product_id"], product["product_code"])
            for product in product_details
            for img in product["images"]
        ]
        await asyncio.gather(*download_tasks)

        self.logger.info("Scraping complete!")


if __name__ == "__main__":
    item_type = input("Enter item type: ")
    scraper = PNJScraper(item_type)
    asyncio.run(scraper.run())
