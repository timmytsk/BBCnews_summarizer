from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep
from tqdm import tqdm


# class BBCNewsParser:
#     def __init__(self):
#         self.url = 'https://www.bbc.com/russian'
#         self.data = {}
#         self.df = pd.DataFrame(columns=['title', 'text', 'link'])
#         self.get_titles_and_links()
#         self.data_for_one_n = pd.DataFrame.from_dict(self.data.items())
#         self.data_for_one_n.columns = ['title', 'link']
#         self.amount_of_news = len(self.data_for_one_n)
#         self.index = 0
#
#     def get_main_news(self):
#         page = requests.get(self.url)
#         soup = BeautifulSoup(page.text, "html.parser")
#         section_heading = soup.find(class_="bbc-1rrncb9")
#         return section_heading
#
#     def get_titles_and_links(self):
#         section_heading = self.get_main_news()
#         for n in section_heading.find_all('a', href=True):
#             self.data[n.text] = n['href']
#
#     def get_text(self):
#         print('Парсинг новостей с BBCNews Russia')
#         for title, link in tqdm(self.data.items()):
#             text = ''
#             page = requests.get(link)
#             soup = BeautifulSoup(page.text, "html.parser")
#             if soup.find(class_="css-2je8ow"):
#                 section_heading = soup.find(class_="css-2je8ow")
#                 for t in section_heading.find_all(class_=["postStyles", "css-wzuydr", "e17g058b0"]):
#                     text += f'{t.text}\n'
#             elif soup.find(class_="bbc-fa0wmp"):
#                 section_heading = soup.find(class_="bbc-fa0wmp")
#                 for t in section_heading.find_all(class_=["bbc-d8piq7", "e17g058b0"]):
#                     text += f'{t.text}\n'
#             else:
#                 continue
#             df = pd.DataFrame([[title, text, link]], columns=['title', 'text', 'link'])
#             self.df = pd.concat([self.df, df])
#             sleep(3)
#         self.df.reset_index(drop=True, inplace=True)
#
#     def return_dataset(self):
#         return self.df
#
#     def get_one_news(self):
#         if self.index >= self.amount_of_news:
#             self.index -= self.amount_of_news
#         title, link = self.data_for_one_n.loc[self.index]
#         text = ''
#         page = requests.get(link)
#         soup = BeautifulSoup(page.text, "html.parser")
#         if soup.find(class_="css-2je8ow"):
#             section_heading = soup.find(class_="css-2je8ow")
#             for t in section_heading.find_all(class_=["postStyles", "css-wzuydr", "e17g058b0"]):
#                 text += f'{t.text}\n'
#         elif soup.find(class_="bbc-fa0wmp"):
#             section_heading = soup.find(class_="bbc-fa0wmp")
#             for t in section_heading.find_all(class_=["bbc-d8piq7", "e17g058b0"]):
#                 text += f'{t.text}\n'
#         else:
#             text += 'Ошибка получения новости, попробуйте следующую'
#         self.index += 1
#         df = pd.DataFrame([[title, text, link]], columns=['title', 'text', 'link'])
#         return df, self.index - 1


class RTNewsParser:
    def __init__(self):
        self.url = 'https://russian.rt.com/news'
        self.data = {}
        self.df = pd.DataFrame(columns=['title', 'text', 'link'])
        self.get_titles_and_links()
        self.data_for_one_n = pd.DataFrame.from_dict(self.data.items())
        self.data_for_one_n.columns = ['title', 'link']
        self.amount_of_news = len(self.data_for_one_n)
        self.index = 0

    def get_main_news(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        section_heading = soup.find(class_="listing__rows listing__rows_all-news listing__rows_js")
        return section_heading

    def get_titles_and_links(self):
        section_heading = self.get_main_news()
        for n in section_heading.find_all(class_='card__heading_all-news'):
            self.data[n.text.strip()] = 'https://russian.rt.com' + n.find('a')['href']

    def get_text(self):
        print('Парсинг новостей с RT')
        for title, link in tqdm(self.data.items()):
            text = ''
            page = requests.get(link)
            soup = BeautifulSoup(page.text, "html.parser")

            if soup.find(class_='article__summary article__summary_article-page js-mediator-article'):
                section_sum = soup.find(class_='article__summary article__summary_article-page js-mediator-article')
                text += section_sum.text
            if soup.find(class_="article__text article__text_article-page js-mediator-article"):
                section_heading = soup.find(class_="article__text article__text_article-page js-mediator-article")
                text += section_heading.text

            else:
                continue
            df = pd.DataFrame([[title, text, link]], columns=['title', 'text', 'link'])
            self.df = pd.concat([self.df, df])
            sleep(3)
        self.df.reset_index(drop=True, inplace=True)

    def return_dataset(self):
        return self.df

    def get_one_news(self):
        if self.index >= self.amount_of_news:
            self.index -= self.amount_of_news
        title, link = self.data_for_one_n.loc[self.index]
        text = ''
        page = requests.get(link)
        soup = BeautifulSoup(page.text, "html.parser")
        if soup.find(class_='article__summary article__summary_article-page js-mediator-article'):
            section_sum = soup.find(class_='article__summary article__summary_article-page js-mediator-article')
            text += section_sum.text
        if soup.find(class_="article__text article__text_article-page js-mediator-article"):
            section_heading = soup.find(class_="article__text article__text_article-page js-mediator-article")
            text += section_heading.text
        else:
            text += 'Ошибка получения новости, попробуйте следующую'
        self.index += 1
        df = pd.DataFrame([[title, text, link]], columns=['title', 'text', 'link'])
        return df, self.index - 1


if __name__ == '__main__':
    parser = RTNewsParser()
    news, _ = parser.get_one_news()
    print(news['title'].values[0])
    print(news['text'].values[0])
    print(news['link'].values[0])
    print(news.index.values[0])
