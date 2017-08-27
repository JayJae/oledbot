from oled_crawler import OledCrawler
from oled_database import OledDatabase
from oled_bot import OledBot
import time
import json
import schedule

def job() :
    oledCrawler = OledCrawler()
    oledDB = OledDatabase("127.0.0.1", "root", "", "trading")

    purchasers = oledDB.select_purchasers_from_eval_results()
    print(purchasers)
    eval_results = {}
    tender_awards = {}

    for purchaser in purchasers :
        for i, eval_result in enumerate(oledDB.select_eval_results(purchaser, "2017-08-23")) :
            if eval_results.get(purchaser) is None :
                eval_results[purchaser] = []
            eval_results[purchaser].append(eval_result)
            eval_results[purchaser][i]['bidders'] = oledDB.select_first_eval_results_bidder(eval_result['no'])
            print(eval_results[purchaser][i]['bidders'])
        for tender_award in oledDB.select_tender_awards(purchaser, "2017-08-23") :
            if tender_awards.get(purchaser) is None :
                tender_awards[purchaser] = []
            tender_awards[purchaser].append(tender_award)

    print(json.dumps(eval_results, indent=1))
    msg = ""
    for i, (key, value) in enumerate(eval_results.items()) :
        msg += """사전평가{0}\n내용 : {1}\n업체 : {2}\n평가 확정일 : {3}\n생산업체/장비 :\n"""\
                .format(i+1, value[0]['name'],
                        key, value[0]['ending_date'])
        for j, eval_result in enumerate(value) :
            msg += """{0}. {1}({2}) / {3}\n""".format(j+1,
                        eval_result['bidders']['manufacturer'],
                        eval_result['bidders']['country'],
                        eval_result['content'])
        msg += "\n"

    for i, (key, value) in enumerate(tender_awards.items()) :
        msg += """수주확정{0}\n내용 : {1}\n업체 : {2}\n수주 확정일 : {3}\n생산업체/장비 :\n"""\
                .format(i+1, value[0]['name'],
                        key, value[0]['bidding_result'])
        for j, tender_award in enumerate(value) :
            msg += """{0}. {1}({2}) / {3}\n""".format(j+1,
                        tender_award['manufacturer'],
                        tender_award['country'],
                        tender_award['content'])
        msg += "\n"

    print(msg)
    oledBot = OledBot()
    oledBot.get_users()
    try:
        oledBot.send_message(msg)
    except err :
        oledBot.send_message("Error Occured!\n Error : " + err )


if __name__ == "__main__" :
    current_date = time.strftime("%Y-%m-%d")
    current_day= time.strftime("%w")
    print(current_date)
    print(current_day)
    schedule.every().day.at("14:54").do(job)

    while True :
        #if current_day != 6 and current_day != 0 :
        schedule.run_pending()
        time.sleep(60)

