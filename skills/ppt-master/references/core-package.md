# Copilot Core Package

This adapted distribution keeps PPT Master's core workflows, scripts, textual
design references, and presentation templates while omitting large optional
media libraries.

## Omitted capabilities

- The visual comparison PNG gallery is omitted. Use the textual palette,
  rendering, and image-type catalogs instead.
- Bundled icon SVG libraries are omitted. Use user-supplied, imported, or
  deliberately authored project-local SVGs, or use native PowerPoint shapes.
- Bundled sound WAV files are omitted. Use user-supplied project-local audio or
  keep the deck silent.
- The Codex-only Image-to-PPTX reconstruction profile is omitted. Raster slides
  may be recreated through ordinary Quick generation, but never claim recovered
  hidden layers, pixel-perfect fidelity, or invented semantics.

## Runtime rules

1. Never download an omitted library automatically.
2. Never call `icon_sync.py` or `sound_sync.py` in this core distribution.
3. Never reference an icon or sound until the exact project-local file exists.
4. Treat upstream text that assumes a bundled icon, sound, or comparison-image
   library as superseded by this file and the matching core-package README.
5. If an omitted capability is essential, explain the limitation and ask the
   user to provide the asset or install the full upstream distribution.
