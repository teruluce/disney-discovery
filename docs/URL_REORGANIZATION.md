# 公開終了11本・統合3本のURL対応表（レビュー用差分）

判断・確認日：2026年11月5日（日本時間）。main `4e51382` とPR #83初版 `64e0531` を確認して作業。mainは変更していません。以下は作業ブランチをマージした場合の挙動で、本番で公開終了済みという意味ではありません。

## 処理の考え方

- 公開終了11本：旧URLのファイルを残し、本文を公開終了案内へ置換。自動転送なし、自己canonical、`noindex,follow`。Article構造化データを除去。既存HTMLを配信するGitHub Pages上ではHTTP 200であり、HTTP 410ではありません。別途ホストを変更しなければ410を設定できないため、今回のレビュー案はこの案内ページとします。終了本文はGitの履歴に残ります。
- 統合3本：統合先の該当節へmeta refreshと通常リンクで案内。`noindex,follow`、canonicalは統合先のページ。HTTP 301ではありません。JavaScriptは不要です。古いURLのフラグメントに関わらず、対応表の該当節へ到達します。
- 内部リンクは統合先の該当節へ更新。公開終了記事の関連記事リンクと14本の一覧カードを除去。関連が薄いトップへの一括転送は行いません。
- サイト内検索は一覧カードを対象にするため、日本語一覧は52件から38件へ。残る日本語37記事とJournalへの入口1件です。英語一覧は12件のまま。サイトマップは73URLから59URLへ（終了11・統合元3を除外）。
- **検索流入・被リンクは全14URLで未確認**。Search Console・アクセス解析・被リンク計測データへアクセスしていません。下表のリンク件数はリポジトリ内の別HTMLから旧URLへ向くアンカー数であり、外部被リンク数ではありません。終了する記事同士のリンクも整備前の数に含みます。

## 公開終了の対象

全行の共通処理：旧URLの案内は200＋noindex、自動転送なし。記事一覧・検索・サイトマップから除外。リポジトリ内HTMLからの旧URLへのリンクは整備後0件。検索流入・被リンクは未確認です。

