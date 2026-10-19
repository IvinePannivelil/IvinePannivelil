# Verification — 16 October 2026

## Completed here

- Approved source PNG compared byte-for-byte against the finalized generated
  image. It is unchanged; SHA-256 is recorded in `asset-manifest.json`.
- All six SVGs parse as XML. Runtime artwork embeds its PNG, references only
  local SVG definitions and contains no script or foreignObject element.
- Static SVGs contain no animation keyframes.
- Desktop and mobile static layouts rendered with Sharp/librsvg and visually
  inspected. Text, face, full body and shoes are visible in the rendered layouts.
- Individual head and body regions rendered and inspected. The body contains
  no duplicate head; a neck overlap is intentional.
- Head angles 0°, −0.65° and +0.35° rendered with explicit SVG transforms.
  Pixel differences are confined to the head/neck area: desktop difference
  bounds left `(717,26)-(791,122)`, right `(717,26)-(792,122)` in a 960×540 image.
  Body, arms and shoes are unchanged in these sampled poses.
- Preview JavaScript passes Node syntax checking.
- Build script successfully regenerates all variants with Python standard library.

## Pending in Antigravity / Chrome

The local browser binary was unavailable and its download failed. No live-browser
execution, CSS-timeline capture, keyboard interaction check or console/network
inspection is claimed here. Static angle renders verify geometry, not browser
timing or CSS transform-origin behavior. The task prompt includes these checks.

- Verify CSS head pivot and timing, external `<img>` animation and controls.
- Test Replay, static toggle, phone toggle, region isolation and angle slider.
- Test real browser widths 1440, 1024, 390 and 360 px.
- Test system reduced-motion emulation and the complete still compositions.
- Inspect edges and neck join during motion, including against light/checkerboard.
- Record 12 seconds covering entrance and at least one idle cycle.
- Verify actual GitHub README rendering later, before public-profile publication.

## Known prototype limits

- Embedded source makes each generated SVG approximately 2.36 MiB. This is a
  fidelity-first prototype, not a final optimized publication payload. The full
  kit includes repeated assets for inspection; a final README should load only
  the appropriate hero variant.
- Manual SVG contours retain small colored edge halos from the approved source.
  Full clean matting is not claimed, especially for large white backgrounds.
- Motion is deliberately small and limited to the head. It is not a fully rigged
  person, body-part PNG set, blink sequence, arm gesture or video generation.
- The face and fuller build are approved; the hero layout and motion await review.

## Source checks for optional tools

Checked on 16 October 2026:

- Google Antigravity Browser overview:
  <https://antigravity.google/docs/ide/browser>
- Live Server listing (local server and reload):
  <https://open-vsx.org/extension/ritwickdey/LiveServer/5.7.4>
- SVG extension listing (syntax, preview and minimization caveat):
  <https://open-vsx.org/extension/jock/svg>

No assumption is made that a particular extension is installed in the user's IDE.
