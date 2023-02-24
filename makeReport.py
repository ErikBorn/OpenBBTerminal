from multiprocessing.connection import wait
from openbb_terminal import api as openbb
from openbb_terminal.stocks.fundamental_analysis import av_model
import pandas as pd
import time

def clean_numbers(dataframe):
    for column in dataframe.columns:
        if column != 'Reported Currency' and column != "reportedCurrency":
            dataframe[column] = dataframe[column].replace({"None": 0,"K":"*1e3", "M":"*1e6", "B":"*1e9", "T":"*1e9"}, regex=True).map(pd.eval).astype(int)

#These are the export parameters
stock_list = ["aapl","bird","AXP","ETSY","IDXX","NVDA","TGT","DIS","YETI"] #Portfolio: ["aapl","bird","AXP","ETSY","IDXX","NVDA","TGT","DIS","YETI"] #Every stock you want data on!
num = 15            #Seems to limit to five anyway...
quarterly = False 

for exportTicker in stock_list:
    #This uses five separate API calls to get the information into DataFrames -- max use of one (set of five) per minute
    df_overview = av_model.get_overview(exportTicker)
    df_cash = av_model.get_cash_flow(exportTicker,num,quarterly)
    df_income = av_model.get_income_statements(exportTicker,num,quarterly)
    df_balance = av_model.get_balance_sheet(exportTicker,num,quarterly)
    df_earnings = av_model.get_earnings(exportTicker,quarterly)
    time.sleep(60)

    #Transposes dataframes to match export target format
    df_cash = df_cash.transpose()
    df_income = df_income.transpose()
    df_balance = df_balance.transpose() 
    df_earnings = df_earnings.transpose()

    #Fixes earnings format (writes in column titles)
    df_earnings.columns = df_earnings.iloc[0]
    df_earnings = df_earnings.drop(df_earnings.index[0])
    # if quarterly:
    #     df_earnings = df_earnings.drop(df_earnings.index[0])

    #This converts all the strings into numbers inside the dataframes -- a little clunky but seems to work
    df_list = [df_cash,df_income,df_balance,df_earnings]
    for data in df_list:
        clean_numbers(data)
    
    ###Creates and calculates the df_metrics dataframe
    df_metrics = pd.DataFrame() #Creates
    #Caluculations
    df_metrics['Gross Margin'] = df_income['grossProfit']/df_income['totalRevenue']
    df_metrics['Operating Margin'] = df_income['operatingIncome']/df_income['totalRevenue']
    df_metrics['ROTA'] = (df_income['operatingIncome']+df_income['depreciationAndAmortization'])/\
        (df_balance['totalAssets']-df_balance['intangibleAssets']-df_balance['goodwill']-\
            (.75*df_balance['cashAndCashEquivalentsAtCarryingValue']))
    df_metrics['FCF'] = df_cash['operatingCashflow'] - df_cash['capitalExpenditures']
    df_metrics['ROIIC'] = df_metrics['FCF'].mul(0) #This is a lame way to just get a column of zeros which will be overwritten
    #This is all for ROIIC calculation!
    for i in range(0, len(df_income)-1):
        if df_income.iloc[i+1,df_income.columns.get_loc('operatingIncome')] - df_income.iloc[i,df_income.columns.get_loc('operatingIncome')] < 0:
            df_metrics.iloc[i+1,df_metrics.columns.get_loc('ROIIC')] = "negative"
        elif df_cash.iloc[i+1,df_cash.columns.get_loc('capitalExpenditures')] - df_cash.iloc[i+1,df_cash.columns.get_loc('depreciationDepletionAndAmortization')] \
            + (df_cash.iloc[i+1,df_cash.columns.get_loc('changeInOperatingAssets')]-df_cash.iloc[i+1,df_cash.columns.get_loc('changeInOperatingLiabilities')]) < 0:
            df_metrics.iloc[i+1,df_metrics.columns.get_loc('ROIIC')] = "infinite"
        else: 
            df_metrics.iloc[i+1,df_metrics.columns.get_loc('ROIIC')] = ((df_income.iloc[i+1,df_income.columns.get_loc('operatingIncome')] - df_income.iloc[i,df_income.columns.get_loc('operatingIncome')]) /\
                (df_cash.iloc[i+1,df_cash.columns.get_loc('capitalExpenditures')] - df_cash.iloc[i+1,df_cash.columns.get_loc('depreciationDepletionAndAmortization')] \
                    + (df_cash.iloc[i+1,df_cash.columns.get_loc('changeInOperatingAssets')]-df_cash.iloc[i+1,df_cash.columns.get_loc('changeInOperatingLiabilities')]))).round(4)*100.
    #Convert to Percentages
    df_metrics['Gross Margin'] = df_metrics['Gross Margin'].round(4).mul(100)
    df_metrics['Operating Margin'] = df_metrics['Operating Margin'].round(4).mul(100) 
    df_metrics['ROTA'] = df_metrics['ROTA'].round(4).mul(100) 
    #Final Cleanup
    df_metrics = df_metrics.transpose()
    df_metrics = df_metrics.reindex(['Gross Margin', 'Operating Margin','ROIIC', 'ROTA', 'FCF'])
    ###

    #Does the output
    if quarterly:
        filename = '/Users/erikborn/Dropbox/Mac/Documents/Python/Financial_Files/'+exportTicker+'QRTreport.xlsx'
    else:
        filename = '/Users/erikborn/Dropbox/Mac/Documents/Python/Financial_Files/'+exportTicker+'report.xlsx'
    
    with pd.ExcelWriter(filename) as writer:
        df_metrics.to_excel(writer, sheet_name = "metrics")
        df_overview.to_excel(writer, sheet_name = "overview")
        df_cash.to_excel(writer, sheet_name = "cash")
        df_income.to_excel(writer, sheet_name = "income")
        df_balance.to_excel(writer, sheet_name = "balance")
        df_earnings.to_excel(writer, sheet_name = "earnings")


