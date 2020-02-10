# coding: UTF-8

import soundfile as sf
import pyloudnorm as pyln
import os
import sys
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk as ttk
from matplotlib import pyplot

ver = "Ver. 2.3"

### 関数定義 ###
# リソースファイルを参照する関数（参考：https://qiita.com/firedfly/items/f6de5cfb446da4b53eeb）
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# オーディオファイルを書き出す関数
def audioWrite(input, output, volume, sample, bit): # input, outputは拡張子込み
    input = '"{}"'.format(input)
    cmd = 'ffmpeg -hide_banner -i {} -ar {} -c:a pcm_{} -af "volume = {} dB" {}'.format(input, sample, bit, volume, output)
    os.system(cmd)


# ラウドネスを測定する関数
def measureLoudness(input):
    CheckLoudness, rate = sf.read(input) # オーディオ読み込み
    meter = pyln.Meter(rate) # ラウドネスメーター生成
    result = meter.integrated_loudness(CheckLoudness) # Integrated Loudnessを測定
    return result


# 音声処理をする関数
def AudioAnalyze(bln, n, sample, bit):
    if bln == False: # クイックスキャン無効時の音声処理
        first_or_mid = ""
        LUFS = [0 for i in range(n)] # ラウドネスの測定結果をLUFSに代入していく
        for i in range(n):
                print("+ {} dB".format(i))
                audioWrite("srcWav.wav", "processing.wav", i, sample, bit) # i[dB]だけ音量を上げる
                LUFS[i] = measureLoudness("processing.wav") # 音量操作後のIntegrated Loudnessを測定
                os.remove("processing.wav") # ファイルの上書きができないので、ファイルを消す必要がある

        max_value = max(LUFS) # ラウドネスの最大値を取得
        max_index = LUFS.index(max_value) # そのインデックスを取得

    else: # クイックスキャン有効時の音声処理
        # 1, 最大ゲインの半分あたりのLUFSを２つ取得（testLUFS[round(n/2)], testLUFS[round(n/2)+1]）
        # 2, 前者より後者の方が小さければ、ゲインをマイナスしていって最大値を求める
        # 3, それ以外は、ゲインをプラスしていって最大値を求める

        testLUFS = [0,0]
        for i in [0, 1]:
            print("+ {} dB".format(round(n/2)+i))
            audioWrite("srcWav.wav", "processing.wav", round(n/2)+i, sample, bit) # i[dB]だけ音量を上げる
            testLUFS[i] = measureLoudness("processing.wav") # 音量操作後のIntegrated Loudnessを測定
            os.remove("processing.wav") # ファイルの上書きができないので、ファイルを消す必要がある
        
        LUFS = [0 for i in range(round(n/2))] # ラウドネスの測定結果をLUFSに代入していく
        if testLUFS[0] > testLUFS[1]:
            first_or_mid = "first"
            for i in range(round(n/2)):
                print("+ {} dB".format(i))
                audioWrite("srcWav.wav", "processing.wav", i, sample, bit) # i[dB]だけ音量を上げる
                LUFS[i] = measureLoudness("processing.wav") # 音量操作後のIntegrated Loudnessを測定
                os.remove("processing.wav") # ファイルの上書きができないので、ファイルを消す必要がある
            max_value = max(LUFS) # ラウドネスの最大値を取得
            max_index = LUFS.index(max_value) # そのインデックスを取得
        else:
            first_or_mid = "mid"
            for i in range(round(n/2)):
                print("+ {} dB".format(round(n/2)+i))
                audioWrite("srcWav.wav", "processing.wav", round(n/2)+i, sample, bit) # i[dB]だけ音量を上げる
                LUFS[i] = measureLoudness("processing.wav") # 音量操作後のIntegrated Loudnessを測定
                os.remove("processing.wav") # ファイルの上書きができないので、ファイルを消す必要がある
            max_value = max(LUFS) # ラウドネスの最大値を取得
            max_index = round(n/2) + LUFS.index(max_value) # そのインデックスを取得
    
    return LUFS, max_value, max_index, first_or_mid



