# ptt-gossip-parker
PTT 八卦版鄉民參與度統計
  
### 功能
輸入一個標題關鍵字，爬蟲程式會去爬最近 200 篇相關文章  
並統計所有帳號參與的文章篇數 ( 只要有推文就算 )  
  
  
### 執行
若有 python 環境，則可直接 clone source 並執行：  
```
python3 parker.py 關鍵字
```
若無，則可直接從[此處下載](https://github.com/nopixel/ptt-gossip-parker/releases) Binary 檔，並在 command line 執行
```
# win command 
./parker.exe 關鍵字

# mac command 
./parker 關鍵字
```

### 輸出
會產生一個 gossip_{關鍵字}_{日期} 的資料夾，點選資料夾中的 index.html 即可觀看結果



