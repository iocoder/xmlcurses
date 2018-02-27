DROP TABLE IF EXISTS PERIOD;
DROP TABLE IF EXISTS TRANSACT;

CREATE TABLE PERIOD (
    ID                INT                       NOT NULL AUTO_INCREMENT,
    FIRSTDAY          DATE                      NOT NULL               ,
    LASTDAY           DATE                      NOT NULL               ,
    PRIMARY KEY(ID)
);

CREATE TABLE TRANSACT(
    ID                INT                       NOT NULL AUTO_INCREMENT,
    DAY               DATE                      NOT NULL               ,
    NAME              VARCHAR(255)              NOT NULL               ,
    CARD              ENUM('DEBIT', 'CREDIT')   NOT NULL               ,
    AMNT              INT                       NOT NULL               ,
    PRIMARY KEY(ID)
);

