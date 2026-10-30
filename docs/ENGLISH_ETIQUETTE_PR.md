## 目的と変更
海外ゲスト向けに `en/articles/park-etiquette.html` を1本追加し、声量・待ち列・公共空間・ショー鑑賞時の配慮を自然な英語で説明します。地面への着座やカチューシャを一律禁止にせず、公式要件・キャストの現地案内・編集上の配慮を区別。視線の意図や国籍への一般化を避け、困ったときの相談方法を案内します。マージ・本番公開はこの依頼の対象外です。

英語トップ・一覧・既存4記事に導線を追加。トップOGP説明文の不一致、一覧title/description/H1、CollectionPage生成を改善し、新記事のself-canonical・OGP・Article/BreadcrumbList・CSP・サイトマップを整合させました。実質的な翻訳関係がないAboutと日本語運営者プロフィールのhreflangを解除。既存10記事は本文とSEOを全件監査し、根拠のない一括書換えはしていません。

## 重複回避と企画
新記事は会話・列・共有空間・鑑賞時の配慮に限定。撮影機材詳細は `park-photography.html`、準備・天候・アプリ・チケットは既存記事へ誘導します。全10記事の意図比較、未実装の追加記事候補4本（短い日本語・食事注文・ゲストサービス・アクセシビリティ）は `docs/ENGLISH_ETIQUETTE_RESEARCH.md` に記録しました。SEO方針と作業ログも更新済みです。

## 出典調査と公開前のブロッカー
**ライブ出典調査は通信制限のため未完了です。このPRはDraftとして公開保留にします。** 以下はレビュー対象であり、最新内容を確認済みの資料としては扱っていません。

- https://www.tokyodisneyresort.jp/en/theme_park_terms_of_use.html （英語利用約款、URLを含め要確認）
- https://www.tokyodisneyresort.jp/theme_park_terms_of_use.html （日本語利用約款）
- https://www.tokyodisneyresort.jp/topics/info/stay.html （既存日本語記事の出典URL）
- https://www.tokyodisneyresort.jp/tdr/resort/entertainment.html （既存日本語記事の出典URL）
- JNTO／JR Eastの一次資料、英語検索結果の比較も接続許可後に実施が必要です。

TDRとGitHub APIは環境プロキシのCONNECTで403。必要なドメインを環境設定下書きへ保存済みですが、有効化は別です。出典URLの実到達・重要ルールの英日比較・交通マナーの一次資料・英語SERP比較を完了してから公開可否を判断してください。本文に確認日を捏造していません。検索語は仮説で、検索需要の実測ではありません。

## 検証
- `python scripts/check_site.py`: PASS、74ページ・71サイトマップURL。内部リンク・アンカー・記事掲載・hreflang相互参照・JSON-LD・CSPを検証。英語メタ重複とOGP不一致の回帰チェックを追加。
- `python scripts/sync_metadata.py --check`: PASS、差分0。
- `CHROMIUM_PATH=/usr/bin/chromium python tests/browser_checks.py`: PASS、全6グループ。全ページ描画、9ページ×320/390/768/960/1440px、新記事の検索・リンク、キーボード操作、JS無効時の11英語記事表示など。
- 新記事390px／1440pxのスクリーンショットを目視確認。ローカル開発サーバーのHTTP 200と本文も確認。
- `git diff --check`: PASS。

Search Console、順位・流入・CTR・インデックス状況、実機Safari、外部URLの最新内容、独立した英文校正、GitHub Pages反映は未確認。技術チェック成功と編集上の公開承認を区別しています。
