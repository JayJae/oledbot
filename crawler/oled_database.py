from database import Database
import pymysql
import unidecode
import json
class OledDatabase(Database) :
    def select_purchasers_from_eval_results(self) :
        sql = """select distinct PURCHASERS from EVAL_RESULTS"""
        purchasers = []
        with self.conn.cursor() as cur :
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows :
                purchasers.append(str(row[0]))

            return purchasers

    def insert_eval_result(self, eval_result) :
        sql = """insert into EVAL_RESULTS (PROJECT_NAME, BIDDING_NO,
                BIDDING_CONTENT, BIDDING_AGENCY, PURCHASERS, OPEN_TIME,
                ENDING_DATE) values (%s, %s, %s, %s, %s, %s, %s)"""
        with self.conn.cursor() as cur :
            cur.execute(sql, (eval_result['name'], eval_result['no'],
                        eval_result['content'], eval_result['agency'],
                        eval_result['purchasers'], eval_result['open_time'],
                        eval_result['ending_date']))

        self.conn.commit()

    def insert_eval_results(self, eval_results) :
        sql = """insert into EVAL_RESULTS (PROJECT_NAME, BIDDING_NO,
                BIDDING_CONTENT, BIDDING_AGENCY, PURCHASERS, OPEN_TIME,
                ENDING_DATE) values (%s, %s, %s, %s, %s, %s, %s)"""
        with self.conn.cursor() as cur :
            for eval_result in eval_results :
                print(eval_result['content'])
                try :
                    cur.execute(sql, (eval_result['name'], eval_result['no'],
                                eval_result['content'], eval_result['agency'],
                                eval_result['purchasers'], eval_result['open_time'],
                                eval_result['ending_date']))
                except pymysql.err.IntegrityError :
                    continue

        self.conn.commit()


    def select_eval_results(self, purchaser, date)  :
        sql = '''select * from EVAL_RESULTS where PURCHASERS="%s" and OPEN_TIME>="%s"''' % (purchaser, date)
        eval_results = []
        print(sql)
        with self.conn.cursor() as cur :
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows :
                eval_result = {}
                eval_result['name'] = row[0]
                eval_result['no'] = row[1]
                eval_result['content'] = row[2]
                eval_result['agency'] = row[3]
                eval_result['purchasers'] = row[4]
                eval_result['open_time'] = row[5]
                eval_result['ending_date'] = row[6]
                eval_results.append(eval_result)
        return eval_results

    def insert_eval_results_bidders(self, bidders) :
        sql = """insert into EVAL_RESULTS_BIDDER (RANK, BID_WINNER, MANUFACTURER,
                COUNTRY, BIDDING_NO) values (%s, %s, %s, %s, %s)"""

        with self.conn.cursor() as cur :
            for bidder in bidders :
                try :
                    print(bidder['manufacturer'])
                    cur.execute(sql, (bidder['rank'], bidder['winner'],
                                bidder['manufacturer'], bidder['country'],
                                bidder['no']))
                except UnicodeEncodeError :
                    try :
                        bidder['rank'] = bidder['rank'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        bidder['winner'] = bidder['winner'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        bidder['manufacturer'] = bidder['manufacturer'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        bidder['country'] = bidder['country'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        bidder['no'] = bidder['no'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        cur.execute(sql, (bidder['rank'], bidder['winner'],
                                    bidder['manufacturer'], bidder['country'],
                                    bidder['no']))
                    except pymysql.err.IntegrityError :
                        continue
                except pymysql.err.IntegrityError :
                    continue
        self.conn.commit()


    def select_eval_results_bidders(self, bidding_no) :
        sql = '''select * from EVAL_RESULTS_BIDDER
                where BIDDING_NO="%s"''' % (bidding_no)
        bidders = []
        with self.conn.cursor() as cur :
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows :
                bidder = {}
                bidder['rank'] = row[0]
                bidder['winner'] = row[1]
                bidder['manufacturer'] = row[2]
                bidder['country'] = row[3]
                bidder['no'] = row[4]
                bidders.append(bidder)

        return bidders

    def select_first_eval_results_bidder(self, bidding_no) :
        sql = '''select * from EVAL_RESULTS_BIDDER
                where BIDDING_NO="%s"''' % (bidding_no)
        bidder = {}
        with self.conn.cursor() as cur :
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows :
                print(row[0])
                if row[0] == 1 :
                    bidder['rank'] = row[0]
                    bidder['winner'] = row[1]
                    bidder['manufacturer'] = row[2]
                    bidder['country'] = row[3]
                    bidder['no'] = row[4]
                    return bidder

    def insert_tender_awards(self, tender_awards) :
        sql = """insert into TENDER_AWARDS (PROJECT_NAME, BIDDING_NO,
                BIDDING_CONTENT, BIDDING_AGENCY, PURCHASERS, OPEN_TIME,
                EVAL_RESULT_DATE, BIDDING_RESULT_DATE, FINAL_WINNER,
                MANUFACTURER, COUNTRY)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        with self.conn.cursor() as cur :
            for award in tender_awards :
                try :
                    print(json.dumps(award, indent=1))
                    cur.execute(sql, (award['name'], award['no'], award['content'],
                                award['agency'], award['purchasers'],
                                award['open_time'], award['eval_result'],
                                award['bidding_result'], award['winner'],
                                award['manufacturer'], award['country']))
                except UnicodeEncodeError :
                    try :
                        award['name'] = award['name'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        award['no'] = award['no'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '').replace('Bidding NO', '').strip()
                        award['content'] = award['content'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        award['agency'] = award['agency'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        award['purchasers'] = award['purchasers'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        award['winner'] = award['winner'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        award['manufacturer'] = award['manufacturer'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        award['country'] = award['country'].replace('\uff1f', '').replace('\uff1a', '').replace('\u3000', '')
                        """
                        award['name'] = unidecode.unidecode(award['name'])
                        award['content'] = unidecode.unidecode(award['content'])
                        award['purchasers'] = unidecode.unidecode(award['purchasers'])
                        award['winner'] = unidecode.unidecode(award['winner'])
                        award['manufacturer'] = unidecode.unidecode(award['manufacturer'])
                        """
                        cur.execute(sql, (award['name'], award['no'], award['content'],
                                    award['agency'], award['purchasers'],
                                    award['open_time'], award['eval_result'],
                                    award['bidding_result'], award['winner'],
                                    award['manufacturer'], award['country']))
                    except pymysql.err.IntegrityError :
                        continue

                except pymysql.err.IntegrityError :
                    continue
        self.conn.commit()

    def select_tender_awards(self, purchaser, date) :
        sql = '''select * from TENDER_AWARDS
                where PURCHASERS="%s" and BIDDING_RESULT_DATE>="%s"''' % (purchaser, date)
        tender_awards = []

        with self.conn.cursor() as cur :
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows :
                award = {}
                award['name'] = row[0]
                award['no'] = row[1]
                award['content'] = row[2]
                award['agency'] = row[3]
                award['purchasers'] = row[4]
                award['open_time'] = row[5]
                award['eval_result'] = row[6]
                award['bidding_result'] = row[7]
                award['winner'] = row[8]
                award['manufacturer'] = row[9]
                award['country'] = row[10]

                tender_awards.append(award)
        return tender_awards
