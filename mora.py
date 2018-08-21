import requests,json
from lxml import etree

class Mora:
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }

    def __init__(self):
        pass

    @classmethod
    def get(cls):
        headers = cls.headers
        url = 'http://mora.jp/special/anime/'
        res = requests.get(url,headers=headers)
        content = res.content.decode()
        
        html = etree.HTML(content)
        groups = html.xpath("//div[@class='mainContestsA']")
        result = {}
        for group in groups:
            title = group.xpath(".//h2/span/text()")
            title_groups = []
            for i in range(len(title)):
                try:
                    title_groups.append([title[i],title[i+1]])
                except:
                    title_groups.append([title[i]])

            divs = {}

            for title_group in title_groups:
                if len(title_group)==1:
                    rule = './/div[contains(@class,"partsA")][preceding-sibling::h2/span[text()="{}"]/..]'.format(title_group[0])
                else:
                    rule = './/div[contains(@class,"partsA")][preceding-sibling::h2/span[text()="{}"]/..][following-sibling::h2/span[text()="{}"]/..]'.format(title_group[0],title_group[1])

                divs[title_group[0]] = group.xpath(rule)


            for name,item in divs.items():
                song_list = []
                for song in item:
                    song_type = song.xpath('.//div/span/text()')[0]
                    song_title = song.xpath('.//div/p[@class="partsATitle"]/text()')[0]
                    song_artist = song.xpath('.//div/p[@class="partsAArtist"]/text()')[0]
                    song_list.append({'title':song_title,'type':song_type,'artist':song_artist})
                result[name] = song_list
        
        return result
            

if __name__ == "__main__":
    res = Mora.get()
    with open('songs.json','w',encoding='utf8') as f:
        f.write(json.dumps(res,ensure_ascii=False))