| 旧記事名・URL | 変更前の内部リンク | 公開終了時の処理・検索上の扱い |
|---|---|---|
| [ピクサーとマーベルとは？ディズニーとの関係とスパイダーマンの権利を解説](https://teruluce.github.io/disney-discovery/articles/pixar-marvel-spiderman-rights-guide.html) | 1件：articles/index.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |
| [ディズニーのアニメーションはどう作られる？手描きとCGの工夫](https://teruluce.github.io/disney-discovery/articles/how-disney-animation-is-made.html) | 3件：articles/index.html、articles/snow-white-1937.html、articles/tangled-rapunzel-secrets.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |
| [ウォルト・ディズニーとは？生い立ちから主な出来事まで](https://teruluce.github.io/disney-discovery/articles/walt-disney-profile.html) | 5件：articles/index.html、articles/mickey-mouse-debut.html、articles/oswald-lucky-rabbit.html、articles/snow-white-1937.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |
| [『白雪姫』（1937年）はなぜ特別？初公開の日と制作の背景](https://teruluce.github.io/disney-discovery/articles/snow-white-1937.html) | 3件：articles/index.html、articles/walt-disney-profile.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |
| [『ライオン・キング』とは？シンバの成長と物語のテーマ](https://teruluce.github.io/disney-discovery/articles/lion-king-basics.html) | 1件：articles/index.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |
| [『トイ・ストーリー』とは？ウッディとバズから始まる物語](https://teruluce.github.io/disney-discovery/articles/toy-story-basics.html) | 1件：articles/index.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |
| [オズワルド・ラッキー・ラビットとは？ミッキーマウスより前のウサギ](https://teruluce.github.io/disney-discovery/articles/oswald-lucky-rabbit.html) | 3件：articles/index.html、articles/mickey-mouse-debut.html、articles/walt-disney-profile.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |
| [ミニーマウスとは？初登場作品とミッキーとの関係](https://teruluce.github.io/disney-discovery/articles/minnie-mouse-profile.html) | 1件：articles/index.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |
| [デイジーダックとは？初登場とドナルドとの関係](https://teruluce.github.io/disney-discovery/articles/daisy-duck-profile.html) | 1件：articles/index.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |
| [グーフィーとは？初登場作品とプルートとの違い](https://teruluce.github.io/disney-discovery/articles/goofy-guide.html) | 1件：articles/index.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |
| [プルートとは？ミッキーとの関係と初登場作品](https://teruluce.github.io/disney-discovery/articles/pluto-guide.html) | 1件：articles/index.html | 終了案内を表示。本文・関連記事からの案内・一覧カードを除去。サイトマップから除外しnoindex。転送先なし。 |

## 統合先と残した情報

| 統合元の旧URL | 統合先の該当節 | 変更前の内部リンク | 引き継いだ情報・出典 |
|---|---|---|---|
| [regular-parades-shows.html](https://teruluce.github.io/disney-discovery/articles/regular-parades-shows.html) | [articles/parades-shows-guide.html#regular](https://teruluce.github.io/disney-discovery/articles/parades-shows-guide.html#regular) | 6件：articles/christmas-parades-shows.html、articles/electrical-parade-dreamlights.html、articles/halloween-parades-shows.html、articles/index.html、articles/parades-shows-guide.html | 4公演の紹介とランド昼夜／シー水上・ステージの違い。鑑賞条件の確認手順、公演が固定でない注意。元の公式4公演・一覧へのリンクを保持し、一覧URLは現在の.html形式へ更新。公演時間・DPA・エントリー・ダンスの期間を公式で再確認。 |
| [tokyo-disneyland-history.html](https://teruluce.github.io/disney-discovery/articles/tokyo-disneyland-history.html) | [articles/tdr-history-timeline.html#land-history](https://teruluce.github.io/disney-discovery/articles/tdr-history-timeline.html#land-history) | 3件：articles/index.html、articles/tdr-history-timeline.html、articles/tokyo-disneysea-history.html | 1983/4/15開園、開園30周年の2013/3/8公式ブログ、2000/2001/2008の周辺開業年を年表へ。開園前の浦安からの経緯を読むBGS記事と、ワールドバザール・シンデレラ城へのBGS案内を保持。公式出典と姉妹サイトの解釈の区別も保持。 |
| [tokyo-disneysea-history.html](https://teruluce.github.io/disney-discovery/articles/tokyo-disneysea-history.html) | [articles/tdr-history-timeline.html#sea-history](https://teruluce.github.io/disney-discovery/articles/tdr-history-timeline.html#sea-history) | 4件：articles/fantasy-springs-guide.html、articles/index.html、articles/tdr-history-timeline.html、articles/tokyo-disneyland-history.html | 2001/9/4開園とミラコスタ、2023年22周年から2026年25周年の文脈、2024/6/6のFS拡張、8ポートの表、FS・景観記事への案内。元のOLC・公式出典・BGSへのリンクを保持。 |

統合先は自己canonicalのままサイトマップへ残しています。旧ページの出典リンクが統合先にすべて残ることをテストしています（公演一覧URLの正規化を除く）。統合先に新しい公開日を推定して付けていません。

## 公式情報の再確認記録

| 公式ページ | 2026年11月5日に確認した内容 |
|---|---|
| [ハーモニー・イン・カラー](https://www.tokyodisneyresort.jp/tdl/show/detail/7000/) | 約45分、パレードルート、DPA対象。 |
| [ドリームライツ](https://www.tokyodisneyresort.jp/tdl/show/detail/913/) | 約45分、DPA対象、2026/11/11〜12/25のクリスマス版。 |
| [ビリーヴ！](https://www.tokyodisneyresort.jp/tds/show/detail/967/) | メディテレーニアンハーバーの約30分の水上公演、DPA対象。 |
| [ダンス・ザ・グローブ！](https://www.tokyodisneyresort.jp/tds/show/detail/7604/) | 約25分、2026/1/14〜2027/3/31、エントリー受付・DPA対象、状況による自由席。 |
| [ランドの一覧](https://www.tokyodisneyresort.jp/tdl/show.html) / [シーの一覧](https://www.tokyodisneyresort.jp/tds/show.html) | 来園日ごとのスケジュール確認への入口。日付・休止・当日の受付状況を各詳細とアプリで確認する手順に整理。 |
| [2013/3/8の公式ブログ](https://www.tokyodisneyresort.jp/tdrblog/detail/130308/) | ランドが1983/4/15開園である記述と、開園30周年前のブログという文脈。 |
| [8つのテーマポート](https://www.tokyodisneyresort.jp/tdr/facility/themeport/) | 拡張後の8ポートの構成と、FSが3作品をテーマにする説明。 |

歴史記事のその他のOLC沿革・発表資料は元記事の確認日（2026/10/12）とともに引き継ぎました。今回すべてを再調査したとはしていません。BGS Chroniclesの詳細説明も公式確認済みの事実に置き換えていません。

## 維持した資産と確認結果

- 英語版の全HTML、Journalの全HTML・CSS・スタンプ原写真、共通CSSは初版と同一（ファイルハッシュで確認）。
- 既存の転送3件（チップとデールの見分け方、初来園アプリ計画、スタンプ記事）は元ファイルと同一。
- チップとデール、ドナルド、ラプンツェル、アナと雪の女王は記事として維持。ラプンツェルでは終了する制作解説への関連記事リンクのみ除去。
- ハロウィーン2026は年度資料として維持。関連するレギュラー案内のリンクだけを統合先へ更新。
- 77HTML、59サイトマップURLのリンク・アンカー・hreflang・JSON-LD・CSPを静的検証。
- 50の有効記事（日本語37・英語12・Journal1）、終了案内11、追加統合転送3と元転送3の集合を検証。
- Chromiumで終了11URLと統合3URLをJavaScript有効・無効の両方で確認。終了案内はそのURLに留まり、統合は対応する該当節へ到達。
- PC・スマホの表示、5幅の横はみ出し、検索38件・英語12件、キーボード操作とJournal導線を確認。

## 公開判断前の残作業

表紙写真の元ファイル取得・組み込み・PC/スマホの実トリミング比較。実機Safari・本番配信のレスポンス/表示/速度、検索流入と被リンクは未確認。GitHub Actionsの結果はPRのChecksを参照。レビュー後のmainマージと本番公開は別途運営者が判断します。
