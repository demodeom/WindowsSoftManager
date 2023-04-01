import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class UpdateInfo:
    def __init__(self, update_date, update_version, update_download_url, update_content, soft_package_name):
        self.update_date = update_date
        self.update_version = update_version
        self.update_download_url = update_download_url
        self.update_content = update_content
        self.soft_package_name = soft_package_name

    def __repr__(self):
        str_update_info = '\n'
        str_update_info += '-------------{}----------------\n'.format(self.soft_package_name)
        str_update_info += '更新时间：{}\n'.format(self.update_date)
        str_update_info += '更新版本：{}\n'.format(self.update_version)
        str_update_info += '更新内容：\n'
        for c in self.update_content:
            str_update_info += "\t{}\n".format(c)
        str_update_info += '下载地址：{}\n'.format(self.update_download_url)
        str_update_info += ''
        return str_update_info


def QQ():
    soft_package_name = "腾讯QQ"
    qq_download_page_url = "https://im.qq.com/pcqq"
    res = requests.get(qq_download_page_url)
    response_test = res.text
    soup = BeautifulSoup(response_test, 'html5lib')

    desc_version_soup = soup.find('span', class_='desc-version')
    desc_date_soup = soup.find('span', class_='desc-date')
    download_soup = soup.find('a', class_='download')
    features_soup = soup.find('ul', class_='features')

    update_date = desc_version_soup.text.replace('QQ Windows版 ', '').strip()
    update_version = desc_date_soup.text.replace('发布时间：', '').strip()
    update_download_url = download_soup['href']
    update_content = []
    for li in features_soup.find_all('li'):
        update_content.append(li.text.strip())

    return UpdateInfo(update_date, update_version, update_download_url, update_content, soft_package_name)


def we_chat():
    """
    微信更新日志
    1. 先获取最新版本的日志连接
    2. 再获取日志最新详情
    """
    # 1.先获取最新版本的日志连接
    soft_package_name = "微信"
    qq_download_page_url = "https://weixin.qq.com/cgi-bin/readtemplate?lang=zh_CN&t=weixin_faq_list&head=true"
    res = requests.get(qq_download_page_url)
    response_test = res.text
    soup = BeautifulSoup(response_test, 'html5lib')

    new_version_href = soup.find('h3', class_='faq_section_title', string="Windows平台") \
        .find_next_sibling('ul') \
        .find('li') \
        .find('a')['href']

    new_version_url = urljoin(res.url, new_version_href)

    # 2.再获取日志最新详情
    res = requests.get(new_version_url)
    response_test = res.text
    soup = BeautifulSoup(response_test, 'html5lib')

    desc_date_soup = soup.find('div', 'content') \
        .find('p')
    update_date = desc_date_soup.text.replace('发布日期：', '').strip()

    desc_version_soup = soup.find('div', id='page_top').find('p')

    update_version = desc_version_soup.text \
        .replace('发布版本： 微信 ', '') \
        .replace('for Windows', '') \
        .replace('下载最新版本', '') \
        .strip()

    # 微信最新版下载地址是固定的
    update_download_url = "https://dldir1.qq.com/weixin/Windows/WeChatSetup.exe"

    update_content = []
    for h4 in soup.find(id='page_center').find_all('h4'):
        update_content.append(h4.text.strip())

    return UpdateInfo(update_date, update_version, update_download_url, update_content, soft_package_name)


if __name__ == '__main__':
    # qq_update_info = QQ()
    # print(qq_update_info)

    we_chat_update_info = we_chat()
    print(we_chat_update_info)
