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

filename = f'C:/Users/82108/Desktop/KBO/{teamname}_기록.xlsx'

# empty dataframe
df2 = pd.DataFrame()

# Create empty Lists
ips,hs,hrs,bbs,hbps,sos,rs,ers,whips,cgs,shos,qss,bsvs,tbfs,nps,avgs,b22,b32 = ([] for i in range(18))
sacs,sfs,ibbs,wps,bks,BBs,IBBs,HBPs,SOs,GDPs,SLGs,OBPs,OPSs,MHs,RISPs,PH_BAs= ([] for i in range(16))
GSs,Wgss,Wgrs,GFs,SVOs,TSs,gdps,GOs,AOs,GO_AOs= ([] for i in range(10))

# convert data type(str > int)
def convert_data_type(dataframe,num):
    for p in range(len(dataframe.columns)):
        dataframe[dataframe.columns[p]] = dataframe[dataframe.columns[p]].replace(['-'],10000)
    
    for k in range(num,len(dataframe.columns)):
        if dataframe[dataframe.columns[k]].dtypes == object:
            dataframe[dataframe.columns[k]] = dataframe[dataframe.columns[k]].astype(float)

    for l in range(len(dataframe.columns)):
        dataframe[dataframe.columns[l]] = dataframe[dataframe.columns[l]].replace([10000],'-')
    
# Hitter_Record
def Hitter_Record(pos):
    global df2

    position_choose = browser.find_element(By.XPATH,'//*[@id="cphContents_cphContents_cphContents_ddlPos_ddlPos"]')
    select_position = Select(position_choose)

    select_position.select_by_visible_text(pos)
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

    df = pd.DataFrame(record_split)

    df.drop([0,0],axis=0,inplace=True)
    df.columns= ['순위','선수명','포지션','AVG','G','PA','AB','R','H','2B','3B','HR','TB','RBI','SAC','SF']
    df.drop(['순위'],axis=1,inplace=True)
    df['포지션'] = df['포지션'].replace([teamname],pos)

    # click button to next page
    browser.find_element(By.XPATH,'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[2]/div[2]/a[2]').click()

    time.sleep(2)

    df2 = df2.append(df)

    for num in range(1,len(record)):
        bb = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[5]').text
        ibb = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[6]').text
        hbp = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[7]').text
        so = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[8]').text
        gdp = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[9]').text
        slg = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[10]').text
        obp = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[11]').text
        ops = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[12]').text
        mh = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[13]').text
        risp = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[14]').text
        ph_ba = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[15]').text

        BBs.append(bb)
        IBBs.append(ibb)
        HBPs.append(hbp)
        SOs.append(so)
        GDPs.append(gdp)
        SLGs.append(slg)
        OBPs.append(obp)
        OPSs.append(ops)
        MHs.append(mh)
        RISPs.append(risp)
        PH_BAs.append(ph_ba)

        
    df2['BB'] = BBs
    df2['IBB'] = IBBs
    df2['HBP'] = HBPs
    df2['SO'] = SOs
    df2['GDP'] = GDPs
    df2['SLG'] = SLGs
    df2['OBP'] = OBPs
    df2['OPS'] = OPSs
    df2['MH'] = MHs
    df2['RISP'] = RISPs
    df2['PH-BA'] = PH_BAs
    
    convert_data_type(df2,2)
    
    # return
    browser.find_element(By.XPATH,'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[2]/div[2]/a[1]').click()
    
  
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

    browser.find_element(By.XPATH,'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[2]/div[1]/ul/li[2]/a').click()

    for num in range(1,len(record)):
        gs= browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[5]').text
        wgs = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[6]').text
        wgr = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[7]').text
        gf = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[8]').text
        svo = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[9]').text
        ts = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[10]').text
        gdp = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[11]').text
        go = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[12]').text
        ao = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[13]').text
        go_ao = browser.find_element(By.XPATH,f'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[{num}]/td[14]').text
        
        GSs.append(gs)
        Wgss.append(wgs)
        Wgrs.append(wgr)
        GFs.append(gf)
        SVOs.append(svo)
        TSs.append(ts)
        gdps.append(gdp)
        GOs.append(go)
        AOs.append(ao)
        GO_AOs.append(go_ao)

    df3['GS'] = GSs
    df3['Wgs'] = Wgss
    df3['Wgr'] = Wgrs
    df3['GF'] = GFs
    df3['SVO'] = SVOs
    df3['TS'] = TSs
    df3['GDP'] = gdps
    df3['GO'] = GOs
    df3['AO'] = AOs
    df3['GO/AO'] = GO_AOs        

    convert_data_type(df3,3)
    df3 = df3.sort_values(by='GS',ascending=False)

    empty_list = []
    for i in range(1,len(record)):
        empty_list.append(i)
    df3 = df3.set_index(keys=[empty_list],inplace=False)
        
    
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
