# 🎨 Assets Directory

This directory contains visual assets for the Movember AI Rules System.

## 📁 Directory Structure

```
assets/
├── images/
│   ├── logo.png              # Movember logo (add your logo here)
│   ├── logo.svg              # Vector version of logo
│   ├── favicon.ico           # Browser favicon (✅ Added)
│   ├── favicon-16x16.png     # Small favicon (✅ Added)
│   ├── favicon-32x32.png     # Standard favicon (✅ Added)
│   ├── apple-touch-icon.png  # iOS touch icon (✅ Added)
│   ├── android-chrome-192x192.png  # Android icon (✅ Added)
│   ├── android-chrome-512x512.png  # Android icon large (✅ Added)
│   └── README.md             # This file
├── site.webmanifest          # Web app manifest (✅ Added)
```

## 🎯 Logo Requirements

**Supported Formats:**
- PNG (recommended for web)
- SVG (for scalable graphics)
- JPG (if needed)
- ICO (for favicon)

**Recommended Specifications:**
- **Logo**: 200x200px minimum, transparent background
- **Favicon**: 32x32px, 16x16px, and 48x48px versions
- **File size**: Under 500KB for optimal loading

## 🎯 Favicon Requirements

**✅ Complete Favicon Set Added:**
- **favicon.ico**: 16x16, 32x32, 48x48 ICO format
- **favicon-16x16.png**: Small PNG favicon
- **favicon-32x32.png**: Standard PNG favicon
- **apple-touch-icon.png**: 180x180 iOS touch icon
- **android-chrome-192x192.png**: Android app icon
- **android-chrome-512x512.png**: Large Android app icon

**✅ Web App Manifest:**
- **site.webmanifest**: PWA manifest with Movember branding
- **Theme colour**: Movember Blue (#2E86AB)
- **App name**: "Movember AI Rules System"

## 📋 How to Add Your Logo

1. **Place your Movember logo file** in this directory
2. **Name it appropriately** (e.g., `movember-logo.png`)
3. **Update the frontend** to reference the correct file
4. **Test the display** across different screen sizes

## 🔗 Usage in Frontend

The logo and favicon will be automatically loaded by the frontend components:

```html
<!-- In HTML files -->
<img src="/static/images/logo.png" alt="Movember Logo">
<link rel="icon" href="/static/images/favicon.ico">

<!-- In React components -->
<img src="/static/images/logo.png" alt="Movember Logo" />
```

## 🎨 Brand Guidelines

- **Primary colour**: Movember blue (#2E86AB)
- **Secondary colour**: Movember orange (#F7931E)
- **Typography**: Professional, accessible fonts
- **Spacing**: Consistent padding and margins
- **Accessibility**: Alt text and proper contrast ratios

## 📱 Responsive Design

The logo should be responsive and work well on:
- Desktop (1920x1080 and larger)
- Tablet (768x1024)
- Mobile (375x667)
- Small mobile (320x568)

## 🔧 Integration Points

**Frontend Components:**
- Dashboard header
- Navigation bar
- Login pages
- Report headers
- Email templates
- Browser tabs (favicon)

**API Responses:**
- Include logo URL in branding metadata
- Provide logo for client applications
- Serve favicon for browser tabs

**Documentation:**
- Include logo in PDF reports
- Add to presentation templates
- Use in stakeholder communications

## 🚀 PWA Features

**✅ Progressive Web App Support:**
- **Web manifest**: site.webmanifest
- **App icons**: Multiple sizes for all devices
- **Theme colour**: Movember blue
- **Standalone mode**: App-like experience
- **Installable**: Can be added to home screen

## 📊 Current Assets Status

**✅ Favicon Set**: Complete (6 files)
**✅ Web Manifest**: Configured with Movember branding
**✅ Logo Placeholder**: Available for testing
**⏳ Your Logo**: Ready to add (logo.png) 