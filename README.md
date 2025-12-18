# Web_novel_bulletin_board_story_maker

Web小説用の、掲示板回作成用スクリプトです。

## 概要

コメントを入力すると、掲示板形式（番号 + 名無し）に自動フォーマットします。

## 使い方

### 基本的な使い方（標準入力）

```bash
python3 bulletin_board_formatter.py
```

テキストを入力後、`Ctrl+D`（Mac/Linux）または `Ctrl+Z`（Windows）で終了します。

### ファイルから読み込む場合

```bash
python3 bulletin_board_formatter.py input.txt
```

### ファイルに出力する場合

```bash
python3 bulletin_board_formatter.py input.txt -o output.txt
```

### コマンドラインオプション

| オプション | 説明 |
|-----------|------|
| `input_file` | 入力ファイルのパス（省略で標準入力） |
| `-o`, `--output` | 出力ファイルのパス（省略で標準出力） |
| `-n`, `--start-number` | 開始番号（デフォルト: 1） |
| `--name` | 匿名名（デフォルト: 名無し） |
| `--jump-min` | 「＊」後のジャンプ最小値（デフォルト: 50） |
| `--jump-max` | 「＊」後のジャンプ最大値（デフォルト: 250） |

### 使用例

```bash
# 基本的な使い方
python3 bulletin_board_formatter.py input.txt -o output.txt

# 開始番号を100に指定
python3 bulletin_board_formatter.py input.txt -o output.txt -n 100

# 匿名名とジャンプ範囲をカスタマイズ
python3 bulletin_board_formatter.py input.txt --name "ななしさん" --jump-min 100 --jump-max 300
```

## 入力形式

```
## タイトル
コメント

コメント

コメント
```

※ 空行でコメントを区切ります

## 出力形式

```
## タイトル
1. 名無し
コメント

2. 名無し
コメント

3. 名無し
コメント
```

## 実行例

**入力：**
```
## 【悲報】主人公、転生する
異世界転生キタ━━━━(ﾟ∀ﾟ)━━━━!!

おめでとう

これはひどいwww
```

**出力：**
```
## 【悲報】主人公、転生する
1. 名無し
異世界転生キタ━━━━(ﾟ∀ﾟ)━━━━!!

2. 名無し
おめでとう

3. 名無し
これはひどいwww
```

**開始番号指定の例：**
```
10
## 続きのスレッド
10番目からのコメント

次のコメント
```

↓

```
## 続きのスレッド
10. 名無し
10番目からのコメント

11. 名無し
次のコメント
```
