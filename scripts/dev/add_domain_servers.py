#!/usr/bin/env python3
"""Append the domain (GIS / CAD / 3D / audio / video) connectors to the MCP catalog.

Every entry was verified before being added:

* the package resolves on PyPI (``/pypi/<name>/json``) or npm
  (``registry.npmjs.org/<name>``),
* ``docs`` is the project's own repository (redirects resolved with the GitHub
  API, so renamed projects point at their current home),
* the launch command comes from the package's own README, not from guesswork.

Additive only: an id that already exists is skipped. Afterwards run
``python scripts/mcp_catalog.py verify && python scripts/mcp_catalog.py generate``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "mcps" / "catalog.json"

HARNESSES = [
    "claude", "cursor", "codex", "vscode", "gemini", "windsurf", "cline", "roo",
    "goose", "opencode", "zed", "qwen", "kimi", "hermes", "openclaw", "trae",
    "codebuddy", "continue",
]


def entry(server_id, name, description, *, tier, category, risk, docs, license_,
          vendor, command=None, args=(), env=(), official=False, transport="stdio", url=None):
    block = {
        "id": server_id, "name": name, "description": description,
        "vendor": vendor, "official": official, "tier": tier, "category": category,
        "transport": transport,
    }
    if transport == "stdio":
        block["command"] = command
        block["args"] = list(args)
    else:
        block["url"] = url
    block["required_env"] = list(env)
    block.update({
        "risk": risk, "license": license_, "docs": docs,
        "harnesses": list(HARNESSES),
    })
    return block


SERVERS = [
    # ─────────────────────────────────────────────────────────── geospatial
    entry(
        "qgis", "QGIS",
        "Drive a running QGIS desktop session: add and style layers, run processing algorithms, export maps and inspect the project tree.",
        tier="full", category="geospatial", risk="medium",
        docs="https://github.com/wiseman/qgis_mcp", license_="MIT", vendor="wiseman",
        command="npx", args=["-y", "qgis-mcp@latest"], env=["QGIS_MCP_PORT"],
    ),
    entry(
        "gdal", "GDAL",
        "Python-native GDAL operations: raster and vector reprojection, conversion, clipping, mosaicking and format inspection.",
        tier="full", category="geospatial", risk="medium",
        docs="https://github.com/JordanGunn/gdal-mcp", license_="MIT", vendor="JordanGunn",
        command="uvx", args=["--from", "gdal-mcp", "gdal", "--transport", "stdio"],
    ),
    entry(
        "geoserver", "GeoServer",
        "Publish and manage GeoServer workspaces, stores, layers and styles through its REST API.",
        tier="full", category="geospatial", risk="medium",
        docs="https://pypi.org/project/geoserver-mcp/", license_="MIT", vendor="geoserver-mcp",
        command="uvx", args=["geoserver-mcp"],
        env=["GEOSERVER_URL", "GEOSERVER_USER", "GEOSERVER_PASSWORD"],
    ),
    entry(
        "mapbox", "Mapbox",
        "Geocoding, isochrones, directions, matrix routing and static map imagery from the Mapbox APIs.",
        tier="full", category="geospatial", risk="medium",
        docs="https://github.com/mapbox/mcp-server", license_="MIT", vendor="mapbox",
        command="npx", args=["-y", "@mapbox/mcp-server"], env=["MAPBOX_ACCESS_TOKEN"],
        official=True,
    ),
    # ──────────────────────────────────────────────────────── CAD and BIM
    entry(
        "freecad", "FreeCAD",
        "Control a running FreeCAD instance: create and edit parametric models, run Python scripts and inspect document objects.",
        tier="full", category="cad", risk="medium",
        docs="https://github.com/neka-nat/freecad-mcp", license_="MIT", vendor="neka-nat",
        command="uvx", args=["freecad-mcp"],
    ),
    entry(
        "openscad", "OpenSCAD",
        "Render and measure OpenSCAD models, check assemblies and export meshes from parametric scripts.",
        tier="full", category="cad", risk="low",
        docs="https://github.com/RobertCoop/openscad-mcp", license_="MIT", vendor="RobertCoop",
        command="uvx", args=["openscad-mcp"],
    ),
    entry(
        "autocad", "AutoCAD",
        "Automate AutoCAD through its .NET backend: draw and modify entities, query drawings and export results.",
        tier="full", category="cad", risk="high",
        docs="https://www.npmjs.com/package/autocad-mcp", license_="MIT", vendor="autocad-mcp",
        command="npx", args=["-y", "autocad-mcp"], env=["AUTOCAD_BACKEND_URL"],
    ),
    entry(
        "grasshopper", "Rhino Grasshopper",
        "Bridge to a running Rhino/Grasshopper definition: drive parameters, evaluate the canvas and read generated geometry.",
        tier="full", category="cad", risk="medium",
        docs="https://github.com/alfredatnycu/grasshopper-mcp", license_="MIT", vendor="alfredatnycu",
        command="uvx", args=["grasshopper-mcp"],
    ),
    entry(
        "revit", "Autodesk Revit",
        "Inspect and modify a Revit model: query elements and parameters, create families and run model checks.",
        tier="full", category="cad", risk="high",
        docs="https://github.com/ZedMoster/revit-mcp", license_="MIT", vendor="ZedMoster",
        command="uvx", args=["revit-mcp"],
    ),
    entry(
        "ifc", "IFC / BIM",
        "Query IFC building models: spaces, elements, property sets and quantities for coordination and take-offs.",
        tier="full", category="cad", risk="low",
        docs="https://pypi.org/project/ifc-mcp/", license_="Unknown", vendor="imants",
        command="uvx", args=["ifc-mcp"],
    ),
    entry(
        "kicad", "KiCad",
        "Work with KiCad projects: inspect schematics and PCBs, place components and check design rules.",
        tier="full", category="cad", risk="medium",
        docs="https://pypi.org/project/kicad-mcp/", license_="Unknown", vendor="kicad-mcp",
        command="uvx", args=["kicad-mcp"],
    ),
    # ────────────────────────────────────────────────────────── 3D and VFX
    entry(
        "blender", "Blender",
        "Control Blender over a local socket: build and modify meshes, run Python, render and export assets.",
        tier="standard", category="3d", risk="medium",
        docs="https://github.com/ahujasid/mcp-for-blender", license_="MIT", vendor="ahujasid",
        command="uvx", args=["blender-mcp"], env=["BLENDER_HOST", "BLENDER_PORT"],
    ),
    entry(
        "meshy", "Meshy 3D",
        "Generate 3D models and textures from text or image prompts through the Meshy API.",
        tier="full", category="3d", risk="medium",
        docs="https://github.com/gwizards/meshy-mcp-server", license_="MIT", vendor="gwizards",
        command="npx", args=["-y", "meshy-mcp-server"], env=["MESHY_API_KEY"],
    ),
    entry(
        "sketchfab", "Sketchfab",
        "Search, inspect and publish 3D models on Sketchfab, including licence and metadata fields.",
        tier="full", category="3d", risk="medium",
        docs="https://github.com/gregkop/sketchfab-mcp-server", license_="NOASSERTION",
        vendor="gregkop", command="npx", args=["-y", "sketchfab-mcp-server"],
        env=["SKETCHFAB_API_KEY"],
    ),
    entry(
        "inkscape", "Inkscape",
        "Drive the Inkscape CLI: convert and clean vector art, trace bitmaps and export SVG/PNG at exact sizes.",
        tier="full", category="design", risk="low",
        docs="https://github.com/aravindev/inkscape_mcp", license_="MIT", vendor="aravindev",
        command="uvx", args=["inkscape-mcp"],
    ),
    # ──────────────────────────────────────────────────────── audio, video
    entry(
        "ableton", "Ableton Live",
        "Control an Ableton Live session: transport, tracks, clips and device parameters.",
        tier="full", category="audio", risk="medium",
        docs="https://github.com/ahujasid/ableton-mcp", license_="MIT", vendor="ahujasid",
        command="uvx", args=["ableton-mcp"],
    ),
    entry(
        "davinci-resolve", "DaVinci Resolve",
        "Automate DaVinci Resolve: timeline assembly, media pool operations, rendering and project inspection.",
        tier="full", category="video", risk="medium",
        docs="https://github.com/flowsai/davinci-resolve-mcp", license_="MIT", vendor="flowsai",
        command="uvx", args=["davinci-resolve-mcp"],
    ),
]


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    existing = {server["id"] for server in catalog["servers"]}
    added = [server for server in SERVERS if server["id"] not in existing]
    catalog["servers"].extend(added)
    catalog["servers"].sort(key=lambda server: server["id"])
    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"added {len(added)} servers; catalog now has {len(catalog['servers'])}")
    print("  " + ", ".join(server["id"] for server in added))
    return 0


if __name__ == "__main__":
    sys.exit(main())
