from oled_crawler import OledCrawler
from oled_database import OledDatabase
from oled_bot import OledBot
import time
import json
import schedule
from datetime import datetime, timedelta

def job() :
    print(1)
    result_data_list = []
    award_data_list = []

    oledCrawler = OledCrawler()
    result_data_list, award_data_list = oledCrawler.crawl_new_pages()
    oledDB = OledDatabase("127.0.0.1", "root", "gold2451", "OLED")
    oledDB.insert_eval_results(result_data_list)
    oledDB.insert_tender_awards(award_data_list)
    for result_data in result_data_list :
        if result_data['bidder'] :
            oledDB.insert_eval_results_bidders(result_data['bidder'])

    purchasers = oledDB.select_purchasers_from_eval_results()
    eval_results = {}
    tender_awards = {}

    current_date = time.strftime("%Y-%m-%d")

    for purchaser in purchasers :
        for i, eval_result in enumerate(oledDB.select_eval_results(purchaser, current_date)) :
            if eval_results.get(purchaser) is None :
                eval_results[purchaser] = []
            eval_results[purchaser].append(eval_result)
            eval_results[purchaser][i]['bidders'] = oledDB.select_first_eval_results_bidder(eval_result['no'])
        for tender_award in oledDB.select_tender_awards(purchaser, current_date) :
            if tender_awards.get(purchaser) is None :
                tender_awards[purchaser] = []
            tender_awards[purchaser].append(tender_award)

    long_msg = ""
    for i, (key, value) in enumerate(eval_results.items()) :
        long_msg += """사전평가{0}\n내용 : {1}\n업체 : {2}\n평가 확정일 : {3}\n생산업체/장비 :\n"""\
                .format(i+1, value[0]['name'],
                        key, value[0]['ending_date'])
        for j, eval_result in enumerate(value) :
            if eval_result['bidders'] is not None :
                long_msg += """{0}. {1}({2}) / {3}\n""".format(j+1,
                            eval_result['bidders']['manufacturer'],
                            eval_result['bidders']['country'],
                            eval_result['content'])
        long_msg += "\n"

    for i, (key, value) in enumerate(tender_awards.items()) :
        long_msg += """수주확정{0}\n내용 : {1}\n업체 : {2}\n수주 확정일 : {3}\n생산업체/장비 :\n"""\
                .format(i+1, value[0]['name'],
                        key, value[0]['bidding_result'])
        for j, tender_award in enumerate(value) :
            long_msg += """{0}. {1}({2}) / {3}\n""".format(j+1,
                        tender_award['manufacturer'],
                        tender_award['country'],
                        tender_award['content'])
        long_msg += "\n"

    print("MSG : " + long_msg)
    oledBot = OledBot()
    oledBot.get_users()

    msg_list = long_msg.split('\n')
    try:
        full_msg = ""
        full_msg_list = []

        for i, msg in enumerate(msg_list):
            full_msg += msg + '\n'
            if len(full_msg) > 4096 :
                full_msg = full_msg[:-(len(msg)+1)]
                full_msg_list.append(full_msg)
                full_msg = msg + '\n'
            if i == len(msg_list) - 1 :
                full_msg_list.append(full_msg)

        print(full_msg_list)
        for a in full_msg_list :
            oledBot.send_message(a)
    except Exception as e:
        oledBot.send_message("Error Occured!\n" + str(e))


if __name__ == "__main__" :
    current_date = time.strftime("%Y-%m-%d")
    current_day= time.strftime("%w")
    schedule.every().day.at("14:52").do(job)
    while True :
        schedule.run_pending()

