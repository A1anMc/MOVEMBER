# 🎨 Assets Directory

This directory contains visual assets for the Movember AI Rules System.

## 📁 Directory Structure

```
assets/
├── images/
│   ├── logo.png          # Movember logo (add your logo here)
│   ├── logo.svg          # Vector version of logo
│   ├── favicon.ico       # Browser favicon
│   └── README.md         # This file
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

## 📋 How to Add Your Logo

1. **Place your Movember logo file** in this directory
2. **Name it appropriately** (e.g., `movember-logo.png`)
3. **Update the frontend** to reference the correct file
4. **Test the display** across different screen sizes

## 🔗 Usage in Frontend

The logo will be automatically loaded by the frontend components:

```html
<!-- In HTML files -->
<img src="/assets/images/logo.png" alt="Movember Logo">

<!-- In React components -->
<img src="/assets/images/logo.png" alt="Movember Logo" />
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

**API Responses:**
- Include logo URL in branding metadata
- Provide logo for client applications

**Documentation:**
- Include logo in PDF reports
- Add to presentation templates
- Use in stakeholder communications 