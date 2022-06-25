import cgi
from selenium import webdriver
from datetime import date
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np

# datetime
today = date.today()
current_time = today.strftime('%Y/%m/%d')

# input
teamname = input("Team: ")
browser = webdriver.Chrome("./chromedriver.exe")
browser.get("https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx")

# team
team = browser.find_element(By.XPATH,'//*[@id="cphContents_cphContents_cphContents_ddlTeam_ddlTeam"]')
select_team = Select(team)
select_team.select_by_visible_text(f'{teamname}')

filename = f'C:/Users/82108/Desktop/KBO/{teamname}_기록.xlsx'

# empty dataframe
df2 = pd.DataFrame()

# Hitter_Record
def Hitter_Record(pos):
    global df2
    position_choose = browser.find_element(By.XPATH,'//*[@id="cphContents_cphContents_cphContents_ddlPos_ddlPos"]')
    select_position = Select(position_choose)

    select_position.select_by_visible_text(pos)
    time.sleep(3)


    # record-1 Split by line 
    records = browser.find_element(By.CSS_SELECTOR,"div.record_result").text
    record = records.split('\n')
    del record[-1]
    
   
    # record-2 Split by empty
    record_split= []
    for j in range(len(record)):
        a = record[j].split()
        record_split.append(a)


    df = pd.DataFrame(record_split)

    df.drop([0,0],axis=0,inplace=True)
    df.columns= ['순위','선수명','포지션','AVG','G','PA','AB','R','H','2B','3B','HR','TB','RBI','SAC','SF']
    df.drop(['순위'],axis=1,inplace=True)
    df['포지션'] = df['포지션'].replace([teamname],pos)

    for p in range(len(df.columns)):
        df[df.columns[p]] = df[df.columns[p]].replace(['-'],10000)
    
    for k in range(2,15):
        if df[df.columns[k]].dtypes == object:
            df[df.columns[k]] = df[df.columns[k]].astype(float)

    for l in range(len(df.columns)):
        df[df.columns[l]] = df[df.columns[l]].replace([10000],'-')

    df2 = df2.append(df)
  
# Pitcher record
def Pitcher_Record():
    browser.find_element(By.XPATH,'//*[@id="contents"]/div[2]/div[2]/ul/li[2]/a').click()

    time.sleep(2)
    curr_handle = browser.current_window_handle 
    handles = browser.window_handles

    for handle in handles:
        browser.switch_to.window(handle)

    #team
    team = browser.find_element(By.XPATH,'//*[@id="cphContents_cphContents_cphContents_ddlTeam_ddlTeam"]')
    select_team = Select(team)
    select_team.select_by_visible_text(f'{teamname}')
    time.sleep(2)


    # record-1 Split by line 
    records = browser.find_element(By.CSS_SELECTOR,"div.record_result").text
    record = records.split('\n')
    del record[-1]

    # record-2 Split by empty
    record_split= []
    for j in range(len(record)):
        a = record[j].split()
        record_split.append(a)

    df3 = pd.DataFrame(record_split)

    df3.drop([0,0],axis=0,inplace=True)
    df3.columns= ['순위','선수명','포지션','ERA','G','W','L','SV','HLD','WPCT','IP','H','HR','BB','HBP','SO','R','ER','WHIP','None']
    df3.drop(['순위','IP','H','HR','BB','HBP','SO','R','ER','WHIP','None'],axis=1,inplace=True)
    df3['포지션'] = df3['포지션'].replace([teamname],'투수')
    
    # 잘못된 데이터 다시 수정
    ips = []
    hs = []
    hrs = []
    bbs = []
    hbps = []
    sos = []
    rs = []
    ers = []
    whips = []
    cgs= []
    shos = []
    qss = []
    bsvs = []
    tbfs = []
    nps = []
    avgs = []
    b22 = []
    b32 = []
    sacs = []
    sfs = []
    ibbs = []
    wps = []
    bks = []


    for num in range(1,len(record)):
        
        ip = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[11]').text
        h = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[12]').text
        hr = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[13]').text
        bb = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[14]').text
        hbp = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[15]').text
        so = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[16]').text
        r = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[17]').text
        er = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[18]').text
        whip = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[19]').text
        ips.append(ip)
        hs.append(h)
        hrs.append(hr)
        bbs.append(bb)
        hbps.append(hbp)
        sos.append(so)
        rs.append(r)
        ers.append(er)
        whips.append(whip)
    
    df3['H'] =  hs
    df3['HR'] = hrs
    df3['BB'] = bbs
    df3['HBP'] = hbps
    df3['SO'] = sos
    df3['R'] = rs
    df3['ER'] = ers
    df3['WHIP'] = whips
    df3.insert(2,'IP',ips)

    browser.find_element(By.XPATH,'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[2]/div[2]/a[2]').click()

    for num in range(1,len(record)):
        
        cg = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[5]').text
        sho = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[6]').text
        qs = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[7]').text
        bsv = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[8]').text
        tbf = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[9]').text
        np = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[10]').text
        avg = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[11]').text
        b2 = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[12]').text
        b3 = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[13]').text
        sac = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[14]').text
        sf = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[15]').text
        ibb = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[16]').text
        wp = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[17]').text
        bk = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[18]').text


        cgs.append(cg)
        shos.append(sho)
        qss.append(qs)
        bsvs.append(bsv)
        tbfs.append(tbf)
        nps.append(np)
        avgs.append(avg)
        b22.append(b2)
        b32.append(b3)
        sacs.append(sac)
        sfs.append(sf)
        ibbs.append(ibb)
        wps.append(wp)
        bks.append(bk)

    
    df3['CG'] =  cgs
    df3['SHO'] = shos
    df3['QS'] = qss
    df3['BSV'] = bsvs
    df3['TBF'] = tbfs
    df3['NP'] = nps
    df3['AVG'] = avgs
    df3['2B'] = b22
    df3['3B'] = b32
    df3['SAC'] = sacs
    df3['SF'] = sfs
    df3['IBB'] = ibbs
    df3['WP'] = wps
    df3['BK'] = bks

    for p in range(len(df3.columns)):
        df3[df3.columns[p]] = df3[df3.columns[p]].replace(['-'],10000)

    try :
        for k in range(3,32):
            if df3[df3.columns[k]].dtypes== object:
                df3[df3.columns[k]] = df3[df3.columns[k]].astype(float)
    except:
        pass
    
    for l in range(len(df3.columns)):
        df3[df3.columns[l]] = df3[df3.columns[l]].replace([10000],'-')
    
    # put the data in Excel
    with pd.ExcelWriter(filename) as writer:
        df2[df2.포지션 == '포수'].to_excel(writer,sheet_name='포수')
        df2[df2.포지션 == '내야수'].to_excel(writer,sheet_name='내야수')
        df2[df2.포지션 == '외야수'].to_excel(writer,sheet_name='외야수')
        df3[df3.포지션 == '투수'].to_excel(writer,sheet_name='투수')
    

    browser.switch_to.window(curr_handle)




Hitter_Record('포수')
Hitter_Record('내야수')
Hitter_Record('외야수')
Pitcher_Record()


browser.quit()
