# Domain coverage — what All-Skills can actually do

This page is the honest inventory of the library across **disciplines**, not just software
engineering. It answers two questions:

1. Which domains have a real playbook (workflow, inputs, tools, safety, failure modes) *and* a
   verified connector so the agent can drive the tool rather than describe it?
2. Which domains are still gaps, and what would closing them take?

Counts come from `skills/*/*/SKILL.md` and `mcps/catalog.json`; regenerate the numbers with
`python scripts/compute_stats.py` and `python scripts/mcp_catalog.py generate` after changing either.

---

## 1. Covered domains

**504 curated skills in 45 categories**, **113 MCP servers in 35 categories**.

| Domain | Skills | Connector(s) | Notes |
| :--- | ---: | :--- | :--- |
| **GIS, cartography, remote sensing** | 12 (`geospatial`) | `qgis`, `gdal`, `geoserver`, `mapbox` | Map production, CRS/datums, PostGIS, LiDAR, photogrammetry, spatial statistics |
| **CAD, drafting, BIM, fabrication** | 10 (`cad`) | `freecad`, `openscad`, `autocad`, `grasshopper`, `revit`, `ifc`, `kicad` | Parametric modelling, DXF/DWG interchange, GD&T, IFC coordination, PCB |
| **CNC and fabrication** | 2 of the 10 `cad` skills | — | Toolpaths, feeds/speeds, G-code verification, laser kerf and settings |
| **3D, texturing, VFX** | 13 (`3d`) | `blender`, `meshy`, `sketchfab` | Topology, retopo, rigging, geometry nodes, shading, render, PBR, Houdini, compositing |
| **Audio and music** | 6 (`audio`) | `ableton` | DAW production, mixing/mastering, foley, podcast, notation, live sound |
| **Video and broadcast** | 5 (`video`) | `davinci-resolve` | Editing, grading, motion graphics, encoding/delivery, live streaming |
| **Photography** | 2 (`photography`) | `filesystem` | RAW pipeline, studio lighting, colour management, soft proofing |
| **Architecture and interiors** | 4 (`architecture`) | `revit`, `ifc` | Design workflow, space planning, construction documents and specifications |
| **Graphic and product design** | 13 (`design`) | `inkscape` | Vector/SVG, typography, prepress, editorial layout, icon systems, UI/UX, branding |
| **Software engineering** | 330+ across `development`, `programming`, `web`, `mobile`, `data`, `databases`, `cloud`, `devops`, `security`, `testing`, `ai` | 90+ | The original core of the library |
| **Agent engineering** (`agents`) | 4 | `filesystem`, `github`, `slack`, `opentelemetry`, `grafana`, `sentry` | MCP integration testing, agent observability, reliability, human-in-the-loop |
| **Product and growth** (`product`) | 10 | `postgres`, `bigquery`, `stripe`, `notion`, `playwright` | Research, analytics, CRO, pricing, support automation |
| **Enterprise and back office** | 60+ across `legal`, `finance`, `finops`, `product`, `productivity`, `communication`, `documents`, `research`, `education`, `healthcare` | 20+ | Contracts, analysis, reporting, work tracking |

Everything above is installable per skill (`allskills install <skill-id>`) and per profile
(`--profile library` installs the whole curated tree).

---

## 2. Gaps this round closed

| Was missing | Now |
| :--- | :--- |
| QGIS / map making | `geospatial/qgis-map-production` + `qgis` server |
| CRS, datums, reprojection traps | `geospatial/spatial-reference-systems` |
| Raster/vector data wrangling | `geospatial/gdal-ogr-pipelines` + `gdal` server |
| Web maps and tiles | `geospatial/vector-tile-web-maps`, `geospatial/openstreetmap-data` |
| Point clouds and imagery | `geospatial/lidar-point-clouds`, `geospatial/remote-sensing-indices`, `geospatial/drone-photogrammetry` |
| CAD from scratch | `cad/freecad-parametric-modeling`, `cad/openscad-programmatic-cad`, `cad/fusion360-solid-modeling` |
| Drafting standards | `cad/autocad-drafting`, `cad/technical-drawing-gdt`, `cad/dxf-dwg-interchange` |
| BIM and IFC | `cad/bim-ifc-coordination` + `ifc`, `revit` servers |
| Blender, end to end | 7 `3d/blender-*` skills + `blender` server |
| Asset pipeline and print prep | `3d/three-d-asset-pipeline`, `3d/mesh-repair-printing`, `3d/pbr-texture-authoring` |
| Animation and VFX | `3d/character-animation-principles`, `3d/houdini-procedural-vfx`, `3d/vfx-compositing` |
| Music and sound | `audio/*` (DAW, mixing, foley, podcast, notation, live sound) + `ableton` |
| Video and colour | `video/*` (editing, grading, motion, encoding, streaming) + `davinci-resolve` |
| Photography | `photography/*` (RAW pipeline, studio lighting + colour management) |
| Architecture | `architecture/*` (design workflow, space planning, construction documents) |
| Print and layout craft | `design/print-production-prepress`, `design/editorial-layout-design`, `design/typography-and-type-systems`, `design/vector-illustration-svg`, `design/iconography-systems` |
| Shop-floor fabrication | `cad/cnc-machining-fabrication`, `cad/laser-cutting-engraving` |

---

## 3. Still not covered

These are real gaps. None of them is hidden behind a vague "and more" — each is listed with what it
would actually take, so the next contributor knows where to start.

