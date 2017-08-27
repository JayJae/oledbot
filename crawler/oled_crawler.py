from base_crawler import BaseCrawler
import requests
from bs4 import BeautifulSoup
import json

class OledCrawler(BaseCrawler) :
    key_word_dict = {'CSOT' : (1, 4), 'BOE' : (6, 11), 'Tianma' : (1, 3),
                     'Optoelectronics' : (5, 19), 'CEC' : (3, 8),
                     'Optronics' : (1, 1), 'Yungu' : (1, 3), 'Royole' : (1, 4)}
    new_key_word_dict = {'CSOT' : (2, 3), 'BOE' : (2, 3), 'Tianma' : (2, 3),
                     'Optoelectronics' : (2, 3), 'CEC' : (2, 3),
                     'Optronics' : (2, 3), 'Yungu' : (2, 3), 'Royole' : (2, 3)}
    results_soup_list = []
    awards_soup_list = []
    result_link_list = []
    award_link_list = []
    result_data_list = []
    award_data_list = []

    def __init__(self) :
        self.url = "http://www.chinabidding.com/en/info/search.htm"

    def crawl_new_pages(self) :
        for key, value in self.new_key_word_dict.items() :
            self.search_oled_results(key, value[0])
            self.search_oled_awards(key, value[1])
            self.get_links_from_soup()
            self.results_soup_list = []
            self.awards_soup_list = []
        return self.get_data_from_links()

    def crawl_pages(self) :
        for key, value in self.key_word_dict.items() :
            self.search_oled_results(key, value[0])
            self.search_oled_awards(key, value[1])
            self.get_links_from_soup()
            self.results_soup_list = []
            self.awards_soup_list = []
        return self.get_data_from_links()

    def search_oled_results(self, key_word, last_page) :
        for page_num in range(1, last_page+1) :
            with requests.Session() as s:
                res = s.post(self.url, data={'fullText' : key_word, 'infoClassCodes' : 'e0907', 'currentPage' : str(page_num)})
                if res.status_code != 200 :
                    return False
                else :
                    html = res.text
                    self.results_soup_list.append(BeautifulSoup(html, 'lxml'))
        return True

    def search_oled_awards(self, key_word, last_page) :
        for page_num in range(1, last_page+1) :
            print(page_num, last_page)
            with requests.Session() as s:
                res = s.post(self.url, data={'fullText' : key_word, 'infoClassCodes' : 'e0908', 'currentPage' : str(page_num)})
                if res.status_code != 200 :
                    print("FALSE!, status : %d" % res.ststus_code);
                    return False
                else :
                    html = res.text
                    self.awards_soup_list.append(BeautifulSoup(html, 'lxml'))
        print(self.awards_soup_list)
        return True

    def get_links_from_soup(self) :
        if len(self.results_soup_list) == 0 or len(self.awards_soup_list) == 0:
            return False
        else :
            for results_soup in self.results_soup_list :
                list_items = results_soup.find_all("li", class_="list-item")
                for list_item in list_items :
                    result_title = list_item.find("a", class_="item-title-text")
                    result_time = list_item.find("span", class_="item-title-data").get_text().strip()#.split(":", 1)[1]
                    print(result_time)
                    if result_time < "Time：2017-07-01" :
                        break
                    self.result_link_list.append(str(result_title.get('href')))
            for awards_soup in self.awards_soup_list :
                list_items = awards_soup.find_all("li", class_="list-item")
                for list_item in list_items :
                    award_title = list_item.find("a", class_="item-title-text")
                    award_time = list_item.find("span", class_="item-title-data").get_text().strip()#.split(":", 1)[1]
                    if award_time < "Time：2017-07-01" :
                        break
                    self.award_link_list.append(str(award_title.get('href')))

                print(self.award_link_list)
            return True


    def get_data_from_links(self) :
        result_data_list = []
        award_data_list = []
        self.__get_data_from_links(self.result_link_list, result_data_list)
        self.__get_data_from_links(self.award_link_list, award_data_list)
        return (result_data_list, award_data_list)

    def __get_data_from_links(self, link_list, data_list) :
        for link in link_list :
            res = requests.get(link)
            soup = BeautifulSoup(res.text, 'lxml')
            for br in soup.find_all("br") :
                br.replace_with("||")
            raw_data = soup.find("div", class_="main-info")
            data_list.append(self.__refine_data(raw_data))

    def __refine_data(self, raw_data) :
        refined_data = {}
        temp_data = [data for data in raw_data.get_text().split("||") if data]
        refined_data['name'] = self.__prettify(temp_data[0])
        refined_data['no'] = self.__prettify(temp_data[1])
        refined_data['content'] = self.__prettify(temp_data[2])
        refined_data['agency'] = self.__prettify(temp_data[3])
        refined_data['purchasers'] = self.__prettify(temp_data[4])
        refined_data['open_time'] = temp_data[5].strip().split(":", 1)[1]

        if raw_data.find("tr") is not None or "No Proposed Bidder-Winner" in temp_data[7] :
            refined_data['ending_date'] = temp_data[6].strip().split(":", 1)[1]

            bidder_list = []
            trs = raw_data.find_all("tr")
            for tr in trs[1:] :
                bidder = {}
                tds = tr.find_all("td")
                bidder['rank'] = tds[0].get_text()
                bidder['winner'] = tds[1].get_text()
                bidder['manufacturer'] = tds[2].get_text()
                bidder['country'] = tds[3].get_text()
                bidder['no'] = refined_data['no']
                bidder_list.append(bidder)
            refined_data['bidder'] = bidder_list

        else :
            refined_data['eval_result'] = temp_data[6].strip().split(":", 1)[1]
            refined_data['bidding_result'] = temp_data[7].strip().split(":", 1)[1]
            refined_data['winner'] = self.__prettify(temp_data[8])
            refined_data['manufacturer'] = self.__prettify(temp_data[9])
            refined_data['country'] = self.__prettify(temp_data[10])

        print (json.dumps(refined_data, indent=1))
        return refined_data

    def __prettify(self, text) :
        return text.strip().split(":")[-1]
