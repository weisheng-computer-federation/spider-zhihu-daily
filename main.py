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
    path = 'zhihu-daily/'
    if not os.path.exists(path):
        os.makedirs(path)
    path = path + '/' + title.replace('/','') + '.md'
    
    try:
        headline = soup.find(name='div', attrs={'class':'headline'})
        title = '# ' + headline.find(name='h1').string
        image = str(headline.find(name='img'))
        image_source = '>' + headline.find(name='span').string
        answers = soup.find_all(name='div', attrs={'answer'})
        with open(path, 'w', encoding='UTF-8') as file:
            file.write('---\ntitle: $=-titel-=$\ndate: $=-date-=$\ntags: [知乎日报]\n---\n'.replace('$=-titel-=$', title).replace('$=-date-=$', str(datetime.datetime.now())))
            file.write(title + '\n')
            file.write(image + '\n')
            if image_source != None:
                file.write(image_source + '\n')
            for answer in answers:
                file.write(str(answer) + '\n')
    except:
        pass

for url in get_urls():
    write_one_page(url)
