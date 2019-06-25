import requests
import sys
import os
import json
import time
import re
import shutil
from bs4 import BeautifulSoup


class GossipingParker(object):

    pttUrl = 'https://www.ptt.cc'
    pttGossipSearchUrl = pttUrl + "/bbs/Gossiping/search"

    def __init__(self):
        self.keyword = ""
        self.articleCounter = 0
        self.villagerCouter = {}

    def parseArticle(self, articleText):
        bs = BeautifulSoup(articleText, 'html.parser')
        content = bs.find(id="main-content")
        metas = content.select('div.article-metaline')
        villagers = []
        if metas and metas[0].select('span.article-meta-value')[0]:
            author = metas[0].select('span.article-meta-value')[0].string
            if author is None:
                return None
            villagers.append(author.split()[0])
        pushes = content.find_all('div', class_='push')
        for push in pushes:
            if not push.find('span', 'push-tag'):
                continue
            accid = push.find('span', 'push-userid').string.strip(' \t\n\r')
            if accid not in villagers :
                villagers.append(accid)

        return villagers

    def crawlArticle(self, link):
        print("Crawl Article : " + link)
        resp = requests.get(url=link, cookies={'over18': '1'}, verify=True, timeout=3)
        if resp.status_code != 200:
            print('invalid url:', resp.url)
            return None
        return self.parseArticle(resp.text)
        
    def countPeople(self, villagers):
        for villager in villagers:
            num = self.villagerCouter.get(villager)
            if num is None:
                self.villagerCouter[villager] = 1
            else:
                num = num + 1
                self.villagerCouter[villager] = num

    def search(self, keyword, pageNums):
        print("Search {0} at Ptt Gossiping Board".format(keyword))
        self.keyword = keyword
        self.articleCounter = 0
        self.villagerCouter = {}
        for page in range(1, pageNums + 1):
            if not self.searchBoard(keyword, page):
                break
        self.exportResult()

    def searchBoard(self, keyword, pageNum=1):
        resp = requests.get(url = self.pttGossipSearchUrl, params={'q': keyword, 'page': pageNum}, cookies={'over18': '1'}, verify=True, timeout=3)
        if resp.status_code != 200:
            print('invalid url:', resp.url)
            return False
        bs = BeautifulSoup(resp.text, 'html.parser')
        rows = bs.find_all("div", "r-ent")
        for row in rows:
            href = row.find('a')['href']
            link = self.pttUrl + href
            villagers = self.crawlArticle(link)
            if villagers is not None:
                self.articleCounter = self.articleCounter + 1
                self.countPeople(villagers)

        return True

    def exportResult(self):
        folderName = "gossip_" + keyword + "_" + time.strftime("%Y-%m-%d %H.%M.%S", time.localtime())
        folderName = re.sub("[\\/:*?\"<>|]+", "x", folderName)
        folderPath = os.path.join(".", folderName)
        if not os.path.exists(folderPath) :
            os.mkdir(folderPath)

        exportData = {}
        exportData['keyword'] = self.keyword
        exportData['total'] = self.articleCounter
        exportData['villagers'] = self.villagerCouter
        filename = os.path.join(folderPath, "data.js")
        with open(filename, 'w') as outfile:  
            outfile.write("var metadata = ")
            outfile.write(json.dumps(exportData))

        # copy index.html
        srcViewer = os.path.join(".", "viewer.html")
        dstIndex = os.path.join(folderPath, "index.html")
        shutil.copy(srcViewer, dstIndex)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("invalid argument")
    else:
        keyword = sys.argv[1]
        parker = GossipingParker()
        parker.search(keyword, 10) # search 10 page, 1 page has 20 articles    


