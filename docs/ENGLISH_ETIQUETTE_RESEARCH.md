# English etiquette article: editorial research and review

Prepared 2026-10-30 against main `c65d998` (fetched from origin). Publication is pending review; this is not a publication date.

## Scope and search intent

Implement one original English guide, `en/articles/park-etiquette.html`: how an international visitor can share queues, transport, walkways and show-viewing space comfortably. The title is **Tokyo Disney Resort Etiquette: Park Rules & Japanese Customs**. The guide separates published requirements, local cast directions and editorial courtesy recommendations. It does not present every courtesy as an official prohibition. No new images or third-party prose are reproduced.

English query hypotheses: `Tokyo Disney Resort etiquette`, `Tokyo Disneyland manners`, `Tokyo DisneySea parade etiquette`, `Tokyo Disney rules for tourists`. These are planning hypotheses, not measured demand, rankings or keyword-volume findings. We could not inspect English search results in this session: the environment's restricted network excludes search engines and the primary-source domains. SERP comparison and live official-source verification remain publication gates. No Search Console access or performance assessment was available.

## Existing English content: full-body overlap audit

All ten articles still exist on the fetched main. Read their bodies, metadata and intent rather than inferring from filenames.

| Existing page | Main reader question | Boundary for the new guide |
| --- | --- | --- |
| first-visit.html | Where do I start planning a first visit? | Keep overview; link to etiquette and detailed ticket/app/train/packing guides. |
| land-vs-sea.html | Which park suits my group? | No new park comparison; etiquette applies to both. |
| rainy-day.html | How should I adapt to rain? | No new weather checklist or indoor itinerary. |
| unique-tokyo-disneysea.html | What makes the park's design distinctive? | No environmental-storytelling expansion. |
| electrical-parade.html | What is Dreamlights and how do I plan viewing? | Link to shared viewing-space advice; do not duplicate the show introduction. |
| getting-there-by-train.html | Which trains and station transfers reach Maihama? | New page covers considerate conversation; existing route guide links to it. |
| official-app-guide.html | Which services does the app offer and when? | Link for bookings; no new app tutorial or service conditions. |
| ticket-basics.html | Which park/date/category and purchase checks matter? | No ticket or refund guide. |
| what-to-pack.html | What essentials and weather/family items should I bring? | No duplicate packing list; link to existing checklist. |
| park-photography.html | How do I take considerate photos and check equipment rules? | Keep equipment and detailed filming coverage there; new page has only a short sightline reminder and link. |

## Sources and verification status

The following are **primary-source review targets**, not sources freshly verified during this session. Existing Japanese photography coverage links to the Japanese TDR pages below and records its own historical check date of 2026-10-11; that date must not be reused as evidence of a new check.

| Target | Intended verification | Status |
| --- | --- | --- |
| https://www.tokyodisneyresort.jp/en/theme_park_terms_of_use.html | English park requirements and instructions; exact wording and live URL | Unverified live; TDR host denied by environment policy |
| https://www.tokyodisneyresort.jp/theme_park_terms_of_use.html | Compare Japanese requirements with English | Unverified live |
| https://www.tokyodisneyresort.jp/topics/info/stay.html | Visitor conduct and park-space guidance | URL present in repository; current content unverified |
| https://www.tokyodisneyresort.jp/tdr/resort/entertainment.html | Sitting/standing arrangements, accessories, sightlines and photography | URL present in repository; current content unverified |
| https://www.japan.travel/en/ | JNTO primary material on considerate travel and customs; locate a specific relevant page | Research pending, not cited as proof in article |
| https://www.jreast.co.jp/multi/en/ | JR East primary guidance on phone calls and train etiquette; locate specific guidance | Research pending, not cited as proof in article |

Observed network evidence: TDR HTTPS request returned `CONNECT tunnel failed, response 403`. Git fetch through existing proxy succeeded; `gh api repos/teruluce/disney-discovery` returned `Forbidden`. No new tokens requested. Research/API domains were added to the environment configuration draft; saving a draft does not activate or publish it. Do not treat a source URL's presence or a static-link check as an HTTP/content validation.

