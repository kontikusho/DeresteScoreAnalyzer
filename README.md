# DeresteScoreAnalyzer
デレステのスコア画面から各種情報を読み取ります

# 使ってるもの
* pyocr
* opencv
* PIL
* numpy

# 使い方
``` python
python3 src/analyze.py [画像ファイル]
```
これで結果が返ってきます

# 仕組み
画像を固定値でそれぞれ切り分けてからpyocrで文字起こしします。
難易度はヒストグラムの比較で一番一致率が高かったものを選択しています。
