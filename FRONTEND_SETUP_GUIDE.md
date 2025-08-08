# 🎨 **Movember AI Rules System - Frontend Setup Guide**

## **📋 Overview**

The Movember AI Rules System frontend is a React 18 application built with TypeScript, Tailwind CSS, and modern development tools. It provides an intuitive dashboard for grant evaluation, impact reporting, and system monitoring.

**Live Demo**: `https://movember-frontend.onrender.com`  
**Repository**: `frontend/` directory

## **🏗️ Technology Stack**

### **Core Technologies**
- **React 18** - Modern React with hooks and concurrent features
- **TypeScript** - Type-safe JavaScript development
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **React Query** - Data fetching and caching
- **Recharts** - Data visualization library
- **Framer Motion** - Animation library
- **Axios** - HTTP client for API calls

### **Development Tools**
- **ESLint** - Code linting and formatting
- **Prettier** - Code formatting
- **TypeScript** - Type checking
- **Vite** - Hot module replacement

## **🚀 Quick Start**

### **1. Prerequisites**

```bash
# Node.js 18+ required
node --version  # Should be 18.0.0 or higher
npm --version   # Should be 9.0.0 or higher
```

### **2. Install Dependencies**

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### **3. Start Development Server**

```bash
# Start development server
npm run dev

# Open in browser
open http://localhost:5173
```

### **4. Build for Production**

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## **📁 Project Structure**

```
frontend/
├── public/                 # Static assets
│   ├── favicon.ico
│   └── index.html
├── src/
│   ├── components/         # React components
│   │   ├── Dashboard.tsx
│   │   ├── GrantEvaluation.tsx
│   │   ├── AIGrantAssistant.tsx
│   │   ├── SystemHealth.tsx
│   │   └── Metrics.tsx
│   ├── hooks/             # Custom React hooks
│   │   ├── useApi.ts
│   │   └── useMetrics.ts
│   ├── services/          # API services
│   │   ├── api.ts
│   │   └── types.ts
│   ├── utils/             # Utility functions
│   │   ├── formatting.ts
│   │   └── validation.ts
│   ├── App.tsx           # Main app component
│   ├── main.tsx          # App entry point
│   └── index.css         # Global styles
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── tailwind.config.js    # Tailwind CSS configuration
├── postcss.config.js     # PostCSS configuration
└── vite.config.ts        # Vite configuration
```

## **🎨 Component Architecture**

### **Main Components**

#### **Dashboard.tsx**
```typescript
import React from 'react';
import { SystemHealth } from './SystemHealth';
import { GrantEvaluation } from './GrantEvaluation';
import { AIGrantAssistant } from './AIGrantAssistant';
import { Metrics } from './Metrics';

export const Dashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          Movember AI Rules System
        </h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <SystemHealth />
          <Metrics />
        </div>
        
        <div className="mt-8">
          <GrantEvaluation />
        </div>
        
        <div className="mt-8">
          <AIGrantAssistant />
        </div>
      </div>
    </div>
  );
};
```

#### **SystemHealth.tsx**
```typescript
import React from 'react';
import { useApi } from '../hooks/useApi';

interface SystemHealthData {
  system_status: string;
  uptime_percentage: number;
  active_rules: number;
  average_response_time: number;
  memory_usage: number;
  cpu_usage: number;
}

export const SystemHealth: React.FC = () => {
  const { data, loading, error } = useApi<SystemHealthData>('/health/');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">System Health</h2>
      
      <div className="grid grid-cols-2 gap-4">
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">
            {data?.uptime_percentage}%
          </div>
          <div className="text-sm text-gray-600">Uptime</div>
        </div>
        
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">
            {data?.active_rules}
          </div>
          <div className="text-sm text-gray-600">Active Rules</div>
        </div>
        
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-600">
            {data?.average_response_time}s
          </div>
          <div className="text-sm text-gray-600">Avg Response</div>
        </div>
        
        <div className="text-center">
          <div className="text-2xl font-bold text-orange-600">
            {data?.memory_usage}%
          </div>
          <div className="text-sm text-gray-600">Memory Usage</div>
        </div>
      </div>
    </div>
  );
};
```