Before editorial approval: read the English and Japanese TDR pages, follow the official English site to any changed URLs, compare important rule wording, confirm transport advice with JR East/JNTO, and inspect English search results. Add an actual source-check date only after performing those checks. The article deliberately uses headband removal as courtesy rather than inventing a park-wide ban, distinguishes seated viewing from obstructing a walkway, and offers cast assistance without generalising about nationality or dismissing discomfort. The draft is not cleared for publication until these source checks finish.

## English SEO source audit

- Audited English homepage, listing and all ten original articles: unique title/description, one H1, `lang=en`, self-canonical, sitemap membership, OGP, schema and reciprocal hreflang. Existing self-canonicals already used the correct `teruluce.github.io` host; no blanket URL rewrite needed.
- Fixed stale hand-authored English-homepage `og:description` by letting the existing metadata synchronizer derive it from the source description.
- Gave the article listing a specific English Tokyo Disney Resort title, H1 and description, and generated CollectionPage data. Existing article titles/descriptions remain unchanged where the audit found no demonstrated defect.
- Added Article/BreadcrumbList data and OGP for the new article through the existing generator, including CSP hashes. No fabricated publication dates, FAQ schema, ratings or authorship credentials.
- No Japanese equivalent for the new etiquette article: no invented hreflang mapping. Its Japanese navigation goes to the article listing and is labelled accordingly.
- Removed the unrelated `en/about.html` ↔ `profile.html` hreflang pairing: English site/editorial information is not a translation of the operator's Japanese biography. Kept ordinary navigation links. Other existing article pairs concern the corresponding subject; reciprocal references pass static validation.
- Added contextual links from the English home, listing, first-visit, train, parade and photography pages. No new duplicate first-visit, packing, app or weather articles.
- Sitemap dates change only for pages actually changed. New draft has no invented publication date. No indexation, CTR, rankings or traffic claims.

## Further article proposals (not implemented)

All query phrases below are unmeasured hypotheses. Primary-source review and English SERP research are still needed before selection.

| Proposal | Reader question | Difference from existing coverage | English query hypothesis | Required sources | Priority |
| --- | --- | --- | --- | --- | --- |
| Asking for help: useful short Japanese at Tokyo Disney Resort | How can I explain a simple need or understand a direction? | Situation-based phrases and pronunciation; expands beyond the two courtesy phrases here, without repeating conduct advice | `Japanese phrases Tokyo Disney Resort` | TDR English service terminology; Japanese-language editorial verification; JNTO language resources | Medium |
| Ordering meals and using park restaurants | What happens from choosing a restaurant to ordering and collecting food? | Dining workflow, counter/table service and where to check dietary needs; app guide remains the source for app preparation | `how to order food Tokyo Disney`, `Tokyo Disney restaurant ordering` | TDR English dining, Mobile Order, Priority Seating and dietary guidance; no guarantee of allergen accommodation | High |
| Where to get help when a park day goes wrong | Where do I go for lost items, a separated group, first aid or language help? | Service locations and practical next steps; existing articles focus on planning rather than problem resolution | `Tokyo DisneySea guest services`, `Tokyo Disneyland lost property` | TDR Guest Relations, lost property, first aid, children and accessibility pages; no invented service/language guarantees | High |
| Accessibility planning for an international visit | What should I check before using mobility or other accessibility support? | Service eligibility, preparation and official contact routes; distinct from train directions and generic first-visit planning | `Tokyo Disney Resort accessibility guide English` | Current TDR accessibility and disability services in English/Japanese; railway accessible station information; eligibility must be verified | Medium, high maintenance |

A broad “differences from other Disney parks” article is deferred: it risks competing with first-visit, tickets, app and this etiquette guide. Use links and carefully sourced additions in those pages first.
