import datetime, re, requests, os
from bs4 import BeautifulSoup

def get_one_page(url):
    # 获取单个页面的信息
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    if response.ok:
        return response

def get_urls():
    # 获取知乎日报每篇文章的url
    main_url = 'https://daily.zhihu.com'
    response = get_one_page(main_url)
    urls = re.findall('"box".*?href="(.*?)".*?"link-button"', response.text)
    for iter in range(0, len(urls)):
        urls[iter] = main_url + urls[iter]
    return urls

def write_one_page(url):
    # 将单篇文章写入文件
    soup = BeautifulSoup(get_one_page(url).text, 'lxml')
    title = soup.find(name='title').string.replace('\r\n', '')
    print('- ' + url + ': ' + title)
    
    # 创建文件夹
    path = 'zhihu-daily/' + str(datetime.date.today())
    if not os.path.exists(path):
        os.makedirs(path)
    path = path + '/' + title + '.md'
    
    # 有时候会有奇妙的FNFE报错
    try:
        with open(path, 'w', encoding='UTF-8') as file:
            file.write(str(soup.find(name='h1', attrs={'class':'headline-title'})))
            file.write(str(soup.select('.headline')[0].select('img')[0]) + '\n')
            if len(soup.select('.headline')[0].select('span')):
                file.write('>' + soup.select('.headline')[0].select('span')[0].string + '\n')
            file.write(str(soup.find(name='div', attrs={'class':'content'})))
    except FileNotFoundError:
        pass

for url in get_urls():
    write_one_page(url)
