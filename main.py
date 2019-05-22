from bs4 import BeautifulSoup
from datetime import datetime
from os import makedirs
from os.path import exists
from requests import get


class Page():

    def __init__(self, url):
        self.url = url
        self.soup_init()

    def soup_init(self):
        response = get(self.url, headers={'User-Agent': 'Mozilla/5.0 (Windows N\
                                T 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, l\
                                ike Gecko) Chrome/73.0.3683.86 Safari/537.36'})
        if response.ok:
            self.soup = BeautifulSoup(response.text, 'lxml')

    def content_init(self):
        if self.soup == None:
            return
        headline = self.soup.find('div', {'class': 'headline'})
        self.title = headline.h1.string
        self.tag = '---\ntitle: 知乎日报|$t$\ndate: $d$\ntags: [知乎日报]\n---\n'
        self.tag = self.tag.replace('$t$', self.title)
        self.tag = self.tag.replace('$d$', str(datetime.now()))
        self.image = '![](' + headline.img.attrs['src'] + ')'
        self.answers = self.soup.find_all('div', {'class': 'answer'})
        self.path = 'zhihu-daily/知乎日报' + self.title.replace('/', '') + '.md'
        try:
            self.image_source = headline.span.string
        except:
            self.image_source = None

    def write(self):
        if self.soup == None:
            return
        print('[Info] ' + self.url + ': ' + self.title + ' printing now.')
        try:
            with open(self.path, 'w', encoding='utf-8') as text:
                text.write(self.tag)
                text.write('# ' + self.title + '\n')
                text.write(self.image + '\n')
                if self.image_source:
                    text.write('> ' + self.image_source + '\n')
                for answer in self.answers:
                    text.write(str(answer) + '\n<hr>\n')
        except:
            self.error_report()

    def error_report(self):
        print('[Error] An error happened when printing.')
        print('[Error] Please contact the administrator.')


path = 'zhihu-daily/'
if not exists(path):
    makedirs(path)

main = 'https://daily.zhihu.com'
divs = Page(main).soup.find_all('div', {'class': 'box'})
for div in divs:
    page = Page(main + div.a.attrs['href'])
    page.content_init()
    page.write()
