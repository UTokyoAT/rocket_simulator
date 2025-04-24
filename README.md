# rocket_simulator
主にハイブリッドロケットの陸打ちを想定したシミュレータです。

## 環境構築

### Anacondaの仮想環境を使う場合

Anacondaをインストールしておく。

```
conda create -n rocket_simulator python=3.11.9
```

```
conda activate rocket_simulator
```

```
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
```
## コンフィグ設定方法

### config.json

#### wind_speed
基準高度での風速[m/s]

#### wind_direction
風向[deg]

北を0として時計回りに計る。真方位を用いる。

#### wind_reference_height
風速を測定した高度[m]

#### wind_exponent
べき法則のべき定数

高度z[m]での風速は
wind_speed * (z / wind_reference_height)^(1 / wind\_exponent)

#### CA
軸力係数

すなわち、機体の前後方向に受ける空気力を無次元化したもの。空気抵抗係数とは迎角0の時のみ一致する。

#### CN_alpha
放線力傾斜[1/rad]

すなわち、機体の前後方向に垂直な向きに受ける空気力を無次元化したものを迎角で微分したもの。

#### body_diameter
ロケットの直径[m]

#### wind_center
風圧中心[m] 向きはx軸正の向きがロケットの先端を向く。原点はgravity_centerと整合していれば良い。

#### dt
シミュレーションの時間刻みはば[t]

#### launcher_length

ランチャーの長さ[m]

#### 慣性モーメント
I_xx, I_yy, I_zz, I_zy, I_xz, I_xy

機体の前後方向がx軸である

#### parachute_terminal_velocity
パラシュートの終端速度[m/s]

#### parachute_delay_time
最高高度に達してからパラシュートが開傘するまでの時間[s]

#### first_elevation
発射前の機体の仰角[deg] 90の時真上に打ち上げる。

#### first_azimuth
発射前の機体の方位角[deg] 北を0として時計回りに計る。真方位を用いる。

#### first_roll
発射前の機体のロール角[deg]

#### first_gravity_center
機体発射時の重心の位置[m] 向きはx軸正の向きがロケットの先端を向く。原点はwind_centerと整合していれば良い。

#### end_gravity_center
燃焼終了時の重心の位置[m] 向きはx軸正の向きがロケットの先端を向く。原点はwind_centerと整合していれば良い。
