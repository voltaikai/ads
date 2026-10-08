---
name: Solar Poppy — California Virtual Power Plant Program
canvas: { width: 1080, height: 1920, fps: 30 }
colors:
  navy: "#13304A"          # canvas, glass tint, text on light surfaces, all shadows
  poppy: "#F7941D"         # main accent: highlight words, active subtitle word, checks
  burnt: "#E2711D"         # secondary accent: gradients with poppy, alt petals, orange shadows, corner glow
  gold: "#FFD27A"          # eyebrows, bolt, small glints/glows only
  white: "#FFFFFF"         # headlines/main text on navy, logo disc
  greyblue: "#D5DEE7"      # sublines, muted text, inactive subtitle words
typography:
  headline: { family: Sora, weight: 800, letterSpacing: -0.025em, lineHeight: 1.0, case: sentence }
  eyebrow: { family: Sora, weight: 600, letterSpacing: 0.3em, case: upper, color: gold }
  subline: { family: Sora, weight: 400, color: greyblue, separator: "poppy dot •" }
  chip: { family: Sora, weight: 600, case: sentence }
  subtitle: { family: Montserrat, weight: 700 }
  numeral: { family: Bricolage Grotesque, weight: 800 }
type_scale_px:
  headline-xl: 84        # cutaway + end-card headlines
  headline-l: 72         # glass cards over footage
  row: 56                # list rows inside cards
  chip: 38
  subline: 30
  eyebrow: 24
  subtitle: 68
  numeral: 64
  footer: 26
spacing_px:
  gutter: 90             # left/right content edge (text stack is left-aligned at x=90)
  card-pad-x: 48
  card-pad-y: 40
  stack-gap: 18          # eyebrow -> headline
  stack-gap-sub: 24      # headline -> subline
safe_zone_px: { top: 250, bottom: 1270 }     # nothing above 250 or below 1270 (Meta UI)
zones_px:
  card-over-footage: [900, 1170]   # glass cards on talking-head shots (face sits ~70-900)
  subtitles: [1190, 1270]          # line centre ~1230 (64% down)
glass:
  fill: "rgba(19,48,74,0.42)"      # navy at 42%
  blur: 26px                       # pills/subtitles: 16px
  border: "1px solid rgba(255,255,255,0.18)"
  top-highlight: "inset 0 1px 0 rgba(255,210,122,0.25)"
  shadow: "0 34px 72px rgba(19,48,74,0.40)"
  radius: 32px                     # cards; pills/chips fully rounded
  grain: 2.5%                      # static noise texture inside every glass surface
  sweep: { band: "gold→white", opacity: 0.14, duration: 0.9s, ease: power2.inOut }
motion:
  ease-enter: expo.out             # alt: power4.out
  ease-exit: power3.in
  ease-move: power3.inOut
  dur-enter: [0.6, 0.9]
  dur-exit: [0.35, 0.5]
  word-stagger: 0.07
  row-stagger: 0.12
  content-stagger: 0.08
  check-delay: 0.15
  transition: 0.35                 # blur-through / glass-wipe
  banned: [linear, bounce, elastic, back]
camera:
  push-in: "scale 1.00 → 1.06 per talking-head section"
  punch-in: "1.12, power3.out 0.35s, ease back over the next sentence (power3.inOut)"
---

## Overview

Warm California light meets clean tech. Navy is the canvas; orange is sunlight, used once per
screen. Everything is deliberate, with lots of negative space, frosted navy glass that catches a
gold edge of sun, and calm, overlapping motion. Think product film, not infomercial.

## The frame

- 1080x1920. Content lives between y=250 and y=1270. Text stacks are left-aligned at x=90.
- Talking-head shots: the A-roll is framed 280px higher than shot (face ~y 70–900) with a navy
  fade at the foot (inside Meta's bottom UI zone), so glass cards own y 900–1170 and never
  touch the face. Subtitles sit at y 1190–1270 on every shot.
- Cutaways: solid navy plus one burnt-orange radial glow (12%) in the top-right corner,
  like late sun. Graphics occupy y 260–1170, above the subtitles.

## Brand stack (every title moment and the end card)

1. Eyebrow: Sora 600, uppercase, 0.3em, gold, 24px.
2. Headline: Sora 800, white, -0.025em, line-height 1.0; the final words in poppy orange.
3. Subline: Sora 400, grey-blue, items separated by poppy-orange dots.

## Composition rules

- One orange accent per screen, usually a headline's final words.
- Gold only small: eyebrows, the bolt, glints, glow pulses.
- Shadows are navy at reduced opacity. Never #000.
- Icons: 2px line, round caps/joins, white or poppy, friendly rounded geometry.
- Charts are illustrative only: no values, labels or currency.
- Under any graphic over footage: a soft navy vignette so text always reads.

## Do / Don't

- Do let entrances overlap; the next element starts before the last lands.
- Do make exits faster than entrances and reverse the stagger.
- Don't pop anything on/off, bounce, wobble, or use linear easing on anything visible.
- Don't show "No debt", "lower bills", numbers, prices, PG&E or Sunrun logos.
