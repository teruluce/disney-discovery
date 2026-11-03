# Discovery Journal の運用

Disney Discovery内の「日々の記録」。コンセプトは「何気ない日も、思い出に。」。てるがディズニーや舞浜で過ごした時間を、写真と自分の言葉で残します。情報ガイドの制作方針とは分けて運用します。

## 編集方針

- 自然体の一人称を尊重し、本人の書いていない感情・出来事を加えません。
- 観光情報を無理に補わず、事実と感想を区別します。更新頻度・文字数は自由です。
- 写真・キャプション・出典を大切にします。同行者の実名や特定情報を新たに記載しません。
- 写真はローカルでEXIF（GPS等）と写り込みを確認します。外部画像サービスへの送信は不要です。懸念がある既存内容は勝手に消さず運営者に確認します。

## 日記を追加する

1. 作業ブランチで `docs/templates/journal-entry.html.tmpl` を `journal/好きな英数字名.html` にコピーします。CMS・ビルドは不要です。
2. `ENTRY-SLUG` をファイル名（拡張子なし）に置換し、タイトル・description・H1・パンくず・概要文・本文を記入します。公開日は実際の公開日を `published-date` に指定します。公開前の予定日を公開済み日付として扱いません。
3. 体験日は任意です。不明なら `experience-date` のliを削除します。更新時だけ `updated-date` の行を追加します。各timeの `datetime` は `YYYY-MM-DD`、表示は日本語です。体験日は公開日と別に管理し、構造化データの公開日に転用しません。
4. 写真を `assets/img/` に置き、src・実寸width/height・altを記入します。キャプションは任意。写真の順序は自分の記録に合わせます。
5. `journal/index.html` の `.journal-list` 内のliをコピーし、サムネイル（写真をそのまま利用可能）、リンク、タイトル、短い紹介文、日付を変更します。体験日があれば体験日、なければ公開日の新しい順に手動で並べます。両方不明なら日付を表示・推定せず、日付のある記事の後へ追加します。初回移行記事は公開日不明のため体験日のみです。
6. `sitemap.xml` に記事canonicalのurl要素を追加します。翻訳のないJournalにはhreflangや架空の英語版リンクを追加しません。英語サイトのJournalリンクは日本語ページへの入口で、翻訳の対応指定ではありません。
7. 次を実行し、ブラウザ確認後にPRでレビューします。メタ同期でOGP・Article・パンくず・CSPハッシュが生成されます。生成ブロックは直接編集しません。

```sh
python scripts/sync_metadata.py
python scripts/check_site.py
CHROMIUM_PATH=/usr/bin/chromium python tests/browser_checks.py
```

必要な依存関係・Chromiumの導入方法は [MAINTENANCE.md](MAINTENANCE.md) を参照。本番マージ・公開は運営者の承認後に行います。

## 初回移行の調査と設計（2026-11-03）

- HTML/CSSの静的サイト。共通CSSは `assets/css/style.css`、検索JSは `assets/js/article-search.js`。ヘッダー・フッターは各HTMLに記述され、テンプレートエンジンなし。日本語と英語は翻訳対応があるページだけ相互hreflangを設定。
- ライトテーマ固定、共通の色・フォント・角丸を継承。Journal専用CSSで写真中心のカード・読みやすい幅と余白を設定。写真は一覧でも切り取らず全体を表示。
- 既存記事一覧はHTMLカードを検索・カテゴリの元データにする設計。スタンプ記事カードは新URLへの入口として維持。トップの導線は控えめな1セクションを追加。既存メニューは残し、PC/モバイル双方へJournalを追加。
- 既存記事のH1・導入・本文・写真1枚・キャプション・内外リンクを保持。体験日は2026-10-18。公開日は確認できず、移行日を公開日としていない。画像900×1339、EXIFタグなし／GPSなし、ファイル変更なし。既存キャプションの「写真：てる」を保持。
- 開催期間（2026-10-31まで）に対し、既存本文は開催中の表現が残る。依頼に従い書き換えず、本文外に体験時点の記録という注記を追加。最新の開催情報としての再検証はしていない。
- 旧URLは既存サイト同様のmeta refreshと通常リンクで案内。JS不要。旧ページはnoindex,followと新canonical、サイトマップは新URLだけを登録。GitHub Pages上でHTTP 301を設定する変更ではない。
- 変更対象：新Journal2ページ、旧URL案内、各ページのナビ、トップ・記事一覧リンク、共通CSSのナビ切替幅、Journal CSS、メタ同期・検査スクリプト、ブラウザ検証、サイトマップ、投稿テンプレート・運用文書・作業ログ。

