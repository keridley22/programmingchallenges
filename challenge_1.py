from multiprocessing.connection import answer_challenge
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

#import accounts and acc trans csvs as dataframes
# accounts:
# sum number of account holders with each unique title
# produce a cross tabulation of of account holders by title and account type e.g. a count of people with each combination of of possible account types and titles
# produce a cross tabulation of AVERAGE OVERDRAFT LIMIT by title and account type
# produce a cross tabulation of AGGREGATE (SUM) OVERDRAFT LIMIT by title and account type
#plot the distribution of overdraft limits

# open ended, look at relation ship between date opened and date closed, summarise what you see

#exercise 2:

#currentacctrans csv: for each person, count number of transactions, compute total value of those transactions. add columns for n_transactions and trans_total

#accounts10k csv: add n_2018_01 (number of transactions that month?), n_2018_02 and trans_2018_01 column and so on for each customer for every month in which there are transactions

# accounts10k: report:

# customer with highest overall transaction values
#customer with highest number of transactions
# the customer with lowest overall transaction values
# the number of customers with transactions per month
#number of customers with no transactions

def question_1(accounts):
    titles= list(accounts.title.unique())
    for title in titles:
        print(title,':', len(accounts.loc[accounts['title']==title]), 'account(s)')
        
    
def question_2(accounts):
    print('Crosstabulation of title and account type')
    return pd.crosstab(accounts['title'], accounts['account_type'], None, None)

#crosstab_accountholders = question_2(accounts)


def question_3(accounts):
    print('Average overdraft limit by title and account type')
    return pd.crosstab(accounts['title'], accounts['account_type'], values=accounts.overdraft_limit, aggfunc=np.mean)

#crosstab_avg_overdraft = question_3(accounts)


def question_4(accounts):
    print('Sum overdraft limit by title and account type')
    return pd.crosstab(accounts['title'], accounts['account_type'], values=accounts.overdraft_limit, aggfunc=np.sum)

#crosstab_sum_overdraft = question_4(accounts)


def question_5(accounts):
    plt.figure()
    sns.distplot(accounts.overdraft_limit, kde_kws={"color": "black", "lw": 3, "label": "KDE"}, hist_kws={"color": "gray", "alpha": 0.5, "lw": 3, "label": "Histogram"})
    plt.savefig('overdraft_dist.png')
    plt.show()


#def question_6():

def question_7_and_8(accounts, currents):
    currents.trans_date = pd.to_datetime(currents.trans_date)   
    currents['trans_month'] = currents['trans_date'].dt.strftime('%y_%m')

    for acc in accounts['account_number']: 
        current_loop = currents.loc[currents['acc_number']==acc]
        accounts.loc[accounts['account_number']==acc, 'n_transactions'] = len(current_loop)
        accounts.loc[accounts['account_number']==acc, 'trans_total'] = current_loop.amount.sum()
        unique_months = current_loop['trans_month'].unique()
        for m in unique_months:
            current_loop_month = current_loop.loc[current_loop['trans_month']==m]
            accounts.loc[accounts['account_number']==acc, 'n_{month}'.format(month=m)] = len(current_loop_month)
            accounts.loc[accounts['account_number']==acc, 'trans_{month}'.format(month=m)] = current_loop_month['amount'].sum()

    return accounts

def question_9(accounts, currents):
    highest_value = accounts['trans_total'].max()
    print('Highest transaction value account:', accounts.loc[accounts.trans_total==highest_value, 'account_number'].values[0])
    highest_number = accounts['n_transactions'].max()
    print('Highest # transactions account:', accounts.loc[accounts.n_transactions==highest_number, 'account_number'].values[0])
    lowest_value = accounts['trans_total'].min()
    print('Lowest transaction value account:', accounts.loc[accounts.trans_total==lowest_value, 'account_number'].values[0])
    currents.trans_date = pd.to_datetime(currents.trans_date)   
    currents['trans_month'] = currents['trans_date'].dt.strftime('%y_%m')
    unique_months = currents['trans_month'].unique()
    for m in unique_months: 
        print('# accounts with transactions in {m}:'.format(m=m), len(accounts.loc[accounts['n_{m}'.format(m=m)]>0]))

    print('The # accounts with no transactions:', len(accounts.loc[(accounts['n_transactions']==0)|(accounts['n_transactions']==np.nan)]))



accounts=pd.read_csv("accounts.csv")
currents= pd.read_csv("current-acc-trans.csv")

question_1(accounts)

print(question_2(accounts))

print(question_3(accounts))

print(question_4(accounts))

question_5(accounts)




