import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Avatar,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  AppBar,
  Toolbar,
  useTheme,
  useMediaQuery,
  CircularProgress,
  Alert,
  Snackbar,
  Fab,
  Zoom,
  Fade,
  Slide,
  Grow,
  Collapse,
  Divider,
  Paper,
  Tabs,
  Tab,
  Badge,
  Tooltip,
  Menu,
  MenuItem,
  Switch,
  FormControlLabel,
  Slider,
  Select,
  FormControl,
  InputLabel,
  OutlinedInput,
  InputAdornment,
  TextField,
  Autocomplete,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  LinearProgress,
  Skeleton,
  AlertTitle,
  Backdrop,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  BottomNavigation,
  BottomNavigationAction,
  MobileStepper
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Analytics as AnalyticsIcon,
  HealthAndSafety as HealthIcon,
  TrendingUp as TrendingIcon,
  Notifications as NotificationsIcon,
  Settings as SettingsIcon,
  Menu as MenuIcon,
  Close as CloseIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  Share as ShareIcon,
  Print as PrintIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
  LocationOn as LocationIcon,
  AccessTime as TimeIcon,
  Person as PersonIcon,
  Group as GroupIcon,
  Business as BusinessIcon,
  School as SchoolIcon,
  Science as ScienceIcon,
  Psychology as PsychologyIcon,
  LocalHospital as HospitalIcon,
  VolunteerActivism as VolunteerIcon,
  Campaign as CampaignIcon,
  Assessment as AssessmentIcon,
  Timeline as TimelineIcon,
  BarChart as BarChartIcon,
  PieChart as PieChartIcon,
  ShowChart as ShowChartIcon,
  BubbleChart as BubbleChartIcon,
  ScatterPlot as ScatterPlotIcon,
  DonutLarge as DonutLargeIcon,
  TrendingDown as TrendingDownIcon,
  Speed as SpeedIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  CheckCircle as CheckCircleIcon,
  Info as InfoIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  KeyboardArrowUp as ArrowUpIcon,
  KeyboardArrowDown as ArrowDownIcon,
  KeyboardArrowLeft as ArrowLeftIcon,
  KeyboardArrowRight as ArrowRightIcon,
  Fullscreen as FullscreenIcon,
  FullscreenExit as FullscreenExitIcon,
  ZoomIn as ZoomInIcon,
  ZoomOut as ZoomOutIcon,
  FilterList as FilterIcon,
  Sort as SortIcon,
  Search as SearchIcon,
  Clear as ClearIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  SkipNext as SkipNextIcon,
  SkipPrevious as SkipPreviousIcon,
  Replay as ReplayIcon,
  Shuffle as ShuffleIcon,
  Repeat as RepeatIcon,
  VolumeUp as VolumeUpIcon,
  VolumeDown as VolumeDownIcon,
  VolumeOff as VolumeOffIcon,
  Brightness4 as DarkModeIcon,
  Brightness7 as LightModeIcon,
  Language as LanguageIcon,
  Translate as TranslateIcon,
  Accessibility as AccessibilityIcon,
  Hearing as HearingIcon,
  Visibility as VisibilityIcon,
  VisibilityOff as VisibilityOffIcon,
  VpnKey as VpnKeyIcon,
  Security as SecurityIcon,
  Lock as LockIcon,
  LockOpen as LockOpenIcon,
  AccountCircle as AccountCircleIcon,
  ExitToApp as LogoutIcon,
  Help as HelpIcon,
  Feedback as FeedbackIcon,
  BugReport as BugReportIcon,
  Report as ReportIcon,
  Support as SupportIcon,
  ContactSupport as ContactSupportIcon,
  LiveHelp as LiveHelpIcon,
  Chat as ChatIcon,
  Forum as ForumIcon,
  QuestionAnswer as QuestionAnswerIcon,
  RateReview as RateReviewIcon,
  Star as StarIcon,
  StarBorder as StarBorderIcon,
  StarHalf as StarHalfIcon,
  Favorite as FavoriteIcon,
  FavoriteBorder as FavoriteBorderIcon,
  ThumbUp as ThumbUpIcon,
  ThumbDown as ThumbDownIcon,
  ThumbUpOutlined as ThumbUpOutlinedIcon,
  ThumbDownOutlined as ThumbDownOutlinedIcon,
  Share as ShareOutlinedIcon,
  Bookmark as BookmarkIcon,
  BookmarkBorder as BookmarkBorderIcon,
  Flag as FlagIcon,
  FlagOutlined as FlagOutlinedIcon,
  Report as ReportOutlinedIcon,
  Block as BlockIcon,
  BlockOutlined as BlockOutlinedIcon,
  MoreVert as MoreVertIcon,
  MoreHoriz as MoreHorizIcon,
  Apps as AppsIcon,
  ViewModule as ViewModuleIcon,
  ViewList as ViewListIcon,
  ViewComfy as ViewComfyIcon,
  ViewCompact as ViewCompactIcon,
  ViewStream as ViewStreamIcon,
  ViewWeek as ViewWeekIcon,
  ViewDay as ViewDayIcon,
  ViewAgenda as ViewAgendaIcon,
  ViewCarousel as ViewCarouselIcon,
  ViewColumn as ViewColumnIcon,
  ViewHeadline as ViewHeadlineIcon,
  ViewQuilt as ViewQuiltIcon,
  ViewSidebar as ViewSidebarIcon,
  ViewTimeline as ViewTimelineIcon,
  ViewWeek as ViewWeekOutlinedIcon,
  ViewDay as ViewDayOutlinedIcon,
  ViewAgenda as ViewAgendaOutlinedIcon,
  ViewCarousel as ViewCarouselOutlinedIcon,
  ViewColumn as ViewColumnOutlinedIcon,
  ViewHeadline as ViewHeadlineOutlinedIcon,
  ViewQuilt as ViewQuiltOutlinedIcon,
  ViewSidebar as ViewSidebarOutlinedIcon,
  ViewTimeline as ViewTimelineOutlinedIcon
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';
import { motion, AnimatePresence } from 'framer-motion';