## 今回の変更ファイル一覧

ナビゲーションが各HTMLに配置されているため、Journalへの入口追加は各ページに反映しています。

- `.github/workflows/check-site.yml`
- `404.html`
- `README.md`
- `articles/baymax-guide.html`
- `articles/character-greeting-guide.html`
- `articles/chip-and-dale-guide.html`
- `articles/christmas-parades-shows.html`
- `articles/d-otaku-terms.html`
- `articles/daisy-duck-profile.html`
- `articles/disney-hot-weather-guide.html`
- `articles/disney-mobile-order-guide.html`
- `articles/disney-park-budget-tips.html`
- `articles/disney-park-packing-list.html`
- `articles/disney-with-kids-guide.html`
- `articles/donald-duck-profile.html`
- `articles/electrical-parade-dreamlights.html`
- `articles/fantasy-springs-guide.html`
- `articles/first-visit-checklist.html`
- `articles/frozen-character-guide.html`
- `articles/goofy-guide.html`
- `articles/halloween-parades-shows.html`
- `articles/how-disney-animation-is-made.html`
- `articles/index.html`
- `articles/lion-king-basics.html`
- `articles/maihama-train-confusion-guide.html`
- `articles/mickey-mouse-debut.html`
- `articles/minnie-mouse-profile.html`
- `articles/oswald-lucky-rabbit.html`
- `articles/parades-shows-guide.html`
- `articles/park-day-and-night.html`
- `articles/park-photography-rules.html`
- `articles/park-ticket-basics.html`
- `articles/paypay-payment-guide.html`
- `articles/pixar-marvel-spiderman-rights-guide.html`
- `articles/pluto-guide.html`
- `articles/rainy-day-disney-guide.html`
- `articles/regular-parades-shows.html`
- `articles/resort-line-stamp-rally-2026.html`
- `articles/restaurant-priority-seating-guide.html`
- `articles/snow-white-1937.html`
- `articles/stitch-guide.html`
- `articles/tangled-rapunzel-secrets.html`
- `articles/tdr-access-guide.html`
- `articles/tdr-app-guide.html`
- `articles/tdr-history-timeline.html`
- `articles/tdr-hotel-types.html`
- `articles/ticket-change-cancellation-guide.html`
- `articles/time-saving-services.html`
- `articles/tokyo-disneyland-history.html`
- `articles/tokyo-disneyland-vs-disneysea.html`
- `articles/tokyo-disneysea-history.html`
- `articles/toy-story-basics.html`
- `articles/walt-disney-profile.html`
- `articles/what-is-bgs.html`
- `articles/why-park-areas-feel-different.html`
- `articles/winnie-the-pooh-guide.html`
- `assets/css/journal.css`
- `assets/css/style.css`
- `contact.html`
- `docs/AI_WORK_LOG.md`
- `docs/JOURNAL.md`
- `docs/templates/journal-entry.html.tmpl`
- `en/about.html`
- `en/articles/electrical-parade.html`
- `en/articles/first-visit.html`
- `en/articles/getting-there-by-train.html`
- `en/articles/index.html`
- `en/articles/land-vs-sea.html`
- `en/articles/official-app-guide.html`
- `en/articles/park-etiquette.html`
- `en/articles/park-photography.html`
- `en/articles/rainy-day.html`
- `en/articles/ticket-basics.html`
- `en/articles/unique-tokyo-disneysea.html`
- `en/articles/what-to-pack.html`
- `en/index.html`
- `index.html`
- `journal/index.html`
- `journal/resort-line-stamp-rally-2026.html`
- `privacy.html`
- `profile.html`
- `scripts/check_site.py`
- `scripts/sync_metadata.py`
- `sitemap.xml`
- `tests/browser_checks.py`
- `tests/journal_preservation.py`
