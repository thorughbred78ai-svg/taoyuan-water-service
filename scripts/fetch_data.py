#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桃園市政府水務局資料生成腳本
不依賴外部 API，直接生成靜態 JSON 資料供前端使用
"""

import json
import os
from datetime import datetime

# 便民服務連結
SERVICE_LINKS = [
    {
        "title": "桃園市下水道雲端智慧管理系統",
        "url": "https://sewergis.tycg.gov.tw/PeopleApplyCase/PeopleApplyCase",
        "description": "污水案件獎勵補助申請、污水申請案件查詢、水肥證線上申請",
        "category": "補助申請",
        "icon": "💰"
    },
    {
        "title": "水情資訊網",
        "url": "https://winfo.tycg.gov.tw/tysafep/",
        "description": "即時水情、水位、雨量資訊查詢，淹水警戒、土石流警戒防災資訊",
        "category": "資訊查詢",
        "icon": "💧"
    },
    {
        "title": "地下水管理智慧平台",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "地下水相關資訊與管理，包含監測資料與管理措施",
        "category": "資訊查詢",
        "icon": "🌊"
    },
    {
        "title": "桃園網路e指通",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "線上申辦各項水務相關業務，免出門即可完成申請",
        "category": "線上申請",
        "icon": "🖱️"
    },
    {
        "title": "水利設施參訪預約系統",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "預約參訪水利設施，了解水資源管理與防洪設施",
        "category": "線上申請",
        "icon": "🏗️"
    },
    {
        "title": "申報案件查詢",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "查詢各項申報案件進度，隨時掌握申請狀態",
        "category": "資訊查詢",
        "icon": "🔍"
    },
    {
        "title": "市管河川及區域排水公開資訊",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "市管河川及區域排水相關公開資訊，包含治理規劃與現況",
        "category": "資訊查詢",
        "icon": "🏞️"
    },
    {
        "title": "重大點源放流水自動連續監測資訊公開查詢系統",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "查詢重大污染源放流水監測資料，確保水質安全",
        "category": "資訊查詢",
        "icon": "📊"
    },
    {
        "title": "龜山水肥站水肥投入預約系統",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "水肥站投入預約服務，方便管理水肥處理",
        "category": "線上申請",
        "icon": "📅"
    },
    {
        "title": "檔案應用專區",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "申請閱覽、抄錄或複製本局檔案資料",
        "category": "線上申請",
        "icon": "📁"
    },
    {
        "title": "容積移轉專區",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "山坡地容積移轉相關資訊與申請說明",
        "category": "資訊查詢",
        "icon": "🏔️"
    },
    {
        "title": "污水系統公告範圍",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "查詢污水下水道系統公告使用範圍",
        "category": "資訊查詢",
        "icon": "🚰"
    }
]

# 業務資訊
BUSINESS_INFO = [
    {
        "title": "綜合企劃科",
        "description": "負責水資源綜合規劃、施政畫研擬、水利相關政策規劃等業務。",
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
        "services": ["河岸地管理", "河川區域使用管理", "河岸設施維護"]
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
        "services": ["山坡地管理", "土石流防災", "水土保持", "容移轉"]
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
        "answer": "可透過「桃園市下水道雲端智慧管理系統」線上申請，或至水務局臨櫃辦理。申請時需準備建築物相關證明文件。"
    },
    {
        "question": "水情資訊如何查詢？",
        "answer": "可至「水情資訊網」(winfo.tycg.gov.tw/tysafep/) 查詢即時雨量、水位、淹水警戒等資訊。"
    },
    {
        "question": "山坡地容積移轉如何申請？",
        "answer": "請至水務局「容積移轉專區」查詢相關規定與申請流程，或洽坡地管理科辦理。"
    },
    {
        "question": "污水下水道工程是否有補助？",
        "answer": "部分污水用戶接管工程可申請獎勵補助，詳情請至「下水道雲端智慧管理系統」查詢或洽污水設施管理工程科。"
    },
    {
        "question": "如何預約參訪水設施？",
        "answer": "可透過「水利設施參訪預約系統」線上預約，或電洽水務局相關科別安排。"
    },
    {
        "question": "發現排水溝堵塞或積水如何通報？",
        "answer": "可撥打 1999 市民服務專線通報，或聯繫水務局水利養護工程科處理。"
    },
    {
        "question": "水肥清除許可證如何申請？",
        "answer": "可透過「下水道雲端智慧管理系統」線上申請水肥證，需準備相關車輛及公司資料。"
    },
    {
        "question": "河川區域內可以從事哪些活動？",
        "answer": "河川區域內活動需依水利法規申請許可，詳情請洽水利行政科或查詢相關法規。"
    }
]

# 聯絡資訊
CONTACT_INFO = {
    "phone": "03-3322101",
    "extension": "6961、6962",
    "address": "330206 桃園市桃園區縣府路1號",
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
            "description": "整合桃園市政府水務局各項資訊，提供民眾輕鬆查詢與線上申請",
            "updated_at": datetime.now().isoformat(),
            "version": "2.0.0",
            "data_source": "桃園市政府水務局官方網站"
        },
        "service_links": SERVICE_LINKS,
        "business_info": BUSINESS_INFO,
        "faq": FAQ,
        "contact": CONTACT_INFO,
        "regulations": REGULATIONS
    }

    os.makedirs("docs", exist_ok=True)
    with open("docs/data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("靜態資料生成完成，已輸出至 docs/data.json")
    print(f"  - 便民服務連結: {len(SERVICE_LINKS)} 項")
    print(f"  - 業務資訊: {len(BUSINESS_INFO)} 項")
    print(f"  - 常見問答: {len(FAQ)} 項")
    print(f"  - 法規連結: {len(REGULATIONS)} 項")

if __name__ == "__main__":
    main()
