## mitmproxy-mobile
![](https://github.com/mym8989/mitmiproxy-mobile/blob/master/gaiyou.png)  
  
mitmproxyを使って、画像を圧縮＋広告を除去するプロキシです。  
  
画像圧縮は、https://qiita.com/tongari0/items/ffa3297630547c3bb712　をそのまま使いました。（感謝！）  
広告除去は、280blocksのリストを元に画面要素を削除しています。  
現状ではリスト内の、要素指定行（##で始まる行）のみが対象。  
GCPで環境構築していますが、遅いので広告除去は今は使っていません。  
（私はAdguardライセンス持ってるので、そっちで除去させてる）  
  
起動まで  
docker-compose build  
docker-compose up  
./login.sh　←これでmitmproxy-dockerの中に入れる  
./st.sh　←これでmitmprosyがポート8080で起動する  
  
この段階で、グローバルIPでも8080が公開されている。  
後はファイヤーウォールで8080を許可すればよい。  
  
実際の使い方  
Android  
　モバイルネットワークのAPN設定でプロキシをこれに指定してもできるが、それだとマップなど色んなアプリでSSLハンドシェークエラーがでる。  
　それでも通信したい場合は、st.shの無視リストに入れていくが、きりがないので、  
　Firefoxだけプロキシ設定を指定してブラウジングするのが良い。（その代わり他のアプリでは画像圧縮が効かない）。  
　Firefoxは、mozilaの証明書とmitmproxyの証明書の２つを、AndroidシステムじゃなくFirefoxに入れる必要がある点に注意。  
