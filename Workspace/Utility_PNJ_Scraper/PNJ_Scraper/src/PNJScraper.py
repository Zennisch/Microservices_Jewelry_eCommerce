import asyncio
import json
import os
import re
from datetime import datetime
import random
from typing import Dict, List, Any, Optional, Tuple

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from zns_logging import ZnsLogger


class PNJScraper:
    def __init__(self, item_type: str, max_concurrent_requests: int = 10):
        self.base_url = f"https://www.pnj.com.vn/{item_type}"
        self.item_type = item_type
        self.logger = ZnsLogger(__name__, "DEBUG")
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)

        # Create directories for output
        os.makedirs(f"data/{item_type}/json", exist_ok=True)
        os.makedirs(f"data/{item_type}/images", exist_ok=True)
        os.makedirs(f"data/{item_type}/sql", exist_ok=True)

    def determine_material(self, product_name: str) -> str:
        """Determine material based on product name or randomly if not found"""
        product_name = product_name.lower()

        if "vàng" in product_name:
            return "Gold"
        elif "bạc" in product_name:
            return "Silver"
        elif "kim cương" in product_name or "diamond" in product_name:
            return "Diamond"
        elif "ngọc trai" in product_name or "pearl" in product_name:
            return "Pearl"
        elif "đá quý" in product_name or "ruby" in product_name or "sapphire" in product_name:
            return "Gemstone"
        elif "platinum" in product_name or "bạch kim" in product_name:
            return "Platinum"
        else:
            # Random selection if not found in name
            materials = ["Gold", "Silver", "Diamond", "Pearl", "Gemstone", "Platinum", "Mixed"]
            return random.choice(materials)

    def generate_gold_karat(self, material: str) -> Optional[int]:
        """Generate appropriate gold karat based on material"""
        if material == "Gold":
            return random.choice([10, 14, 18, 24])
        return None  # Not applicable for other materials

    def generate_color(self, material: str) -> str:
        """Generate appropriate color based on material"""
        if material == "Gold":
            return random.choice(["Yellow", "White", "Rose"])
        elif material == "Silver":
            return "Silver"
        elif material == "Platinum":
            return "White"
        elif material == "Pearl":
            return random.choice(["White", "Black", "Pink", "Cream"])
        elif material == "Diamond":
            return random.choice(["Clear", "White", "Yellow", "Pink", "Blue"])
        elif material == "Gemstone":
            return random.choice(["Red", "Blue", "Green", "Purple", "Yellow", "Pink", "Orange"])
        else:
            return random.choice(["Mixed", "Gold", "Silver", "Various"])

    def generate_brand(self) -> str:
        """Generate a random brand"""
        brands = ["PNJ", "DOJI", "SJC", "Tinh Tú Jewelry", "Kim Ngọc Uy Tín",
                  "Vàng Bạc Đá Quý Phú Nhuận", "Vàng Bạc Đá Quý Thế Giới",
                  "Vàng Bạc Đá Quý Minh Phát", "Vàng Bạc Đá Quý Châu Á"]
        return random.choice(brands)

    def generate_gender(self) -> int:
        """Generate a random gender (0=female, 1=male, 2=unisex)"""
        return random.choice([0, 1, 2])

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

    async def scrape_product_details(self, url: str) -> Optional[Dict[str, Any]]:
        """Fetch product details from product page and return raw JSON data"""
        self.logger.info(f"Fetching product details from {url}")
        try:
            html = await self.fetch(url)
            soup = BeautifulSoup(html, "html.parser")
            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            if not script_tag:
                return None

            # Parse the JSON data
            data = json.loads(script_tag.string)

            # Save raw JSON data for reference
            product_data = data["props"]["pageProps"]["dataServerSide"]
            product_id = str(product_data["product_id"]).zfill(6)

            # Save the raw JSON
            # with open(f"data/{self.item_type}/json/{product_id}.json", "w", encoding="utf-8") as f:
            #     json.dump(data, f, ensure_ascii=False, indent=2)

            return data

        except Exception as e:
            self.logger.error(f"Error fetching product data from {url}: {e}")
            return None

    def sanitize_text(self, text: str) -> str:
        """Clean text for SQL insertion"""
        if not text:
            return ""
        # Replace single quotes with escaped single quotes
        return text.replace("'", "''")

    def extract_category_data(self, data: Dict) -> List[Dict]:
        """Extract category information from product data"""
        categories = []
        try:
            for category in data["props"]["pageProps"]["dataServerSide"]["category_seo"]:
                categories.append({
                    "id": category["category_id"],
                    "name": self.sanitize_text(category["category"]),
                    "url": category["seo_name_url"],
                })
        except (KeyError, TypeError):
            self.logger.warning("Failed to extract category data")
        return categories

    def extract_product_data(self, data: Dict) -> Dict:
        """Extract product information from product data"""
        product = {}
        try:
            product_data = data["props"]["pageProps"]["dataServerSide"]
            product_name = self.sanitize_text(product_data["product"])

            # Determine material based on name or random
            material = self.determine_material(product_name)

            product = {
                "id": product_data["product_id"],
                "name": product_name,
                "code": product_data["product_code"],
                "description": self.sanitize_text(product_data.get("full_description", "")),
                "price": product_data["price"],
                "status": "ACTIVE" if product_data.get("status") == "A" else "INACTIVE",
                "quantity": product_data.get("amount", 0),
                "category_id": data["props"]["pageProps"]["dataServerSide"]["category_seo"][0]["category_id"],
                "material": material,
                "gold_karat": self.generate_gold_karat(material),
                "color": self.generate_color(material),
                "brand": self.generate_brand(),
                "gender": self.generate_gender(),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        except (KeyError, TypeError, IndexError) as e:
            self.logger.warning(f"Failed to extract product data: {e}")
        return product

    def extract_product_images(self, data: Dict) -> List[Dict]:
        """Extract product images from product data"""
        images = []
        try:
            product_id = data["props"]["pageProps"]["dataServerSide"]["product_id"]
            img_list = data["props"]["pageProps"]["dataServerSide"]["images"]

            for i, img_url in enumerate(img_list):
                images.append({
                    "product_id": product_id,
                    "image_url": img_url,
                    "is_primary": i == 0,  # First image is primary
                    "sort_order": i + 1,
                })
        except (KeyError, TypeError):
            self.logger.warning("Failed to extract image data")
        return images

    def extract_product_features(self, data: Dict) -> List[Dict]:
        """Extract product features/attributes from product data"""
        features = []
        try:
            product_id = data["props"]["pageProps"]["dataServerSide"]["product_id"]
            feature_list = data["props"]["pageProps"]["dataServerSide"]["features"]

            for feature in feature_list:
                features.append({
                    "product_id": product_id,
                    "name": self.sanitize_text(feature["feature"]),
                    "value": self.sanitize_text(feature["text"]),
                })
        except (KeyError, TypeError):
            self.logger.warning("Failed to extract feature data")
        return features

    def extract_product_variants(self, data: Dict) -> List[Dict]:
        """Extract product variants (sizes, colors) from product data"""
        variants = []
        try:
            product_id = data["props"]["pageProps"]["dataServerSide"]["product_id"]
            size_prices = data["props"]["pageProps"]["dataServerSide"]["size_modifier_prices"]

            for size, price_info in size_prices.items():
                variants.append({
                    "product_id": product_id,
                    "variant_type": "SIZE",
                    "variant_value": size,
                    "price": price_info["price"],
                    "quantity": data["props"]["pageProps"]["dataServerSide"].get("amount", 0),
                })
        except (KeyError, TypeError):
            self.logger.warning("Failed to extract variant data")
        return variants

    def generate_sql_script(self, products: List[Dict], categories: List[Dict],
                            images: List[Dict], features: List[Dict], variants: List[Dict]) -> str:
        """Generate SQL script for PostgreSQL from extracted data"""
        sql = "-- PNJ Data Import Script\n"
        sql += f"-- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Begin transaction
        sql += "BEGIN;\n\n"

        # Create constraints if they don't exist
        sql += "-- Add necessary constraints for ON CONFLICT clauses\n"
        sql += "DO $$ BEGIN\n"
        sql += "    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'categories_id_key') THEN\n"
        sql += "        ALTER TABLE categories ADD CONSTRAINT categories_id_key UNIQUE (id);\n"
        sql += "    END IF;\n"
        sql += "    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'products_id_key') THEN\n"
        sql += "        ALTER TABLE products ADD CONSTRAINT products_id_key UNIQUE (id);\n"
        sql += "    END IF;\n"
        sql += "    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'product_images_product_id_image_url_key') THEN\n"
        sql += "        ALTER TABLE product_images ADD CONSTRAINT product_images_product_id_image_url_key UNIQUE (product_id, image_url);\n"
        sql += "    END IF;\n"
        sql += "    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'product_features_product_id_name_key') THEN\n"
        sql += "        ALTER TABLE product_features ADD CONSTRAINT product_features_product_id_name_key UNIQUE (product_id, name);\n"
        sql += "    END IF;\n"
        sql += "    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'product_variants_product_id_variant_type_variant_value_key') THEN\n"
        sql += "        ALTER TABLE product_variants ADD CONSTRAINT product_variants_product_id_variant_type_variant_value_key UNIQUE (product_id, variant_type, variant_value);\n"
        sql += "    END IF;\n"
        sql += "EXCEPTION\n"
        sql += "    WHEN others THEN\n"
        sql += "    RAISE NOTICE 'Error adding constraints: %', SQLERRM;\n"
        sql += "END $$;\n\n"

        # Insert categories
        sql += "-- Categories Table\n"
        if categories:
            # Get unique categories by ID
            unique_categories = {}
            for cat in categories:
                unique_categories[cat["id"]] = cat

            for cat in unique_categories.values():
                # Version without ON CONFLICT
                sql += f"DO $$ BEGIN\n"
                sql += f"    IF NOT EXISTS (SELECT 1 FROM categories WHERE id = {cat['id']}) THEN\n"
                sql += f"        INSERT INTO categories (id, name, url) VALUES ({cat['id']}, '{cat['name']}', '{cat['url']}');\n"
                sql += f"    ELSE\n"
                sql += f"        UPDATE categories SET name = '{cat['name']}', url = '{cat['url']}' WHERE id = {cat['id']};\n"
                sql += f"    END IF;\n"
                sql += f"END $$;\n"

        # Insert products
        sql += "\n-- Products Table\n"
        for product in products:
            # Handle NULL values properly
            gold_karat = "NULL" if product.get('gold_karat') is None else product['gold_karat']

            sql += f"DO $$ BEGIN\n"
            sql += f"    IF NOT EXISTS (SELECT 1 FROM products WHERE id = {product['id']}) THEN\n"
            sql += f"        INSERT INTO products (id, name, code, description, price, status, quantity, category_id, material, gold_karat, color, brand, gender, created_at, updated_at) VALUES \n"
            sql += f"        ({product['id']}, '{product['name']}', '{product['code']}', '{product['description']}', {product['price']}, '{product['status']}', {product['quantity']}, {product['category_id']}, '{product['material']}', {gold_karat}, '{product['color']}', '{product['brand']}', {product['gender']}, '{product['created_at']}', '{product['updated_at']}');\n"
            sql += f"    ELSE\n"
            sql += f"        UPDATE products SET name = '{product['name']}', price = {product['price']}, status = '{product['status']}', quantity = {product['quantity']}, material = '{product['material']}', gold_karat = {gold_karat}, color = '{product['color']}', brand = '{product['brand']}', gender = {product['gender']}, updated_at = '{product['updated_at']}' WHERE id = {product['id']};\n"
            sql += f"    END IF;\n"
            sql += f"END $$;\n"

        # Insert product images
        sql += "\n-- Product Images Table\n"
        for img in images:
            # Version without ON CONFLICT
            sql += f"DO $$ BEGIN\n"
            sql += f"    IF NOT EXISTS (SELECT 1 FROM product_images WHERE product_id = {img['product_id']} AND image_url = '{img['image_url']}') THEN\n"
            sql += f"        INSERT INTO product_images (product_id, image_url, is_primary, sort_order) VALUES \n"
            sql += f"        ({img['product_id']}, '{img['image_url']}', {str(img['is_primary']).lower()}, {img['sort_order']});\n"
            sql += f"    END IF;\n"
            sql += f"END $$;\n"

        # Insert product features
        sql += "\n-- Product Features Table\n"
        for feature in features:
            # Version without ON CONFLICT
            sql += f"DO $$ BEGIN\n"
            sql += f"    IF NOT EXISTS (SELECT 1 FROM product_features WHERE product_id = {feature['product_id']} AND name = '{feature['name']}') THEN\n"
            sql += f"        INSERT INTO product_features (product_id, name, value) VALUES \n"
            sql += f"        ({feature['product_id']}, '{feature['name']}', '{feature['value']}');\n"
            sql += f"    ELSE\n"
            sql += f"        UPDATE product_features SET value = '{feature['value']}' WHERE product_id = {feature['product_id']} AND name = '{feature['name']}';\n"
            sql += f"    END IF;\n"
            sql += f"END $$;\n"

        # Insert product variants
        sql += "\n-- Product Variants Table\n"
        for variant in variants:
            # Version without ON CONFLICT
            sql += f"DO $$ BEGIN\n"
            sql += f"    IF NOT EXISTS (SELECT 1 FROM product_variants WHERE product_id = {variant['product_id']} AND variant_type = '{variant['variant_type']}' AND variant_value = '{variant['variant_value']}') THEN\n"
            sql += f"        INSERT INTO product_variants (product_id, variant_type, variant_value, price, quantity) VALUES \n"
            sql += f"        ({variant['product_id']}, '{variant['variant_type']}', '{variant['variant_value']}', {variant['price']}, {variant['quantity']});\n"
            sql += f"    ELSE\n"
            sql += f"        UPDATE product_variants SET price = {variant['price']}, quantity = {variant['quantity']} WHERE product_id = {variant['product_id']} AND variant_type = '{variant['variant_type']}' AND variant_value = '{variant['variant_value']}';\n"
            sql += f"    END IF;\n"
            sql += f"END $$;\n"

        # Commit transaction
        sql += "\nCOMMIT;\n"

        return sql

    async def download_image(self, image_url: str, product_id: str, index: int):
        """Download image and save to disk"""
        try:
            image_name = image_url.split("/")[-1]
            file_name = f"data/{self.item_type}/images/{product_id}_{index}_{image_name}"
            self.logger.info(f"Downloading {file_name}")
            image_data = await self.fetch(image_url, return_bytes=True)
            with open(file_name, "wb") as f:
                f.write(image_data)
        except Exception as e:
            self.logger.error(f"Failed to download image {image_url}: {e}")

    async def run(self, start_page: int = 1, end_page: int = 1):
        """Orchestrates the scraping process"""
        self.logger.info(f"Starting PNJ Scraper for {self.item_type} pages {start_page}-{end_page}")

        # Step 1: Get all product URLs
        product_urls = []
        for page in range(start_page, end_page + 1):
            urls = await self.scrape_product_links(page)
            product_urls.extend(urls)
            self.logger.info(f"Found {len(urls)} products on page {page}")

        self.logger.info(f"Total of {len(product_urls)} products found")

        # Step 2: Get product details
        all_products_data = []
        for url in product_urls:
            data = await self.scrape_product_details(url)
            if data:
                all_products_data.append(data)

        # Step 3: Process data and generate SQL
        products = []
        categories = []
        images = []
        features = []
        variants = []

        for data in all_products_data:
            product_data = self.extract_product_data(data)
            # Only include complete product records
            if product_data and 'id' in product_data:
                products.append(product_data)
                categories.extend(self.extract_category_data(data))
                images.extend(self.extract_product_images(data))
                features.extend(self.extract_product_features(data))
                variants.extend(self.extract_product_variants(data))
            else:
                self.logger.warning(f"Skipping incomplete product data")
                continue

            categories.extend(self.extract_category_data(data))
            images.extend(self.extract_product_images(data))
            features.extend(self.extract_product_features(data))
            variants.extend(self.extract_product_variants(data))

        # Generate SQL script
        sql_script = self.generate_sql_script(products, categories, images, features, variants)

        # Save SQL script
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sql_file = f"data/{self.item_type}/sql/{self.item_type}_{timestamp}.sql"
        with open(sql_file, "w", encoding="utf-8") as f:
            f.write(sql_script)

        self.logger.info(f"SQL script saved to {sql_file}")

        # Step 4: Download images (optional)
        download_tasks = []
        for img_data in images:
            product_id = str(img_data["product_id"]).zfill(6)
            # download_tasks.append(self.download_image(img_data["image_url"], product_id, img_data["sort_order"]))

        # Run image download in parallel
        if download_tasks:
            self.logger.info(f"Downloading {len(download_tasks)} images...")
            await asyncio.gather(*download_tasks)

        self.logger.info(f"Scraping complete! Processed {len(products)} products")
        self.logger.info(
            f"Generated SQL with {len(categories)} categories, {len(products)} products, {len(images)} images, {len(features)} features, and {len(variants)} variants")


if __name__ == "__main__":
    item_type = input("Enter item type (e.g., nhan, day-chuyen, lac): ")
    start_page = int(input("Enter start page number: ") or "1")
    end_page = int(input("Enter end page number: ") or "1")

    scraper = PNJScraper(item_type)
    asyncio.run(scraper.run(start_page, end_page))
