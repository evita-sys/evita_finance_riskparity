from package_calc import calc_fn 
import streamlit as st

if __name__ == "__main__":
    # tickers = ['VTI', 'VEA', 'VWO', 'AGG', 'IAU', 'IYR']
    # df = calc_fn.riskparity(tickers)
    # print(df)
    st.title('Ms. Evita Finance')
    
    rp_url = 'https://msevitafinance.blog.fc2.com/blog-entry-2.html'
    # st.write('check out this [link](%s)' % rp_url)
    st.write('[レイダリオ氏が考える運用手法リスク・パリティとは](%s)' % rp_url)
    
    # 既設定の銘柄INPUT
    dict_tickers = calc_fn.get_tickers()
    tickers_list = dict_tickers.keys()
    
    target_tickers = st.multiselect(
        '対象銘柄を指定してください。',
        tickers_list,  # 選択対象銘柄
        ['VTI', 'VEA', 'VWO', 'AGG', 'IAU', 'IYR'],  # Default値
    )
    
    if len(target_tickers) < 2:
        st.error('最低2銘柄以上を選択してください。')
    else:
        if st.button('実行'):
            tkr = [v for k, v in dict_tickers.items() if k in target_tickers]
            df = calc_fn.riskparity(tkr)
            st.write(df)
            
    
    disclaimer_url = 'https://msevitafinance.blog.fc2.com/blog-entry-1.html'
    st.write('[免責事項](%s)' % disclaimer_url)
