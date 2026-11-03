# 英語Suica支払いガイドの調査・実装

## 目的と範囲（2026-11-03）

運営者が自販機でクレジット払いを試みていた人を見かけたことをきっかけに、訪日読者へSuicaの準備を勧める英語記事を作成。観察した人の国籍・端末・場所・支払い失敗原因は推測せず、記事は一般的な支払いの案内とする。

最新main `58908bf` から `content/english-suica-guide`。AGENTS.md、AI_GOVERNANCE.md、編集・保守規則、英語ページ・ナビ・一覧・SEO・テストを確認。静的HTML、共通CSS、メタ同期と検索を継承。Journalの文体は適用せず、実用記事の自然な英語で執筆する。

## 編集判断

- Suicaをおすすめするが、「キャッシュレス対応なら基本的に交通系ICが使える」「クレジットが使えなければ必ずSuicaで解決する」とは断定しない。設備の受け付け方式が異なり、Suicaまたは相互利用する交通系ICのロゴを確認する形にする。
- カード／スマホのSuica残高による決済とクレジットのタッチ決済を区別。既に対応ICカードを持つ人にはSuicaを買い足す必要が通常ないと説明。
- 物理カードの現金チャージと、対応端末・カードによるWelcome Suica MobileのApple Payチャージを区別。外国の任意のクレジットカードで必ずチャージできると保証しない。
- パーク内の支払いとDisney Mobile Orderの支払いを区別。パーク・ホテルにチャージ設備がないことは、スマホでのオンラインチャージができないという意味にしない。
- 28日・デポジットなし・残高原則返金なしは短期用の物理Welcome Suicaの条件。モバイル版・長期用の条件と混同しない。利用予定分を少しずつチャージする提案は編集上のアドバイス。
- 日本語版は作成せず、PayPay記事等を翻訳の対応先としてhreflang設定しない。日本語ナビの入口は既存どおりトップ／一覧。
- 新規ロゴ・写真・外部スクリプトを追加しない。

## 一次資料と確認内容

以下の本文を2026-11-03に確認。リンクは原稿の該当箇所に配置し、更新・公開日を捏造せず確認日を明記。

| 資料 | 確認した内容 |
| --- | --- |
| [JR EAST Suica](https://www.jreast.co.jp/en/multi/pass/suica.html) | プリペイド、対象交通機関・買い物で利用、対応ロゴ、駅機器での現金チャージ。すべての店舗・路線で利用可能とはしていない。 |
| [JR EAST Welcome Suica](https://www.jreast.co.jp/en/multi/welcomesuica/welcomesuica.html) | 対応ロゴの自販機・店舗・交通機関で利用可能。 |
| [購入・チャージ](https://www.jreast.co.jp/en/multi/welcomesuica/purchase.html) | 短期用物理カードの購入場所、28日、デポジットなし、現金チャージ、Seven Bank ATM、残高の通常返金なし。 |
| [Welcome Suica Mobile](https://www.jreast.co.jp/en/multi/wsmlp/) | Apple Pay対応端末等の要件、物理カードと異なる条件。 |
| [モバイルチャージFAQ](https://apfaq.mobilesuica.com/faq/show/7110?site_domain=wsm) | Apple Payに登録したクレジットカードによるアプリからのチャージ手順。 |
| [TDR電子マネー](https://faq-en.tokyodisneyresort.jp/answer/680ba03be1d0a08019a6a0be/) | Suica等を両パーク・ボンヴォヤージュの店舗・飲食・一部施設で利用可能。メダル・カプセルトイ・一部ワゴン・ロッカー等に例外。 |
| [TDRチャージ場所](https://faq-en.tokyodisneyresort.jp/answer/680ba048d7820362f46c7c1e/) | パーク・ホテル内にチャージ設備なし。舞浜駅・リゾートライン駅の案内。 |
| [Disney Mobile Order](https://www.tokyodisneyresort.jp/en/tdr/guide/app_service/mobileorder.html) | アプリ内ではクレジットカードまたはコード決済。Suica残高決済と分ける。 |

補助確認：[TDR支払方法](https://faq-en.tokyodisneyresort.jp/answer/683f07a106123b9c605e8636/)ではクレジットのタッチ決済に非対応の施設がある。自販機全台の個別仕様・実機決済、各国発行カードの実動作は検証していない。自販機の機種別の操作順は固定せず、表示に従う案内にした。

## 変更ファイル

- `en/articles/suica-payment-guide.html`：新規英語記事。canonical・OGP・Article・パンくず・CSPを同期。
- `en/articles/index.html`：12本目のカードを追加。
- `en/index.html`：Plan Your Visitから案内。
- `en/articles/what-to-pack.html`：支払い準備から相互リンク。
- `sitemap.xml`：新規URL。
- `tests/browser_checks.py`：新記事の5画面幅、検索と記事遷移・持ち物記事との往復リンク、JS無効時の12記事表示。
- `docs/SUICA_GUIDE_RESEARCH.md`、`docs/AI_WORK_LOG.md`：調査・作業記録。

## 公開前の制限

実機でのSuica決済、各スマホ・外国発行クレジットカードの動作、公開ホスト・実機Safari、独立した英文校正は未実施。原稿は確認済みの公式条件に基づき、個別の決済成功を保証しない。本番マージ・公開は運営者の承認後。
