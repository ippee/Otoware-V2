# Otoware-V2
「**音割れマイスター V2**（旧名：音割戦隊ウルセンジャー - ピークレッドV2）」とは、入力した音源のラウドネスを強制的に最大化し、音割れさせるプログラムおよびアプリです  
**本アプリの使用にはFFmpegのインストールが必須です**、各自でインストールをお願いいたします  
  　  
  　  
## 注意事項
<font color="red">**音割れ音源は耳だけでなく、再生機材にもダメージを与える危険があります  
このアプリを使っていかなる損害が発生したとしても、私は一切の責任を負いかねます**</font>  
耳とか再生機材は大切にね  
  　  
  　  
## exeファイルを作成しました！
「音割れマイスター_V2」の中にあるexeファイルがあれば動きます  
使用する際には、「**README.txt**」に目を通してください  
  　  
  　  
## アプリの使い方
１、**音割れマイスター.exe** を起動（時間がかかります）  
２、出力設定で、**サンプリングレート**と**ビット深度**を決める  
　　・サンプリングレートを上げるとほんのちょっとだけ音圧が上がります  
　　・ビット深度については、私が試した限りでは24bitより16bitの方が音圧は高くなりました  
　　・32/64bit floatは、音声自体がクリップするということはほぼありません（ただし音量は上がり続けます）  
３、**ラウドネスの推移をグラフで表示**するかどうかを決める  
４、最大で何dBFS音量を上げるか決める  
　　・大きくするほど処理に時間がかかります  
５、**音源を最適化** をクリックして、音割れさせるファイルを選択  
６、処理が終了するまで待機  
７、終了するとメッセージボックスがラウドネスに関係する情報付きで鳴ります  
　　・「ラウドネスの推移を表示」にチェックを入れていればグラフが表示されます  
  　  
### 使う上での注意
- FFmpegを使用する都合上、本アプリはコンソールの表示が有効になっています  
アプリ起動中にコンソールを閉じるとアプリも終了しますのでご注意ください
- 音声処理の途中、「srcWav.wav」「processing.wav」という２つのファイルを生成します  
前者は選択された音声ファイルを、一度.wavに変換してから処理に用いるためのファイルです  
後者は音声処理の途中経過ファイルです  
アプリのフリーズ等で音声処理が中断された場合、この２つが削除されない場合があります  
アプリを再起動すれば、これらのファイルは削除されます  
手動で消しても問題ありません
  　  
  　  
## V1と何が違うの？
### 音声処理をFFmpegのコマンドから実行  
V1ではpydubを使用していましたが、pydubで音量操作をした場合、ある一定ラインまで達すると音量が上げることが出来ませんでした  
V2ではsubprocessからFFmpegのコマンドを実行することでこの問題が解決し、本当の意味でのラウドネス最大化が可能になりました  
この問題の解決に伴い、<u>V1よりラウドネスをさらに高くできるようになりました</u>
  　  
### GUIの作成
GUI付けた方が私個人としては扱いやすいのでつけました
  　  
### ハイレゾ対応  
FFmpegのコマンドでハイレゾ音源を作れるようになったのでつけました  
（音割れハイレゾ音源とは）
  　  
  　  
## その他（補足など）
- 作業環境  
  - Windows 10
  - Python 3.6.4
- Pythonで動かしているので、基本的に挙動は遅いです  
起動ものっそりとしていますが、気長に待ってやってください  
- 「動けばなんでもいいだろ精神」で作っているので、コードの見やすさとか全く考えてないです()  
見にくかったらごめんなさい  
見やすいコードを書けるようになったら改訂する<u>かも</u>しれません  

## 更新履歴
- 2020/02/08: スペースが含まれるファイル名を読み込んだ時のバグを解消（V2.2）
- 2020/02/08: アプリ名変更、FFmpegコマンドの実行をffmpyからsubprocessに変更（V2.1）
- 2020/02/02: 本アプリ作成（V2.0）