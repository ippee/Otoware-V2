# coding: UTF-8

##################################################
# 
# 【Readme】 
# 音割戦隊ウルセンジャー ピークレッド V2では、
# 人間の聴覚特性を考慮した音のうるささを測る指標「ラウドネス」を用いることで、
# 人間が最もうるさいと感じる真の音割れ音源の生成します
# （測定アルゴリズム: ITU-R BS.1770）
# 
# ・V1との変更点
#   - 音声処理にffmpyを使用
#   - GUIの作成
#   - ハイレゾ対応
#
# 音割れ音源は耳に悪いだけでなく、再生機器にもダメージを与える危険があります
# 本アプリによっていかなる損害等が発生したとしても、製作者は一切の責任を負いかねます
# 
# いっぺー (Twitter: @ippee1410)
# 
##################################################

import soundfile as sf
import pyloudnorm as pyln
import os
from ffmpy import FFmpeg
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
from matplotlib import pyplot



### 関数定義 ###
# オーディオファイルを書き出す関数
def ffmpegWrite(input, output, volume, sample, bit): # input, outputは拡張子込み
    ff = FFmpeg(
        inputs={input: None}, 
        outputs={output: '-ar ' + str(sample) + ' -c:a pcm_' + bit + ' -af "volume=' + str(volume) + 'dB"'}
    )
    ff.cmd
    ff.run() # 実行されるコマンドは、ffmpeg -i (input) -af "volume = i dB" (output)

# ラウドネスを測定する関数
def measureLoudness(input):
    CheckLoudness, rate = sf.read(input) # オーディオ読み込み
    meter = pyln.Meter(rate) # ラウドネスメーター生成
    result = meter.integrated_loudness(CheckLoudness) # Integrated Loudnessを測定
    return result

# ボタンを押したときに動く関数
def AudioProcessing(n, sample, bit, blnLoud):
    # 音声読み込み
    typ = [('', '*'), ('wav','*.wav'), ('mp3','*.mp3'), ('ogg','*.ogg'), ('flac','*.flac'), ('wma','*.wma'), ('aac','*.aac'), ('m4a','*.m4a')] 
    dir = os.getcwd()
    path = tkinter.filedialog.askopenfilename(filetypes = typ, initialdir = dir)
    path = path.replace("/", "\\")
    
    FileName = path[path.rfind( "\\" ) + 1 : path.rfind(".")] # ファイル名取得
    ffmpegWrite(path, "srcWav.wav", 0, sample, bit)
    LUFS_start = measureLoudness("srcWav.wav") # 原曲のIntegrated Loudnessを測定


    # 音声処理
    LUFS = [[] for i in range(n)] # ラウドネスの測定結果をLUFSに代入していく

    for i in range(n):
        ffmpegWrite("srcWav.wav", "processing.wav", i, sample, bit) # i[dB]だけ音量を上げる
        LUFS[i] = measureLoudness("processing.wav") # 音量操作後のIntegrated Loudnessを測定
        os.remove("processing.wav") # ffmpyではファイルの上書きができないので、音量操作後のファイルを一度消す必要がある


    # 音声出力
    max_value = max(LUFS) # ラウドネスの最大値を取得
    max_index = LUFS.index(max_value) # そのインデックスを取得

    if os.path.exists("音割れ"+FileName+".wav") == True:
        os.remove("音割れ"+FileName+".wav")
    ffmpegWrite("srcWav.wav", "音割れ"+FileName+".wav", max_index, sample, bit)
    os.remove("srcWav.wav")


    # 結果表示
    tkinter.messagebox.showinfo("音割れ完了", "ラウドネスを最大化しました\n\n" + "・Before: " + str(round(LUFS_start, 3)) + " LUFS\n" + "・After: " + str(round(max_value, 3)) + " LUFS\n" + "・音量変化: +" + str(max_index) + "dB")
    if blnLoud == True:
        x = [i+1 for i in range(n)]
        pyplot.plot(x, LUFS) # ラウドネスの変化をグラフで表示
        pyplot.xlabel("Gain [dB]")
        pyplot.ylabel("Loudness [LUFS]")
        pyplot.show()
        


### ウインドウ設定 ###
root = tk.Tk()
root.title("音割戦隊ウルセンジャー ピークレッド V2")
root.geometry("340x570")
root.resizable(0,0)

image1 = tk.PhotoImage(file = "bg.png")
tk.Label(root, image=image1).pack()

discription = tk.Label(root, text="楽曲のラウドネスを最大化し、高品質な音割れ音源を生成します\n（測定アルゴリズム: ITU-R BS.1770）")
discription.pack(pady=10, side="top")

### ウィジェット ###
blnLoud = tk.BooleanVar()
blnLoud.set(True) # ラウドネスの推移を表示するか否か
sample = tk.IntVar()
sample.set(44100) # サンプリングレートの初期値
n = 151 # 最大ゲインの初期値
dB = tk.Entry(root)
bit = tk.StringVar()
bit.set("s16le") # ビット深度の初期値

# 最適化開始ボタン
def pushed():
    n = dB.get()
    AudioProcessing(int(n)+1, sample.get(), bit.get(), blnLoud.get())

button = tk.Button(root, text="音源を最適化", command=pushed)
button.pack(pady=10, side="bottom")

# 最大ゲイン
dB.pack(pady=10, side="bottom")
dB.insert(tk.END, n-1)
opt1 = tk.Label(root, text="\n【最大ゲイン [dB]】")
opt1.pack(side="bottom")

# ラウドネスの推移の表示
c1 = tk.Checkbutton(root, text="ラウドネスの推移を表示", variable=blnLoud)
c1.pack(side="bottom")

# 出力設定
opt2 = tk.Label(root, text="【出力設定】")
opt2.pack(side="top")

# サンプリングレート
frame1 = ttk.LabelFrame(root,text="サンプリングレート")
for x in (44100, 48000, 96000, 192000):
    tk.Radiobutton(frame1, text = '{} Hz'.format(x), value = x, variable = sample).pack()
frame1.pack(padx=57, pady=10, side="left", anchor=tk.N)

# ビット深度
frame2 = ttk.LabelFrame(root,text="ビット深度")
SampleRateList = ["16 bit", "24 bit", "32 bit float", "64 bit float"]
ValuesList = ["s16le", "s24le", "f32le", "f64le"]
for i in range(len(SampleRateList)):
    tk.Radiobutton(frame2, text = SampleRateList[i], value = ValuesList[i], variable = bit).pack()
frame2.pack(pady=10, side="left", anchor=tk.N)

# 出力
root.mainloop()