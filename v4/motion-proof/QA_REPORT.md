# Motion Proof QA Report — 17 October 2026 (Revision 2)

## 1. Delivery Summary

| Item | Artifact Path / Value |
|---|---|
| Working folder | `v4/motion-proof/` |
| Local preview URL | `http://127.0.0.1:8089/preview.html` |
| Server command | `python -m http.server 8089 --bind 127.0.0.1 --directory v4/motion-proof` |
| Continuous motion recording | `screenshots/RECORDING_hero_motion_continuous_11s.webp` (1.57 MB, 116 frames, 11.60 s encoded playback, 10 fps) — clean continuous capture of full hero covering 0.8s entrance + full 7s head-idle cycle with no UI interference. |
| General test-session recording | `screenshots/RECORDING_test_session_54s.webp` (6.4 MB, 541 frames at 100 ms = 54.1 s encoded playback) — preserved full interactive test session. |
| Real 1440 px viewport screenshot | `screenshots/vp_real_1440.png` |
| Real 1024 px viewport screenshot | `screenshots/vp_real_1024.png` |
| Real 390 px mobile screenshot (full hero + shoes) | `screenshots/vp_real_390_full_hero.png` |
| Real 360 px compact screenshot (full hero + shoes) | `screenshots/vp_real_360_full_hero.png` |
| Reduced motion (HTML preview enforced) | `screenshots/proof_reduced_motion_preview.png` |
| Reduced motion (direct animated SVG test) | `screenshots/proof_direct_animated_svg_reduced_motion.png` |
| Layer isolation: Head-only | `screenshots/phase3_body_hidden_1792211980423.png` |
| Layer isolation: Body-only | `screenshots/phase3_head_hidden_1792211995040.png` |
| Layer inspector slider: −0.65° | `screenshots/inspector_slider_neg_0_65deg.png` |
| Layer inspector slider: +0.35° | `screenshots/inspector_slider_pos_0_35deg.png` |
| Updated review package | `v4/motion-proof-v1.zip` |

---

## 2. Actual Implementation Values (Verified Against Source & Runtime)

- **Head idle rotation range**: Asymmetric **−0.65° to +0.35°** around source pivot `(493px, 292px)`.
- **Head idle timing**: 7.0 seconds cycle duration, 1.2 seconds delay, infinite repeat (`@keyframes headIdle` in animated SVGs).
- **Entrance animation**: **0.8 seconds with `ease-out`** (`@keyframes arrive { from { opacity: .35; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }`).
- **Decorative keyframe name**: **`trace`** (`@keyframes trace { to { stroke-dashoffset: -188; } }`).
- **Manual layer inspector slider**: Native `<input type="range">` with range **−0.65° to +0.35°** (`min="-0.65" max="0.35" step="0.05"`).
  *(Correction: The previously submitted screenshot labeled "slider_15deg" displayed +0.25°; the slider was never ±15°. The new screenshots `inspector_slider_neg_0_65deg.png` and `inspector_slider_pos_0_35deg.png` document the exact −0.65° and +0.35° extremes).*

---

## 3. Real Browser Viewport Verification (Actual CSS Window Widths)

All metrics recorded in live Google Chrome browser sessions:

| Target Viewport | window.innerWidth | clientWidth | scrollWidth | Device Pixel Ratio | Horizontal Overflow? | Composition Rendered |
|---|---|---|---|---|---|---|
| **1440 px** (Desktop) | 1440 px | 1440 px | 1440 px | 1.0 | **NO** (`scrollWidth <= clientWidth`) | Desktop layout (`hero-desktop.svg`), stage max 960px |
| **1024 px** (Laptop) | 1024 px | 1024 px | 1024 px | 1.0 | **NO** (`scrollWidth <= clientWidth`) | Desktop layout (`hero-desktop.svg`), stage scales smoothly |
| **390 px** (Phone) | 390 px | 390 px | 390 px | 1.0 | **NO** (`scrollWidth <= clientWidth`) | Mobile layout (`hero-mobile.svg`), 390×650 vertical stack |
| **360 px** (Compact phone) | 360 px | 360 px | 360 px | 1.0 | **NO** (`scrollWidth <= clientWidth`) | Mobile layout (`hero-mobile.svg`), complete hero & shoes visible |

### Page-Wide Overflow Auditing (at 360 px):
- **Hero controls**: `flex-wrap: wrap; gap: 8px` wraps cleanly without horizontal overflow.
- **Layer inspector**: CSS grid switches to single-column layout via `@media (max-width: 660px)`, canvas and controls fit within 360px.
- **Asset sizes table**: Wrapped in `<div class="table-wrap" style="overflow-x:auto">`, preventing wide monospace text from pushing the viewport.
- **Code & text**: `word-break: break-all` on code and `main { overflow-x: clip }` ensure zero page-level horizontal scrollbar.
- **Full character visibility**: Both `vp_real_390_full_hero.png` and `vp_real_360_full_hero.png` capture the complete mobile composition from the top headline down to the white shoes.

---

## 4. Preview-Width Bug Fix & Controls Clarification

### Bug Fix
- **Issue**: In `preview.html`, `render()` previously computed `stage.style.maxWidth = (phone ? 390 : activeVp) + 'px'`. When phone mode was active, selecting the 360 px container button was overridden with 390 px.
- **Resolution**: Updated `render()` to use `stage.style.maxWidth = activeVp + 'px'`. Clicking `vp-360` sets stage max-width to exactly 360px (verified by computed style measurement `stage.style.maxWidth === "360px"`). Clicking `vp-390` sets 390px, `vp-1024` sets 760px, and `vp-1440` sets 960px.
- **Layout Consistency**: When the browser window width is <= 480px, phone layout defaults to active. The desktop/phone layout toggle updates `activeVp` and active button states synchronously.

