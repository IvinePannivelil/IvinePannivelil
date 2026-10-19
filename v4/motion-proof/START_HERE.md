# Ivine — character motion kit 01

This is a small local prototype and Antigravity handoff, dated 16 October 2026.
The appearance reference is the FINAL approved, fuller-build arms-folded image.
It has been copied without changing its pixels. Your existing project is not
included or overwritten by this package.

## What to do

1. Extract this ZIP. Copy the complete `ivine-motion-kit` folder into the root
   of your existing README project, next to `README.md` and `v4`.
2. Open that existing project in Antigravity.
3. Open `ivine-motion-kit/ANTIGRAVITY_PROMPT.md`, copy its contents into the
   Antigravity chat, and run the task.
4. Review its browser recording and updated preview before accepting a new
   visual direction. Share the updated folder/ZIP and recording for review.

## Preview it yourself on Windows

In Antigravity's terminal, with the project root as the current folder:

```powershell
py -m http.server 8089 --bind 127.0.0.1 --directory ivine-motion-kit
```

Then open <http://127.0.0.1:8089/preview.html> in Chrome.
If `py` is unavailable but Python is installed, use `python` instead.
If port 8089 is occupied, use 8090 and update the address accordingly.
Stop the server with Ctrl+C. No Python packages are needed for this command.

Alternatively, use Live Server on `preview.html`. The page can also be opened
directly, but its layer inspector needs HTTP and will explain this if unavailable.

## What is included

| File | Purpose |
| --- | --- |
| `assets/ivine-approved-arms-folded.png` | Immutable approved master, original resolution |
| `assets/hero-desktop.svg` | Entrance, head-only idle and small data trace |
| `assets/hero-mobile.svg` | Separate readable phone composition |
| `assets/hero-desktop-static.svg` | Complete still desktop version |
| `assets/hero-mobile-static.svg` | Complete still mobile version |
| `assets/head-region.svg` | Isolated head/beard/neck region, original coordinate system |
| `assets/body-region.svg` | Isolated body/folded-arms region, original coordinate system |
| `preview.html` | Motion/still, layout, replay and head/body inspection controls |
| `scripts/build_motion.py` | Standard-library SVG generator, paths resolved from script location |
| `asset-manifest.json` | Source checksum, dimensions, pivot and scope |
| `ANTIGRAVITY_PROMPT.md` | Exact next implementation task |
| `MOTION_SPEC.md` | Motion constraints and future asset requirements |
| `VERIFICATION.md` | Checks performed and checks still required |

## Optional extensions

No extension is required to open the prototype. Extensions help inspection;
they do not make an animation more natural by themselves.

- **Live Server — `ritwickdey.LiveServer`**: optional local preview with reload.
  Listing: <https://open-vsx.org/extension/ritwickdey/LiveServer/5.7.4>
- **SVG — `jock.svg`**: optional SVG syntax support and preview.
  Listing: <https://open-vsx.org/extension/jock/svg>
  Avoid its automatic minify action on animated files; the extension's listing
  specifically reports cases of minimization breaking SVGs.
- **Antigravity Browser Tools**: use your installed IDE's browser integration
  to test the preview in Chrome. Follow its own setup prompts if needed.
  Current documentation: <https://antigravity.google/docs/ide/browser>

Search the exact extension identifier in Antigravity's Extensions view. Registry
availability can differ by installation. The terminal command above is sufficient
if an extension is unavailable. No paid animation extension is needed for this phase.

## Current scope

The hero styling is a test fixture, not a finalized redesign. This first rig has
an entrance and a small head tilt. The arms stay folded. There is no blinking,
independent arm gesture, torso breathing, image-to-video output, or published
GitHub compatibility claim.

The head/body regions are SVG clips of one immutable PNG. They expose different
pixels and are independent visible layers, with a small neck overlap. They are
not separately redrawn body-part PNGs. The source contains colored background
glow; the contour clips remove most of it, retaining small lit edges. This is a
conservative dark-background proof, not a final edge matte for every background.

Rebuild from the project root:

```powershell
py ivine-motion-kit/scripts/build_motion.py
```

Keep the source PNG unchanged. Make composition or movement adjustments in the
generator, rebuild all variants, and test the generated SVGs through image tags.
