You are working in my existing GitHub profile README project. Implement and verify
the FIRST CHARACTER MOTION PROOF using the supplied `ivine-motion-kit` folder.
Treat this as a small local development task, not the full profile redesign.

First read `ivine-motion-kit/START_HERE.md`, `MOTION_SPEC.md`, `VERIFICATION.md`
and `asset-manifest.json`. Inspect the approved master image, the existing `v4`
folder, and the SVG generator. Follow applicable project instructions.

My identity is Ivine P Sabu — AI Engineer, Machine Learning, Data Science,
Applied AI. The appearance in `assets/ivine-approved-arms-folded.png` is final:
the face, grown beard, hair and naturally fuller build must be preserved.
Do not regenerate or beautify the face, narrow the waist or add muscle definition.

Do the work in `v4/motion-proof/`, copying this supplied kit there first. Keep
the existing V3 files, existing V4 hero/lanyard, root README and GitHub workflows
untouched. Do not commit, push or publish. Use local tools already available.

The kit already contains a conservative prototype. Continue from its generator;
do not rebuild from memory or discard the approved pixels. Its two visible regions
share one embedded PNG through DIFFERENT SVG clip paths. This is legitimate
independent head/body visibility, not nested transformations of one whole picture.
The fixed folded arms are intentional. It is not a full articulated rig yet.

TASKS

1. Start a localhost preview using the available server; use Python's standard
   library if convenient. Open the actual page in Chrome through browser tools.
   Check both external `<img>` rendering and the inline inspector. If browser
   tools cannot run, state that explicitly rather than claiming browser QA passed.
2. Verify the approved source checksum before and after work. Preserve its pixels.
   Edit the build script and rebuild output variants whenever changing the rig.
3. Inspect head/body contours and neck overlap at 0°, −0.65° and +0.35°. Refine
   SVG clip paths or the hidden underlap only if required to remove a visible
   gap, duplicate edge, clipped hair/shoe, or colored backdrop fragment. Retain
   the same fuller silhouette. Check dark, checkerboard and light surroundings
   in the inspector; the hero itself has a fixed dark background.
4. Verify actual animation: 0.8-second entrance, a slow 7-second head-only idle,
   and a stationary body after entrance. Head should move around the neck.
   Hide the head to prove the body contains no duplicate head; hide the body to
   prove head movement is isolated. The inspector's neck underlap belongs to
   the body and should hide with it. Use debug controls only in local HTML.
5. Check that the visible motion remains subtle but readable. Do not move the
   whole person to simulate head motion. Avoid puppet movement or moving shoes.
   Do not add torso breathing, arm movement, or blinking without the missing assets.
6. Verify Replay, still/motion toggle, desktop/phone toggle, region visibility,
   and manual angle controls. Test viewport widths 1440, 1024, 390 and 360 px.
   Check overflow, name/role readability, visible feet, and keyboard controls.
7. Test the actual system `prefers-reduced-motion` setting in the browser, as well
   as the explicit still toggle. The complete name, face and body must remain
   visible. Reduced motion must stop all runtime motion, including SVG traces.
8. Inspect asset sizes and missing-resource/console errors. Keep the initial
   approved PNG unmodified. Report embedded-raster size as a prototype limitation;
   propose a derivative optimization separately if it is worthwhile. Do not
   assume a local preview proves final GitHub compatibility.
9. If improving the hero composition, keep it restrained and accessible. Do not
   add the remaining README sections, fake metrics or additional visual concepts.

TECHNICAL BOUNDARIES

- Runtime SVGs must be self-contained, without JS, external fonts, `<foreignObject>`
  or external image dependencies. Local HTML may use JavaScript for inspection.
- Preserve full static versions and a separately composed mobile variant.
- Use built-in browser tooling if available. Editor extensions are optional.
- Make routine local reversible fixes directly. If a missing asset genuinely
  prevents independent motion, identify exactly what is missing without faking it.
- No public GitHub changes in this task. A later GitHub-render check is separate.

DELIVERABLES

- Updated `v4/motion-proof/` with generator, assets, inspector and instructions.
- Local preview URL and exact startup command.
- A 12-second browser recording showing the entrance and one complete head cycle.
- Desktop and 390/360 px captures, plus a reduced-motion capture.
- A concise QA report listing checks actually run, exact failures fixed, remaining
  limitations and file sizes. Clearly distinguish CSS/browser checks from static
  renders supplied by ChatGPT; do not repeat supplied checks as if you ran them.
- Package the updated `v4/motion-proof/` folder in a ZIP for me to upload for review.

Proceed with this first motion proof now. Stop after delivering its local preview
and QA report; do not expand into the full README until I review the motion.
