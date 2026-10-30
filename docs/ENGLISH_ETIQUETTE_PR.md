## 目的と変更
海外ゲスト向けに `en/articles/park-etiquette.html` を1本追加し、声量・待ち列・公共空間・ショー鑑賞時の配慮を自然な英語で説明します。地面への着座やカチューシャを一律禁止にせず、公式要件・キャストの現地案内・編集上の配慮を区別。視線の意図や国籍への一般化を避け、困ったときの相談方法を案内します。マージ・本番公開はこの依頼の対象外です。

英語トップ・一覧・既存4記事に導線を追加。トップOGP説明文の不一致、一覧title/description/H1、CollectionPage生成を改善し、新記事のself-canonical・OGP・Article/BreadcrumbList・CSP・サイトマップを整合させました。実質的な翻訳関係がないAboutと日本語運営者プロフィールのhreflangを解除。既存10記事は本文とSEOを全件監査し、根拠のない一括書換えはしていません。

## 重複回避と企画
新記事は会話・列・共有空間・鑑賞時の配慮に限定。撮影機材詳細は `park-photography.html`、準備・天候・アプリ・チケットは既存記事へ誘導します。全10記事の意図比較、未実装の追加記事候補4本（短い日本語・食事注文・ゲストサービス・アクセシビリティ）は `docs/ENGLISH_ETIQUETTE_RESEARCH.md` に記録しました。SEO方針と作業ログも更新済みです。

## 出典確認（2026-10-30）
公開済み開発環境からTDR利用約款（英日）、滞在中のお願い、エンターテイメント案内（英日）の本文を確認しました。

- https://www.tokyodisneyresort.jp/en/theme_park_terms_of_use.html
- https://www.tokyodisneyresort.jp/theme_park_terms_of_use.html
- https://www.tokyodisneyresort.jp/topics/info/stay.html
- https://www.tokyodisneyresort.jp/tdr/resort/entertainment.html
- https://www.tokyodisneyresort.jp/en/tdr/resort/entertainment.html
- https://www.japan.travel/fr/guide/understanding-and-mastering-japanese-manners-and-etiquette/ （JNTO、フランス語。英語URLからリダイレクト。公共交通の会話・電話マナーを確認）

英語の大型帽子等の取り外し要請と、日本語の公演によるカチューシャ等への案内の違いを本文で説明し、確認日を追記。機材等の詳細は既存記事へ誘導しています。引用の長い転載や新規画像はありません。

英語検索結果調査は試みましたが、GoogleはJS誘導、Bingは一般的な東京旅行結果を返し、対象テーマの競合比較に使える結果は取得できませんでした。検索意図は一次資料と既存本文の比較を基に設計した編集仮説であり、需要や競合性を実測したものではありません。JR Eastは403でしたが、交通マナーはJNTOで確認しました。以前の通信ブロッカーは解消済みです。

ユーザーから今回の変更のマージ指示あり。チェック成功後にマージします。

## 検証
- `python scripts/check_site.py`: PASS、74ページ・71サイトマップURL。内部リンク・アンカー・記事掲載・hreflang相互参照・JSON-LD・CSPを検証。英語メタ重複とOGP不一致の回帰チェックを追加。
- `python scripts/sync_metadata.py --check`: PASS、差分0。
- `CHROMIUM_PATH=/usr/bin/chromium python tests/browser_checks.py`: PASS、全6グループ。全ページ描画、9ページ×320/390/768/960/1440px、新記事の検索・リンク、キーボード操作、JS無効時の11英語記事表示など。
- 新記事390px／1440pxのスクリーンショットを目視確認。ローカル開発サーバーのHTTP 200と本文も確認。
- `git diff --check`: PASS。

Search Console、順位・流入・CTR・インデックス状況、実機Safari、独立した英文校正、GitHub Pages反映は未確認。技術チェック成功と編集上の公開承認を区別しています。
