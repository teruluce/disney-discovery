# Disney Discovery

**ディズニーの、気になることと出会う。**

Disney Discoveryは、ディズニーの実用情報、舞浜での体験、写真、個人的な記録、キャラクターや映画の読み物を発信する独立した情報サイトです。既存の記事・URL・日本語版・英語版・Discovery Journalを活用し、無理のないペースで運営します。

主力ブランドのBGS Chroniclesは、BGS・パークの物語・世界観・イマジニアリングを深く扱います。DDは実用情報と体験・写真・読み物を担当し、BGSの記事を移植・言い換え量産しません。

運営上はSEO・Webデザイン・記事構成・AIによる品質監査を検証します。読者向けには通常の情報サイトとして案内し、実験を理由に正確性や既存資産の保護を緩めません。CMSや実験管理システムは導入しません。

## 編集方針
- 検索している人の疑問に、まずわかりやすく答える
- 初心者・ライト層にも伝わる言葉で書く
- 事実と推測を分け、公式情報や信頼できる情報源を確認する
- 更新頻度を無理に上げず、正確さと読みやすさを優先する
- 既存プロジェクト「BGS」とは別のリポジトリ・編集方針で運営する

## English version
An English-language section for international visitors is available under `en/`. It includes practical Tokyo Disney Resort guides and approachable articles about park experiences. The English pages share the existing visual system and are linked from the Japanese homepage.

## Discovery Journal

てるのディズニーや舞浜での日々を写真と文章で残す[日々の記録](journal/)。投稿方法と編集方針は [Journalの運用](docs/JOURNAL.md) を参照してください。

## Project documents
- [公開前チェックと保守](docs/MAINTENANCE.md)
- [サイト企画書](docs/SITE_PLAN.md)
- [SEO・記事戦略](docs/SEO_STRATEGY.md)
- [コンテンツ制作ガイドライン](docs/CONTENT_GUIDELINES.md)
- [ChatGPT・Claude共通作業ログ](docs/AI_WORK_LOG.md)

## Status
トップページ・運営者プロフィール・日本語と英語の記事一覧・各テーマの記事・プライバシーポリシー・お問い合わせ・404ページを用意しています。現在の記事は[日本語の記事一覧](articles/index.html)と[英語の記事一覧](en/articles/index.html)で確認できます。

HTML/CSSによる静的サイトとして構成し、GitHub Pagesで公開しています。公開先URLは https://teruluce.github.io/disney-discovery/ です。

記事では、制度や運営情報の確認先・確認時点を必要な箇所に示します。検索エンジン向けに `sitemap.xml`、`robots.txt`、Googleの所有権確認用HTMLを配置しています。Search Consoleの管理画面での登録・計測状況は、リポジトリだけでは確認できません。

## 正式デザインと公開確認

写真入りトップの写真誌スタイルを全ページに適用しています。共通の表示は `assets/css/magazine.css`、ページ構造は既存HTML/CSSで管理します。[正式版の確認資料](docs/FINAL_REVIEW.md)を参照してください。mainへのpushでは既存検証に加えて、GitHub Pages上の実URLを確認する検証ジョブの公開URLチェックを実行します。
