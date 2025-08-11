import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  IconButton,
  BottomNavigation,
  BottomNavigationAction,
  Fab,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
  SwipeableDrawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  AppBar,
  Toolbar,
  useTheme,
  useMediaQuery,
  CircularProgress,
  Alert,
  Snackbar,
  Paper,
  Tabs,
  Tab,
  Badge,
  Tooltip,
  Switch,
  FormControlLabel,
  Slider,
  TextField,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  LinearProgress,
  Skeleton,
  AlertTitle,
  Backdrop,
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

interface MobileDashboardData {
  peopleReached: string;
  totalFunding: string;
  countries: string;
  researchProjects: string;
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

const Phase3Mobile: React.FC = () => {
  const [data, setData] = useState<MobileDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [settings, setSettings] = useState({
    darkMode: false,
    accessibility: false,
    autoRefresh: true,
    notifications: true,
    sound: false,
    animations: true,
  });

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  useEffect(() => {
    fetchMobileData();
  }, []);

  const fetchMobileData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockData: MobileDashboardData = {
        peopleReached: '8.5M',
        totalFunding: '$125M AUD',
        countries: '25',
        researchProjects: '450',
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
      setError('Failed to load mobile dashboard data');
      console.error('Mobile dashboard data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDrawerToggle = () => setDrawerOpen(!drawerOpen);
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => setActiveTab(newValue);
  const handleThemeToggle = () => {
    setSettings(prev => ({ ...prev, darkMode: !prev.darkMode }));
  };
  const handleRefresh = () => fetchMobileData();

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 2 }}>
        <Alert severity="error" action={
          <Button color="inherit" size="small" onClick={fetchMobileData}>
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
    <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: 'background.default', pb: 7 }}>
      {/* Mobile App Bar */}
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
            Movember AI
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Tooltip title="Refresh">
              <IconButton color="inherit" onClick={handleRefresh}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
            
            <Tooltip title="Notifications">
              <IconButton color="inherit">
                <Badge badgeContent={3} color="error">
                  <NotificationsIcon />
                </Badge>
              </IconButton>
            </Tooltip>
            
