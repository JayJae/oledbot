from oled_crawler import OledCrawler
from oled_database import OledDatabase
from oled_bot import OledBot
import time
import json
import schedule
import csv
from datetime import datetime, timedelta
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from pympler.tracker import SummaryTracker
#Set up users for email

def send_email(file_name, message):
    gmail_user = 'yesty.chung@gmail.com'
    gmail_pwd = 'atiwrtq21!'
    gmail_recipients= ['yesty.chung@gmail.com', 'yesty.chung@nhqv.com']

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = ",".join(gmail_recipients)
    msg['Subject'] = "China Bidding {0}".format(time.strftime("%y/%m/%d"))

    msg.attach(MIMEText(message))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(file_name, 'rb').read())
    encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name)
    msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, gmail_recipients, msg.as_string())
    mailServer.close()


def convert_company(company) :
    if 'WONIK HOLDINGS' in company :
        return '원익 홀딩스'
    if 'ZEUS' in company :
        return '제우스'
    if 'DONG A ELTEK' in company or 'DONGAELTEK' in company:
        return '동아엘텍'
    if 'Advanced Process Systems' in company :
        return 'AP시스템'
    if 'SFA ENGINEERING' in company :
        return '에스에프에이'
    if 'Tera Semicon' in company or 'TeraSemicon' in company :
        return '테라세미콘'
    if 'AVACO' in company :
        return '아바코'
    if 'DMS' in company :
        return 'DMS'
    return company


def write_csv(oledDB, file_name) :
    tender_list = oledDB.select_all_tender_awards()
    with open(file_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['Project Name', 'Bidding NO', 'Bidding Content',
                        'Bidding Agency', 'Purchasers', 'Open-Time of Bids',
                        'Data of Evaluation Result', 'Data of Bidding Result',
                        'Final-Winner', 'Manufacturer', 'Manufacturer Country'])
        for tender in tender_list :
            writer.writerow([tender['name'], tender['no'], tender['content'].replace('\015', '').replace('^M', '').replace('\n', ''),
                            tender['agency'], tender['purchasers'], tender['open_time'],
                            tender['eval_result'], tender['bidding_result'],
                            tender['winner'], tender['manufacturer'], tender['country']])


def job() :
    tracker = SummaryTracker()
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
            #print(eval_results[purchaser][i]['bidders'])
        for tender_award in oledDB.select_tender_awards(purchaser, current_date) :
            if tender_awards.get(purchaser) is None :
                tender_awards[purchaser] = []
            tender_awards[purchaser].append(tender_award)

    #print(json.dumps(eval_results, indent=1))
    long_msg = "■ {0} China Bidding\n\n".format(time.strftime("%m/%d"))
    i = 1
    for key, value in eval_results.items() :
        korea_exists = False
        for eval_result in value :
            if eval_result['bidders'] is not None :
                if 'Korea' in eval_result['bidders']['country'] :
                    korea_exists = True
        if korea_exists :
            if 'Tianma' in key or 'TIANMA' in key:
                long_msg += """사전평가{0}\n업체: {1}\n평가 확정일: {2}\n생산업체/장비:\n"""\
                        .format(i, key, value[0]['ending_date'][:10])
            else :
                long_msg += """사전평가{0}\n내용: {1}\n업체: {2}\n평가 확정일: {3}\n생산업체/장비:\n"""\
                        .format(i, value[0]['name'],
                                key, value[0]['ending_date'][:10])
            i += 1
            j = 1
            for eval_result in value :
                if eval_result['bidders'] is not None :
                    if 'Korea' in eval_result['bidders']['country'] :
                        long_msg += """{0}. {1} / {2}\n""".format(j,
                                    convert_company(eval_result['bidders']['manufacturer']),
                                    eval_result['content'])
                        j += 1
            long_msg += "(총 {0}건 중 한국업체 {1}건)\n\n".format(len(value), j-1)

    i = 1
    for key, value in tender_awards.items() :
        korea_exists = False
        for tender_award in value :
            if 'Korea' in tender_award['country'] :
                korea_exists = True

        if korea_exists :
            if 'Tianma' in key or 'TIANMA' in key:
                long_msg += """수주확정{0}\n업체: {1}\n수주 확정일: {2}\n생산업체/장비:\n"""\
                        .format(i, key, value[0]['bidding_result'][:10])
            else :
                long_msg += """수주확정{0}\n내용: {1}\n업체: {2}\n수주 확정일: {3}\n생산업체/장비:\n"""\
                        .format(i, value[0]['name'],
                                key, value[0]['bidding_result'][:10])
            i += 1
            j = 1
            for tender_award in value :
                if 'Korea' in tender_award['country'] :
                    if tender_award['manufacturer'] == "-" or tender_award['manufacturer'] == "" :
                        tender_award['manufacturer'] = tender_award['winner']
                    long_msg += """{0}. {1} / {2}\n""".format(j,
                                convert_company(tender_award['manufacturer']),
                                tender_award['content'])
                    j += 1
            long_msg += "(총 {0}건 중 한국업체 {1}건)\n\n".format(len(value), j-1)


    file_name = "{0}_China Bidding_DB.csv".format(time.strftime("%y%m%d"))
    write_csv(oledDB, file_name)
    oledBot = OledBot()
    oledBot.get_users()

    msg_list = long_msg.split('\n')
    try:
        full_msg = ""
        full_msg_list = []

        for i, msg in enumerate(msg_list):
            full_msg += msg + '\n'
            if i == len(msg_list) - 1 :
                full_msg_list.append(full_msg)
                break

            if len(full_msg) > 4096 :
                full_msg = full_msg[:-(len(msg)+1)]
                full_msg_list.append(full_msg)
                full_msg = msg + '\n'

        for a in full_msg_list :
            oledBot.send_message(a)

        send_email(file_name, "\n".join(full_msg_list))
    except Exception as e:
        oledBot.send_message("Error Occured!\n" + str(e))
        send_email(file_name, str(e))

    del result_data_list[:]
    del result_data_list
    del award_data_list[:]
    del award_data_list
    del eval_results
    del tender_awards

    tracker.print_diff()

def is_2nd_or_4th_friday() :
    current_day = int(time.strftime("%w"))
    current_date = int(time.strftime("%d"))
    return current_day == 5 and (7 <= current_date < 14 or 21 <= current_date < 28)


if __name__ == "__main__" :
    if is_2nd_or_4th_friday() :
        schedule.every().day.at("16:30").do(job)
    else :
        schedule.every().day.at("17:30").do(job)


    while True :
        schedule.run_pending()
        time.sleep(60)

