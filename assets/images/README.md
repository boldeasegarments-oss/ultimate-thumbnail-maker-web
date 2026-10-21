# Image Assets Guide & Replacement Instructions

This directory contains the image assets for the **Ultimate Thumbnail Maker** static SEO website.

The placeholder images currently generated in this folder provide visually accurate, structured placeholders that prevent layout shifts and broken images during initial preview and staging. 

Before final production launch, replace these placeholders with **actual, genuine screenshots taken directly from the Android app** (`com.sk.thumbnailmaker`).

---

## Image Inventory & Specifications

| Filename | Purpose | Recommended Resolution | Aspect Ratio | Replacement Instructions |
| :--- | :--- | :--- | :--- | :--- |
| `app-home.webp` | Homepage & feature showcase | 800 × 600 px (or 1080 × 1920 mobile portrait) | 4:3 or 9:16 | Capture the actual template selection screen or home dashboard of the app showing real template categories. |
| `thumbnail-editor.webp` | Editor tools showcase (YouTube page & How-To) | 800 × 600 px (or 1080 × 1920 mobile portrait) | 4:3 or 9:16 | Capture the live editing canvas with font controls, color pickers, text effect sliders, or sticker selection in action. |
| `gaming-thumbnail-example.webp` | Gaming thumbnail landing page | 800 × 450 px (or 1280 × 720 px) | 16:9 | Export an actual finished gaming thumbnail created within the app showing bold text, high contrast, and game-themed graphic elements. |
| `background-removal-example.webp` | Background removal feature landing page | 800 × 500 px (or 1200 × 750 px) | 16:10 | Capture a side-by-side or before/after cutout showing subject isolation performed using the app's real background removal feature. |
| `og-image.webp` | Open Graph / Twitter Card social share preview | 1200 × 630 px | 1.91:1 | Branded preview card shown when links are shared on Twitter/X, Facebook, Discord, WhatsApp, and LinkedIn. |
| `favicon.svg` | Browser tab icon | Scalable vector | 1:1 | The official app icon or vector mark. |

---

## Guidelines for Real App Screenshots

1. **Authenticity:**
   - Use only authentic screenshots taken from your Android phone or an emulator running the official package `com.sk.thumbnailmaker`.
   - Never use screenshots from competitor apps or generic stock assets.
   - Do not make unverified claims in the images (e.g., claiming features not present in the app).

2. **Format & Compression:**
   - Convert device PNGs to `.webp` format for minimal payload and maximum mobile speed.
   - Recommended tools: Squoosh (`squoosh.app`), cwebp CLI, or Photoshop/GIMP WebP export at 85-90% quality.
   - Ensure file size is kept under 120KB per screenshot to maintain Core Web Vitals performance.

3. **Dimensions & Layout Shifts:**
   - Keep the width and height attributes in HTML matching the aspect ratio of the replaced images to prevent Cumulative Layout Shift (CLS).

4. **Accessibility (Alt Text):**
   - Whenever an image is updated, verify that the corresponding `<img alt="...">` attribute accurately describes what is visible in the new screenshot.
