# Interface rules

Rule ids are stable (`U1` to `U9` are the nine passes, `U10` is the catalogue of specific tells). A removed rule leaves a gap. Each pass names a residue pattern in a rendered surface and its fix.

Adapted from [heydamir/unslop](https://github.com/heydamir/unslop) (`skills/unslop`, CC BY 4.0, by Damir Sokolovsky), reduced to the detection rules a SWE task needs. The original is licensed CC BY 4.0; keep this credit in any copy or adaptation.

## What good looks like

- **One bright element.** The screen has one polished thing carrying the colour and the craft; everything around it is quiet, so the eye lands where it should.
- **Quiet chrome.** Navigation, buttons and text use tinted neutrals and one accent. Nothing glows, nothing competes with the bright element.
- **A clear idea.** One sentence says what the screen shows and why it belongs to this product.
- **Text on calm space.** The headline sits on the empty part of the image or layout, with one primary and one secondary action.
- **Real product, real material.** Previews look like the real app with plausible data; objects look like real things with weight, light and shadow.

The difference between slop and craft is where the richness goes. Slop spreads colour and effects over the chrome. Craft keeps the chrome quiet and puts the richness into one or two moments of content.
## Before the passes

**Size the job honestly.** Audit against U10 first, then pick the path. Many signs across colour, type, icons, and copy: run every pass. A mostly designed screen with a few signs: fix only what the audit found, keep the palette, type, and layout, and report the larger ideas as suggestions rather than applying them. No signs: say so and stop; a good screen is not changed to make it different.

**Read the project's own design system before inventing one.** A token file, a theme stylesheet, a component library, or a config naming the scale and the accent is the answer, and the passes then name its tokens instead of new values. A house style that a pass would flatten is a house style, not slop. Invent a ramp only when the project has none, and say in the report that it is new.

**Judge what renders, not what the source says.** Open the page, run the app, take a screenshot, and look at it before changing a value; a rule can pass in the source and still look wrong on the screen. Re-render once after the passes and compare against the audit, rather than reasoning about the CSS.

**Write the direction first, in five lines:** what the product does and for whom; two or three concrete character words ("clean", "modern", "minimal", and "premium" describe every template, so they are not words); the world it belongs to, which tints the neutrals and picks the accent; one or two moments that carry the richness; and one signature detail only this product would have. Derive all five from the product, never from what is trending.

## U1. Spacing

- Everything sits on a 4px grid: margins, paddings, gaps, fixed heights. `mt-[13px]` and `py-[11px]` break the rhythm; replace them with steps from the scale.
- Same thing, same size. All rows in a list share one height and one gap; all cards in a row share one padding.
- Space shows grouping: space inside a group is smaller than space between groups.
- Things line up. Icons sit in one column, labels start on one line, numbers align right in one column. Nothing is nudged off the line by a stray translate or odd margin.
- Padding follows density: compact panels and sidebars around 16, cards 20 to 24, page edges 24 to 32.
- Navigation is the densest part of an app: rows 32 to 36 tall with 2 to 4 between them, a section label 24 above its items and 8 below.

## U2. Color

- Build from one neutral ramp, tinted toward the product's world. Background, raised surfaces, borders and text all come from that ramp.
- In apps and dashboards the surfaces stay neutral. The world shows in the accent, the charts and the moments, not in the backgrounds.
- Three text roles: primary, secondary, muted. Not ten slightly different shades of one hue.
- One accent in the chrome, used rarely: the primary action, the selection, the one number that matters.
- The moments are the exception. Inside them colour can be rich, several hues in a chart, a rendered object with real materials.
- Accent with text on it reaches 4.5 to 1 contrast. Darken it or put dark text on it.
- On dark themes depth comes from surface steps and hairlines, not shadows.
- Semantic colours only carry meaning, like green for a good change and red for an error, toned down to sit inside the palette.
- Remove hue gradients on surfaces, gradient text, coloured glows and coloured shadows, radial colour washes, blobs behind content, and neon borders.
- Borders are quiet hairlines, the text colour of the ramp at 6 to 10% opacity.
- A gradient is allowed only as a small tone shift inside one neutral. Never from one hue to another.

## U3. Icons

- Every emoji used as an icon or as decoration in a label becomes a line icon from one set. Use the set the project already has, otherwise lucide.
- One size and one stroke everywhere, 16 or 18px with a 1.5 stroke.
- Icons take the colour of their text role, usually secondary or muted. They never get their own colours.
- The icon box has the same width in every row and a fixed gap to the label, 8 or 10.
- Drop icons that add nothing. Categories that need colour get a small status dot.

## U4. Copy

- Headlines say what the product does for whom, in plain words, so they could not fit another product. Use the facts already on the page.
- No exclamation marks in interface text, and never `!!`.
- No greeting headlines. The title names the context, like the page name or the period.
- Short labels: `Search`, not `Search anything...`.
- A change says what it compares to: `+12% vs last month`.
- Headlines, subheads, labels, buttons and captions end without a period. Only paragraphs of several sentences keep their periods.
- No hype words like "supercharge", "seamless", "unlock", "magic", "revolutionize", "game-changing", and no `AI-powered` on everything.
- Claims that cannot be checked, like `Loved by 10,000+ teams`, become quiet and specific if the user confirms they are real, and are removed otherwise.
- Mock data looks real, with plausible numbers and names, never a bracketed placeholder.
- Badges like `PRO`, `New` or `Beta` go away unless the product needs them, and then they are quiet text.

## U5. Type

- Choose type for the character of the product. Keep the project's font when it is part of a real brand; a default nobody chose may be swapped when another family fits better.
- One family for the interface, plus at most one partner: a mono for figures and meta, or a display face for large headlines.
- A few sizes from a scale and two weights, 400 and 500, with 600 at most for rare emphasis.
- Hierarchy comes from size and colour, not from weight.
- Sentence case everywhere. Labels like `NAVIGATION` become `Navigation`.
- Small text never gets negative letter spacing. Tight tracking is only for large display text.
- Numbers use tabular figures and one format across the screen.
- No italic for emphasis.

## U6. Layout

- Keep the sections and their order. Inside a section, alignment and proportions may change when that makes the screen clearer.
- Apps and dashboards keep real app proportions: the shell fills the viewport, a sidebar of 240 to 280, fluid content capped around 1440 to 1600, and the page as long as its content. Never shrink an app into a narrow centred column.
- Without a scene, use an asymmetric split, text on one side and the visual given at least half the width. Everything stacked and centred is the template default.
- Long headlines align left. Centred text works for one or two short lines.
- One primary action and at most one secondary action next to it.
- Navigation stays quiet: logo, the existing links, one button. A floating pill header is not required.
- Compose the first screen as a whole, with no dead empty band.
- On small screens everything stacks in reading order, the headline drops to the mobile size, and the visual comes after the actions.

## U7. Details

- Nested radius: an inner radius equals the outer radius minus the padding between them, never less than 4. Controls 8 to 10, cards 12 to 16, panels 14 to 20. Not everything is a pill.
- Counts and meta become quiet text, often mono and muted, instead of glowing pills.
- Charts sit on a muted grid with muted mono labels. No rainbow bars inside one series, no glowing bars, no uppercase day labels.
- Charts have a hierarchy: one main chart is clearly the biggest thing on the screen; anything else is smaller and different in kind, like a ranked list with thin bars or a short table.
- One accent per chart. The thing that matters gets the accent, everything else sits in neutral steps.
- Stat cards are numbers: a label, a big figure, and a change with what it compares to. No sparklines, tallies or mini bars added for decoration.
- Vary the sizes. Cards of equal width side by side with the same content read as a template.
- Pick the chart type for the data: a trend is a line, a comparison is bars, a share is one stacked bar or a list, a single goal is a progress bar.
- Hover and focus states exist and stay inside the palette. A visible focus ring for keyboard users.
- The logo is the product name in the main family, plus a simple mark if there is one. No gradient wordmark, no sparkle tile.

## U8. Visuals

- Decorative filler goes: glossy blobs, orbs, nebulas, floating cubes, glowing grids, holographic brains and robots say nothing about the product.
- A landing hero gets a visual that shows something true.
- Dashboards and app screens almost never need generated images. Their moments come from the product itself: a chart drawn with care, figures set well, real content, a status that feels alive.
- Generate images for an app only for empty states, onboarding and marketing moments, or when the user asks for it.
- Under a scene, or as the visual when there is no tool, show the product: a preview in code of what the page already promises, with plausible data.
- The product view carries a moment, not just a plain card.
- With an image tool: show the user the prompt and the model before running it, since generation can cost money; run once and judge the result against the sentence you wrote before trying again.
- Without one: build what you can in code, write the prompts for the rest, and leave an empty slot of the right size so nothing unfinished ships by accident.

## U9. Motion

- Remove motion that loops for no reason: `animate-pulse`, `animate-ping` on things that are not live, shimmer on headings, breathing glows, floating elements, parallax.
- Remove `transition-all`, bouncy springs, `hover:scale` on cards, and anything that moves more than a few pixels on hover.
- Keep motion that explains something: a quick colour or surface change on hover, a tiny scale down on press, a menu that fades and rises a few pixels, a changed number that tweens.
- Transition colour, background, border, opacity and transform, and name them. Never animate width, height, top, left, margins or large blurs.
- One easing curve and a few durations across the screen.
- At most one entrance on load: a short fade and rise with a small stagger.

## U10. Signs of slop

Each line pairs a sign with its fix.

- Purple to blue or violet to pink gradients on backgrounds, cards, buttons, the active nav item → one neutral surface, accent only where it means something.
- Gradient text in headings, numbers or the logo → solid primary text colour.
- Coloured glows, `drop-shadow` on emoji, glowing pills → remove; depth from surface steps and hairlines.
- Radial colour washes or blurred blobs behind content → remove.
- Neon or high-contrast coloured borders → hairline at 6 to 10% opacity.
- Many near-identical tints of the same hue for text → three text roles from one neutral ramp.
- Every element highlighted, so nothing stands out → one accent used once or twice per screen.
- Headings at weight 800 or 900 → 400 to 500, and size for hierarchy.
- Uppercase labels with wide tracking → sentence case at normal tracking.
- Too many sizes and weights on one screen → a few sizes, weights 400 and 500.
- Numbers in mixed formats, like `$48,210` next to `$124,860.40` → one format, tabular figures.
- Negative letter spacing on small text → zero or slightly positive.
- Italic used for emphasis → colour or weight instead.
- Emoji as nav icons, label decoration or status → one line icon set or nothing.
- Icons in many sizes and colours → one size, one stroke, text-role colour.
- Arbitrary spacing values → steps on the 4px scale.
- Rows in one list with different heights or gaps → one height, one gap.
- Greeting headlines, exclamation marks, `!!` → plain statement.
- Changes without a reference → `+12% vs last month`.
- Hype words → what the thing actually does.
- Trailing periods on labels and buttons → none.
- Glowing pills for counts, plans, shortcuts, status → quiet mono text or a keycap.
- `PRO`, `New`, `Beta` badges everywhere → remove, or one quiet text badge.
- Every element a full pill → radius by size, nested radius math.
- Charts with rainbow bars, glowing bars, uppercase day labels → one or two series, muted grid and mono labels.
- Sparklines or mini bars added to every stat card → the number, its label and its change.
- Equal cards side by side, each with the same chart → one main chart, compact stats, varied widths.
- Logo as a gradient tile with a sparkle → product name as text plus a flat mark.
- A pill badge above the headline → remove, or a quiet text link if it is real news.
- A headline that could fit any product → say what the product does for whom.
- Floating blobs, orbs, grids and glowing lines behind the hero → plain background or one real product visual.
- Three or more buttons under the headline → one primary and at most one secondary action.
- `Trusted by 10,000+ teams` without a source → ask if it is real, then make it quiet and specific or remove it.
- Feature cards with an emoji, a bold title and a vague line → fewer features, concrete copy, line icons or none.
- Stock robots, glowing brains, circuit lines, holograms for anything AI → remove, or show what the AI actually produces.
- Text, fake buttons or a fake logo baked into an image → real text in the page, a clean image without text.
- An image with a hard edge against the page → background matched to the page and a soft mask.
- A visual on every section → one visual where it helps, usually only the hero.
- `animate-pulse`, `animate-ping`, breathing glows on things that are not live → static.
- `transition-all` and `hover:scale` → colour or surface step on hover, a tiny scale down on press.
- Everything flying in on load from different directions → one short fade and rise with a small stagger.
- Parallax and elements floating on scroll → static layout.
- Animating width, height, top or left → transform and opacity.

## The template check

This is not slop, but it is what a cleaned-up screen falls back to when nobody made a decision. After the passes, swap the product name for another product's: would the screen still fit? If yes, push the direction harder in the copy, the visual, and the one detail only this product would have.
