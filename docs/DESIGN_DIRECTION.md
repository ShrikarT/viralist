# Design direction — an editor's evidence desk

One direction: a focused editorial workbench. The user's video occupies the center; timestamped findings and their evidence sit beside it. The product should feel precise and approachable enough that a founder can decide on an edit without learning an analytics tool. The audience graph supplies an explanatory live moment, not the report's permanent visual hierarchy.

## Layout and typography

- Desktop ≥1024px: 56px utility header; main split around 58/42 between player/timeline and notes. Limit readable copy to 65–75 characters per line. Report headline precedes metrics; evidence opens inline at the selected timestamp.
- 640–1023px: player then notes, with compact run status above; compare toggles between cuts while retaining the same timeline position. Below 640px: one column, full-width play controls, notes as an ordered list, compact metric table; no sideways dashboard scrolling.
- System sans serif for body/UI, 16px/24px body, 14px/20px supporting labels, 28–36px semibold verdict. System monospace/tabular numerals only for timecodes and measured values. No font download required for the first slice.
- Spacing scale 4/8/12/16/24/32/48px. Flat surfaces, 1px dividers, restrained 6–8px radii; reserve cards for a separately actionable note or error. Keep controls at least 44px high.

## Proposed palette and visual semantics

Warm paper `#F6F4EF`, white surface `#FFFFFF`, primary ink `#17211F`, muted ink `#53615B`, action green `#175B43`, caution `#8B4A12`, error `#9E2F2F`, selection tint `#E3EEE8`. These are proposed tokens, not a verified accessibility result; measure final pairings at implementation. Use dark text on light tints; white text only on verified dark buttons.

Skip, watch, save and share each use an icon, word label and distinct shape as well as color. Use simple stroke icons and the creator's own frames; no stock persona portraits implying real people. Network edges signify simulation flow, never real social connections. Distinguish actual cast count from hypothetical reach at every size.

## Interaction and states

1. Upload is the sole primary landing action; sample report is secondary and marked recorded. Reels and audience have visible defaults; no signup wall. Show format/size limits and processor disclosure near upload.
2. Stages update only on persisted events. Show elapsed time and completed/total personas; do not animate invented progress or fake quotes. No precise ETA until measured.
3. Select a note → seek video → highlight its range → open reasons. Quote heading says “Simulated persona reason,” not “customer feedback.” Separate measured condition from proposed interpretation.
4. A/B names the baseline and revised cut, shows settings mismatches before deltas, and displays “no clear simulated difference” when the paired interval crosses zero. Never automatically select B as winner.
5. Display model ID, provider version if reported, prompt/extractor versions, trend-pack date, effective cast and assumptions inside the report. Model training cutoff is “not provided” unless the provider supplies it; do not substitute trend-pack date.
6. Empty: one upload prompt; no mock dashboard. Loading: stage and latest real finding. No audio: caveat with usable visual analysis. Thin cast: visible warning. Provider failure: failed stage, retry eligibility and deletion control. Empty notes: “No supported edit found,” not invented advice.
7. Deletion: one clear confirmation, revoke access immediately, show local/provider cleanup separately, and retain a pending state when the provider is unavailable.

Motion: 120–180ms focus/selection transitions; event nodes enter once and stop pulsing. Play/pause live graph; reduced-motion mode swaps animations for static event counts. Do not couple animation timing to fabricated inference progress. When implementing new motion, prefer the repository's animejs guidance.

## Accessibility acceptance

Keyboard upload, seek, note/evidence expansion, compare and deletion; visible focus and logical order; no keyboard trap. Player captions/transcript when available, explicit missing-audio/transcript state. Charts have a text table; graph has an equivalent ordered event list. WCAG AA contrast targets: 4.5:1 body text and 3:1 large text/essential UI. Status announcements are throttled, not one announcement per persona. Support 200% zoom and 320px width. Actual browser checks remain pending.

## Reference principles — no copied product skin

| Reference | Take | Avoid copying |
|---|---|---|
| [Frame.io comments](https://help.frame.io/en/articles/9105278-comments-panel-overview) | Time-linked feedback and explicit resolution | Collaboration sidebar complexity and branding |
| [Descript transcript editing](https://www.descript.com/tools/video-transcript-generator) | Selecting language should reveal the corresponding media moment | A full editing timeline or editing promises |
| [GitHub comparisons](https://docs.github.com/en/pull-requests/how-tos/commit-changes/comparing-commits) | Clearly named base/revision and inspectable differences | Developer jargon and red/green-only interpretation |

Assets needed: owned A/B demo clips, their extracted poster frames, captions, simple wordmark, licensed icon set. Record provenance before public use. These are interaction references from documentation, not a pixel audit.

Avoid stock AI gradients, decorative glass, fake KPIs, endless card grids, generic marketing sections before upload, confetti for higher scores, automatic sound, jittering force graphs and green “viral” badges. Visual emphasis belongs to the clip, the proposed edit and the evidence.
