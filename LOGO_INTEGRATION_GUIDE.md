# 🎨 Movember Logo Integration Guide

## 📋 Overview

This guide explains how to integrate your Movember logo into the AI Rules System.

## 📁 File Structure

```
assets/
├── images/
│   ├── logo.png              # Your Movember logo (add here)
│   ├── logo.svg              # Vector version (optional)
│   ├── logo-placeholder.svg  # Placeholder for testing
│   ├── favicon.ico           # Browser favicon
│   └── README.md             # Asset documentation
```

## 🎯 How to Add Your Logo

### Step 1: Prepare Your Logo File

**Supported Formats:**
- **PNG** (recommended for web)
- **SVG** (for scalable graphics)
- **JPG** (if needed)

**Recommended Specifications:**
- **Size**: 200x200px minimum
- **Background**: Transparent (PNG) or white
- **File size**: Under 500KB
- **Aspect ratio**: Square or rectangular (max 2:1)

### Step 2: Add Your Logo

1. **Copy your logo file** to `assets/images/`
2. **Name it** `logo.png` (or `logo.svg`)
3. **Ensure it's accessible** and readable

```bash
# Example: Copy your logo
cp /path/to/your/movember-logo.png assets/images/logo.png
```

### Step 3: Test the Integration

**Check the logo loads:**
```bash
# Test the logo endpoint
curl http://localhost:8001/logo/

# Test the static file serving
curl http://localhost:8001/static/images/logo.png
```

**View in browser:**
- Open: `http://localhost:8001/frontend/data_upload.html`
- The logo should appear at the top of the page

## 🔧 Integration Points

### Frontend Components

**Data Upload Interface:**
- ✅ Logo displayed in header
- ✅ Fallback text if logo fails to load
- ✅ Responsive design for all screen sizes

**React Dashboard:**
- Logo will be automatically loaded
- Consistent branding across all pages

### API Endpoints

**Logo Endpoint:**
```bash
GET /logo/
# Returns the Movember logo
```

**Static File Serving:**
```bash
GET /static/images/logo.png
# Serves the logo file directly
```

### Brand Guidelines

**Colours:**
- **Primary**: Movember Blue (#2E86AB)
- **Secondary**: Movember Orange (#F7931E)
- **Background**: White or transparent

**Typography:**
- **Font**: Arial, sans-serif
- **Weight**: Bold for emphasis
- **Case**: Uppercase for brand name

**Spacing:**
- **Logo size**: 80px height (responsive)
- **Padding**: 20px around logo
- **Margins**: Consistent spacing

## 📱 Responsive Design

The logo automatically adapts to:

**Desktop (1920x1080+):**
- Logo: 80px height
- Max width: 200px
- Centered alignment

**Tablet (768x1024):**
- Logo: 60px height
- Maintains aspect ratio
- Responsive scaling

**Mobile (375x667):**
- Logo: 50px height
- Optimized for touch
- Fallback text if needed

## 🎨 CSS Styling

**Logo Container:**
```css
.logo-container {
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}
```

**Logo Image:**
```css
.logo {
    height: 80px;
    width: auto;
    max-width: 200px;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
```

**Fallback Text:**
```css
.logo-fallback {
    background: linear-gradient(135deg, #2E86AB 0%, #F7931E 100%);
    color: white;
    padding: 15px 30px;
    border-radius: 25px;
    font-size: 24px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
}
```

## 🔍 Testing Checklist

**✅ Logo Loading:**
- [ ] Logo displays correctly
- [ ] Fallback text shows if logo fails
- [ ] No console errors

**✅ Responsive Design:**
- [ ] Desktop display (1920x1080)
- [ ] Tablet display (768x1024)
- [ ] Mobile display (375x667)
- [ ] Small mobile (320x568)

**✅ Performance:**
- [ ] Logo loads quickly (< 2 seconds)
- [ ] File size under 500KB
- [ ] No layout shifts

**✅ Accessibility:**
- [ ] Alt text present
- [ ] Good contrast ratio
- [ ] Keyboard navigation works

## 🚀 Deployment

**Local Development:**
```bash
# Start the API server
python -m uvicorn api.movember_api:app --reload --port 8001

# Access the upload interface
open http://localhost:8001/frontend/data_upload.html
```

**Production (Render):**
- Logo files are automatically deployed
- Static file serving is configured
- CDN caching for performance

## 🐛 Troubleshooting

**Logo Not Loading:**
1. Check file path: `assets/images/logo.png`
2. Verify file permissions
3. Check browser console for errors
4. Test static file serving

**Wrong Size/Display:**
1. Check CSS styles
2. Verify image dimensions
3. Test responsive breakpoints
4. Check object-fit property

**Performance Issues:**
1. Optimize image file size
2. Use WebP format if possible
3. Enable compression
4. Check CDN settings

## 📞 Support

If you need help with logo integration:

1. **Check the logs**: `tail -f logs/api.log`
2. **Test endpoints**: Use the curl commands above
3. **Verify file structure**: Ensure logo is in correct location
4. **Check browser console**: For JavaScript errors

## 🎯 Next Steps

Once your logo is integrated:

1. **Test across all pages** and components
2. **Verify brand consistency** throughout the system
3. **Update documentation** with new branding
4. **Deploy to production** and test live

**Your Movember logo will now be displayed consistently across the entire AI Rules System!** 🇦🇺 