#### **GrantEvaluation.tsx**
```typescript
import React, { useState } from 'react';
import { useApi } from '../hooks/useApi';

interface GrantForm {
  grant_id: string;
  title: string;
  description: string;
  budget: number;
  timeline_months: number;
  organisation: string;
  contact_person: string;
  email: string;
}

export const GrantEvaluation: React.FC = () => {
  const [formData, setFormData] = useState<GrantForm>({
    grant_id: '',
    title: '',
    description: '',
    budget: 0,
    timeline_months: 12,
    organisation: '',
    contact_person: '',
    email: ''
  });

  const { mutate: evaluateGrant, loading, data } = useApi('/grants/', {
    method: 'POST'
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    evaluateGrant(formData);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Grant Evaluation</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Grant ID"
            value={formData.grant_id}
            onChange={(e) => setFormData({...formData, grant_id: e.target.value})}
            className="border rounded px-3 py-2"
            required
          />
          
          <input
            type="text"
            placeholder="Title"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
            className="border rounded px-3 py-2"
            required
          />
          
          <textarea
            placeholder="Description"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
            className="border rounded px-3 py-2"
            rows={3}
            required
          />
          
          <input
            type="number"
            placeholder="Budget (AUD)"
            value={formData.budget}
            onChange={(e) => setFormData({...formData, budget: Number(e.target.value)})}
            className="border rounded px-3 py-2"
            required
          />
          
          <input
            type="number"
            placeholder="Timeline (months)"
            value={formData.timeline_months}
            onChange={(e) => setFormData({...formData, timeline_months: Number(e.target.value)})}
            className="border rounded px-3 py-2"
            required
          />
          
          <input
            type="text"
            placeholder="Organisation"
            value={formData.organisation}
            onChange={(e) => setFormData({...formData, organisation: e.target.value})}
            className="border rounded px-3 py-2"
            required
          />
          
          <input
            type="text"
            placeholder="Contact Person"
            value={formData.contact_person}
            onChange={(e) => setFormData({...formData, contact_person: e.target.value})}
            className="border rounded px-3 py-2"
            required
          />
          
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            className="border rounded px-3 py-2"
            required
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Evaluating...' : 'Evaluate Grant'}
        </button>
      </form>
      
      {data && (
        <div className="mt-6 p-4 bg-gray-50 rounded">
          <h3 className="font-semibold mb-2">Evaluation Results</h3>
          <div className="text-sm">
            <p><strong>Score:</strong> {data.score}/10</p>
            <p><strong>Recommendations:</strong></p>
            <ul className="list-disc list-inside ml-4">
              {data.recommendations?.map((rec: string, i: number) => (
                <li key={i}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};
```

## **🔧 Configuration Files**

### **package.json**
```json
{
  "name": "movember-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.1",
    "@tanstack/react-query": "^4.29.5",
    "axios": "^1.3.4",
    "recharts": "^2.5.0",
    "framer-motion": "^10.0.1",
    "@heroicons/react": "^2.0.16"
  },
  "devDependencies": {
    "@types/react": "^18.0.28",
    "@types/react-dom": "^18.0.11",
    "@typescript-eslint/eslint-plugin": "^5.57.1",
    "@typescript-eslint/parser": "^5.57.1",
    "@vitejs/plugin-react": "^3.1.0",
    "autoprefixer": "^10.4.14",
    "eslint": "^8.38.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.3.4",
    "postcss": "^8.4.21",
    "tailwindcss": "^3.2.7",
    "typescript": "^4.9.3",
    "vite": "^4.1.0"
  }
}
```

### **tsconfig.json**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### **tailwind.config.js**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'movember-blue': '#0072CE',
        'movember-orange': '#FF6B35',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

### **vite.config.ts**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
  define: {
    'process.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL || 'https://movember-api.onrender.com'),
  },
})
```

## **🔌 API Integration**

### **API Service (src/services/api.ts)**
```typescript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://movember-api.onrender.com';

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add authentication token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const healthApi = {
  getHealth: () => api.get('/health/'),
  getMetrics: () => api.get('/metrics/'),
};

export const grantsApi = {
  evaluateGrant: (data: any) => api.post('/grants/', data),
  getGrant: (id: string) => api.get(`/grants/${id}`),
  getGrantEvaluations: () => api.get('/grant-evaluations/'),
};

export const aiApi = {
  getGrantAssistant: (data: any) => api.post('/ai-grant-assistant/', data),
};

export const scraperApi = {
  scrapeData: (data: any) => api.post('/scraper/', data),
  getExternalData: () => api.get('/external-data/'),
};
```

### **Custom Hook (src/hooks/useApi.ts)**
```typescript
import { useState, useEffect } from 'react';
import { api } from '../services/api';

interface UseApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  immediate?: boolean;
}

export function useApi<T = any>(
  url: string,
  options: UseApiOptions = {}
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const execute = async (body?: any) => {
    setLoading(true);
    setError(null);

    try {
      const method = options.method || 'GET';
      const response = await api.request({
        url,
        method,
        data: body,
      });
      setData(response.data);
    } catch (err) {
      setError(err as Error);
    } finally {
      setLoading(false);
    }
  };

  const mutate = (body?: any) => {
    execute(body);
  };

  useEffect(() => {
    if (options.immediate !== false) {
      execute();
    }
  }, [url]);

  return { data, loading, error, mutate };
}
```

## **🎨 Styling & Theming**

### **Global Styles (src/index.css)**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

@layer base {
  html {
    font-family: 'Inter', system-ui, sans-serif;
  }
  
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn-primary {
    @apply bg-movember-blue text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors;
  }
  
  .btn-secondary {
    @apply bg-gray-200 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-300 transition-colors;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-sm border border-gray-200 p-6;
  }
  
  .input-field {
    @apply border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-movember-blue focus:border-transparent;
  }
}

@layer utilities {
  .text-balance {
    text-wrap: balance;
  }
}
```

