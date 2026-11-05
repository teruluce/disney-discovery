# Disney Discovery 正式再編・リデザイン

2026年11月5日の運営者指示により、PR #83の全体展開・mainへのマージ・GitHub Pages公開を承認済み。最新mainは4e51382でPR起点と一致し、競合なし。AGENTS.md / AI_GOVERNANCE.mdを確認。

## 正式デザイン

白に近い背景、深緑の文字、明朝体の見出し、細い罫線を日本語・英語・Journal・固定ページに適用。共通ナビとフッターを各言語で統一し、モバイルはキーボード操作できるdetailsメニューを使用。共通CSS magazine.cssで表示を統一し、本文・目次・検索の構造を維持しています。

| 主な画面 | PC | スマホ |
|---|---|---|
| 写真入りトップ | [画像](prototype/final/home-pc.jpg) | [画像](prototype/final/home-mobile.jpg) |
| 日本語記事一覧 | [画像](prototype/final/articles-pc.jpg) | [画像](prototype/final/articles-mobile.jpg) |
| 代表記事 | [画像](prototype/final/guide-pc.jpg) | [画像](prototype/final/guide-mobile.jpg) |
| プロフィール | [画像](prototype/final/profile-pc.jpg) | [画像](prototype/final/profile-mobile.jpg) |
| Journal | [画像](prototype/final/journal-pc.jpg) | [画像](prototype/final/journal-mobile.jpg) |
| 英語トップ | [画像](prototype/final/english-pc.jpg) | [画像](prototype/final/english-mobile.jpg) |

## 記事・写真の保持

- トップは来園ガイド・パークを楽しむ・Journalが中心。残す映画・キャラクター記事は記事一覧から探せます。BGSへの案内は関連する本文の箇所に残しています。
- 公開終了11件は200＋noindexの終了案内（自動転送なし）。統合3件は関連ガイドの該当節へのmeta refreshと通常リンク。旧URLの3既存転送も保持。[URL対応表](URL_REORGANIZATION.md)を参照。
- Journalと英語版のmain本文は全件、全体展開前のハッシュと同一。Journalの本人の出来事・感情・写真・クレジットを維持。ヘッダー・フッター・スタイルは今回の承認に基づき更新しています。
- 表紙はユーザー提供の中庭写真。EXIF/GPS等を除去した640px/1280pxのJPEGのみ配信。原本や共有URLは非掲載。PC・スマホとも4:3で写真を切らずに表示。
- 撮影場所の参考として[東京ディズニーランドホテル公式の施設案内](https://www.tokyodisneyresort.jp/hotel/tdh/facility.html)を確認しましたが、この写真の撮影地点との確実な対応を確認できなかったため、キャプションは「中庭の建築と空。写真：てる」を維持しました。

## 検証

77HTML・59サイトマップURL。内部リンク、アンカー、hreflang、JSON-LD、CSP、一覧の整合を検証。公開終了11件、統合3件、元転送3件と、日英の検索・メニュー・キーボード・写真表示・横はみ出しをChromiumで確認。主要ページは320/390/768/960/1440pxで検証し、PC・スマホの実表示画像を上記に保存。

検索一覧の検査は、共通ナビのリンクと一覧カードを混同しないようarticle-list内に限定しました。保護テストは、今回変更が承認された共通スタイル・ヘッダー/フッターと、保持すべき本文・写真・転送を区別しています。Journalの本文ハッシュ・図版・体験事実も引き続き検査しています。

## 公開確認

mainへのpush時には既存の静的/ブラウザ検証に続き検証ジョブの公開URLチェックを実行。実際の https://teruluce.github.io/disney-discovery/ で配信CSSのSHA-256が今回の版と一致するまで待ち、トップ・一覧・代表記事・Journal・英語版・写真・日英メニュー・検索・旧URLを本番のPlaywrightで確認します。ローカルファイルへの応答差し替えは使いません。

この作業環境からgithub.ioへの直接接続はネットワークポリシーで403になり、Web取得ツールでも取得できませんでした。公開サイトの確認結果は、GitHub Actionsの検証ジョブの公開URLチェックの実行結果で確認します。

実機Safari、検索流入・被リンク、全既存記事の変動情報の再調査、Claudeによる独立レビューは今回の検証外です。
