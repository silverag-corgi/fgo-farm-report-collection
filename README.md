# fgo-farm-report-collection (FGO周回報告収集) <!-- omit in toc -->


# 0. 目次 <!-- omit in toc -->

- [1. 概要](#1-概要)
- [2. 機能](#2-機能)
- [3. 動作確認済み環境](#3-動作確認済み環境)
- [4. セットアップ手順](#4-セットアップ手順)
- [5. 使い方](#5-使い方)
  - [5.1. 周回報告一覧生成](#51-周回報告一覧生成)
    - [5.1.1. 実行コマンド](#511-実行コマンド)
    - [5.1.2. 実行結果](#512-実行結果)
  - [5.2. 周回報告概要生成](#52-周回報告概要生成)
    - [5.2.1. 実行コマンド](#521-実行コマンド)
    - [5.2.2. 実行結果](#522-実行結果)
  - [5.3. 周回報告実績生成](#53-周回報告実績生成)
- [6. 連絡先](#6-連絡先)
- [7. ライセンス](#7-ライセンス)


# 1. 概要

FGOの周回報告をWebスクレイピングにより収集・集計し、csvファイルに保存する。

また、そのcsvファイルの一部は`twitter-lib-for-me`リポジトリの入力ファイルになる。


# 2. 機能

アプリケーションとしてコマンドラインから実行できる。

- 周回報告一覧生成
  - 周回報告一覧ファイルを生成する
- 周回報告概要生成
  - 周回報告一覧ファイル、周回報告概要ファイルを生成する
- 周回報告実績生成
  - 周回報告一覧ファイル、周回報告実績ファイルを生成する
  - 今後実装予定


# 3. 動作確認済み環境

- Windows 10 Pro
- Python 3.10.1
- Pipenv 2022.1.8


# 4. セットアップ手順

セットアップにあたり前提として、PythonとPipenvがインストール済みであること。

まず、下記リポジトリをクローンもしくはダウンロードする。

- fgo-farm-report-collection
  - 本リポジトリ
- python-lib-for-me
  - 自分用のPythonライブラリ

次に、下記コマンドを実行する。

実行例：
```cmd
> cd fgo-farm-report-collection   # アプリケーションのパスに移動する
> set PIPENV_VENV_IN_PROJECT=true # 仮想環境のインストール先をアプリケーション配下に設定する
> pipenv install                  # 仮想環境をインストールする
```

次に、下記コマンドを実行して、アプリケーション配下に`.venv`フォルダが作成されていることを確認する。

実行例：
```cmd
> pipenv --venv                   # 仮想環境のインストール先を表示する
C:/Git/python/twitter-lib-for-me/.venv
```


# 5. 使い方

アプリケーションの実行手順を機能ごとに示す。


## 5.1. 周回報告一覧生成


### 5.1.1. 実行コマンド

下記コマンドを実行する。

実行例：
```cmd
> cd fgo-farm-report-collection
> pipenv run list-gen 2022-01
[2022-02-09 00:45:02.844][INF][farm_report_list_gen:0044][main] 実行コマンド：['farm_report_list_gen.py', '2022-01']
[2022-02-09 00:45:02.847][INF][farm_report_list_gen:0027][do_logic] 周回報告一覧生成を開始します。
[2022-02-09 00:45:02.848][INF][farm_report_list_gen:0065][do_logic] 周回報告一覧を生成します。(2022-01-01～2022-01-31)
[2022-02-09 00:45:02.849][INF][farm_report_list_gen:0069][do_logic] 周回報告一覧ファイル：./dest/farm_report_list/farm_report_list_2022-01.csv
[2022-02-09 00:45:02.852][INF][farm_report_list_gen:0175][__generate_farm_report_list] https://fgojunks.max747.org/harvest/contents/date/2022-01-01.html
[2022-02-09 00:45:03.414][INF][farm_report_list_gen:0175][__generate_farm_report_list] https://fgojunks.max747.org/harvest/contents/date/2022-01-02.html
[2022-02-09 00:45:04.034][INF][farm_report_list_gen:0175][__generate_farm_report_list] https://fgojunks.max747.org/harvest/contents/date/2022-01-03.html
...
[2022-02-09 00:45:16.382][INF][farm_report_list_gen:0175][__generate_farm_report_list] https://fgojunks.max747.org/harvest/contents/date/2022-01-29.html
[2022-02-09 00:45:16.871][INF][farm_report_list_gen:0175][__generate_farm_report_list] https://fgojunks.max747.org/harvest/contents/date/2022-01-30.html
[2022-02-09 00:45:17.316][INF][farm_report_list_gen:0175][__generate_farm_report_list] https://fgojunks.max747.org/harvest/contents/date/2022-01-31.html
[2022-02-09 00:45:18.713][INF][farm_report_list_gen:0225][__generate_farm_report_list] 周回報告一覧(追加分)
     quest_kind         posting_date  user_id                 quest_place  num_of_farms  material
0      通常クエ  2022-01-01 23:55:18    xxxxx              殺の修練場初級           100  歯車: 4, ランタン: 5, 塵: 12, 牙: 13, 殺輝: 145, 殺モ: 5, ...
1      通常クエ  2022-01-01 23:50:23    xxxxx          バビロニアエリドゥ            50  牙: 36, 騎魔: 10, 騎輝: 24, 騎猛火: 7
2      通常クエ  2022-01-01 23:43:56    xxxxx            ロンドンサザーク           100  ホム: 34, 骨: 28, 槍魔: 14, 弓輝: 23, 槍輝: 40, 槍灯火: 17...
3      通常クエ  2022-01-01 23:42:00    xxxxx          キャメロット大神殿           120  スカラベ: 16, 鎖: 55, 術秘: 10, 殺輝: 9, 狂輝: 17, 術業火: 2...
4      通常クエ  2022-01-01 23:41:17    xxxxx              殺の修練場極級           100  脂: 19, ランタン: 27, 種: 38, 塵: 25, 牙: 32, 鎖: 23, 殺...
[2022-02-09 00:45:18.721][INF][farm_report_list_gen:0226][__generate_farm_report_list] 周回報告一覧(追加分)
     quest_kind         posting_date  user_id                 quest_place  num_of_farms  material
2260   通常クエ  2022-01-31 04:00:10    xxxxx        オケアノス隠された島            25  貝殻: 4, 剣魔: 1, 剣輝: 13, 剣猛火: 1
2261   通常クエ  2022-01-31 02:04:40    xxxxx          セプテムエトナ火山           200  ランタン: 22, 殺輝: 77
2262   通常クエ  2022-01-31 00:19:18    xxxxx              下総国荒川の原           350  胆石: 51, 勾玉: 75, 塵: 105, 狂秘: 11, 剣魔: 117, 剣猛火: ...
2263   通常クエ  2022-01-31 00:15:54    xxxxx      キャメロット砂嵐の砂漠           160  スカラベ: 15, 骨: 119, 術秘: 5, 剣輝: 19, 弓輝: 19, 槍輝: 1...
2264   通常クエ  2022-01-31 00:00:01    xxxxx  アナスタシアヤガ・モスクワ           100  結氷: 47, 殺魔: 49, 殺猛火: 37
[2022-02-09 00:45:18.736][INF][farm_report_list_gen:0076][do_logic] 周回報告一覧生成を終了します。
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

実行例：
```cmd
> pipenv run list-gen -h
usage: farm_report_list_gen.py [-h] col_year_month

positional arguments:
  col_year_month  収集年月(yyyy-mm形式)

options:
  -h, --help      show this help message and exit
```


### 5.1.2. 実行結果

周回報告一覧ファイルが下記パスに生成される。

| 種類         | ファイルパス                                            |
| ------------ | ------------------------------------------------------- |
| フォーマット | ./dest/farm_report_list/farm_report_list_[取得年月].csv |
| 例           | ./dest/farm_report_list/farm_report_list_2022-01.csv    |

また、下記画像はあるエディタ(editcsv)で開いた際のデータ例である。

![farm_report_list](./pic/farm_report_list.JPG)


## 5.2. 周回報告概要生成


### 5.2.1. 実行コマンド

下記コマンドを実行する。

実行例：
```cmd
> cd fgo-farm-report-collection
> pipenv run sum-gen 2022-01 -a 100
[2022-02-09 08:22:57.496][INF][farm_report_summary_gen:0049][main] 実行コマンド：['farm_report_summary_gen.py', '2022-01', '-a', '100']
[2022-02-09 08:22:57.500][INF][farm_report_list_gen:0027][do_logic] 周回報告一覧生成を開始します。
[2022-02-09 08:22:57.523][INF][farm_report_list_gen:0058][do_logic] 周回報告一覧は最新です。(2022-01)
[2022-02-09 08:22:57.524][INF][farm_report_list_gen:0076][do_logic] 周回報告一覧生成を終了します。
[2022-02-09 08:22:57.525][INF][farm_report_summary_gen:0028][do_logic] 周回報告概要生成を開始します。
[2022-02-09 08:22:57.525][INF][farm_report_summary_gen:0051][do_logic] 周回報告概要ファイル：./dest/farm_report_summary/farm_report_summary_2022-01_全て_100周以上.csv
[2022-02-09 08:22:57.549][INF][farm_report_summary_gen:0133][__generate_farm_report_summary] 
                user_name  num_of_farms
user_id
xxxxx                   -         19171
xxxxx                   -         10184
xxxxx                   -          9902
xxxxx                   -          8025
xxxxx                   -          6390
...                   ...           ...
xxxxx                   -           100
xxxxx                   -           100
xxxxx                   -           100
xxxxx                   -           100
xxxxx                   -           100

[283 rows x 2 columns]
[2022-02-09 08:22:57.553][INF][farm_report_summary_gen:0060][do_logic] 周回報告概要生成を終了します。
```

また、ヘルプを呼び出す時は下記コマンドを実行する。

実行例：
```cmd
> pipenv run sum-gen -h
usage: farm_report_summary_gen.py [-h] (-a MIN_NUM_OF_ALL_QUEST | -n MIN_NUM_OF_NORMAL_QUEST | -e MIN_NUM_OF_EVENT_QUEST) [-u] col_year_month

positional arguments:
  col_year_month        収集年月(yyyy-mm形式)

options:
  -h, --help            show this help message and exit
  -a MIN_NUM_OF_ALL_QUEST, --min_num_of_all_quest MIN_NUM_OF_ALL_QUEST
                        最低周回数(全て)
                        グループで1つのみ必須
  -n MIN_NUM_OF_NORMAL_QUEST, --min_num_of_normal_quest MIN_NUM_OF_NORMAL_QUEST
                        最低周回数(通常クエ)
                        グループで1つのみ必須
  -e MIN_NUM_OF_EVENT_QUEST, --min_num_of_event_quest MIN_NUM_OF_EVENT_QUEST
                        最低周回数(イベクエ)
                        グループで1つのみ必須
  -u, --should_output_user_name
                        ユーザ名出力要否
```


### 5.2.2. 実行結果

周回報告一覧ファイルが周回報告一覧生成と同様に生成され、周回報告概要ファイルが下記パスに生成される。

| 種類         | ファイルパス                                                                                 |
| ------------ | -------------------------------------------------------------------------------------------- |
| フォーマット | ./dest/farm_report_summary/farm_report_summary\_[取得年月]\_[クエスト種別]\_[最低周回数].csv |
| 例           | ./dest/farm_report_summary/farm_report_summary_2022-01_全て_100周以上.csv                    |

また、下記画像はあるエディタ(editcsv)で開いた際のデータ例である。

![farm_report_summary](./pic/farm_report_summary.JPG)


## 5.3. 周回報告実績生成

今後実装予定


# 6. 連絡先

[Twitter(@silverag_corgi)](https://twitter.com/silverag_corgi)


# 7. ライセンス

MITライセンスの下で公開している。
詳細はLICENSEを確認すること。

