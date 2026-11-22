# DevFest 台中 2026｜報帳 Agent 安全實作

Alice 可以查自己的報帳。如果她要求查 Bob 的單，究竟是模型、Google 的安全服務，還是報帳程式決定要不要執行？這是「從 MCP Tool Poisoning 到 Google Cloud Agent Security 實戰」的聽眾教材。所有金額、單號與人物都是合成資料。

[下載台中場投影片（PDF，59 頁）](https://raw.githubusercontent.com/Ko-Ko-Kirk/2026GoogleDevFestTaichung-Workshop/main/slides/DevFest-Taichung-2026.pdf)

講者原創的投影片文字與圖解沿用教材的 [MIT 授權](LICENSE)。書封、商標與第三方截圖的權利屬於各權利人。

## 跑一遍 Alice 的例子

使用 Python 3.10 或更新版本，在專案根目錄執行。只用 Python 標準函式庫，不需雲端帳號或 API 金鑰。

```sh
python3 workshop.py check EXP-ALICE
python3 workshop.py check EXP-BOB
```

第一行讀到金額 120，狀態為待審核。第二行顯示拒絕並回傳狀態碼 1。兩次登入者都是 Alice，程式從可信任的身分資料查單據歸屬。[查看授權規則](devfest_security/policy.py)

## 核對工具清單

```sh
python3 workshop.py manifest examples/approved-tools.json
python3 -m unittest -v
```

核准的清單隨教材提供。測試會複製一份清單，只改一行普通的工具說明，確認程式能發現差異。正式系統需限制核准基準的寫入權，由有權限的人審核變更。[核准清單](examples/approved-tools.json) · [核對程式](workshop.py)

## 讀取演講中的雲端實測

```sh
python3 workshop.py replay alice
python3 workshop.py replay bob
python3 workshop.py replay cloud
```

這三個指令只讀取已存檔的結果。前兩個案例是 Vertex AI 的 Gemini 4 Hydrogen 彩排。Alice 查自己時執行了一次工具，留下 1 張收據；查 Bob 時，應用程式拒絕，收據為 0。第三個指令列出較早的六案測試、私有 Cloud Run 的身分驗證及獨立的遠端 Agent Runtime 查詢。六案當中有三案呼叫了 Gemini Developer API，使用 Gemini 3.1 Flash-Lite。[Hydrogen 紀錄](examples/hydrogen-stage.json) · [雲端實測摘要](examples/cloud-summary.json)

## 報帳助理怎麼用到 Google Cloud？

| 問題 | 實測中的分工 |
| --- | --- |
| Agent 在哪裡執行？ | 遠端查詢使用 Agent Runtime 執行 LangGraph，由服務帳戶取得 Secret Manager 的模型金鑰。 |
| 哪個服務能連到工具？ | 自建的報帳 MCP 部署在私有 Cloud Run，IAM 驗證呼叫端身分。單據權限由報帳程式核對。 |
| 工具說明改了，誰能發現？ | LangGraph 主動送工具定義給 Model Armor。清單完整性另由程式比對核准基準。 |
| 怎麼查證工具真的跑過？ | Cloud Logging 可按執行編號找到工具事件，再從 Cloud Storage 讀回收據及帳本，核對有無變更。 |

Google 也提供 [BigQuery 遠端 MCP](https://docs.cloud.google.com/bigquery/docs/use-bigquery-mcp) 等代管端點。這場報帳 Demo 使用的是自己寫的 MCP。延伸閱讀見 [Agent Runtime](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/runtime)、[Cloud Run 服務身分驗證](https://docs.cloud.google.com/run/docs/authenticating/service-to-service) 和 [Model Armor](https://docs.cloud.google.com/model-armor/overview)。

如果這份教材對你有幫助，歡迎按右上角的 **Star**，下次設計工具授權時回來查。授權條款見 [MIT License](LICENSE)。
