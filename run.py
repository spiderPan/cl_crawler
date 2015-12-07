from bs4 import BeautifulSoup
import urllib2
import os.path
import re


HOME_URL = 'http://t66y.com/thread0806.php?fid=16'
REQUEST_HEADERS = {
"Accept-Language": "en-US,en;q=0.5",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
"Referer": "http://thewebsite.com",
"Connection": "keep-alive" 
}

def read_html_content(html_url):
    request = urllib2.Request(html_url, headers=REQUEST_HEADERS)
    contents = urllib2.urlopen(request).read()
    soup = BeautifulSoup(contents, "html5lib")
    return soup

def download_file(url, folder='test'):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = url.split('/')[-1]
    complete_filename = os.path.join(folder,filename)
    try:
        u = urllib2.urlopen(url)
        req = urllib2.Request(url, headers=REQUEST_HEADERS)
        handle = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'We failed with error code - %s.' % e.code
        return False
    
    data = handle.read()

    with open(complete_filename, 'wb') as f:
        f.write(data)
        print 'success'
		
    return True
	
def get_article_list():
    article_list = []
    content = read_html_content(HOME_URL)
    for title in content.find_all(href=re.compile('htm_data')):
        if title.string.find('P]') == -1:
           continue
        comments = title.parent.parent.next_sibling.next_sibling.next_sibling.next_sibling.string
        if int(comments) <= 30:
           continue
        article_list.append('http://t66y.com/'+title.get('href'))
    
    return article_list

def run():
    article_list = get_article_list()
    for article in article_list:
        print article
        content = read_html_content(article)
        folder_name = content.title.string
        for link in content.find_all(type='image'):
            image_url = link.get('src')
            try:
                download_file(image_url,folder_name)
            except Exception:
                print 'failed in '+image_url
                continue
                pass

            print image_url

run()