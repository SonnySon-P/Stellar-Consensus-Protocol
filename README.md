# SCP
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
