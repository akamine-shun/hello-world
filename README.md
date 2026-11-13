
# 給付金データ管理・分析システム

## 概要
PythonとSQLiteを使用して、給付金データの取り込み・保存・集計を行うシステムです。

※ 使用するデータは架空のサンプルデータです。

## 使用技術
- Python
- SQLite
- SQL
- FastAPI
- Git / GitHub

## 主な機能
1. CSVファイルから給付金データを読み込む
2. SQLiteデータベースに登録する
3. SQLで支払状況別の件数・合計金額を集計する
4. 集計結果をターミナルに表示する
5. FastAPIで集計結果を取得する
6. 支払状況を指定して給付金データを検索する
7. 最低金額を指定して検索結果を絞り込む
8. 不正な検索条件をバリデーションで防ぐ

## ファイル構成
- main.py：全体の処理を実行
- import_csv.py：CSVデータをDBに登録
- analysis.py：SQLによる集計
- api.py：FastAPIによる集計・検索API
- kyufukin_sample.csv：架空の給付金データ50件
- result.csv：CSV集計結果のサンプル

## 実行方法
Python 3が必要です。

以下のコマンドで実行します。

```bash
python3 main.py
```
### APIの起動方法

以下のコマンドでAPIを起動します。

```bash
uvicorn api:app --reload
```

起動後、ブラウザで以下にアクセスします。

http://127.0.0.1:8000/docs

### APIの機能

- GET /summary：支払状況別の件数・合計金額を取得
- GET /claims：支払状況・最低金額を指定して検索

## 今後の改善予定
- エラー処理の追加
- 自動テストの導入
