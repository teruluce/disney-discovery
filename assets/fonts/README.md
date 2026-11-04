# Notebook typography

These fonts are served from this repository. Page rendering does not contact Google Fonts or another font service. Both families use `font-display: swap`; system fonts remain usable when a font is unavailable.

| File | Upstream source | License |
| --- | --- | --- |
| `yomogi-notebook.woff2` | [Yomogi Regular](https://github.com/google/fonts/blob/main/ofl/yomogi/Yomogi-Regular.ttf), downloaded 2026-11-04 | [SIL OFL 1.1](Yomogi-OFL.txt) |
| `caveat-latin.woff2` | [Caveat variable](https://github.com/google/fonts/blob/main/ofl/caveat/Caveat%5Bwght%5D.ttf), downloaded 2026-11-04 | [SIL OFL 1.1](Caveat-OFL.txt) |

Yomogi is used for headings, not long-form body text. It contains the characters in the site's existing HTML, Latin U+0020–00FF and Japanese punctuation/kana U+3000–30FF. New characters outside the subset use the CSS fallback. Caveat contains Latin U+0020–024F, arrows U+2192/U+2197 and punctuation U+2019/U+2014; its original weight axis is retained.

To regenerate from the upstream TTF files, use FontTools with Brotli support (`fonttools[woff]`): collect the codepoints from the site's HTML, include the ranges above, pass them to `fontTools.subset.Subsetter.populate(unicodes=...)`, subset the TTF, set `font.flavor = 'woff2'`, and save. Keep the accompanying license files. No font build or download is required to serve the site.
