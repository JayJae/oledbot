create database OLED;
use OLED;

create table EVAL_RESUTLS(
    PROJECT_NAME varchar(512),
    BIDDING_NO varchar(32),
    BIDDING_CONTENT varchar(512),
    BIDDING_AGENCY varchar(256),
    PURCHASERS varchar(256),
    OPEN_TIME varchar(32),
    ENDING_DATE varchar(32),
    INSERT_DATE datetime DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (BIDDING_NO)
);

create table TENDER_AWARDS(
    PROJECT_NAME varchar(512),
    BIDDING_NO varchar(32),
    BIDDING_CONTENT varchar(512),
    BIDDING_AGENCY varchar(256),
    PURCHASERS varchar(256),
    OPEN_TIME varchar(32),
    EVAL_RESULT_DATE varchar(64),
    BIDDING_RESULT_DATE varchar(32),
    FINAL_WINNER varchar(256),
    MANUFACTURER varchar(256),
    INSERT_DATE datetime DEFAULT CURRENT_TIMESTAMP,
    COUNTRY varchar(64)
);

create table EVAL_RESULTS_BIDDER(
    RANK integer,
    BID_WINNER varchar(256),
    MANUFACTURER varchar(256),
    COUNTRY varchar(64),
    BIDDING_NO varchar(32),
    INSERT_DATE datetime DEFAULT CURRENT_TIMESTAMP
);
