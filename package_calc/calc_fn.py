# py -m pip install yfinance
# py -m pip install scipy 
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import datetime, timedelta

# 銘柄設定
def get_tickers():
    dict_tickers = {
        'VTI':'VTI', 
        'VEA':'VEA',
        'VWO':'VWO',
        'AGG':'AGG',
        'IAU':'IAU',
        'IYR':'IYR',
        'Apple':'AAPL',
        'Amazon':'AMZN',
        'NVIDIA':'NVDA',
        'Microsoft':'MSFT',
        'MongoDB':'MDB',
        'Alphabet':'GOOG',
        'Cisco':'CSCO',
        'Meta':'META',
        'TheWaltDisney':'DIS',
        'Salesforce':'CRM',
        'Starbucks':'SBUX',
        'TaiwanSemiconductor':'TSM'
    }
    return dict_tickers

# ポートフォリオ全体の標準偏差
def sigma_P(w,cov):
    return np.sqrt((w*cov*w.T)[0,0])

# リスク寄与度
def RC(w,cov):
    return np.multiply(cov*w.T, w.T)/sigma_P(w,cov)

# 目的関数
def objective_function(x, params):
    wt = np.asmatrix(x)
    cov = params[0]

    # ポートフォリオ全体標準偏差
    sig_p = sigma_P(wt, cov)

    # 資産毎のリスク寄与度
    rc = RC(wt, cov)

    # 目標リスク（sigma_Pを資産数で除算）
    target_risk = np.full((1, len(x)), sig_p/len(x))

    # 目的関数の計算(penaltyを大きくするため1000をかける)
    return sum(np.square(rc - target_risk.T))[0]*1000

def total_weight_constraint(x):
    return np.sum(x) - 1.0

def long_only_constraint(x):
    return x

def riskparity(tickers):
    
    dict_tickers = get_tickers()

    # データの取得と日次リターンの計算
    # 直近日
    end_date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    # 260平日/年 * 5年 = 1,300平日を前提
    start_date = (datetime.now() - timedelta(1300)).strftime('%Y-%m-%d')

    data = yf.download(tickers, start = start_date, end = end_date)['Adj Close']
    returns = data.pct_change().dropna()

    # 共分散行列計算
    V = returns.cov().to_numpy()

    # 最適化
    num_assets = len(tickers)
    w0 = [1 / num_assets for i in range(num_assets)]  # ウェイト初期値
    cons = ({'type': 'eq', 'fun': total_weight_constraint},{'type': 'ineq', 'fun': long_only_constraint})
    res = minimize(objective_function, x0=w0, args=[V], method='SLSQP',constraints=cons, options={'disp': True, 'ftol': 1e-12})

    w_final = np.asmatrix(res.x)
    rc_final = RC(np.matrix(w_final), V)

    w_final = np.array(w_final).flatten()
    w_fixed = [str(round(s*100,1)) + ' %' for s in w_final]
    rc_final = np.array(rc_final).flatten()
    
    # df = pd.DataFrame({'Weight': w_final, 'Risk Contrib': rc_final}, index = data.columns)
    df = pd.DataFrame({'Weight': w_fixed}, index = data.columns)

    return df