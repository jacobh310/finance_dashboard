import yfinance as yf
import pandas as pd
import  numpy as np
import requests
from bs4 import BeautifulSoup as bs



# ticker = 'AAPL'

def get_metrics(ticker):
    stock = yf.Ticker(ticker)
    url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'


    valuation = pd.read_html(url)[0]
    income_statement = stock.financials
    cash_flow = stock.cashflow

    ## yearly metrics
    revenue = income_statement.loc['Total Revenue']
    gross_profit = income_statement.loc['Gross Profit']
    try: gross_margin =  gross_profit/revenue
    except: gross_margin = np.nan
    ebit = (income_statement.loc['Net Income From Continuing Ops'] + income_statement.loc['Income Tax Expense'] +(-1*income_statement.loc['Interest Expense']))
    ebitda = ebit + cash_flow.loc['Depreciation']
    try: ebitda_margin = ebitda/revenue
    except: ebitda_margin = np.nan
    fcf = cash_flow.loc['Total Cash From Operating Activities'] + cash_flow.loc['Capital Expenditures']
    try: ccr = fcf/ebitda
    except: ccr = np.nan
    icr = (ebitda + cash_flow.loc['Capital Expenditures'])/(-1*income_statement.loc['Interest Expense'])


    # quarterly metrics
    income_quarterly = stock.quarterly_financials
    cash_flow_quarterly = stock.quarterly_cashflow
    balance_sheet_quart = stock.quarterly_balance_sheet

    gross_quarterly = income_quarterly.loc['Gross Profit']
    revenue_quarterly = income_quarterly.loc['Total Revenue']
    try: gross_margin_quarterly = gross_quarterly/revenue_quarterly
    except: gross_margin_quarterly = np.nan
    ebit_quartely = (income_quarterly.loc['Net Income From Continuing Ops'] + income_quarterly.loc['Income Tax Expense'] +(-1*income_quarterly.loc['Interest Expense']))
    ebitda_quarterly = ebit_quartely + cash_flow_quarterly.loc['Depreciation']
    try:ebitda_margin_quarterly = ebitda_quarterly/revenue_quarterly
    except: ebitda_margin_quarterly = np.nan
    fcf_quarterly = cash_flow_quarterly.loc['Total Cash From Operating Activities'] + cash_flow_quarterly.loc['Capital Expenditures']
    try: ccr_quarterly = fcf_quarterly/ebitda_quarterly
    except: ccr_quarterly = np.nan
    icr_quarterly = (ebitda_quarterly + cash_flow_quarterly.loc['Capital Expenditures'])/(-1*income_quarterly.loc['Interest Expense'])
    current_ratio_quart = balance_sheet_quart.loc['Total Current Assets']/ balance_sheet_quart.loc['Total Current Liabilities']

    ev_quarterly = valuation.iloc[1,:].values[2:]
    ev_quarterly = np.array([float(i[:-1]) * 1000000000000 if i[-1].lower() == 't' else float(i[:-1]) * 1000000000  for i in ev_quarterly])
    try: ev_gross_quarterly = ev_quarterly/gross_quarterly
    except: ev_gross_quarterly = np.nan


    try: fcf_yield_quarterly = fcf_quarterly/ev_quarterly
    except: fcf_yield_quarterly = np.nan
    try:ev_revenue_quarterly = ev_quarterly/revenue_quarterly
    except: ev_revenue_quarterly = np.nan
    try: ev_ebitda_quarterly = ev_quarterly/ebitda_quarterly
    except: ev_ebitda_quarterly = np.nan
    try: ev_ebitda_capex_quart = ev_quarterly/(ebitda_quarterly + cash_flow_quarterly.loc['Capital Expenditures'])
    except: ev_ebitda_capex_quart = np.nan
    peg_quarterly = np.array([float(i) for i in valuation.iloc[4,2:].values])
    forward_pe_quart = np.array([float(i) for i in valuation.iloc[3,2:].values])


    mc_quarterly = valuation.iloc[0,:].values[2:]
    mc_quarterly = np.array([float(i[:-1]) * 1000000000000 if i[-1].lower() == 't' else float(i[:-1]) * 1000000000  for i in mc_quarterly])
    # p_rev_quarterly = mc_quarterly / revenue_quarterly
    # p_gross_quarterly = mc_quarterly/gross_quarterly
    # p_ebidta_quarterly = mc_quarterly/ebitda_quarterly
    p_book_quart = valuation.iloc[6,:].values[2:]

    yearly_metrics = pd.DataFrame({ 'Revenue':revenue,
                                   'Gross Margin':gross_margin,
                                   'EBITDA margin': ebitda_margin,
                                   'CCR':ccr,
                                   'ICR':icr})

    quarter_metrics =pd.DataFrame({'Revenue':revenue_quarterly,
                                   'Gross Margin':gross_margin_quarterly,
                                   'EBITDA margin':ebitda_margin_quarterly,
                                   'CCR':ccr_quarterly,
                                   'FCF yield' : fcf_yield_quarterly,
                                   'ICR': icr_quarterly,
                                   'Current ratio': current_ratio_quart,
                                   'EV/Revenue':ev_revenue_quarterly,
                                   'EV/Gross Profit': ev_gross_quarterly,
                                   'EV/EBITDA': ev_ebitda_quarterly,
                                   'EV/(EBITDA-CapEX)' : ev_ebitda_capex_quart,
                                   'Forward P/E': forward_pe_quart,
                                   'PEG': peg_quarterly,
                                   'Price/Book': p_book_quart})
                                   # 'Price/Revenue': p_rev_quarterly,
                                   # 'Price/Gross Profit': p_gross_quarterly
                                   # 'Price/EBITDA': p_ebidta_quarterly,
                                   # 'Forward P/E': forward_pe_quart})

    yearly_metrics = yearly_metrics.reset_index()
    yearly_metrics[''] = pd.to_datetime(yearly_metrics['']).dt.date
    yearly_metrics = yearly_metrics.set_index('')

    quarter_metrics = quarter_metrics.reset_index()
    quarter_metrics[''] = pd.to_datetime(quarter_metrics['']).dt.date
    quarter_metrics = quarter_metrics.set_index('')

    return  yearly_metrics, quarter_metrics


def get_summary(ticker):
    stock = yf.Ticker(ticker)
    overview = pd.Series(stock.info, name='Overview')

    summary = pd.Series({
            'Previous Close': overview['previousClose'],
            'Market Cap' : overview['marketCap'],
            'Enterprise Value': overview['enterpriseValue'],
            'EV/Revenue': overview['enterpriseToRevenue'],
            'EV/EBIDTA': overview['enterpriseToEbitda'],
            '52 week high': overview['fiftyTwoWeekHigh'],
            '52 week low': overview['fiftyTwoWeekLow']},
        name='Overview')

    return summary

# summary = get_summary(ticker)

def get_reccomendations(ticker):
    stock = yf.Ticker(ticker)
    recomends = stock.recommendations
    recomends =recomends['To Grade'].value_counts()

    return recomends

# rec = get_reccomendations(ticker)

