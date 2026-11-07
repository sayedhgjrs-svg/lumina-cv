# Barcode Studio

A standalone, English-language barcode and QR code generator added under `barcode/` so it does not change the existing Lumina CV Streamlit application.

## Run locally

Serve this folder with any static file server, for example:

```sh
python -m http.server 8000 --directory barcode
```

Then open `http://localhost:8000`. The generator uses JsBarcode and QRCode.js from jsDelivr; an internet connection is needed to load those libraries.

## Included pages

- `index.html` — QR and 1D barcode generation, live preview, and PNG/SVG downloads.
- `about.html`, `privacy.html`, `contact.html` — static information pages.
- Labeled ad placeholders are included on the generator page; no advertising scripts are active.

Barcode generation runs in the browser. Review and update the privacy/contact copy and configure an actual ad provider and consent controls before production use, if applicable.
