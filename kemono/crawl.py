
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from urllib import request, error

from time import sleep
from datetime import datetime




def log(*args):
    print(datetime.now().strftime('%H:%M:%S'), *args)


def find_all_article_urls(driver: WebDriver, artist_url, num_target=-1):
    log(f'start finding {"all" if num_target == -1 else num_target} articles from artist')
    start_article_idx = 0
    all_articles_url = []

    log('loading artist', artist_url)
    driver.get(artist_url)
    driver.implicitly_wait(5)
    sleep(3)

    paginator = driver.find_element_by_tag_name('main').find_element_by_tag_name('small')
    num_all_artist_articles = int(paginator.text.split()[-1])
    log(f'number of all articles of artist: {num_all_artist_articles}')
    print()

    while True:
        log(f'finding articles from {start_article_idx} ~')
        url_postfix = f'?o={start_article_idx}'
        tmp_artist_url = artist_url + url_postfix

        driver.get(tmp_artist_url)
        driver.implicitly_wait(5)
        sleep(3)
        log('page loaded')

        main = driver.find_element_by_tag_name('main')
        paginator_text = main.find_element_by_tag_name('small').text.split()
        page_start_idx, page_end_idx = int(paginator_text[1]), int(paginator_text[3])
        num_articles_in_page = page_end_idx - page_start_idx + 1
        log(f'number of articles in page: {num_articles_in_page}')

        articles = main.find_elements_by_tag_name('article')
        log(f'found {len(articles)}/{num_articles_in_page} articles in page')

        for article in articles:
            article_url = artist_url + f"/post/{article.get_attribute('data-id')}"
            all_articles_url.append(article_url)

            if 0 < num_target <= len(all_articles_url):
                log(f'collected desired number of {num_target} articles... stop\n')
                return all_articles_url


        if page_end_idx == num_all_artist_articles:
            log('reached last page... stop\n')
            break
        print()
        start_article_idx += 25

    log(f'number of collected article urls: {len(all_articles_url)}')
    log(f'found total {len(all_articles_url)}/{num_all_artist_articles} articles')

    return all_articles_url


def find_contents_in_article(driver: WebDriver, article_url):
    log('loading article', article_url)

    driver.get(article_url)
    driver.implicitly_wait(5)
    sleep(3)

    main = driver.find_element_by_tag_name('main')
    posts = main.find_elements_by_class_name('post__thumbnail')
    log(f'found {len(posts)} posts')

    post_url = []
    for post in posts:
        img_link = post.find_element_by_class_name('image-link')
        post_url.append(img_link.get_attribute('href'))
    log(f'collected {len(post_url)} post urls')
    print()

    return post_url


def collect_files_from_url(file_urls):
    pass


ops = Options()
# ops.add_argument('headless')
# ops.add_argument('--disable-gpu')
# ops.add_argument('lang=ko_KR')
# ops.add_argument('--disable-extensions')
capa = DesiredCapabilities.CHROME
capa['pageLoadStrategy'] = 'none'

target_artist_url = 'https://kemono.party/fanbox/user/59275588'
driver_path = '../chromedriver/chromedriver.exe'
save_path = ''

sample_article = 'https://kemono.party/fanbox/user/59275588/post/3847980'


if __name__ == '__main__':
    main_driver = webdriver.Chrome(driver_path, options=ops, desired_capabilities=capa)

    # article_urls = find_all_article_urls(main_driver, target_artist_url, 1)
    # for url in article_urls:
    #     find_contents_in_article(main_driver, url)

    image_urls = []
    find_contents_in_article(main_driver, sample_article)