### **Theme Configuration**
```typescript
// src/utils/theme.ts
export const theme = {
  colors: {
    primary: {
      50: '#eff6ff',
      500: '#0072CE',
      600: '#0056b3',
      700: '#004085',
    },
    secondary: {
      50: '#fff7ed',
      500: '#FF6B35',
      600: '#e55a2b',
      700: '#cc4a22',
    },
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
  borderRadius: {
    sm: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
  },
};
```

## **🧪 Testing**

### **Unit Testing Setup**
```bash
# Install testing dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest jsdom

# Run tests
npm test
```

### **Test Example**
```typescript
// src/components/__tests__/SystemHealth.test.tsx
import { render, screen } from '@testing-library/react';
import { SystemHealth } from '../SystemHealth';

describe('SystemHealth', () => {
  it('renders system health information', () => {
    render(<SystemHealth />);
    
    expect(screen.getByText('System Health')).toBeInTheDocument();
    expect(screen.getByText('Uptime')).toBeInTheDocument();
    expect(screen.getByText('Active Rules')).toBeInTheDocument();
  });
});
```

## **🚀 Deployment**

### **Render Deployment**

The frontend is automatically deployed to Render when changes are pushed to the main branch.

**Deployment URL**: `https://movember-frontend.onrender.com`

### **Local Production Build**
```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Serve static files
npx serve dist
```

### **Environment Variables**
```bash
# .env.local
VITE_API_URL=https://movember-api.onrender.com
VITE_APP_NAME=Movember AI Rules System
VITE_APP_VERSION=1.1.0
```

## **🔧 Development Workflow**

### **1. Feature Development**
```bash
# Create feature branch
git checkout -b feature/new-component

# Make changes
# ... edit files ...

# Test changes
npm run dev
npm test

# Commit changes
git add .
git commit -m "feat: add new component"

# Push to remote
git push origin feature/new-component
```

### **2. Code Quality**
```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint -- --fix

# Type check
npx tsc --noEmit
```

### **3. Performance Optimization**
```bash
# Analyze bundle size
npm run build
npx vite-bundle-analyzer dist

# Optimize images
npx imagemin public/images/* --out-dir=public/images/optimized
```

## **📱 Responsive Design**

### **Breakpoint Strategy**
```typescript
// src/utils/breakpoints.ts
export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};

export const useBreakpoint = () => {
  const [breakpoint, setBreakpoint] = useState('lg');
  
  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth;
      if (width >= 1536) setBreakpoint('2xl');
      else if (width >= 1280) setBreakpoint('xl');
      else if (width >= 1024) setBreakpoint('lg');
      else if (width >= 768) setBreakpoint('md');
      else if (width >= 640) setBreakpoint('sm');
      else setBreakpoint('xs');
    };
    
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  return breakpoint;
};
```

## **🎯 Performance Best Practices**

### **1. Code Splitting**
```typescript
// Lazy load components
const GrantEvaluation = lazy(() => import('./components/GrantEvaluation'));
const AIGrantAssistant = lazy(() => import('./components/AIGrantAssistant'));

// Use Suspense
<Suspense fallback={<div>Loading...</div>}>
  <GrantEvaluation />
</Suspense>
```

### **2. Memoization**
```typescript
// Memoize expensive calculations
const expensiveValue = useMemo(() => {
  return calculateExpensiveValue(data);
}, [data]);

// Memoize components
const MemoizedComponent = memo(ExpensiveComponent);
```

### **3. Virtual Scrolling**
```typescript
// For large lists
import { FixedSizeList as List } from 'react-window';

const VirtualList = ({ items }) => (
  <List
    height={400}
    itemCount={items.length}
    itemSize={50}
    itemData={items}
  >
    {({ index, style, data }) => (
      <div style={style}>
        {data[index]}
      </div>
    )}
  </List>
);
```

## **🔍 Debugging**

### **React Developer Tools**
```bash
# Install React Developer Tools
npm install --save-dev @types/react-devtools

# Use in development
import { ReactDevTools } from 'react-devtools';
<ReactDevTools />
```

### **Error Boundaries**
```typescript
class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }

    return this.props.children;
  }
}
```

---

**Movember AI Rules System Frontend v1.1** - Modern, responsive, and user-friendly interface. 🇦🇺 