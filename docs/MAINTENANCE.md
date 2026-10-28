# 公開前チェックと保守

記事本文・タイトル・description・画像のaltは各HTMLで管理します。静的HTMLのまま公開し、ビルドサービスや解析サービスへの依存は追加していません。

## 記事を追加・更新するとき

1. 対応言語の記事一覧に記事カードを登録します。日本語では既存の `data-theme` を選びます。絞り込み件数と検索対象は、画面のカードから自動で読み取ります。別のファイル名別カテゴリ表はありません。
2. 新規公開ページを `sitemap.xml` に登録します。旧URLの転送ページ・404は登録しません。
3. 日英の対応ページがある場合は、片方のheadに正しい `rel="alternate" hreflang` を記載します。単に話題が近い別記事を翻訳ページとして指定しません。
4. `python scripts/sync_metadata.py` を実行します。実在するタイトル・description・H1・canonical・パンくずから、構造化データ、欠けているOGP、相互のhreflangを補います。公開日や更新日は推定しません。生成ブロックを直接編集しないでください。
5. `python scripts/check_site.py` を実行します。リンク・アンカー、ID重複、記事一覧の掲載漏れ、サイトマップ、hreflang、JSON-LD、CSPの整合を検査します。
6. ブラウザで表示と操作を確認します。自動検証には次を使用します。

```sh
pip install -r tests/requirements.txt
python -m playwright install --with-deps chromium
python tests/browser_checks.py
```

ローカルのChromiumを使う場合は `CHROMIUM_PATH=/usr/bin/chromium` を指定できます。ブラウザ検証はリポジトリ内のHTMLと画像を同一オリジンの応答として読み込み、外部サービスへ通信せずに実行します。公開サーバーの速度・ヘッダー・実機Safariの検証は別途必要です。

GitHub ActionsはPRとmainへのpushで静的チェックとChromium検証を実行します。公開前にチェックの成功を確認してください。

## 画像とCSS

- 元の画像ファイルは保持します。プロフィールは同じ写真を縮小した既存の480px版を配信しています。
- imgのwidth/heightには実際の画像寸法を指定します。表示上の大きさはCSSで調整します。
- 共通CSSの冒頭にライトテーマのトークンを集約しました。端末がダーク設定でも、現在の明るいテーマを維持します。
- 検索はタイトル・要約に対して端末内で動作します。Cookie・解析・検索クエリ送信はありません。JavaScriptがない場合は全記事を表示します。

## 公開時のセキュリティと確認範囲

HTMLのmeta CSPにより、同一オリジンのスクリプトとハッシュが一致するJSON-LDのみを許可します。object埋め込み、外部baseへの変更、フォーム送信も制限します。インラインのイベントハンドラーは追加せず、JavaScriptは `assets/js/` に配置してください。JSON-LDを変更した場合もメタ情報同期を実行してハッシュを更新します。

既存のインラインstyleとの互換性のため、style-srcはunsafe-inlineを許可しています。これはscript-srcには許可していません。meta CSPはHTTPヘッダー全体の代替ではありません。frame-ancestorsなどのHTTPヘッダー専用設定は、GitHub Pagesの制約を踏まえ、ホスティングの構成を見直す際に検討します。

Search Consoleの実データ、全記事の最新情報、全素材の利用根拠、GitHubアカウントの二要素認証・管理権限は、この自動チェックの対象外です。既存の編集方針に従い個別に確認します。サイト配下のrobots.txtだけではドメイン全体のクローラー設定は変更できません。別リポジトリのドメイン直下の設定は、このサイトの保守で変更しません。
