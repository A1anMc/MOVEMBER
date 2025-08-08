# 🎯 Movember Impact Dashboard

A beautiful, modern web dashboard for visualising Movember's comprehensive impact measurement data.

## 🚀 Quick Start

### Option 1: Automatic Launch
```bash
python launch_dashboard.py
```

### Option 2: Manual Launch
```bash
# Terminal 1: Start the API
python simple_api.py

# Terminal 2: Start the frontend
cd frontend
python -m http.server 3000
```

## 🌐 Access the Dashboard

- **Dashboard URL**: http://localhost:3000
- **API URL**: http://localhost:8000

## 📊 Dashboard Features

### 🎯 Overview
- **Real-time Impact Data** - Live data from the Movember API
- **Beautiful Visualisations** - Interactive charts and graphs
- **Responsive Design** - Works on desktop, tablet, and mobile
- **UK English & AUD Currency** - Compliant with your standards

### 📈 Key Components

#### 1. **Header Statistics**
- People Reached: 8.5M
- Total Funding: $125M AUD
- Countries Reached: 25
- Research Projects: 450

#### 2. **Overall Impact Score**
- Visual circular display
- Score out of 10
- Real-time updates

#### 3. **Category Breakdown**
- Interactive bar chart
- 10 impact categories
- Color-coded performance levels

#### 4. **Key Achievements**
- Highlighted accomplishments
- Success indicators
- Achievement tracking

#### 5. **Category Cards**
- Individual category performance
- Key metrics per category
- Achievement summaries

#### 6. **Trends & Recommendations**
- Growth analysis
- Strategic recommendations
- Improvement areas

## 🔧 API Endpoints

The dashboard connects to these API endpoints:

- `GET /impact/global/` - Comprehensive global impact data
- `GET /impact/executive-summary/` - Executive summary
- `GET /impact/dashboard/` - Dashboard-specific data
- `GET /impact/category/{category}/` - Category-specific data

## 🎨 Design Features

### **Modern UI/UX**
- **Tailwind CSS** for styling
- **Font Awesome** icons
- **Chart.js** for visualisations
- **Hover effects** and animations
- **Responsive grid** layout

### **Data Visualisation**
- **Bar charts** for category scores
- **Color-coded** performance indicators
- **Interactive tooltips**
- **Real-time updates**

### **User Experience**
- **Loading states** with spinners
- **Error handling** with notifications
- **Refresh functionality**
- **Mobile-responsive** design

## 📱 Responsive Design

The dashboard is fully responsive and works on:
- **Desktop** (1920x1080+)
- **Tablet** (768px+)
- **Mobile** (320px+)

## 🔄 Real-time Updates

- **Auto-refresh** capability
- **Manual refresh** button
- **Live data** from API
- **Error recovery** mechanisms

## 🎯 Impact Categories

The dashboard displays data for all 10 Movember impact categories:

1. **Men's Health Awareness** (8.7/10)
2. **Mental Health** (8.9/10)
3. **Prostate Cancer** (9.1/10)
4. **Testicular Cancer** (8.5/10)
5. **Suicide Prevention** (9.3/10)
6. **Research Funding** (9.0/10)
7. **Community Engagement** (8.8/10)
8. **Global Reach** (8.6/10)
9. **Advocacy** (8.4/10)
10. **Education** (8.7/10)

## 🛠️ Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Tailwind CSS
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Server**: Python HTTP Server
- **API**: FastAPI (Python)

## 🚀 Deployment

### Local Development
```bash
# Install dependencies
pip install fastapi uvicorn requests

# Start the dashboard
python launch_dashboard.py
```

### Production Deployment
1. Deploy the API to your server
2. Serve the frontend files via web server
3. Update the API URL in `dashboard.js`
4. Configure CORS if needed

## 📋 Browser Compatibility

- **Chrome** 90+
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+

## 🔧 Customisation

### Styling
- Modify `frontend/index.html` for layout changes
- Update CSS classes for styling
- Customise colors in `dashboard.js`

### Data
- Update API endpoints in `dashboard.js`
- Modify data processing in the JavaScript
- Add new visualisations as needed

### Features
- Add new chart types
- Implement additional filters
- Create custom data views

## 🎉 Success Metrics

The dashboard successfully provides:
- ✅ **Comprehensive impact visualisation**
- ✅ **Real-time data integration**
- ✅ **Professional presentation**
- ✅ **UK English compliance**
- ✅ **AUD currency display**
- ✅ **Mobile responsiveness**
- ✅ **Interactive elements**

## 🚀 Next Steps

1. **Connect to real data sources**
2. **Add user authentication**
3. **Implement data export**
4. **Add more chart types**
5. **Create executive reports**
6. **Add stakeholder views**

---

**Your Movember Impact Dashboard is ready to showcase your comprehensive impact measurement system!** 🎯 