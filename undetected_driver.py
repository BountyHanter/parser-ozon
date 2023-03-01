import undetected_chromedriver
from bs4 import BeautifulSoup
import json


class Parser:
    def __init__(self):
        self.html = None

    def take_html(self):
        try:
            # product = input('Введите название продукта\n')
            product = 'ноутбук'
            driver = undetected_chromedriver.Chrome()
            driver.get(f'https://www.ozon.ru/search/?from_global=true&page=1&sorting=rating&text={product}')
            self.html = driver.page_source
            with open('data.html', 'w', encoding='utf-8') as file:
                file.write(self.html)
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def take_info(self):
        with open('data.html', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        all_items = soup.find(class_="widget-search-result-container lk1").find_all(class_="yj6 y6j")
        blocks = []
        for item in all_items:
            link_pic = item.find('div', class_='vj8').find('img', class_='z7-a')
            link_prod = item.find('a', class_='wj0 w0j tile-hover-target')
            block = {
                'name': item.find(class_='ie2 ei3 ie3 ie5 tsBodyL jv4 vj4').text,
                'price': item.find(class_='yj7').next_element.next_element.next_element.text.replace('\u2009', ' '),
                'rating': item.find(class_='ef3 e3f fe3 tsBodyMBold').next_element.text.replace('\xa0', '')
                .replace(' ', ''),
                'num_revives': item.find(class_='e4f').find_next(class_='e4f').text.replace('\xa0', '')
                .replace(' · ', ''),
                'picture_link': link_pic['srcset'].replace(' 2x', ''),
                'product_link': 'https://www.ozon.ru'+link_prod['href']
            }
            blocks.append(block)
        with open('all_links.json', 'w', encoding='utf-8') as file:
            json.dump(blocks, file, indent=4, ensure_ascii=False)


prs = Parser()
prs.take_info()
