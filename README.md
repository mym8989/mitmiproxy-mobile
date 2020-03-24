## mitmproxy-mobile
![](https://github.com/mym8989/mitmiproxy-mobile/blob/master/gaiyou.png)  
  
mitmproxyを使って、画像を圧縮＋広告を除去するプロキシです。  
  
画像圧縮は、https://qiita.com/tongari0/items/ffa3297630547c3bb712　をそのまま使いました。（感謝！）  
広告除去は、280blocksのリストを元に画面要素を削除しています。  
現状ではリスト内の、要素指定行（##で始まる行）のみが対象。  
GCPで環境構築していますが、遅いので広告除去は今は使っていません。  
（私はAdguardライセンス持ってるので、そっちで除去させてる）  

