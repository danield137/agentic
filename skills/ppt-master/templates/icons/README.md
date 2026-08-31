# Project-Local Icons

The Copilot core distribution does not include PPT Master's bundled SVG icon
libraries.

Use only icons whose files already exist under `<project>/icons/<library>/`.
They may be supplied by the user, imported from a source presentation, or
authored deliberately for the current deck. Native PowerPoint shapes are the
preferred fallback for simple symbols.

Do not run `icon_sync.py`, search for bundled icon names, or reference
`data-icon="library/name"` until the exact project-local SVG exists. Do not
download an icon library automatically.