// Styled components for enhanced UI
const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[8],
  },
  borderRadius: theme.spacing(2),
  overflow: 'hidden',
}));

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  borderRadius: theme.spacing(2),
  background: `linear-gradient(135deg, ${theme.palette.primary.main}15, ${theme.palette.secondary.main}15)`,
  border: `1px solid ${theme.palette.divider}`,
}));

const MetricCard = styled(Card)(({ theme }) => ({
  background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.primary.dark})`,
  color: theme.palette.primary.contrastText,
  borderRadius: theme.spacing(2),
  padding: theme.spacing(2),
  textAlign: 'center',
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    transform: 'scale(1.05)',
    boxShadow: theme.shadows[12],
  },
}));

const ChartContainer = styled(Box)(({ theme }) => ({
  position: 'relative',
  height: 300,
  width: '100%',
  borderRadius: theme.spacing(2),
  overflow: 'hidden',
  background: theme.palette.background.paper,
  border: `1px solid ${theme.palette.divider}`,
}));

// Types for TypeScript
interface DashboardData {
  peopleReached: string;
  totalFunding: string;
  countries: string;
  researchProjects: string;
  grantEvaluationData: {
    labels: string[];
    datasets: Array<{
      label: string;
      data: number[];
      backgroundColor: string;
    }>;
  };
  impactCategoryScores: Record<string, number>;
  overallImpactScore: number;
  trends: Array<{
    title: string;
    value: string;
    change: number;
    trend: 'up' | 'down' | 'stable';
  }>;
  highlights: Array<{
    title: string;
    description: string;
    type: 'success' | 'warning' | 'info' | 'error';
  }>;
  recommendations: Array<{
    title: string;
    description: string;
    priority: 'high' | 'medium' | 'low';
  }>;
}

interface Phase3DashboardProps {
  onThemeChange?: (isDark: boolean) => void;
  onLanguageChange?: (language: string) => void;
  onAccessibilityChange?: (enabled: boolean) => void;
}

const Phase3Dashboard: React.FC<Phase3DashboardProps> = ({
  onThemeChange,
  onLanguageChange,
  onAccessibilityChange
}) => {
  // State management
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [notifications, setNotifications] = useState<Array<{
    id: string;
    title: string;
    message: string;
    type: 'success' | 'warning' | 'error' | 'info';
    timestamp: Date;
  }>>([]);
  const [settings, setSettings] = useState({
    darkMode: false,
    language: 'en',
    accessibility: false,
    autoRefresh: true,
    refreshInterval: 30,
    notifications: true,
    sound: false,
    animations: true,
  });
  const [mobileView, setMobileView] = useState(false);
  const [fullscreen, setFullscreen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<Record<string, any>>({});
  const [sortBy, setSortBy] = useState('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // Theme and responsive hooks
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isTablet = useMediaQuery(theme.breakpoints.down('lg'));

  // Effects
  useEffect(() => {
    setMobileView(isMobile);
    fetchDashboardData();
  }, [isMobile]);

  useEffect(() => {
    if (settings.autoRefresh) {
      const interval = setInterval(fetchDashboardData, settings.refreshInterval * 1000);
      return () => clearInterval(interval);
    }
  }, [settings.autoRefresh, settings.refreshInterval]);

  // Data fetching
  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockData: DashboardData = {
        peopleReached: '8.5M',
        totalFunding: '$125M AUD',
        countries: '25',
        researchProjects: '450',
        grantEvaluationData: {
          labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          datasets: [
            {
              label: 'Approved Grants',
              data: [65, 59, 80, 81, 56, 55],
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
            },
            {
              label: 'Pending Grants',
              data: [28, 48, 40, 19, 86, 27],
              backgroundColor: 'rgba(153, 102, 255, 0.6)',
            },
          ],
        },
        impactCategoryScores: {
          'Mental Health': 8.5,
          'Physical Health': 7.8,
          'Research': 9.2,
          'Community': 8.1,
          'Education': 7.5,
        },
        overallImpactScore: 8.5,
        trends: [
          { title: 'People Reached', value: '+12%', change: 12, trend: 'up' },
          { title: 'Funding Raised', value: '+8%', change: 8, trend: 'up' },
          { title: 'Research Projects', value: '+15%', change: 15, trend: 'up' },
          { title: 'Volunteer Hours', value: '-3%', change: -3, trend: 'down' },
        ],
        highlights: [
          {
            title: 'Record Breaking Month',
            description: 'Highest number of people reached in a single month',
            type: 'success'
          },
          {
            title: 'New Research Partnership',
            description: 'Collaboration with leading Australian universities',
            type: 'info'
          },
          {
            title: 'Funding Milestone',
            description: 'Reached 90% of annual funding target',
            type: 'warning'
          }
        ],
        recommendations: [
          {
            title: 'Expand Mental Health Programs',
            description: 'Focus on rural and remote communities',
            priority: 'high'
          },
          {
            title: 'Increase Digital Engagement',
            description: 'Develop mobile app for better reach',
            priority: 'medium'
          },
          {
            title: 'Enhance Research Collaboration',
            description: 'Partner with international institutions',
            priority: 'low'
          }
        ]
      };
      
      setData(mockData);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Event handlers
  const handleDrawerToggle = () => setDrawerOpen(!drawerOpen);
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => setActiveTab(newValue);
  const handleThemeToggle = () => {
    const newDarkMode = !settings.darkMode;
    setSettings(prev => ({ ...prev, darkMode: newDarkMode }));
    onThemeChange?.(newDarkMode);
  };
  const handleLanguageChange = (language: string) => {
    setSettings(prev => ({ ...prev, language }));
    onLanguageChange?.(language);
  };
  const handleAccessibilityToggle = () => {
    const newAccessibility = !settings.accessibility;
    setSettings(prev => ({ ...prev, accessibility: newAccessibility }));
    onAccessibilityChange?.(newAccessibility);
  };
  const handleRefresh = () => fetchDashboardData();
  const handleFullscreenToggle = () => setFullscreen(!fullscreen);
  const handleSearch = (query: string) => setSearchQuery(query);
  const handleFilterChange = (filter: string, value: any) => {
    setFilters(prev => ({ ...prev, [filter]: value }));
  };
  const handleSortChange = (field: string) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.5,
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5
      }
    }
  };

  // Loading state
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  // Error state
  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Alert severity="error" action={
          <Button color="inherit" size="small" onClick={fetchDashboardData}>
            Retry
          </Button>
        }>
          {error}
        </Alert>
      </Box>
    );
  }

  if (!data) return null;

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* App Bar */}
      <AppBar position="sticky" elevation={0} sx={{ bgcolor: 'background.paper', color: 'text.primary' }}>
        <Toolbar>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={handleDrawerToggle}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Movember AI Rules System - Phase 3
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Tooltip title="Refresh Data">
              <IconButton color="inherit" onClick={handleRefresh}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
            
            <Tooltip title="Notifications">
              <IconButton color="inherit">
                <Badge badgeContent={notifications.length} color="error">
                  <NotificationsIcon />
                </Badge>
              </IconButton>
            </Tooltip>
            
            <Tooltip title="Settings">
              <IconButton color="inherit">
                <SettingsIcon />
              </IconButton>
            </Tooltip>
            
            <Tooltip title="Toggle Theme">
              <IconButton color="inherit" onClick={handleThemeToggle}>
                {settings.darkMode ? <LightModeIcon /> : <DarkModeIcon />}
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <Box sx={{ p: { xs: 1, sm: 2, md: 3 } }}>
          {/* Search and Filters */}
          <StyledPaper sx={{ mb: 3 }}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  placeholder="Search metrics, trends, or insights..."
                  value={searchQuery}
                  onChange={(e) => handleSearch(e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon />
                      </InputAdornment>
                    ),
                    endAdornment: searchQuery && (
                      <InputAdornment position="end">
                        <IconButton size="small" onClick={() => handleSearch('')}>
                          <ClearIcon />
                        </IconButton>
                      </InputAdornment>
                    )
                  }}
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  <FormControl size="small" sx={{ minWidth: 120 }}>
                    <InputLabel>Sort By</InputLabel>
                    <Select
                      value={sortBy}
                      onChange={(e) => handleSortChange(e.target.value)}
                      label="Sort By"
                    >
                      <MenuItem value="date">Date</MenuItem>
                      <MenuItem value="name">Name</MenuItem>
                      <MenuItem value="value">Value</MenuItem>
                      <MenuItem value="priority">Priority</MenuItem>
                    </Select>
                  </FormControl>
                  
                  <IconButton onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}>
                    {sortOrder === 'asc' ? <ArrowUpIcon /> : <ArrowDownIcon />}
                  </IconButton>
                  
                  <Tooltip title="Filters">
                    <IconButton>
                      <FilterIcon />
                    </IconButton>
                  </Tooltip>
                  
                  <Tooltip title="Toggle Fullscreen">
                    <IconButton onClick={handleFullscreenToggle}>
                      {fullscreen ? <FullscreenExitIcon /> : <FullscreenIcon />}
                    </IconButton>
                  </Tooltip>
                </Box>
              </Grid>
            </Grid>
          </StyledPaper>

          {/* Key Metrics */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6} md={3}>
              <motion.div variants={itemVariants}>
                <MetricCard>
                  <Typography variant="h4" gutterBottom>
                    {data.peopleReached}
                  </Typography>
                  <Typography variant="body2">
                    People Reached
                  </Typography>
                  <Chip 
                    label="+12%" 
                    color="success" 
                    size="small" 
                    sx={{ mt: 1 }}
                  />
                </MetricCard>
              </motion.div>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <motion.div variants={itemVariants}>
                <MetricCard>
                  <Typography variant="h4" gutterBottom>
                    {data.totalFunding}
                  </Typography>
                  <Typography variant="body2">
                    Total Funding
                  </Typography>
                  <Chip 
                    label="+8%" 
                    color="success" 
                    size="small" 
                    sx={{ mt: 1 }}
                  />
                </MetricCard>
              </motion.div>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <motion.div variants={itemVariants}>
                <MetricCard>
                  <Typography variant="h4" gutterBottom>
                    {data.countries}
                  </Typography>
                  <Typography variant="body2">
                    Countries
                  </Typography>
                  <Chip 
                    label="+2" 
                    color="info" 
                    size="small" 
                    sx={{ mt: 1 }}
                  />
                </MetricCard>
              </motion.div>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <motion.div variants={itemVariants}>
                <MetricCard>
                  <Typography variant="h4" gutterBottom>
                    {data.researchProjects}
                  </Typography>
                  <Typography variant="body2">
                    Research Projects
                  </Typography>
                  <Chip 
                    label="+15%" 
                    color="success" 
                    size="small" 
                    sx={{ mt: 1 }}
                  />
                </MetricCard>
              </motion.div>
            </Grid>
          </Grid>

          {/* Tabs for different views */}
          <StyledPaper>
            <Tabs value={activeTab} onChange={handleTabChange} variant="scrollable" scrollButtons="auto">
              <Tab label="Overview" icon={<DashboardIcon />} />
              <Tab label="Analytics" icon={<AnalyticsIcon />} />
              <Tab label="Health Impact" icon={<HealthIcon />} />
              <Tab label="Trends" icon={<TrendingIcon />} />
              <Tab label="Recommendations" icon={<AssessmentIcon />} />
            </Tabs>
            
            <Box sx={{ mt: 3 }}>
              <AnimatePresence mode="wait">
                {activeTab === 0 && (
                  <motion.div
                    key="overview"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Grid container spacing={3}>
                      <Grid item xs={12} lg={8}>
                        <StyledCard>
                          <CardContent>
                            <Typography variant="h6" gutterBottom>
                              Grant Evaluation Trends
                            </Typography>
                            <ChartContainer>
                              {/* Chart component would go here */}
                              <Box sx={{ 
                                height: '100%', 
                                display: 'flex', 
                                alignItems: 'center', 
                                justifyContent: 'center',
                                bgcolor: 'grey.100'
                              }}>
                                <Typography variant="body2" color="text.secondary">
                                  Chart Component
                                </Typography>
                              </Box>
                            </ChartContainer>
                          </CardContent>
                        </StyledCard>
                      </Grid>
                      
                      <Grid item xs={12} lg={4}>
                        <StyledCard>
                          <CardContent>
                            <Typography variant="h6" gutterBottom>
                              Impact Categories
                            </Typography>
                            {Object.entries(data.impactCategoryScores).map(([category, score]) => (
                              <Box key={category} sx={{ mb: 2 }}>
                                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                                  <Typography variant="body2">{category}</Typography>
                                  <Typography variant="body2" fontWeight="bold">
                                    {score}/10
                                  </Typography>
                                </Box>
                                <LinearProgress 
                                  variant="determinate" 
                                  value={score * 10} 
                                  sx={{ height: 8, borderRadius: 4 }}
                                />
                              </Box>
                            ))}
                          </CardContent>
                        </StyledCard>
                      </Grid>
                    </Grid>
                  </motion.div>
                )}
                
                {activeTab === 1 && (
                  <motion.div
                    key="analytics"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Typography variant="h6" gutterBottom>
                      Advanced Analytics Dashboard
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Phase 2 analytics integration coming soon...
                    </Typography>
                  </motion.div>
                )}
                
                {activeTab === 2 && (
                  <motion.div
                    key="health"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Typography variant="h6" gutterBottom>
                      Health Impact Assessment
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Health impact metrics and analysis...
                    </Typography>
                  </motion.div>
                )}
                
                {activeTab === 3 && (
                  <motion.div
                    key="trends"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Grid container spacing={2}>
                      {data.trends.map((trend, index) => (
                        <Grid item xs={12} sm={6} md={3} key={index}>
                          <StyledCard>
                            <CardContent>
                              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <Avatar sx={{ 
                                  bgcolor: trend.trend === 'up' ? 'success.main' : 
                                          trend.trend === 'down' ? 'error.main' : 'warning.main',
                                  mr: 1
                                }}>
                                  {trend.trend === 'up' ? <TrendingIcon /> : 
                                   trend.trend === 'down' ? <TrendingDownIcon /> : <SpeedIcon />}
                                </Avatar>
                                <Typography variant="h6">
                                  {trend.value}
                                </Typography>
                              </Box>
                              <Typography variant="body2" color="text.secondary">
                                {trend.title}
                              </Typography>
                            </CardContent>
                          </StyledCard>
                        </Grid>
                      ))}
                    </Grid>
                  </motion.div>
                )}
                
                {activeTab === 4 && (
                  <motion.div
                    key="recommendations"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.3 }}
                  >
                    <Grid container spacing={2}>
                      {data.recommendations.map((rec, index) => (
                        <Grid item xs={12} md={6} key={index}>
                          <StyledCard>
                            <CardContent>
                              <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 1 }}>
                                <Chip 
                                  label={rec.priority.toUpperCase()} 
                                  color={rec.priority === 'high' ? 'error' : 
                                         rec.priority === 'medium' ? 'warning' : 'info'}
                                  size="small"
                                  sx={{ mr: 1 }}
                                />
                                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                                  {rec.title}
                                </Typography>
                              </Box>
                              <Typography variant="body2" color="text.secondary">
                                {rec.description}
                              </Typography>
                            </CardContent>
                          </StyledCard>
                        </Grid>
                      ))}
                    </Grid>
                  </motion.div>
                )}
              </AnimatePresence>
            </Box>
          </StyledPaper>
        </Box>
      </motion.div>

      {/* Mobile Bottom Navigation */}
      {mobileView && (
        <BottomNavigation
          value={activeTab}
          onChange={(event, newValue) => setActiveTab(newValue)}
          sx={{ 
            position: 'fixed', 
            bottom: 0, 
            left: 0, 
            right: 0,
            zIndex: theme.zIndex.appBar
          }}
        >
          <BottomNavigationAction label="Overview" icon={<DashboardIcon />} />
          <BottomNavigationAction label="Analytics" icon={<AnalyticsIcon />} />
          <BottomNavigationAction label="Health" icon={<HealthIcon />} />
          <BottomNavigationAction label="Trends" icon={<TrendingIcon />} />
          <BottomNavigationAction label="Actions" icon={<AssessmentIcon />} />
        </BottomNavigation>
      )}

      {/* Floating Action Button */}
      <Zoom in={!mobileView}>
        <Fab
          color="primary"
          aria-label="add"
          sx={{ position: 'fixed', bottom: 16, right: 16 }}
          onClick={handleRefresh}
        >
          <RefreshIcon />
        </Fab>
      </Zoom>

      {/* Speed Dial for mobile */}
      {mobileView && (
        <SpeedDial
          ariaLabel="Quick actions"
          sx={{ position: 'fixed', bottom: 80, right: 16 }}
          icon={<SpeedDialIcon />}
        >
          <SpeedDialAction
            icon={<RefreshIcon />}
            tooltipTitle="Refresh"
            onClick={handleRefresh}
          />
          <SpeedDialAction
            icon={<ShareIcon />}
            tooltipTitle="Share"
          />
          <SpeedDialAction
            icon={<DownloadIcon />}
            tooltipTitle="Download"
          />
          <SpeedDialAction
            icon={<PrintIcon />}
            tooltipTitle="Print"
          />
        </SpeedDial>
      )}

      {/* Settings Dialog */}
      <Dialog open={false} maxWidth="sm" fullWidth>
        <DialogTitle>Settings</DialogTitle>
        <DialogContent>
          <FormControlLabel
            control={
              <Switch
                checked={settings.darkMode}
                onChange={handleThemeToggle}
              />
            }
            label="Dark Mode"
          />
          <FormControlLabel
            control={
              <Switch
                checked={settings.accessibility}
                onChange={handleAccessibilityToggle}
              />
            }
            label="Accessibility Mode"
          />
          <FormControlLabel
            control={
              <Switch
                checked={settings.autoRefresh}
                onChange={(e) => setSettings(prev => ({ ...prev, autoRefresh: e.target.checked }))}
              />
            }
            label="Auto Refresh"
          />
        </DialogContent>
      </Dialog>

      {/* Notifications Snackbar */}
      <Snackbar
        open={notifications.length > 0}
        autoHideDuration={6000}
        onClose={() => setNotifications([])}
      >
        <Alert severity="info" sx={{ width: '100%' }}>
          {notifications[0]?.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default Phase3Dashboard;
