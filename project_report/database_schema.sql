CREATE TABLE stock_basic (
	code TEXT, 
	name TEXT, 
	ipo_date TEXT, 
	out_date TEXT, 
	type TEXT, 
	status TEXT
);
CREATE TABLE financial_profit (

    code TEXT,

    pub_date TEXT,

    stat_date TEXT,


    roe_avg REAL,

    np_margin REAL,

    gp_margin REAL,


    net_profit REAL,

    eps_ttm REAL,

    main_business_revenue REAL,


    total_share REAL,

    liqa_share REAL

);
CREATE TABLE dividend (

    code TEXT,

    regist_date TEXT,

    declare_date TEXT,

    pay_date TEXT,

    ex_date TEXT,


    cash_before_tax REAL,

    cash_after_tax REAL,


    bonus_share REAL,

    transfer_share REAL,


    dividend_info TEXT

);
CREATE TABLE download_log (

    code TEXT,

    data_type TEXT,

    status TEXT,

    message TEXT,

    update_time TEXT,

    PRIMARY KEY(code,data_type)

);
CREATE TABLE daily_price_qfq (

    date TEXT,

    open REAL,

    high REAL,

    low REAL,

    close REAL,

    volume INTEGER,

    amount REAL,

    code TEXT

);
CREATE TABLE daily_indicator (

    date TEXT,

    code TEXT,

    MA5 REAL,
    MA10 REAL,
    MA20 REAL,
    MA60 REAL,

    DIF REAL,
    DEA REAL,
    MACD REAL,

    RSI REAL,

    K REAL,
    D REAL,
    J REAL
);
CREATE UNIQUE INDEX idx_financial_profit_unique
ON financial_profit(code, stat_date);
CREATE UNIQUE INDEX idx_dividend_unique
ON dividend(code, ex_date)
;
CREATE UNIQUE INDEX idx_daily_qfq_unique
ON daily_price_qfq(code,date);
CREATE UNIQUE INDEX idx_indicator_unique
ON daily_indicator(code,date);
CREATE TABLE daily_price_raw (

    date TEXT,

    open REAL,

    high REAL,

    low REAL,

    close REAL,

    volume INTEGER,

    amount REAL,

    code TEXT

);
CREATE TABLE daily_price_hfq (

    date TEXT,

    open REAL,

    high REAL,

    low REAL,

    close REAL,

    volume INTEGER,

    amount REAL,

    code TEXT

);
CREATE TABLE financial_profit_normalized (

    code TEXT,

    stat_date TEXT,


    roe REAL,

    net_margin REAL,

    gross_margin REAL,


    net_profit REAL,

    eps REAL,

    revenue REAL,


    update_time TEXT

, pub_date TEXT);
CREATE UNIQUE INDEX idx_financial_profit_normalized_unique
ON financial_profit_normalized(code, stat_date)
;
CREATE TABLE financial_rank (

    code TEXT,

    stat_date TEXT,


    quality_score REAL,

    quality_rank INTEGER,


    roe_rank INTEGER,

    growth_rank INTEGER,


    update_time TEXT

);
CREATE UNIQUE INDEX idx_financial_rank_unique
ON financial_rank(code, stat_date)
;
CREATE TABLE financial_factor (

    code TEXT,

    stat_date TEXT,


    roe_score REAL,

    roe_clip REAL,


    net_margin REAL,

    gross_margin REAL,


    eps REAL,


    profit_growth REAL,

    revenue_growth REAL,


    growth_quality REAL,


    stability_score REAL,


    quality_score REAL,


    update_time TEXT

, pub_date TEXT);
CREATE UNIQUE INDEX idx_financial_factor_unique
ON financial_factor(code, stat_date);
CREATE TABLE valuation_factor (

        code TEXT,

        stat_date TEXT,

        close REAL,

        eps REAL,

        pe REAL,

        pe_rank REAL,

        valuation_score REAL,

        update_time TEXT

    , pub_date TEXT);
CREATE UNIQUE INDEX idx_valuation_factor_unique

    ON valuation_factor(code,stat_date);
CREATE TABLE technical_factor(

        code TEXT,

        date TEXT,


        close REAL,


        ma20 REAL,

        ma60 REAL,

        ma120 REAL,


        return20 REAL,

        return60 REAL,

        return120 REAL,


        volatility REAL,


        trend_score REAL,


        momentum_score REAL,


        technical_score REAL,


        update_time TEXT


    );
CREATE UNIQUE INDEX idx_technical_factor_unique

    ON technical_factor(code,date);
CREATE TABLE technical_rank(

        code TEXT,

        date TEXT,


        technical_score REAL,


        technical_rank INTEGER,


        update_time TEXT

    );
CREATE UNIQUE INDEX idx_technical_rank_unique

    ON technical_rank(code,date);
CREATE TABLE technical_quarter_factor (
	code TEXT, 
	stat_date DATETIME, 
	technical_score FLOAT
);
CREATE TABLE factor_score(

    code TEXT,

    stat_date TEXT,


    quality_score REAL,

    valuation_score REAL,

    technical_score REAL,


    final_score REAL,


    update_time TEXT

, pub_date TEXT);
CREATE UNIQUE INDEX idx_factor_score_unique

ON factor_score(code,stat_date);
CREATE TABLE stock_pool(

    code TEXT,

    stat_date TEXT,

    enable INTEGER,

    reason TEXT,

    update_time TEXT

, pub_date TEXT);
CREATE UNIQUE INDEX idx_stock_pool_unique

ON stock_pool(code,stat_date);
CREATE TABLE index_price
(
    code TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    amount REAL
);
