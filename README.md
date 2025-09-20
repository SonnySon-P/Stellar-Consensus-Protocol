# SCP Simulation

在撰寫論文的研究過程中，為深入掌握SCP（Secure Consensus Protocol）的運作機制，本人特別進行相關實作練習，涵蓋網路建構、提案發起、訊息接受與共識達成等流程，以強化理論與實務之結合。

## 壹、基本說明
**一、目標：**
為實現SCP（Secure Consensus Protocol）演算法，本專案於單機環境中模擬多個網路節點間的共識流程。系統會隨機生成節點，並透過具廣播能力的單一節點以UDP（User Datagram Protocol）協定建立網路，凡可被搜尋到之節點皆視為信任節點（假設不進行節點的信任投票）。 每個節點將構成一個「投票切片」（Quorum Slice），並向其信任夥伴發送議題投票請求。當回應的節點數量達到預設的支持閾值，即進入「接受階段」（Accept Phase）。 當某議題在多個節點及其投票切片間取得一致意見後，即進入「確認階段」（Confirm Phase），並正式記錄該共識結果。

**二、開發環境：**
以下是開發該平台所採用的環境：
* 程式語言：Python
* 虛擬環境：Anaconda
* 程式編輯器：Visual Studio Code

**三、使用相依套件：**
以下是開發該平台所使用的Python套件：
* Pygame
* Numpy

## 貳、操作說明
**一、安裝程式方式：** 
請從GitHub下載aodv.py檔案，具體操作步驟如下所示：
1. 請確認您的電腦已正確安裝Python、Pygame及Numpy套件，以確保程式能順利執行。
2. 請開啟終端機，切換至scp.py所在的資料夾，並執行以下指令：
```bash
python scp.py
```

**二、運行結果：**
執行aodv.py後，畫面將呈現出類似以下的模擬結果。
<br>
  <div align="center">
  	<img src="./截圖.png" alt="Editor" width="500">
  </div>
<br>


撰寫一個基於 SCP（Secure Consensus Protocol）演算法的 Python 程式，並且讓各個節點通過 RESTful API 進行通信，實現提案、認證、投票和認同的流程，是一個有挑戰的任務。以下是這個系統的大致設計：
node1 發起同步提案，內容是檔案 photo.jpg
node2, node3 收到提案後比對：
有無備份過這檔案
若未備份過，投 "yes"
一旦有過半節點同意：
所有節點自動執行 SCP 傳送 photo.jpg 到所有 trust_set 內節點
每個節點都在自己的 backup_log 中記錄該檔案已備份
1. **Node 類別**：
    - 每個節點擁有一個日誌 (`log`) 和一個信任集 (`trust_set`)，信任集是由其他節點組成的列表。
    - 當節點有新的日誌條目時，它會發起提案 (`propose`)。
    - 提案會被其他節點認證，並且投票支持或拒絕。
    - 當一個提案獲得足夠支持時，節點將接受該提案並更新其日誌。

2. **RESTful API**：
    - 我們設置了三個端點：
        - `/propose`：用來接收來自其他節點的提案。
        - `/vote`：用來接收來自其他節點的投票。
        - `/status`：用來查看所有節點的最新日誌狀態。

### 設計思路
1. **節點（Node）**：每個節點有自己的日誌，並且能夠與其他節點進行通信。當日誌中有新的條目時，它會發起提案。
2. **提案（Proposal）**：當有新的條目被添加到日誌中，節點會將這個條目作為提案發送給其他節點。
3. **認證（Certification）**：接收到提案的節點會進行認證，確保該提案是可信的。
4. **投票（Voting）**：節點根據其信任集合投票支持或拒絕提案。
5. **認同（Acceptance）**：當一個提案獲得足夠的支持票時，節點將接受這個提案，並將其更新到自己的日誌中。

### 基本設置
我們會使用 Flask 來搭建 RESTful API，並使用 Python 標準庫來實現節點邏輯和共識算法。

### 程式碼設計

#### 1. 安裝 Flask
首先，需要安裝 Flask：
```bash
pip install flask
```
SCP（Stellar Consensus Protocol）相對適合在移動環境中使用，例如：車聯網、行動裝置、無人機集群

動態維護 quorum slices（信任集）定期更新「我信任誰」來維持共識能力 主動查詢可信節點服務
每個節點各自決定要信任誰，但整體會透過 slice 交錯產生全球共識
Node A 新增 log，發起 proposal。
Node B、C 接收 /propose，進行認證、投票，並對 Node A、B、C 發送 /vote。
每個節點接收 /vote，呼叫 receive_vote()，統計投票數。
達到 quorum 時呼叫 accept_proposal()，更新本地 log。
