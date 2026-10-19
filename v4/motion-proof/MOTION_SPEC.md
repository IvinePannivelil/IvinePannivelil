# Motion specification — first proof

## Appearance lock

Use `assets/ivine-approved-arms-folded.png` as the sole approved appearance.
Preserve face, grown beard, curly hairstyle, fuller waist, normal soft arms,
black clothing, silver watch, white shoes, and cyan/amber accents. The previous
slimmer pointing/waving/laptop variants are not approved body references.

## Implemented geometry

Source coordinates: 1024 × 1536. Head pivot: (493, 292).

| Element | Motion | Timing |
| --- | --- | --- |
| Whole figure entrance | Opacity .35 to 1, translateY 10 to 0 source units | 0.8 s, once |
| Head/beard region | 0°, −0.65°, +0.35°, 0° about neck | 7 s, starts at 1.2 s |
| Body and folded arms | Static after entrance | Entire idle cycle |
| Small data trace | A short dash travels across one path | 6 s loop |
| Name and role | Visible from first frame | Always |

Actual entrance displacement at desktop scale is about 3.4 px; it is deliberately
small. Head rotation is subtle at full hero scale; inspect the enlarged rig as well.
CSS media rules stop movement for `prefers-reduced-motion: reduce`. The static
alternatives contain no keyframes and remain complete without animation support.

## Region structure

An SVG definition embeds the source PNG once. The body group uses `body-region`;
the head uses `head-region`. Each clip reveals different pixels. The idle rotation
applies only to the head wrapper. A small vector neck underlap sits behind both.

Clipping is an SVG composition technique; the approved raster bytes are unchanged.
This limited rig cannot expose large unseen areas, turn the head far sideways,
uncross the arms or rotate the full torso. Do not increase motion amplitude beyond
the tested small range without inspecting seams and overlap.

## Next pose / gesture phase

After this movement and likeness pass review, create a separate pointing pose
that uses this approved fuller build. An arm gesture will need at minimum a
body with reconstructed pixels behind the arm, separate upper arm and forearm/hand
regions with joint overlap, and independent interface graphics. Eyes/blink frames
are optional later assets and require likeness review. Do not label a rotated
complete PNG as independent arm/head movement.

## Integration target

Runtime artwork: self-contained SVG, embedded image, CSS animation, no scripts,
external fonts or network resources. Local preview controls may use JavaScript.
Use real HTML/Markdown outside the SVG for links and essential profile text.
Desktop and phone compositions are separate. Phone image selection is based on
viewport media queries, and still needs actual GitHub rendering verification.

Keep projects in readable Markdown. No fake activity data or skill percentages.
No public-profile updates, commits or pushes in this phase.
