# プロジェクト貢献ガイド

## 開発環境のセットアップ

### 環境構築

README.mdを参照してください。

## コーディング規約

- Ruffを使用し、警告を修正してください。
```
uv run ruff check . --fix
```
- docstringはGoogle形式を使用してください。
- コメントは日本語で記述してください。
- 新規機能を追加する場合でテストが容易な場合はテストコードも追加してください。

## テスト

プルリクエストを提出する前に、すべてのテストが通ることを確認してください：

```bash
uv run python -m unittest discover -s tests
```

## コミットメッセージのガイドライン

コミットメッセージは以下の形式に従ってください：

```
[add/update/fix] 簡潔な説明

詳細な説明（必要な場合）
```

## ファイル構成

### config
シミューレーションの設定
現在は開発中のためUTATの設定を入れているが、今後.gitignoreに追加する予定

### scripts
直接実行できるスクリプト
```bash
uv run python -m scripts.<script_name>
```

### src
コード本体

#### src/core

軌道計算を行うコード

#### src/make_report

シミューレーション結果の可視化を行うコード

### tests
テストコード