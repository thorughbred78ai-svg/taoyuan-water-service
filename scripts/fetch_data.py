#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桃園市政府水務局資料生成腳本
整合官方網站各項資訊，生成靜態 JSON 資料供前端使用
"""

import json
import os
from datetime import datetime

# 便民服務連結（對應實際子連結網址）
SERVICE_LINKS = [
    {
        "title": "申報案件查詢",
        "url": "http://www.wrbtycg.tw/TYSAFE_WRB/view/PublicPage/ApplyPlanDefault.aspx",
        "description": "查詢水路加蓋、水路報廢、水路搭排、水路遷移、溜池報廢、區域排水構造物等申報案件進度",
        "category": "資訊查詢",
        "icon": "🔍"
    },
    {
        "title": "桃園網路e指通",
        "url": "https://e-services.tycg.gov.tw/TycgOnline/tycgOnline.action?cdnCache=Y&func=schedule&qword=",
        "description": "線上申辦各項水務相關業務，查詢申辦進度，免出門即可完成申請",
        "category": "線上申請",
        "icon": "🖱️"
    },
    {
        "title": "水利設施參訪預約系統",
        "url": "http://winfo.tycg.gov.tw/R/",
        "description": "預約參訪桃園北區/龜山/石門/大溪/楊梅水資源回收中心、文青園、龍山滯洪池、大樹林滯洪池、山豬湖生態親水園區等設施",
        "category": "線上申請",
        "icon": "🏗️"
    },
    {
        "title": "檔案應用專區",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10923&sms=14461",
        "description": "申請閱覽、抄錄或複製本局檔案資料，提供檔案借調申請流程說明",
        "category": "線上申請",
        "icon": "📁"
    },
    {
        "title": "容積移轉專區",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10926&sms=14463",
        "description": "查詢桃園市各河川容積移轉實施計畫、得申請容積移轉土地清冊與相關公告",
        "category": "資訊查詢",
        "icon": "🏔️"
    },
    {
        "title": "污水系統公告範圍",
        "url": "https://wrb.tycg.gov.tw/cp.aspx?n=10885",
        "description": "查詢污水下水道系統公告使用地區範圍，了解家是否位於污水管線佈設區域",
        "category": "資訊查詢",
        "icon": "🚰"
    },
    {
        "title": "水情資訊網",
        "url": "https://winfo.tycg.gov.tw/tysafep/",
        "description": "即時水情、水位、雨量資訊查詢，淹水警戒、土石流警戒等防災資訊",
        "category": "資訊查詢",
        "icon": "💧"
    },
    {
        "title": "下水道雲端智慧管理系統",
        "url": "https://sewergis.tycg.gov.tw/Account/Login",
        "description": "污水案件獎勵補助申請、污水申請案件查詢、水肥證線上申請、用戶排水設備許可申請",
        "category": "補助申請",
        "icon": "💰"
    },
    {
        "title": "地下水管理智慧平台",
        "url": "https://gwater.tycg.gov.tw/list/1",
        "description": "地下水即時抽水資料、週期用水報表、設備病例系統、用水量填報與管理",
        "category": "資訊查詢",
        "icon": "🌊"
    },
    {
        "title": "重大點源放流水監測查詢系統",
        "url": "https://cwms.tydep.gov.tw/PUBLIC/RealTime/Get_AVGR.aspx",
        "description": "查詢重大污染源放流水自動連續監測資訊，確保水質安全",
        "category": "資訊查詢",
        "icon": "📊"
    },
    {
        "title": "龜山水肥站水肥投入預約系統",
        "url": "https://sewergis.tycg.gov.tw/Account/Login?ReturnUrl=%2FFertilizerStation%2FScheduledFertilizer",
        "description": "水肥站投入預約服務，方便管理水肥處理作業",
        "category": "線上申請",
        "icon": "📅"
    },
    {
        "title": "市管河川及區域排水公開資訊",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10933&sms=14464",
        "description": "市管河川及區域排水相關公開資訊，包含治理規劃與現況",
        "category": "資訊查詢",
        "icon": "🏞️"
    },
    {
        "title": "下載專區",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10935&sms=14466",
        "description": "水利工程減碳指引、治理計畫說明會資料、污水下水道申請審查手冊等文件下載",
        "category": "資訊查詢",
        "icon": "📥"
    },
    {
        "title": "電子書",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10936&sms=17523",
        "description": "水務局相關電子書籍與宣導資料線上閱覽",
        "category": "資訊查詢",
        "icon": "📖"
    },
    {
        "title": "相關網站連結",
        "url": "https://wrb.tycg.gov.tw/News_Link.aspx?n=10937&sms=14468",
        "description": "彙整水務相關外部網站連結，方便民眾一站式查詢",
        "category": "資訊查詢",
        "icon": "🔗"
    },
    {
        "title": "重大計畫進度查詢",
        "url": "https://reiso.tycg.gov.tw/",
        "description": "查詢水務局各項重大工程計畫的執行進度",
        "category": "資訊查詢",
        "icon": "📈"
    },
    {
        "title": "常用服務",
        "url": "https://wrb.tycg.gov.tw/News_Link.aspx?n=10939&sms=14469",
        "description": "彙整民眾常用的各項水務服務連結與入口",
        "category": "資訊查詢",
        "icon": "⭐"
    },
    {
        "title": "污水下水道排水設備接管融資專案",
        "url": "https://wrb.tycg.gov.tw/cp.aspx?n=21918",
        "description": "污水下水道用戶排水設備接管融資相關資訊與申請說明",
        "category": "補助申請",
        "icon": "🏠"
    }
]

# 政府資訊公開子連結
GOV_INFO_LINKS = [
    {
        "title": "會計專區",
        "url": "https://wrb.tycg.gov.tw/cl.aspx?n=10942",
        "description": "年度預算、決算、會計月報等財務資訊"
    },
    {
        "title": "利衝迴避身分揭露專區",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10948&sms=14475",
        "description": "公職人員利益衝突迴避相關身分揭露資訊"
    },
    {
        "title": "公展公告區",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10949&sms=14476",
        "description": "各項畫公展、公告資訊"
    },
    {
        "title": "公共設施維護管理資訊",
        "url": "https://wrb.tycg.gov.tw/cl.aspx?n=10950",
        "description": "公共設施維護管理相關資訊公開"
    },
    {
        "title": "統計專區",
        "url": "https://statbas.tycg.gov.tw/TCSTATRWD/Page/Publish.aspx?Mid1=380250000G",
        "description": "水務局各項統計資料發布時間表與背景說明"
    },
    {
        "title": "性別主流化專區",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10961&sms=14483",
        "description": "性別主流化相關政策與宣導資訊"
    },
    {
        "title": "個人資料保護專區",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10962&sms=14484",
        "description": "個人資料保護相關規定與宣導"
    },
    {
        "title": "辦理政策及業務宣導之執行情形",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10964&sms=14485",
        "description": "各項政策及業務宣導活動執行情形"
    },
    {
        "title": "國家賠償事件收結情形",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10965&sms=14486",
        "description": "國家賠償事件處理與收結情形"
    },
    {
        "title": "補助專區",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10966&sms=14487",
        "description": "各項補助資訊與申請說明"
    }
]

# 訊息公告
ANNOUNCEMENTS = [
    {
        "title": "最新消息",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10827&sms=14441",
        "description": "水務局最新公告、活動訊息與重要通知"
    },
    {
        "title": "RSS 訂閱",
        "url": "https://wrb.tycg.gov.tw/cp.aspx?n=10828",
        "description": "訂閱水務局 RSS 資訊推播，即時掌握最新動態"
    },
    {
        "title": "新聞專區",
        "url": "https://wrb.tycg.gov.tw/News.aspx?n=10829&sms=14442",
        "description": "水務相關新聞報導與政策宣導資訊"
    },
    {
        "title": "影音專區",
        "url": "https://wrb.tycg.gov.tw/News_Video.aspx?n=10830&sms=14443",
        "description": "水務局宣導影片、活動紀錄與教育影片"
    }
]

# 交通資訊
TRAFFIC_INFO = {
    "address": "33043 桃園市桃園區成功路一段32號7樓",
    "landmark": "【桃園國小旁、郵政總局對面】",
    "bus_stop": "桃園郵局",
    "bus_query": "https://ebus.tycg.gov.tw/",
    "description": "可至桃園市公車動態資訊網查詢，點選乘車規劃，依地標、交叉路口、站牌查詢。本局最近站牌為「桃園郵局」。"
}

# 業務資訊
BUSINESS_INFO = [
{
        "title": "綜合企劃科",
        "phone": "03-303-3688 轉3860",
        "fax": "03-303-3678",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責水資源綜合規劃、施政計畫研擬、水利相關政策規劃等業務。",
        "services": ["水資源規劃", "施政計畫", "政策研擬"]
    },
{
        "title": "水利防災科",
        "phone": "03-303-3688 轉3620",
        "fax": "03-303-3661",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責水利防災相關業務，包含防汛整備、災害搶修、防洪設施管理等。",
        "services": ["防汛整備", "災害搶修", "防洪設施管理", "水情監測"]
    },
{
        "title": "水利行政科",
        "phone": "03-303-3688 轉3700",
        "fax": "03-303-3677",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責水利行政業務，包含河川管理、排水設施管理、水利法規執行等。",
        "services": ["河川管理", "排水設施管理", "水利法規執行", "許可審查"]
    },
{
        "title": "水利工程科",
        "phone": "03-303-3688 轉3310",
        "fax": "03-303-3664",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責水利工程規劃設計、發包監造、施工管理等業務。",
        "services": ["工程規劃設計", "工程發包監造", "施工管理", "工程驗收"]
    },
{
        "title": "水利養護工程科",
        "phone": "03-303-3688 轉3800",
        "fax": "03-303-3665",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責水利設施養護、河道疏濬、設施維修等業務。",
        "services": ["設施養護", "河道疏濬", "設施維修", "清淤工程"]
    },
{
        "title": "河岸地工程管理科",
        "phone": "03-303-3688 轉3830",
        "fax": "03-303-3665",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責河岸地管理、河川區域使用管理、河岸設施維護等業務。",
        "services": ["河岸地管", "河川區域使用管理", "河岸設施維護", "容積移轉"]
    },
{
        "title": "污水企劃工程科",
        "phone": "03-303-3688 轉3510",
        "fax": "03-303-3666",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責污水下水道系統規劃、設計、工程發包等業務。",
        "services": ["污水系統規劃", "污水工程設計", "工程發包"]
    },
{
        "title": "污水促參計畫工程科",
        "phone": "03-303-3688 轉3230",
        "fax": "03-303-3611",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責污水下水道促參計畫、BOT 工程管理等業務。",
        "services": ["促參計畫", "BOT 工程管理", "民間參與"]
    },
{
        "title": "污水設施管理工程科",
        "phone": "03-303-3688 轉3750",
        "fax": "03-303-3663",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責污水處理廠、污水管線、用戶接管等設施管理業務。",
        "services": ["污水處理廠管理", "污水管線管理", "用戶接管", "設施維護"]
    },
{
        "title": "坡地管理科",
        "phone": "03-303-3688 轉3770",
        "fax": "03-337-4285",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責山坡地管理、土石流防災、水土保持等業務。",
        "services": ["山坡地管理", "土石流防災", "水土保持", "容積移轉"]
    },
{
        "title": "雨水下水道科",
        "phone": "03-303-3688 轉3730",
        "fax": "03-303-3662",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責雨水下水道系統規劃、建設、管理與維護業務。",
        "services": ["雨水下水道規劃", "建設管理", "設施維護", "清淤作業"]
    },
{
        "title": "再生水企劃管理工程科",
        "phone": "03-303-3688 轉3340",
        "fax": "03-303-3611",
        "official_url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837",
        "description": "負責再生水利用規劃、推動與管理相關業務。",
        "services": ["再生水規劃", "再生水推動", "水資源再利用"]
    }
]

# 常見問答
FAQ = [
    {
        "question": "如何申請污水下水道用戶接管？",
        "answer": "可透過「下水道雲端智慧管理系統」線上申請，或至水務局臨櫃辦理。申請時需準備建築物相關證明文件。部分污水用戶接管工程可申請獎勵補助。",
        "links": [{"title": "下水道雲端智慧管理系統", "url": "https://sewergis.tycg.gov.tw/Account/Login"}, {"title": "污水下水道系統公告範圍", "url": "https://wrb.tycg.gov.tw/cp.aspx?n=10885"}]
    },
    {
        "question": "水情資訊如何查詢？",
        "answer": "可至水情資訊網查詢即時雨量、水位、淹水警戒、土石流警戒等防災資訊。",
        "links": [{"title": "水情資訊網", "url": "https://winfo.tycg.gov.tw/tysafep/"}]
    },
    {
        "question": "山坡地容積移轉如何申請？",
        "answer": "請至水務局「容積移轉專區」查詢各河川得申請容積移轉土地清冊與相關規定，或洽河岸地工程管理科、坡地管理科辦理。",
        "links": [{"title": "容積移轉專區", "url": "https://wrb.tycg.gov.tw/News.aspx?n=10926&sms=14463"}, {"title": "機關聯絡資訊", "url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837"}]
    },
    {
        "question": "污水下水道工程是否有補助？",
        "answer": "部分污水用戶接管工程可申請獎勵補助，詳情請至下水道雲端智慧管理系統查詢或洽污水設施管理工程科。另有「污水下水道排水設備接管融資專案」可供參考。",
        "links": [{"title": "下水道雲端智慧管理系統", "url": "https://sewergis.tycg.gov.tw/Account/Login"}, {"title": "污水下水道排水設備接管融資專案", "url": "https://wrb.tycg.gov.tw/cp.aspx?n=21918"}]
    },
    {
        "question": "如何預約參訪水利設施？",
        "answer": "可透過水利設施參訪預約系統線上預約，可選擇桃園北區、龜山、石門、大溪、楊梅水資源回收中心，以及文青水園、龍山滯洪池、大樹林滯洪池、山豬湖生態親水園區等設施。",
        "links": [{"title": "水利設施參訪預約系統", "url": "http://winfo.tycg.gov.tw/R/"}]
    },
    {
        "question": "發現排水溝堵塞或積水如何通報？",
        "answer": "可撥打 1999 市民服務專線通報，或聯繫水務局水利養護工程科處理。也可參考水情資訊網掌握相關防災資訊。",
        "links": [{"title": "水情資訊網", "url": "https://winfo.tycg.gov.tw/tysafep/"}, {"title": "機關聯絡資訊", "url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837"}]
    },
    {
        "question": "水肥清除許可證如何申請？",
        "answer": "可透過下水道雲端智慧管理系統線上申請水肥證，需準備相關車輛及公司資料，包含投肥證申請書、自主檢核表、切結書、廢棄物清除許可證等文件。",
        "links": [{"title": "下水道雲端智慧管理系統", "url": "https://sewergis.tycg.gov.tw/Account/Login"}, {"title": "龜山水肥站水肥投入預約系統", "url": "https://sewergis.tycg.gov.tw/Account/Login?ReturnUrl=%2FFertilizerStation%2FScheduledFertilizer"}]
    },
    {
        "question": "河川區域內可以從事哪些活動？",
        "answer": "河川區域內活動需依相關水利法規申請許可，詳情請洽水利行政科或查詢水務局相關法規。未經許可不得於河川區域內從事相關行為。",
        "links": [{"title": "水務類相關法規", "url": "https://law.tycg.gov.tw/"}, {"title": "機關聯絡資訊", "url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837"}]
    },
    {
        "question": "水務局怎麼去？",
        "answer": "地址為 33043 桃園市桃園區成功路一段32號7樓（桃園國小旁、郵政總局對面）。可搭公車至「桃園郵局」站牌下車，建議先查詢乘車規劃。",
        "links": [{"title": "桃園市公車動態資訊網", "url": "https://ebus.tycg.gov.tw/"}, {"title": "機關聯絡資訊", "url": "https://wrb.tycg.gov.tw/cp.aspx?n=10837"}]
    },
    {
        "question": "如何查詢自家附近有無污水管線？",
        "answer": "可至「污水系統公告範圍」頁面查詢，了解自家是否位於污水下水道系統公告使用地區範圍內。",
        "links": [{"title": "污水系統公告範圍", "url": "https://wrb.tycg.gov.tw/cp.aspx?n=10885"}]
    },
]

# 聯絡資訊
CONTACT_INFO = {
    "phone": "03-303-3688",
    "extension": "局本部轉3600",
    "address": "33043 桃園市桃園區成功路一段32號7樓",
    "service_hotline": "1999（桃園市境內）",
    "outside_hotline": "03-2189000（外縣市）",
    "email": "wrb@tycg.gov.tw",
    "hours": "星期一至星期五 上午8:00-12:00 下午1:00-5:00",
    "website": "https://wrb.tycg.gov.tw/"
}

# 法規資訊連結（依官方水務類法規清單，共 59 筆）
REGULATIONS = [
    {
        "title": "桃園市其他排水管理自治條例",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002705",
        "category": "自治條例",
        "date": "115.03.11"
    },
    {
        "title": "桃園市水資源回收中心回饋地方自治條例",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL000288",
        "category": "自治條例",
        "date": "110.12.21"
    },
    {
        "title": "桃園市地下水水權裝置量水設備自治條例",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002048",
        "category": "自治條例",
        "date": "108.07.24"
    },
    {
        "title": "桃園市污水下水道管理自治條例",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL000287",
        "category": "自治條例",
        "date": "107.10.03"
    },
    {
        "title": "桃園市雨水下水道管理自治條例",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001569",
        "category": "自治條例",
        "date": "106.01.25"
    },
    {
        "title": "桃園市污水下水道使用費徵收自治條例",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL000301",
        "category": "自治條例",
        "date": "105.03.21"
    },
    {
        "title": "桃園市市管河川區域使用行為規費收費標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002586",
        "category": "自治規則",
        "date": "114.07.09"
    },
    {
        "title": "桃園市水資源回收中心附屬水肥投入站管理辦法",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL000329",
        "category": "自治規則",
        "date": "114.01.09"
    },
    {
        "title": "桃園市市管區域排水設施範圍使用行為規費收費標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002509",
        "category": "自治規則",
        "date": "113.07.10"
    },
    {
        "title": "桃園市道路側溝及雨水下水道暫掛纜線管理辦法",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001208",
        "category": "自治規則",
        "date": "113.06.28"
    },
    {
        "title": "桃園市污水下水道系統工程案件審查收費標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002417",
        "category": "自治規則",
        "date": "112.06.27"
    },
    {
        "title": "桃園市雨水下水道相關設施審查及查驗收費標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002070",
        "category": "自治規則",
        "date": "111.10.24"
    },
    {
        "title": "桃園市雨水污水下水道人孔設施管理辦法",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002202",
        "category": "自治規則",
        "date": "110.02.08"
    },
    {
        "title": "桃園市水資源發展基金收支保管及運用辦法",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002182",
        "category": "自治規則",
        "date": "109.12.14"
    },
    {
        "title": "桃園市工業區內事業用戶納入公共污水下水道使用管理及收費辦法",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002167",
        "category": "自治規則",
        "date": "109.10.08"
    },
    {
        "title": "桃園市污水下水道審查作業收費標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002139",
        "category": "自治規則",
        "date": "109.06.04"
    },
    {
        "title": "桃園市建築基地開發排入雨水下水道逕流量標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002071",
        "category": "自治規則",
        "date": "108.09.26"
    },
    {
        "title": "桃園市地下水井拆遷補償費及救濟金查估標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002025",
        "category": "自治規則",
        "date": "108.04.29"
    },
    {
        "title": "桃園市公共污水下水道可容納排入之下水水質標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001553",
        "category": "自治規則",
        "date": "106.01.19"
    },
    {
        "title": "桃園市排水計畫審查收費標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001547",
        "category": "自治規則",
        "date": "105.12.27"
    },
    {
        "title": "桃園市蓄水建造物拆除審核辦法",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001337",
        "category": "自治規則",
        "date": "105.11.16"
    },
    {
        "title": "桃園市溫泉開發許可審查收費標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL000331",
        "category": "自治規則",
        "date": "105.05.24"
    },
    {
        "title": "桃園市下水道工程使用土地支付償金或補償費標準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL000250",
        "category": "自治規則",
        "date": "104.12.04"
    },
    {
        "title": "桃園市政府水務局職場霸凌防治措施申訴及調查處理要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002727",
        "category": "行政規則",
        "date": "115.08.13"
    },
    {
        "title": "桃園市山坡地查報取締工作督導考核要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001150",
        "category": "行政規則",
        "date": "115.03.19"
    },
    {
        "title": "桃園市山坡地範圍劃定及檢討變更作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001153",
        "category": "行政規則",
        "date": "114.12.05"
    },
    {
        "title": "桃園市水資源發展基金管理會設置要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002233",
        "category": "行政規則",
        "date": "114.10.01"
    },
    {
        "title": "桃園市政府水患防治專案小組設置要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002593",
        "category": "行政規則",
        "date": "114.08.11"
    },
    {
        "title": "桃園市政府水務局因性別所產生之歧視防治及申訴處理要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001064",
        "category": "行政規則",
        "date": "113.05.31"
    },
    {
        "title": "桃園市政府水務局工程品質督導小組設置及作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001284",
        "category": "行政規則",
        "date": "112.11.27"
    },
    {
        "title": "桃園市政府逕流分擔審議會設置要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002424",
        "category": "行政規則",
        "date": "112.07.27"
    },
    {
        "title": "桃園市政府水利建造物安全檢查督導小組設置及作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002407",
        "category": "行政規則",
        "date": "112.05.26"
    },
    {
        "title": "桃園市政府防汛專用砂包整備領用及回收注意事項",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002350",
        "category": "行政規則",
        "date": "111.08.22"
    },
    {
        "title": "桃園市政府辦理出流管制設施移交及管理作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002341",
        "category": "行政規則",
        "date": "111.07.01"
    },
    {
        "title": "桃園市政府山坡地違規使用查報取締聯繫小組設置要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001152",
        "category": "行政規則",
        "date": "110.10.18"
    },
    {
        "title": "桃園市政府水務局職業安全衛生督導作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002112",
        "category": "行政規則",
        "date": "109.02.26"
    },
    {
        "title": "桃園市備用水井運用及維護管理作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001778",
        "category": "行政規則",
        "date": "107.01.11"
    },
    {
        "title": "桃園市政府水務局公共工程工務管理要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001660",
        "category": "行政規則",
        "date": "106.09.14"
    },
    {
        "title": "桃園市政府水務局工程交通維持計畫夜間稽查小組設置及作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001156",
        "category": "行政規則",
        "date": "105.05.11"
    },
    {
        "title": "桃園市政府水務局人民申請案件審查小組設置及作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001155",
        "category": "行政規則",
        "date": "104.06.30"
    },
    {
        "title": "桃園市轄管河川區域範圍申請綠美化使用要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002722",
        "category": "行政規則",
        "date": "115.07.20"
    },
    {
        "title": "桃園市山坡地違規使用查報取締要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001151",
        "category": "行政規則",
        "date": "115.07.17"
    },
    {
        "title": "桃園市政府水務局督導促進民間參與公共建設計畫辦理附屬設施作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002570",
        "category": "行政規則",
        "date": "114.11.26"
    },
    {
        "title": "桃園市市管河川區域使用行為保證金收取及退還基準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002576",
        "category": "行政規則",
        "date": "114.05.27"
    },
    {
        "title": "桃園市政府山坡地範圍劃定及檢討變更作業審議小組設置要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001154",
        "category": "行政規則",
        "date": "113.12.30"
    },
    {
        "title": "桃園市政府水務局大漢溪綠水兩岸園區管理要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002453",
        "category": "行政規則",
        "date": "112.12.08"
    },
    {
        "title": "桃園市污水下水道系統工程建設申請審查及查驗作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002145",
        "category": "行政規則",
        "date": "112.06.29"
    },
    {
        "title": "桃園市山坡地土地可利用限度查定工作要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001149",
        "category": "行政規則",
        "date": "111.01.17"
    },
    {
        "title": "桃園市雨水下水道設施設計審查及查驗管理要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002073",
        "category": "行政規則",
        "date": "109.06.17"
    },
    {
        "title": "桃園市政府處理違反水土保持法案件裁罰基準",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001159",
        "category": "行政規則",
        "date": "109.01.15"
    },
    {
        "title": "桃園市住宅既有污水處理設施廢除或改設及雨污水管渠分開設置補助要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001160",
        "category": "行政規則",
        "date": "108.12.26"
    },
    {
        "title": "桃園市公共污水下水道工作人員工作證管理要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002095",
        "category": "行政規則",
        "date": "108.12.06"
    },
    {
        "title": "桃園市申請市管防水建造物作為公路或一般道路使用處理原則",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001596",
        "category": "行政規則",
        "date": "106.04.12"
    },
    {
        "title": "桃園市政府水務局補助民間團體作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001220",
        "category": "行政規則",
        "date": "105.08.15"
    },
    {
        "title": "桃園市政府排水計畫書審查作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001158",
        "category": "行政規則",
        "date": "104.11.12"
    },
    {
        "title": "桃園市政府水務局職場霸凌防治申訴及調查處理要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL002620",
        "category": "行政規則",
        "date": "115.08.13"
    },
    {
        "title": "桃園市政府水務局公務人員安全及衛生防護小組設置及作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001933",
        "category": "行政規則",
        "date": "114.10.16"
    },
    {
        "title": "桃園市政府水務局內部控制工作小組設置及作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001221",
        "category": "行政規則",
        "date": "110.08.19"
    },
    {
        "title": "桃園市政府水務局懸帳清理小組設置及作業要點",
        "url": "https://law.tycg.gov.tw/LawContent.aspx?id=GL001157",
        "category": "行政規則",
        "date": "106.06.16"
    }
]


def main():
    output = {
        "metadata": {
            "title": "桃園市政府水務局便民資訊服務",
            "description": "整合桃園市政府水務局官方網站各項資訊，提供民眾輕鬆查詢與線上申請",
            "updated_at": datetime.now().isoformat(),
            "version": "2.2.0",
            "data_source": "桃園市政府水務局官方網站 (wrb.tycg.gov.tw)"
        },
        "service_links": SERVICE_LINKS,
        "gov_info_links": GOV_INFO_LINKS,
        "announcements": ANNOUNCEMENTS,
        "traffic_info": TRAFFIC_INFO,
        "business_info": BUSINESS_INFO,
        "faq": FAQ,
        "contact": CONTACT_INFO,
        "regulations": REGULATIONS
    }

    os.makedirs("docs", exist_ok=True)
    with open("docs/data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("資料生成完成，已輸出至 docs/data.json")
    print(f"  - 便民服務連結: {len(SERVICE_LINKS)} 項")
    print(f"  - 政府資訊公開: {len(GOV_INFO_LINKS)} 項")
    print(f"  - 業務資訊: {len(BUSINESS_INFO)} 項")
    print(f"  - 常見問答: {len(FAQ)} 項")
    print(f"  - 法規連結: {len(REGULATIONS)} 項")

if __name__ == "__main__":
    main()
