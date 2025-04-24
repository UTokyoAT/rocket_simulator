# rocket_simulator
主にハイブリッドロケットの陸打ちを想定したシミュレータです。

## 環境構築

### Anacondaの仮想環境を使う場合

Anacondaをインストールしておく。

```
conda create -n rocket_simulator python=3.11.9
conda activate rocket_simulator
pip install -r requirements.txt
```
次回からは
```
conda activate rocket_simulator
```
を実行したあと、下記の操作を行う。

## 使い方
1. config内の各ファイルに設定を書き込む。
2. 下記のコマンドを実行する。
```
python -m scripts.make_report
