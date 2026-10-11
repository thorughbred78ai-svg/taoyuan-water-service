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
        "description": "負責水資源綜合規劃、施政計畫研擬、水利相關政策規劃等業務。",
        "services": ["水資源規劃", "施政計畫", "政策研擬"]
    },
    {
        "title": "水利防災科",
        "description": "負責水利防災相關業務，包含防汛整備、災害搶修、防洪設施管理等。",
        "services": ["防汛整備", "災害搶修", "防洪設施管理", "水情監測"]
    },
    {
        "title": "水利行政科",
        "description": "負責水利行政業務，包含河川管理、排水設施管理、水利法規執行等。",
        "services": ["河川管理", "排水設施管理", "水利法規執行", "許可審查"]
    },
    {
        "title": "水利工程科",
        "description": "負責水利工程規劃設計、發包監造、施工管理等業務。",
        "services": ["工程規劃設計", "工程發包監造", "施工管理", "工程驗收"]
    },
    {
        "title": "水利養護工程科",
        "description": "負責水利設施養護、河道疏濬、設施維修等業務。",
        "services": ["設施養護", "河道疏濬", "設施維修", "清淤工程"]
    },
    {
        "title": "河岸地工程管理科",
        "description": "負責河岸地管理、河川區域使用管理、河岸設施維護等業務。",
        "services": ["河岸地管", "河川區域使用管理", "河岸設施維護", "容積移轉"]
    },
    {
        "title": "污水企劃工程科",
        "description": "負責污水下水道系統規劃、設計、工程發包等業務。",
        "services": ["污水系統規劃", "污水工程設計", "工程發包"]
    },
    {
        "title": "污水促參計畫工程科",
        "description": "負責污水下水道促參計畫、BOT 工程管理等業務。",
        "services": ["促參計畫", "BOT 工程管理", "民間參與"]
    },
    {
        "title": "污水設施管理工程科",
        "description": "負責污水處理廠、污水管線、用戶接管等設施管理業務。",
        "services": ["污水處理廠管理", "污水管線管理", "用戶接管", "設施維護"]
    },
    {
        "title": "坡地管理科",
        "description": "負責山坡地管理、土石流防災、水土保持等業務。",
        "services": ["山坡地管理", "土石流防災", "水土保持", "容積移轉"]
    },
    {
        "title": "雨水下水道科",
        "description": "負責雨水下水道系統規劃、建設、管理與維護業務。",
        "services": ["雨水下水道規劃", "建設管理", "設施維護", "清淤作業"]
    },
    {
        "title": "再生水企劃管理工程科",
        "description": "負責再生水利用規劃、推動與管理相關業務。",
        "services": ["再生水規劃", "再生水推動", "水資源再利用"]
    }
]

# 常見問答
FAQ = [
    {
        "question": "如何申請污水下水道用戶接管？",
        "answer": "可透過「下水道雲端智慧管理系統」線上申請，或至水務局臨櫃辦理。申請時需準備建築物相關證明文件。部分污水用戶接管工程可申請獎勵補助。"
    },
    {
        "question": "水情資訊如何查詢？",
        "answer": "可至「水情資訊網」(winfo.tycg.gov.tw/tysafep/) 查詢即時雨量、水位、淹水警戒、土石流警戒等防災資訊。"
    },
    {
        "question": "山坡地容積移轉如何申請？",
        "answer": "請至水務局「容積移轉專區」查詢各河川得申請容積移轉土地清冊與相關規定，或洽河岸地工程管科、坡地管理科辦理。"
    },
    {
        "question": "污水下水道工程是否有補助？",
        "answer": "部分污水用戶接管工程可申請獎勵補助，詳情請至「下水道雲端智慧管理系統」查詢或洽污水設施管理工程科。另有「污水下水道排水設備接管融資專案」可供參考。"
    },
    {
        "question": "如何預約參訪水利設施？",
        "answer": "可透過「水利設施參訪預約系統」(winfo.tycg.gov.tw/R/) 線上預約，可選擇桃園北區、龜山、石門、大溪、楊梅水資源回收中心，以及文青水園、龍山滯洪池、大樹林滯洪池、山豬湖生態親水園區等設施。"
    },
    {
        "question": "發現排水溝堵塞或積水如何通報？",
        "answer": "可撥打 1999 市民服務專線通報，或聯繫水務局水利養護工程科處理。也可使用「水情看桃園APP」進行淹水通報。"
    },
    {
        "question": "水肥清除許可證如何申請？",
        "answer": "可透過「下水道雲端智慧管理系統」線上申請水肥證，需準備相關車輛及公司資料，包含投肥證申請書、自主檢核表、切結書、廢棄物清除許可證等文件。"
    },
    {
        "question": "河川區域內可以從事哪些活動？",
        "answer": "河川區域內活動需依水利法規申請許可，詳情請洽水利行政科或查詢相關法規。未經許可不得於河川區域內從事相關行為。"
    },
    {
        "question": "水務局怎麼去？",
        "answer": "地址為 33043 桃園市桃園區成功路一段32號7樓（桃園國小旁、郵政總局對面）。可搭公車至「桃園郵局」站牌下車。建議先至桃園市公車動態資訊網查詢乘車規劃。"
    },
    {
        "question": "如何查詢自家附近有無污水管線？",
        "answer": "可至「污水系統公告範圍」頁面查詢，了解自家是否位於污水下水道系統公告使用地區範圍內。"
    }
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

# 法規資訊連結
REGULATIONS = [
    {"title": "水利法", "url": "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0110001"},
    {"title": "河川管理辦法", "url": "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=J0110005"},
    {"title": "下水道法", "url": "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=O0040001"},
    {"title": "水土保持法", "url": "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=M0110001"},
    {"title": "桃園市河川管理自治條例", "url": "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=O0040011"}
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
