import asyncio
from shops_data.item import Item
from shops_data.shop_base import ShopBase
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup, Tag
from shops_data.shop_category import ShopCategory


class shein(ShopBase):
    STORE = "SHEIN"

    @property
    def shop_categories(self) -> list[ShopCategory]:
        return [ShopCategory.ALL]

    async def get_items(self, search_item) -> list[Item]:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(
                f"https://ar.shein.com/pdsearch/{search_item}")
            await page.wait_for_load_state()
            html = await page.content()

            soup = BeautifulSoup(html, 'html.parser')

            search_items = soup.find_all(
                'section', class_='S-product-item j-expose__product-item product-list__item')
            return [self.get_item_from_dev(search_item) for search_item in search_items]

    def get_item_from_dev(self, search_item: Tag) -> Item:
        title_elem = search_item.find(
            'a', class_='S-product-item__link_jump S-product-item__link')
        title = title_elem.text.strip() if title_elem else 'N/A'

        price_elem = search_item.find(
            'span', class_='normal-price-ctn__sale-price')
        price = price_elem.text.strip() if price_elem else 'N/A'

        image_element = search_item.find('img', class_='falcon-lazyload')
        image_url = image_element.get('src', '') if isinstance(
            image_element, Tag) else ''

        link_element = search_item.find(
            'a', class_='S-product-item__link_jump S-product-item__link')
        link = link_element.get('href', '') if isinstance(
            link_element, Tag) else ''

        return Item(title, price, shein.STORE, link, image_url, '')


if __name__ == "__main__":
    she_in = shein()
    data = asyncio.run(she_in.get_items("مكنسة"))
    # print(she_in.shop_categories)
    print(data)
