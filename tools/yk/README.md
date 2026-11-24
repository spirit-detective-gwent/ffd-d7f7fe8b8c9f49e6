# tools/yk: the Shōwa yankii wardrobe painter (v6.5.60, Nails questline)
`yk.js` paints the yankii looks (tokkōfuku coats, bontan, sarashi, pompadour / punch perm, hachimaki, shades, leopard) onto the
existing cel sheets, in a browser canvas, with the sheets' own flat 3-tone fills and ink lines. `jobs.py` lists every sheet
(source sheet, grid, facings); `bake.py` runs them in headless Chromium through `bake.html` and writes `<key>.webp`, which go
in `world/`. The game only loads those files (index.html, "FFF_YK (Nails questline)"), so nothing is painted at run time.
Sources: the embedded sheets extracted to `ext/` (c2_punk_*, ryo_*, aoi_*), plus `world/*_ambv`, `world/*_gym`, `roster/c2_punk_fig_*`.
Flip's idle sheet is built from his painted walk (frame 0 per facing, a 0/1/2/1 px chest bob).
