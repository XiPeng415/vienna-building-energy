# Vienna — building energy and carbon

Interactive citywide visualization of 251,332 source building objects. Uses the complete exported map snapshot over HTTP/HTTPS, without the local Vite or SQLite API. Existing map geometry, source attributes, energy results and audit packages are retained. New simulation jobs require the local research environment.

Code attribution: Buildings.city / City-Syntax (MIT); retained LICENSE and CITATION.cff. Data licensing remains source-specific: OpenStreetMap / ODbL 1.0; GBA heights / CC BY-NC 4.0; City of Vienna / CC BY 4.0 (Datenquelle: Stadt Wien - data.wien.gv.at). The GBA-derived dataset is for non-commercial use under its source licence.

Large local research databases and bulk exports are omitted from this static visualization package, and their report links are labelled. Local preview: `python -m http.server 8000`.

Published with GitHub Pages from the main branch root. No server or credentials are embedded.

## Deployment package

The complete static site (including all map resources) is stored in numbered snapshot parts. `python build_site.py` verifies each part and every extracted file, then restores the original directory structure to `_site/`. GitHub Actions publishes `_site/` to GitHub Pages. Parts are each below GitHub’s browser upload file limit. The source HTML, CSS and JavaScript are all included in the snapshot.

Website: https://XiPeng415.github.io/vienna-building-energy/
