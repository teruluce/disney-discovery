> 旧デザインの記録です。正式採用された写真誌デザインは[最終確認資料](FINAL_REVIEW.md)を参照してください。

# 手書きノートのデザイン

## 方針

Disney Discoveryを、ディズニーの気になることを書きためた一冊のノートとして表現します。生成りの紙、青黒いインク、控えめなマーカー、淡い色の見出しタブを使います。見出しはYomogi、英字の短いラベルやロゴはCaveat。本文・操作ラベルはシステムフォントで読みやすさを保ちます。

## 変更範囲

- `assets/css/style.css`：共通テーマ、表紙、記事索引、本文、プロフィール、フッター、画面幅・印刷・高コントラスト対応。
- `assets/css/journal.css`：既存写真を紙面に貼ったように見せるJournalの表示。
- `assets/img/notebook-sketch.svg`：オリジナルの装飾用ペン画。既存の装飾SVGをCSSで置き換えて表示。
- `assets/fonts/`：手書きフォントのローカル配信とライセンス。
- `tests/browser_checks.py`：新しい配色のコントラストとフォント読み込みの検証。検索・絞り込み・ナビゲーションなどの既存検証は維持。

HTML・記事本文・見出しの文言・掲載順・リンク先・既存画像・JavaScript・SEOメタ情報は変更しません。ビルドシステムや実行時の外部依存は追加しません。

## 表示上の配慮

スマートフォンでは紙の綴じ穴と左の余白線を省略し、本文幅を確保。テーマの索引は折り返し、記事一覧と本文の目次・表は既存の検索・横スクロール操作を保ちます。動きを減らす設定、高コントラスト表示、JavaScriptを無効にした場合にも対応します。写真の傾きやテープは装飾に限定します。

## 確認

```sh
python scripts/check_site.py
python tests/journal_preservation.py
python tests/reorganization_checks.py
CHROMIUM_PATH=/usr/bin/chromium python tests/browser_checks.py
git diff --check
```

自動検証はローカルのファイルをブラウザに応答させて行います。実際のGitHub Pagesへの公開、実機Safariの表示は別途確認が必要です。
