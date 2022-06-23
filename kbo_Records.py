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
    
    #잘못된 데이터 다시 수정
    ips = []
    hs = []
    hrs = []
    bbs = []
    hbps = []
    sos = []
    rs = []
    ers = []
    whips = []
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


    df3['IP'] = ips
    df3['H'] =  hs
    df3['HR'] = hrs
    df3['BB'] = bbs
    df3['HBP'] = hbps
    df3['SO'] = sos
    df3['R'] = rs
    df3['ER'] = ers
    df3['WHIP'] = whips

    for p in range(len(df3.columns)):
        df3[df3.columns[p]] = df3[df3.columns[p]].replace(['-'],10000)

    try :
        for k in range(2,17):
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
