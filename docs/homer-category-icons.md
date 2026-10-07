# Category icon colors (both Homer dashboards)

Only category heading icons and Font Awesome app icons receive category colors.
Text, cards, navigation, logo/favicon, service URLs/targets/order and the existing
`walkxcode` theme and baseline color settings remain unchanged.

| Category | Color | Light | Dark |
| --- | --- | --- | --- |
| Alltag & Organisation | green | `#238348` | `#69c995` |
| Filme & Musik | purple | `#8050b5` | `#bd95eb` |
| Bücher & Hörbücher | orange | `#b76413` | `#efae60` |
| Fotos & Galerien | pink | `#be4879` | `#ec91b4` |
| Smart Home & Automation | turquoise | `#14847c` | `#59c7be` |
| Monitoring | blue | `#3478bd` | `#7eb7ee` |
| Server & Container | slate | `#66758a` | `#a5b4c8` |
| Netzwerk & Zugang | coral | `#c25847` | `#ef9c8b` |

## YAML-only deployment

Both YAML files include the same `stylesheet` data URL containing the complete
CSS. Homer's supported stylesheet loader imports it normally; no extra file has
to be copied to either web server. The reported existing YAML-only cron sync is
sufficient once these configs are published. This adds no CDN, GitHub Raw
stylesheet dependency, runtime generator, HTML injection or server changes.

`homer-category-icons.css` is the readable source, not a deployed dependency.
After editing it, update both embedded copies with the standard-library-only tool:

```sh
python3 scripts/embed-homer-icons.py
python3 scripts/embed-homer-icons.py --check
```

Keep the `hc-icon-COLOR` class appended to each group/app's existing `icon`
value. Marking the icons rather than just using group classes keeps app colors
when Homer flattens groups for search and works in both layouts. Selectors affect
only heading `i` elements and app `i` elements inside `.card .media-left`; images
and navigation icons are not selected. `#app.light`/`#app.dark` provide the two
palettes, including Homer's auto-theme selection.

## Verification performed

- Parsed both YAML files: eight categories, 31 unique local apps, 19 unique remote
  apps. After removing only the new stylesheet and icon class tokens, each config
  is identical to its previous parsed configuration. Bibel remains under books;
  Asset Tracker uses its cloud URL in both dashboards.
- Both embedded data URLs decode byte-for-byte to the shared CSS source.
- Tested the actual deployed local and remote Homer renderers with browser-local
  replacement of only `/assets/config.yml`; nothing was deployed or published.
  Compared original and modified configs in light and dark modes: exact palette
  matches for every heading/app icon; heading text, card/title/subtitle styles,
  navigation and all rendered service links/targets unchanged.
- Icon contrast against the configured page/card backgrounds: minimum 3.98:1
  light and 5.84:1 dark (non-text icon threshold 3:1).
- Additional local-renderer checks: auto light/dark on reload, Asset Tracker
  search result retains its category color, and horizontal layout retains all
  eight heading and 31 app colors.
- Regenerator and `--check` executed successfully; `git diff --check` clean.

No commit/push was performed. Cron execution and post-publication live sync are
not verified. Browser computed-style tests passed; screenshot capture timed out.
If a future reverse proxy adds a CSP blocking `data:` styles or inline stylesheet
imports, it must allow this mechanism, or the CSS must be deployed separately.

## Upstream implementation checked

Homer upstream `bastienwirtz/homer`: `docs/theming.md`, `docs/configuration.md`,
`src/App.vue`, `src/components/ServiceGroup.vue`,
`src/components/GroupHeader.vue`, `src/components/services/Generic.vue`, and
`src/components/DarkMode.vue`. `App.vue` uses the configured stylesheet URL in
an `@import`; GroupHeader/Generic bind `icon` as class tokens. ServiceGroup
supports group/item classes, but search rebuilds groups without those classes.
The live-renderer test verifies data-URL support instead of assuming it from
upstream alone.