### Label Clarification
- Renamed the section controls description to:
  `Simulated hero container width (does not resize browser viewport):`
- Renamed buttons to:
  - `960 px container (Desktop 1440)`
  - `760 px container (Laptop 1024)`
  - `390 px container (Phone)`
  - `360 px container (Compact phone)`
- Removed `"as GitHub sees it"` from Section 1 heading. The heading now reads:
  `① External <img> rendering` (Local preview). Live GitHub rendering remains unverified until repository publication.

---

## 5. Verified Reduced-Motion Behavior

Tested using both OS-level system setting and direct browser media evaluation:

### A. Preview Page (`preview.html`)
- **System Setting**: Emulated / enabled `prefers-reduced-motion: reduce`.
- **Media Query Check**: `window.matchMedia('(prefers-reduced-motion: reduce)').matches === true`.
- **Enforcement**:
  - `#rm-badge` activates and displays `⚠ Reduced motion active`.
  - `#mode-label` displays `Reduced motion active — still SVG enforced by system.`
  - `#motion-btn` is disabled with text `Still version enforced (Reduced motion)`.
  - `#hero-img` loads the static SVG (`hero-desktop-static.svg` or `hero-mobile-static.svg`) with zero keyframes.
  - Interacting with `Replay`, `Phone layout`, or container width buttons retains the static SVG and keeps the motion toggle disabled.

### B. Direct Animated SVG (`assets/hero-desktop.svg`)
- Navigated directly to `http://127.0.0.1:8089/assets/hero-desktop.svg` in Chrome with `prefers-reduced-motion: reduce` active.
- Evaluated computed styles on the SVG DOM:
  - `.entrance` animation: `animationName: none` (PASS)
  - `.head-idle` animation: `animationName: none` (PASS)
  - `.trace` animation: `animationName: none` (PASS)
  - `.entrance` opacity: `1` (PASS)
  - `.entrance` transform: `none` (PASS)
- Confirms that the SVG's internal `@media (prefers-reduced-motion: reduce)` rule independently stops all animations even when loaded directly without HTML wrapper logic.

---

## 6. Motion Recordings Analysis

| Recording File | Frame Count | Frame Delay | Encoded Duration | Capture Rate | Content & Purpose |
|---|---|---|---|---|---|
| `RECORDING_hero_motion_continuous_11s.webp` | 116 | 100 ms | **11.60 s** | ~10 fps | **Clean continuous proof**: Full desktop hero centered, 0.8s entrance slide followed by complete 7s head-idle cycle (−0.65° to +0.35° back to 0°). Zero UI clicks or scrolling during playback. |
| `RECORDING_test_session_54s.webp` | 541 | 100 ms | **54.10 s** | ~10 fps | **Full interactive test session**: Replay, still/animated toggle, phone layout swap, container width cycling, layer isolation toggles, and angle slider manipulation. |

*Capture limitation note*: Browser subagent recording captures WebP frames at 100 ms intervals (~10 fps). While smooth and representative of the CSS keyframes, higher temporal fidelity (60 fps) is achieved in native Chrome rendering.

---

## 7. Checks Run: Browser-Performed vs Source-Code Inspection

### Browser-Performed Checks (Chrome on localhost:8089)
1. **Continuous motion playback**: Observed 0.8s ease-out entrance followed by 7s head idle oscillation. Body and folded arms confirmed stationary.
2. **Real viewport measurements**: Measured `window.innerWidth`, `clientWidth`, `scrollWidth` at 1440, 1024, 390, and 360 px. Confirmed zero horizontal overflow.
3. **Reduced motion enforcement**: Verified `matchMedia('(prefers-reduced-motion: reduce)').matches` disables animations in both HTML preview and direct SVG.
4. **Layer isolation & pivot test**: Tested `#head-pivot` rotation at −0.65° and +0.35° around `(493px, 292px)`. Verified body and neck underlap hide together without duplicate head.
5. **Interactive controls**: Tested Replay, Still/Animated toggle, Phone layout toggle, container buttons, and Reset pose.

### Source-Code Inspection (PowerShell & Python Verification)
1. **Master image integrity**: SHA-256 `a9885b2629713ef3048b98fe9ded0b749c080dd06b4e8ac1e6f4fe0220d52101` verified identical byte-for-byte before and after all operations.
2. **Deterministic build**: `scripts/build_motion.py` re-run with exit code 0 using Python standard library.
3. **SVG structure**: Grep confirmed static SVGs have zero `@keyframes`; animated SVGs contain `arrive`, `headIdle`, and `trace`. Zero `foreignObject`, `<script>`, or external HTTP font references.

---

## 8. Unverified Scope & Limitations

| Item | Status | Detail |
|---|---|---|
| **Live GitHub rendering** | **UNVERIFIED** | Live rendering on github.com is not verified. GitHub's image proxy / sanitization may pause or strip CSS animations in embedded SVGs. Static SVGs serve as guaranteed fallbacks. |
| **File sizes** | Prototype fidelity | Each SVG is ~2.4 MB due to embedded base64 master PNG. Future production recommendation: WebP derivative (~200-300 KB) while keeping master PNG untouched. |
| **Edge halos** | Prototype fidelity | Clip paths retain slight lit edge contours from source. Looks pristine against dark navy background (`#060913`); not matted for light backgrounds. |

---

QA performed by Antigravity on 17 October 2026. All items in the correction pass are complete and packaged in `v4/motion-proof-v1.zip`.
