import scrapy

class LightingSpider(scrapy.Spider):
    name = 'lighting'
    allowed_domains = ['divan.ru']
    start_urls = ['https://www.divan.ru/category/svet']

    def parse(self, response):
        self.log(f'Parsing page: {response.url}')
        # Используем CSS селектор для извлечения ссылок на продукты
        product_links = response.css('a[href*="/product/"]::attr(href)').getall()
        self.log(f'Found {len(product_links)} product links')

        if not product_links:
            self.log('No product links found!')
        for link in product_links:
            yield response.follow(link, self.parse_product)

        # Проверяем наличие следующей страницы
        next_page = response.css('a.pagination__next::attr(href)').get()
        if next_page:
            self.log(f'Next page found: {next_page}')
            yield response.follow(next_page, self.parse)
        else:
            self.log('No next page link found!')

    def parse_product(self, response):
        # Извлекаем название и цену продукта
        name = response.css('h1[itemprop="name"]::text').get()
        price = response.css('span[itemprop="price"]::attr(content)').get()
        self.log(f'Parsed product: {name} - {price}')

        if not name or not price:
            self.log(f'Missing data on {response.url}')
        yield {
            'name': name,
            'price': price,
            'link': response.url
        }
