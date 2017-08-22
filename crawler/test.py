from oled_crawler import OledCrawler

oledCrawler = OledCrawler()

result_data_list = []
award_data_list = []

if oledCrawler.search_oled_results(2) != True :
    print("Searching OLED Evalution Results Failed")
if oledCrawler.search_oled_awards(2) != True :
    print("Searching OLED Tener Awards Failed")
if oledCrawler.get_links_from_soup() != True :
    print("Get Links Failed")

if oledCrawler.get_data_from_links(result_data_list, award_data_list) != True :
    print("Get Data Failed")
else :
    print("Get Data Succeed")
