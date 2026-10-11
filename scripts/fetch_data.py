
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桃園市政府水務局資料整合腳本
透過政府公開 API 抓取相關資訊

桃園資料開放平台 API 正確格式:
  https://data.tycg.gov.tw/api/v1/rest/datastore/{dataset_id}?format=json

回傳格式:
  {
    "success": true,
    "result": {
      "resource_id": "...",
      "fields": [...],
      "records": [...]   <-- 實際資料在此
    }
  }
"""

import requests
import json
import os
from datetime import datetime

# API 端點設定 (桃園料開放平台正確格式)
APIS = {
    "water_level": {
        "name": "水位站即時偵測資料",
        "url": "https://data.tycg.gov.tw/api/v1/rest/datastore/e3b34ba5-e8ff-4b21-b7a3-4b6f3bfed650?format=json",
        "source": "桃園市政府水務局",
        "description": "提供桃園市政府水務局建置之水位站即時監測資料"
    },
    "rainfall": {
        "name": "水情雨量資料",
        "url": "https://data.tycg.gov.tw/api/v1/rest/datastore/eabd93d1-d526-4de0-b378-b529aa61a4be?format=json",
        "source": "桃園市政府水務局",
        "description": "桃園水情雨量即時資料"
    },
    "welfare": {
        "name": "福利補助資訊",
        "url": "https://data.tycg.gov.tw/api/v1/rest/datastore/b20a8017-2736-448e-86e4-4032211073d7?format=json",
        "source": "桃園市政府",
        "description": "桃園市福利補助資訊，包含政策說明及申請資格"
    },
    "welfare_eligibility": {
        "name": "福利補助申請資格資訊",
        "url": "https://data.tycg.gov.tw/api/v1/rest/datastore/366c47d5-fa52-449c-89a5-230832ff7524?format=json",
        "source": "桃園市政府",
        "description": "桃園市各福利補助項目之申請資格查詢資訊"
    },
    "pump_station": {
        "name": "抽水機資料",
        "url": "https://data.tycg.gov.tw/api/v1/rest/datastore/328dc013-6d8a-41be-bacf-706d6c61a9de?format=json",
        "source": "桃園市政府水務局",
        "description": "桃園市政府水務局抽水機數量"
    }
}

# 水務局相關便民服務連結
SERVICE_LINKS = [
    {
        "title": "桃園市下水道雲端智慧管理系統",
        "url": "https://sewergis.tycg.gov.tw/PeopleApplyCase/PeopleApplyCase",
        "description": "污水案件獎勵補助申請、污水申請案件查詢、水肥證線上申請",
        "category": "補助申請"
    },
    {
        "title": "水情資訊網",
        "url": "https://winfo.tycg.gov.tw/tysafep/",
        "description": "即時水情、水位、雨量資訊查詢",
        "category": "資訊查詢"
    },
    {
        "title": "地下水管理智慧平台",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "地下水相關資訊與管理",
        "category": "資訊查詢"
    },
    {
        "title": "桃園網路e指通",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "線上申辦各項水務相關業務",
        "category": "線上申請"
    },
    {
        "title": "水利設施參訪預約系統",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "預約參訪水利設施",
        "category": "線上申請"
    },
    {
        "title": "申報案件查詢",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "查詢各項申報案件進度",
        "category": "資訊查詢"
    },
    {
        "title": "市管河川及區域排水公開資訊",
        "url": "https://wrb.tycg.gov.tw/",
        "description": "市管河川及區域排水相關公開資訊",
        "category": "資訊查詢"
    }
]

# 聯絡資訊
CONTACT_INFO = {
    "phone": "03-3322101",
    "extension": "6961、6962",
    "address": "330206桃園市桃園區縣府路1號",
    "service_hotline": "1999（桃園市境內）",
    "outside_hotline": "03-2189000（外縣市）",
    "email": "wrb@tycg.gov.tw",
    "hours": "星期一至星期五 上午8:00-12:00 下午1:00-5:00"
}


def fetch_api_data(api_config):
    """抓取單一 API 資料 (桃園 datastore 格式)"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        response = requests.get(api_config["url"], headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        # 桃園 datastore API 回傳格式:
        # {"success": true, "result": {"records": [...]}}
        records = None
        if data.get("success") and "result" in data:
            result = data["result"]
            if isinstance(result, dict) and "records" in result:
                records = result["records"]
            elif isinstance(result, list):
                records = result
        elif isinstance(data, list):
            records = data

        if records is not None:
            return {
                "success": True,
                "data": records,
                "count": len(records),
                "fetched_at": datetime.now().isoformat()
            }
        else:
            return {
                "success": True,
                "data": data,
                "count": "unknown",
                "fetched_at": datetime.now().isoformat()
            }

    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "error": f"HTTP {e.response.status_code}: {str(e)}",
            "fetched_at": datetime.now().isoformat()
        }
    except requests.exceptions.ConnectionError as e:
        return {
            "success": False,
            "error": f"連線失敗: {str(e)}",
            "fetched_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "fetched_at": datetime.now().isoformat()
        }


def main():
    results = {}

    # 抓取所有 API 資料
    for key, config in APIS.items():
        print(f"正在抓取: {config['name']}...")
        results[key] = {
            "config": config,
            "result": fetch_api_data(config)
        }
        status = "成功" if results[key]["result"]["success"] else "失敗"
        print(f"  -> {status}")

    # 建立輸出資料結構
    output = {
        "metadata": {
            "title": "桃園市政府水務局便民資訊服務",
            "description": "整合政府公開 API，提供民眾查詢水務局相關資訊",
            "updated_at": datetime.now().isoformat(),
            "data_source": "桃園市政府資料開放平台",
            "version": "1.1.0"
        },
        "apis": results,
        "service_links": SERVICE_LINKS,
        "contact": CONTACT_INFO
    }

    # 確保輸出目錄存在
    os.makedirs("docs", exist_ok=True)

    # 寫入 JSON 資料檔
    with open("docs/data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("\n資料抓取完成，已輸出至 docs/data.json")

    # 輸出摘要
    success_count = sum(1 for v in results.values() if v["result"]["success"])
    total = len(results)
    print(f"成功: {success_count}/{total} 個 API")


if __name__ == "__main__":
    main()
