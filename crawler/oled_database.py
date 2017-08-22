from database import Database
import pymysql
import unidecode

class OledDatabase(Database) :

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
                    pass

        self.conn.commit()


    def select_all_eval_results(self, sqlwhere)  :
        sql = """select * from EVAL_RESULTS where""" +sqlwhere
        eval_results = []

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
                eval_result['ending_data'] = row[6]
                eval_results.append(eval_result)


    def insert_eval_results_bidders(self, bidders) :
        sql = """insert into EVAL_RESULTS_BIDDER (RANK, BID_WINNER, MANUFACTURER,
                COUNTRY, BIDDING_NO) values (%s, %s, %s, %s, %s)"""

        with self.conn.cursor() as cur :
            for bidder in bidders :
                try :
                    cur.execute(sql, (bidder['rank'], bidder['winner'],
                                bidder['manufacturer'], bidder['country'],
                                bidder['no']))
                except pymysql.err.IntegrityError :
                    pass
        self.conn.commit()


    def select_eval_results_bidders(self) :
        pass

    def insert_tender_awards(self, tender_awards) :
        sql = """insert into TENDER_AWARDS (PROJECT_NAME, BIDDING_NO,
                BIDDING_CONTENT, BIDDING_AGENCY, PURCHASERS, OPEN_TIME,
                EVAL_RESULT_DATE, BIDDING_RESULT_DATE, FINAL_WINNER,
                MANUFACTURER, COUNTRY)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        with self.conn.cursor() as cur :
            for award in tender_awards :
                try :
                    print(award['name'])
                    cur.execute(sql, (award['name'], award['no'], award['content'],
                                award['agency'], award['purchasers'],
                                award['open_time'], award['eval_result'],
                                award['bidding_result'], award['winner'],
                                award['manufacturer'], award['country']))
                except UnicodeEncodeError :
                    """
                    award['name'] = award['name'].replace('\uff1f', '')
                    award['content'] = award['content'].replace('\uff1f', '')
                    award['purchasers'] = award['purchasers'].replace('\uff1f', '')
                    award['winner'] = award['winner'].replace('\uff1f', '')
                    award['manufacturer'] = award['manufacturer'].replace('\uff1f', '')
                    """
                    award['name'] = unidecode.unidecode(award['name'])
                    award['content'] = unidecode.unidecode(award['content'])
                    award['purchasers'] = unidecode.unidecode(award['purchasers'])
                    award['winner'] = unidecode.unidecode(award['winner'])
                    award['manufacturer'] = unidecode.unidecode(award['manufacturer'])
                    cur.execute(sql, (award['name'], award['no'], award['content'],
                                award['agency'], award['purchasers'],
                                award['open_time'], award['eval_result'],
                                award['bidding_result'], award['winner'],
                                award['manufacturer'], award['country']))
                except pymysql.err.IntegrityError :
                    continue
        self.conn.commit()

    def select_tender_awards(self) :
        pass