            <Tooltip title="Theme">
              <IconButton color="inherit" onClick={handleThemeToggle}>
                {settings.darkMode ? <LightModeIcon /> : <DarkModeIcon />}
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <Box sx={{ p: 2 }}>
        {/* Key Metrics Cards */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Key Metrics
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, overflowX: 'auto', pb: 1 }}>
            <Card sx={{ minWidth: 150, flexShrink: 0 }}>
              <CardContent sx={{ textAlign: 'center', p: 2 }}>
                <Typography variant="h4" color="primary" gutterBottom>
                  {data.peopleReached}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  People Reached
                </Typography>
                <Chip label="+12%" color="success" size="small" sx={{ mt: 1 }} />
              </CardContent>
            </Card>
            
            <Card sx={{ minWidth: 150, flexShrink: 0 }}>
              <CardContent sx={{ textAlign: 'center', p: 2 }}>
                <Typography variant="h4" color="primary" gutterBottom>
                  {data.totalFunding}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total Funding
                </Typography>
                <Chip label="+8%" color="success" size="small" sx={{ mt: 1 }} />
              </CardContent>
            </Card>
            
            <Card sx={{ minWidth: 150, flexShrink: 0 }}>
              <CardContent sx={{ textAlign: 'center', p: 2 }}>
                <Typography variant="h4" color="primary" gutterBottom>
                  {data.countries}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Countries
                </Typography>
                <Chip label="+2" color="info" size="small" sx={{ mt: 1 }} />
              </CardContent>
            </Card>
            
            <Card sx={{ minWidth: 150, flexShrink: 0 }}>
              <CardContent sx={{ textAlign: 'center', p: 2 }}>
                <Typography variant="h4" color="primary" gutterBottom>
                  {data.researchProjects}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Research Projects
                </Typography>
                <Chip label="+15%" color="success" size="small" sx={{ mt: 1 }} />
              </CardContent>
            </Card>
          </Box>
        </Box>

        {/* Tabs */}
        <Paper sx={{ mb: 3 }}>
          <Tabs 
            value={activeTab} 
            onChange={handleTabChange} 
            variant="scrollable" 
            scrollButtons="auto"
            sx={{ borderBottom: 1, borderColor: 'divider' }}
          >
            <Tab label="Overview" icon={<DashboardIcon />} />
            <Tab label="Trends" icon={<TrendingIcon />} />
            <Tab label="Highlights" icon={<InfoIcon />} />
            <Tab label="Actions" icon={<AssessmentIcon />} />
          </Tabs>
          
          <Box sx={{ p: 2 }}>
            {activeTab === 0 && (
              <Box>
                <Typography variant="h6" gutterBottom>
                  Overview
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Welcome to the Movember AI Rules System mobile dashboard. 
                  Track key metrics and insights on the go.
                </Typography>
              </Box>
            )}
            
            {activeTab === 1 && (
              <Box>
                <Typography variant="h6" gutterBottom>
                  Trends
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {data.trends.map((trend, index) => (
                    <Card key={index}>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                          <Box>
                            <Typography variant="body1" fontWeight="bold">
                              {trend.title}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {trend.value}
                            </Typography>
                          </Box>
                          <Chip 
                            label={trend.trend === 'up' ? '↗' : trend.trend === 'down' ? '↘' : '→'}
                            color={trend.trend === 'up' ? 'success' : trend.trend === 'down' ? 'error' : 'default'}
                            variant="outlined"
                          />
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              </Box>
            )}
            
            {activeTab === 2 && (
              <Box>
                <Typography variant="h6" gutterBottom>
                  Highlights
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {data.highlights.map((highlight, index) => (
                    <Card key={index}>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                          <Box sx={{ 
                            width: 8, 
                            height: 8, 
                            borderRadius: '50%', 
                            bgcolor: highlight.type === 'success' ? 'success.main' :
                                     highlight.type === 'warning' ? 'warning.main' :
                                     highlight.type === 'error' ? 'error.main' : 'info.main',
                            mt: 1
                          }} />
                          <Box sx={{ flexGrow: 1 }}>
                            <Typography variant="body1" fontWeight="bold">
                              {highlight.title}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {highlight.description}
                            </Typography>
                          </Box>
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              </Box>
            )}
            
            {activeTab === 3 && (
              <Box>
                <Typography variant="h6" gutterBottom>
                  Recommended Actions
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {data.recommendations.map((rec, index) => (
                    <Card key={index}>
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                          <Chip 
                            label={rec.priority.toUpperCase()} 
                            color={rec.priority === 'high' ? 'error' : 
                                   rec.priority === 'medium' ? 'warning' : 'info'}
                            size="small"
                          />
                          <Box sx={{ flexGrow: 1 }}>
                            <Typography variant="body1" fontWeight="bold">
                              {rec.title}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {rec.description}
                            </Typography>
                          </Box>
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              </Box>
            )}
          </Box>
        </Paper>
      </Box>

      {/* Mobile Bottom Navigation */}
      <BottomNavigation
        value={activeTab}
        onChange={(event, newValue) => setActiveTab(newValue)}
        sx={{ 
          position: 'fixed', 
          bottom: 0, 
          left: 0, 
          right: 0,
          zIndex: theme.zIndex.appBar,
          borderTop: 1,
          borderColor: 'divider'
        }}
      >
        <BottomNavigationAction label="Overview" icon={<DashboardIcon />} />
        <BottomNavigationAction label="Trends" icon={<TrendingIcon />} />
        <BottomNavigationAction label="Highlights" icon={<InfoIcon />} />
        <BottomNavigationAction label="Actions" icon={<AssessmentIcon />} />
      </BottomNavigation>

      {/* Speed Dial for quick actions */}
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

      {/* Mobile Drawer */}
      <SwipeableDrawer
        anchor="left"
        open={drawerOpen}
        onClose={handleDrawerToggle}
        onOpen={handleDrawerToggle}
      >
        <Box sx={{ width: 250, p: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              Menu
            </Typography>
            <IconButton onClick={handleDrawerToggle}>
              <CloseIcon />
            </IconButton>
          </Box>
          
          <List>
            <ListItem button>
              <ListItemIcon>
                <DashboardIcon />
              </ListItemIcon>
              <ListItemText primary="Dashboard" />
            </ListItem>
            
            <ListItem button>
              <ListItemIcon>
                <AnalyticsIcon />
              </ListItemIcon>
              <ListItemText primary="Analytics" />
            </ListItem>
            
            <ListItem button>
              <ListItemIcon>
                <HealthIcon />
              </ListItemIcon>
              <ListItemText primary="Health Impact" />
            </ListItem>
            
            <Divider sx={{ my: 2 }} />
            
            <ListItem button>
              <ListItemIcon>
                <SettingsIcon />
              </ListItemIcon>
              <ListItemText primary="Settings" />
            </ListItem>
            
            <ListItem button>
              <ListItemIcon>
                <HelpIcon />
              </ListItemIcon>
              <ListItemText primary="Help & Support" />
            </ListItem>
          </List>
        </Box>
      </SwipeableDrawer>
    </Box>
  );
};

export default Phase3Mobile;