### Trades and physical production
| Gap | Why it is not there yet | What it needs |
| :--- | :--- | :--- |
| Welding, sheet-metal forming, manual machining | Needs process-safety content that varies per shop and code | A skill per process with inspection and PPE sections; no connector exists |
| Textiles: pattern making, draping, grading, sewing | Niche tooling (CLO3D, Gerber, Optitex) with no public MCP server | Skill-first; connectors unverified |
| Woodworking and cabinetry | Same as metal: shop-specific | Skill with joinery and finish schedules |
| Landscaping and hardscape | Overlaps GIS + construction docs | Compose from existing skills; a dedicated one is still missing |
| Surveying with total stations / GNSS RTK | Field-procedure heavy, hardware-bound | Skill with datum and adjustment math; `gdal` partially helps |

### Engineering disciplines beyond CAD
| Gap | Why it is not there yet | What it needs |
| :--- | :--- | :--- |
| Structural analysis (SAP2000, ETABS, RFEM) | Proprietary APIs, no verified MCP server | Skill on load paths and model QA; connector would need vendor API access |
| HVAC / MEP design and load calculation | Code-dependent per jurisdiction | Skill with load-calc workflow; no connector |
| Electronics simulation (SPICE), FPGA/HDL flows | `embedded/*` covers firmware, not simulation | Skills for ngspice/Verilator/Yosys |
| PCB layout *tooling* (Altium, KiCad CLI automation) | `embedded/pcb-design` covers principles; `kicad` server added, no KiCad-specific skill yet | A `cad/kicad-pcb-layout` playbook |
| Metrology and 3D scanning QA | No connector; scanner vendors are closed | Skill on scan-to-CAD deviation analysis |

### Audio/video/photo at professional depth
| Gap | Why it is not there yet | What it needs |
| :--- | :--- | :--- |
| OBS / streaming automation | `obs-websocket` exists as a protocol but no catalogued MCP server was verified | `video/live-streaming-broadcast` covers the workflow; a connector would need an MCP wrapper |
| Pro Tools / Logic automation | No public MCP servers | Skill-level, platform-specific |
| Photoshop / Affinity Photo automation | **No `photoshop-mcp` exists** in any registry as of this writing (checked PyPI and npm) | Skill on non-destructive retouching; scripting via ExtendScript documented but unverified |
| Colour science and LUT authoring | Partly in `video/color-grading` | Deeper skill on ACES and LUT maths |
| Audio plugin/DSP development | Adjacent to `programming` | Skill on JUCE/CLAP plugin workflows |

### Real-world services and professions
| Gap | Why it is not there yet | What it needs |
| :--- | :--- | :--- |
| Clinical documentation and coding (ICD/CPT) | Regulatory and privacy-sensitive; only `healthcare` (1 skill) exists | Skills per specialty plus a compliance review |
| Veterinary practice | Nothing at all | Skill-first |
| Agriculture, agronomy, precision farming | Nothing at all; `geospatial` covers the data side | Skills on crop planning and machinery telemetry |
| Culinary, recipe development, food safety | `media` has one recipe stub | Skills with HACCP and cost cards |
| Aviation, maritime, logistics operations | Nothing at all | Domain-specific regulatory skills; high risk, needs review |
| Mining, oil and gas, utilities field ops | Nothing at all | Out of scope for a general library without domain reviewers |
| Event production and stage management | Overlaps live sound/lighting | A production-scheduling skill |
| Fitness, sports coaching, rehabilitation | Nothing at all | Skill-first, needs professional review |
| Insurance and underwriting | `finance` is thin (3 skills) | Skills on policy structures and claims |

### Tooling gaps behind existing skills
| Gap | Detail |
| :--- | :--- |
| No connector for MuseScore, LilyPond, Scribus, LightBurn, Argyll CMS, Darktable | All are CLI-drivable, so an MCP wrapper is feasible; none has a verified public package yet |
| No connector for Rhino (`grasshopper` bridges Grasshopper only) | Rhino's own bridge requires a Windows plugin |
| `sketchfab` and `meshy` are token-gated | Never installed by default; `full` profile only |
| `ifc` and `kicad` servers have no declared licence upstream | Documented as `Unknown`/`NOASSERTION` in the catalog rather than guessed |

---

## 4. How to add the next domain

Before adding anything, check the name **and** the meaning against the tree — 26 of the 55 skills an
external audit proposed already existed under a different name (see
[`AUDIT-RESPONSE.md`](AUDIT-RESPONSE.md) §4). `python scripts/skills/skills.py route "<task>"`
answers "is this already covered?" faster than writing a new playbook.

1. Write a data module under `scripts/dev/` following `domain_skills_geo.py` (a `TITLES` dict and a
   `SKILLS` list of `skill(...)` calls), and import it from `scripts/dev/add_domain_skills.py`.
2. If a connector exists, verify it first: `curl -s https://pypi.org/pypi/<pkg>/json` or
   `npm view <pkg> repository.url version`, then add it to `scripts/dev/add_domain_servers.py` with
   the launch command taken from the package's own README.
3. Regenerate, in order:
   `refresh_registry.py` → `sync_federated_registry.py` → `compute_stats.py` →
   `generate_readme_stats.py` → `generate_baselines.py` → `skills.py lock` →
   `mcp_catalog.py generate`.
4. Add the new paths to the `canonical-library` install module, then run the gate set in
   `README.md` §Development, CI & Quality Gates.
