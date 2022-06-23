from selenium import webdriver
from datetime import date
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd

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

filename = f'C:/Users/82108/Desktop/대현/{teamname}_기록.xlsx'

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
    df3.drop(['순위'],axis=1,inplace=True)
    df3.drop(['None'],axis=1,inplace=True)
    df3['포지션'] = df3['포지션'].replace([teamname],'투수')

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
