from oled_crawler import OledCrawler
from oled_database import OledDatabase

result_data_list = []
award_data_list = []

oledCrawler = OledCrawler()
result_data_list, award_data_list = oledCrawler.crawl_pages()
oledDB = OledDatabase("127.0.0.1", "root", "", "trading")
oledDB.insert_eval_results(result_data_list)
oledDB.insert_tender_awards(award_data_list)
for result_data in result_data_list :
    if result_data['bidder'] :
        oledDB.insert_eval_results_bidders(result_data['bidder'])