# ボタンを押したときに動く関数
def AudioProcessing(n, sample, bit, blnPlot, blnQuick):
    # ボタン止める
    global button
    button.config(state="disable", text="処理中……")

    # 音声読み込み
    typ = [('', '*'), ('wav','*.wav'), ('mp3','*.mp3'), ('ogg','*.ogg'), ('flac','*.flac'), ('wma','*.wma'), ('aac','*.aac'), ('m4a','*.m4a')] 
    dir = os.getcwd()
    path = tkinter.filedialog.askopenfilename(filetypes = typ, initialdir = dir)
    if path == "":
        button.config(state="active", text="音源を最適化")
        return "break"
    
    # ファイル名取得
    path = path.replace("/", "\\")
    FileName = path[path.rfind( "\\" ) + 1 : path.rfind(".")] 
    audioWrite(path, "srcWav.wav", 0, sample, bit)
    LUFS_start = measureLoudness("srcWav.wav") # 原曲のIntegrated Loudnessを測定

    # 音声処理
    LUFS, max_value, max_index, first_or_mid = AudioAnalyze(blnQuick, n, sample, bit)

    # 音声出力
    if os.path.exists("音割れ"+FileName+".wav") == True:
        os.remove("音割れ"+FileName+".wav")
    print("+ {} dB".format(max_index))
    audioWrite("srcWav.wav", '"音割れ{}.wav"'.format(FileName), max_index, sample, bit)
    os.remove("srcWav.wav")

    # ボタン復活
    button.config(state="active", text="音源を最適化")

    # 結果表示
    tkinter.messagebox.showinfo("音割れ完了", "ラウドネスを最大化しました\n\n" + "・Before: " + str(round(LUFS_start, 3)) + " LUFS\n" + "・After: " + str(round(max_value, 3)) + " LUFS\n" + "・音量変化: +" + str(max_index) + "dB")
    if blnPlot == True:
        if first_or_mid == "first":
            x = [i for i in range(round(n/2))]
        elif first_or_mid == "mid":
            x = [round(n/2)+i for i in range(round(n/2))]
        else:
            x = [i for i in range(n)]
        pyplot.plot(x, LUFS) # ラウドネスの変化をグラフで表示
        pyplot.xlabel("Gain [dB]")
        pyplot.ylabel("Loudness [LUFS]")
        pyplot.Figure()
        thismanager = pyplot.get_current_fig_manager()
        thismanager.window.wm_iconbitmap(resource_path("src/icon.ico"))
        pyplot.show()



### ウインドウ設定 ###
root = tk.Tk()
root.title("音割れマイスター " + ver)
root.geometry("340x570")
root.resizable(0,0)
root.iconbitmap(default=resource_path("src/icon.ico"))

image1 = tk.PhotoImage(file = resource_path("src/bg.png"))
tk.Label(root, image=image1).pack()

discription = tk.Label(root, text="楽曲のラウドネスを最大化し、高品質な音割れ音源を生成します\n（測定アルゴリズム: ITU-R BS.1770）")
discription.pack(pady=10, side="top")



### ウィジェット ###
# 残ってしまった.wavファイルの削除
if os.path.exists("processing.wav") == True:
    os.remove("processing.wav")
if os.path.exists("srcWav.wav") == True:
    os.remove("srcWav.wav") 

# 変数設定
blnPlot = tk.BooleanVar()
blnPlot.set(True) # ラウドネスの推移を表示するか否か
blnQuick = tk.BooleanVar()
blnQuick.set(True) # クイックスキャンを有効にするか否か
sample = tk.IntVar()
sample.set(44100) # サンプリングレートの初期値
n = 151 # 最大ゲインの初期値
bit = tk.StringVar()
bit.set("s16le") # ビット深度の初期値

# 最適化開始ボタン
def pushed():
    global dB
    n = dB.get()
    AudioProcessing(int(n)+1, sample.get(), bit.get(), blnPlot.get(), blnQuick.get())

button = tk.Button(root, text="音源を最適化")
button.config(command=pushed)
button.pack(pady=10, side="bottom")

# 最大ゲイン
dB = tk.Entry(root)
dB.pack(pady=10, side="bottom")
dB.insert(tk.END, n-1)
opt1 = tk.Label(root, text="\n【最大ゲイン [dB]】")
opt1.pack(side="bottom")

# ラウドネスの推移の表示
c1 = tk.Checkbutton(root, text="ラウドネスの推移を表示", variable=blnPlot)
c1.pack(side="bottom")
c2 = tk.Checkbutton(root, text="クイックスキャンを有効", variable=blnQuick)
c2.pack(side="bottom")

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