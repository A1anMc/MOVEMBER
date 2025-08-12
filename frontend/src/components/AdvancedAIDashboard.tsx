import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  LinearProgress,
  IconButton,
  Tooltip,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Avatar,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  Snackbar
} from '@mui/material';
import {
  Psychology,
  TrendingUp,
  Speed,
  Accuracy,
  Science,
  AutoAwesome,
  PlayArrow,
  Refresh,
  Info,
  CheckCircle,
  Warning,
  Error,
  Timeline,
  Analytics,
  ModelTraining,
  Insights
} from '@mui/icons-material';
import { useTheme } from '@mui/material/styles';

interface AIModel {
  model_id: string;
  name: string;
  model_type: string;
  task_type: string;
  version: string;
  accuracy: number;
  is_active: boolean;
  performance_metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
    avg_processing_time: number;
    total_predictions: number;
  };
}

interface AIPrediction {
  prediction_id: string;
  model_id: string;
  input_data: any;
  output_data: any;
  confidence_score: number;
  processing_time: number;
  timestamp: string;
  metadata: {
    model_name: string;
    model_type: string;
    task_type: string;
  };
}

interface AIInsight {
  insight_id: string;
  title: string;
  description: string;
  category: string;
  confidence_level: number;
  supporting_evidence: string[];
  actionable_recommendations: string[];
  impact_score: number;
  created_date: string;
}

interface AIStats {
  total_models: number;
  total_predictions: number;
  total_insights: number;
  avg_accuracy: number;
  active_models: number;
  recent_predictions: number;
}

const AdvancedAIDashboard: React.FC = () => {
  const theme = useTheme();
  const [models, setModels] = useState<AIModel[]>([]);
  const [predictions, setPredictions] = useState<AIPrediction[]>([]);
  const [insights, setInsights] = useState<AIInsight[]>([]);
  const [stats, setStats] = useState<AIStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [predictionDialog, setPredictionDialog] = useState(false);
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [inputData, setInputData] = useState('');
  const [predictionResult, setPredictionResult] = useState<any>(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as any });

  useEffect(() => {
    fetchAIData();
  }, []);

  const fetchAIData = async () => {
    try {
      setLoading(true);
      
      // Fetch AI statistics
      const statsResponse = await fetch('https://movember-api.onrender.com/ai/stats');
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData.ai_statistics);
      }

      // Fetch models
      const modelsResponse = await fetch('https://movember-api.onrender.com/ai/models');
      if (modelsResponse.ok) {
        const modelsData = await modelsResponse.json();
        setModels(modelsData.models || []);
      }

      // Fetch recent predictions
      const predictionsResponse = await fetch('https://movember-api.onrender.com/ai/predictions/recent');
      if (predictionsResponse.ok) {
        const predictionsData = await predictionsResponse.json();
        setPredictions(predictionsData.predictions || []);
      }

      // Fetch insights
      const insightsResponse = await fetch('https://movember-api.onrender.com/ai/insights');
      if (insightsResponse.ok) {
        const insightsData = await insightsResponse.json();
        setInsights(insightsData.insights || []);
      }

    } catch (error) {
      console.error('Error fetching AI data:', error);
      setSnackbar({ open: true, message: 'Error loading AI data', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const makePrediction = async () => {
    if (!selectedModel || !inputData) {
      setSnackbar({ open: true, message: 'Please select a model and provide input data', severity: 'warning' });
      return;
    }

    try {
      const response = await fetch('https://movember-api.onrender.com/ai/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model_id: selectedModel,
          input_data: { text: inputData }
        }),
      });

      if (response.ok) {
        const result = await response.json();
        setPredictionResult(result.prediction);
        setSnackbar({ open: true, message: 'Prediction completed successfully!', severity: 'success' });
      } else {
        throw new Error('Prediction failed');
      }
    } catch (error) {
      console.error('Error making prediction:', error);
      setSnackbar({ open: true, message: 'Error making prediction', severity: 'error' });
    }
  };

  const getModelTypeColor = (modelType: string) => {
    const colors: { [key: string]: string } = {
      'bert': theme.palette.primary.main,
      'gpt': theme.palette.secondary.main,
      'lstm': theme.palette.success.main,
      'transformer': theme.palette.warning.main,
      'vision_transformer': theme.palette.info.main,
      'convolutional': theme.palette.error.main,
      'recurrent': theme.palette.primary.light,
      'ensemble': theme.palette.secondary.light
    };
    return colors[modelType.toLowerCase()] || theme.palette.grey[500];
  };

  const getTaskTypeIcon = (taskType: string) => {
    const icons: { [key: string]: React.ReactNode } = {
      'text_classification': <Psychology />,
      'sentiment_analysis': <TrendingUp />,
      'prediction': <Timeline />,
      'recommendation': <Analytics />,
      'text_generation': <AutoAwesome />,
      'image_classification': <Science />,
      'object_detection': <ModelTraining />,
      'anomaly_detection': <Warning />
    };
    return icons[taskType.toLowerCase()] || <Science />;
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return theme.palette.success.main;
    if (confidence >= 0.6) return theme.palette.warning.main;
    return theme.palette.error.main;
  };

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <LinearProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>Loading Advanced AI Dashboard...</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', gap: 2 }}>
        <AutoAwesome sx={{ fontSize: 40, color: theme.palette.primary.main }} />
        <Box>
          <Typography variant="h4" fontWeight="bold" color="primary">
            Advanced AI & ML Dashboard
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            State-of-the-art AI models and machine learning insights
          </Typography>
        </Box>
        <Box sx={{ ml: 'auto' }}>
          <Button
            variant="contained"
            startIcon={<PlayArrow />}
            onClick={() => setPredictionDialog(true)}
            sx={{ mr: 1 }}
          >
            Make Prediction
          </Button>
          <IconButton onClick={fetchAIData}>
            <Refresh />
          </IconButton>
        </Box>
      </Box>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${theme.palette.primary.main}20, ${theme.palette.primary.light}20)` }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <ModelTraining sx={{ fontSize: 30, color: theme.palette.primary.main, mr: 1 }} />
                <Typography variant="h4" fontWeight="bold" color="primary">
                  {stats?.total_models || 0}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">Active AI Models</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${theme.palette.secondary.main}20, ${theme.palette.secondary.light}20)` }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Speed sx={{ fontSize: 30, color: theme.palette.secondary.main, mr: 1 }} />
                <Typography variant="h4" fontWeight="bold" color="secondary">
                  {stats?.total_predictions || 0}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">Total Predictions</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${theme.palette.success.main}20, ${theme.palette.success.light}20)` }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Accuracy sx={{ fontSize: 30, color: theme.palette.success.main, mr: 1 }} />
                <Typography variant="h4" fontWeight="bold" color="success.main">
                  {((stats?.avg_accuracy || 0) * 100).toFixed(1)}%
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">Average Accuracy</Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${theme.palette.warning.main}20, ${theme.palette.warning.light}20)` }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Insights sx={{ fontSize: 30, color: theme.palette.warning.main, mr: 1 }} />
                <Typography variant="h4" fontWeight="bold" color="warning.main">
                  {stats?.total_insights || 0}
                </Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">AI Insights</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* AI Models Grid */}
      <Typography variant="h5" fontWeight="bold" sx={{ mb: 3 }}>
        AI Models
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {models.map((model) => (
          <Grid item xs={12} md={6} lg={4} key={model.model_id}>
            <Card sx={{ height: '100%', position: 'relative' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: getModelTypeColor(model.model_type), mr: 2 }}>
                    {getTaskTypeIcon(model.task_type)}
                  </Avatar>
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {model.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      v{model.version}
                    </Typography>
                  </Box>
                  <Chip
                    label={model.is_active ? 'Active' : 'Inactive'}
                    color={model.is_active ? 'success' : 'default'}
                    size="small"
                    sx={{ ml: 'auto' }}
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Chip
                    label={model.model_type.toUpperCase()}
                    size="small"
                    sx={{ mr: 1, mb: 1, bgcolor: getModelTypeColor(model.model_type), color: 'white' }}
                  />
                  <Chip
                    label={model.task_type.replace('_', ' ')}
                    size="small"
                    variant="outlined"
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Accuracy: {((model.accuracy || 0) * 100).toFixed(1)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={(model.accuracy || 0) * 100}
                    sx={{ height: 8, borderRadius: 4 }}
                  />
                </Box>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem' }}>
                  <Typography variant="body2" color="text.secondary">
                    Precision: {((model.performance_metrics?.precision || 0) * 100).toFixed(1)}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Recall: {((model.performance_metrics?.recall || 0) * 100).toFixed(1)}%
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Recent Predictions */}
      <Typography variant="h5" fontWeight="bold" sx={{ mb: 3 }}>
        Recent Predictions
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {predictions.slice(0, 6).map((prediction) => (
          <Grid item xs={12} md={6} lg={4} key={prediction.prediction_id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: getModelTypeColor(prediction.metadata.model_type), mr: 2 }}>
                    {getTaskTypeIcon(prediction.metadata.task_type)}
                  </Avatar>
                  <Box sx={{ flex: 1 }}>
                    <Typography variant="subtitle1" fontWeight="bold">
                      {prediction.metadata.model_name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {new Date(prediction.timestamp).toLocaleString()}
                    </Typography>
                  </Box>
                  <Chip
                    label={`${(prediction.confidence_score * 100).toFixed(1)}%`}
                    size="small"
                    sx={{ bgcolor: getConfidenceColor(prediction.confidence_score), color: 'white' }}
                  />
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  Processing Time: {prediction.processing_time.toFixed(3)}s
                </Typography>

                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2" fontWeight="bold" gutterBottom>
                    Output:
                  </Typography>
                  <Paper sx={{ p: 1, bgcolor: 'grey.50' }}>
                    <Typography variant="body2" fontFamily="monospace" fontSize="0.75rem">
                      {JSON.stringify(prediction.output_data, null, 2)}
                    </Typography>
                  </Paper>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* AI Insights */}
      <Typography variant="h5" fontWeight="bold" sx={{ mb: 3 }}>
        AI Insights
      </Typography>
      <Grid container spacing={3}>
        {insights.slice(0, 3).map((insight) => (
          <Grid item xs={12} md={6} lg={4} key={insight.insight_id}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Insights sx={{ fontSize: 30, color: theme.palette.warning.main, mr: 2 }} />
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {insight.title}
                    </Typography>
                    <Chip
                      label={insight.category.replace('_', ' ')}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                  </Box>
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {insight.description}
                </Typography>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" fontWeight="bold" gutterBottom>
                    Confidence: {((insight.confidence_level || 0) * 100).toFixed(1)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={(insight.confidence_level || 0) * 100}
                    sx={{ height: 6, borderRadius: 3 }}
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" fontWeight="bold" gutterBottom>
                    Impact Score: {((insight.impact_score || 0) * 100).toFixed(1)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={(insight.impact_score || 0) * 100}
                    sx={{ height: 6, borderRadius: 3, bgcolor: 'success.light' }}
                    color="success"
                  />
                </Box>

                <Typography variant="body2" fontWeight="bold" gutterBottom>
                  Recommendations:
                </Typography>
                <List dense>
                  {insight.actionable_recommendations.slice(0, 2).map((rec, index) => (
                    <ListItem key={index} sx={{ py: 0 }}>
                      <ListItemIcon sx={{ minWidth: 30 }}>
                        <CheckCircle sx={{ fontSize: 16, color: 'success.main' }} />
                      </ListItemIcon>
                      <ListItemText
                        primary={rec}
                        primaryTypographyProps={{ variant: 'body2', fontSize: '0.75rem' }}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Prediction Dialog */}
      <Dialog open={predictionDialog} onClose={() => setPredictionDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <AutoAwesome sx={{ mr: 1 }} />
            Make AI Prediction
          </Box>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Select AI Model</InputLabel>
                <Select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  label="Select AI Model"
                >
                  {models.map((model) => (
                    <MenuItem key={model.model_id} value={model.model_id}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Avatar sx={{ bgcolor: getModelTypeColor(model.model_type), mr: 1, width: 24, height: 24 }}>
                          {getTaskTypeIcon(model.task_type)}
                        </Avatar>
                        {model.name} ({model.task_type.replace('_', ' ')})
                      </Box>
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Input Data"
                value={inputData}
                onChange={(e) => setInputData(e.target.value)}
                placeholder="Enter text for analysis..."
              />
            </Grid>
            {predictionResult && (
              <Grid item xs={12}>
                <Paper sx={{ p: 2, bgcolor: 'success.light', color: 'success.contrastText' }}>
                  <Typography variant="h6" gutterBottom>
                    Prediction Result:
                  </Typography>
                  <Typography variant="body2" fontFamily="monospace">
                    {JSON.stringify(predictionResult, null, 2)}
                  </Typography>
                </Paper>
              </Grid>
            )}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPredictionDialog(false)}>Cancel</Button>
          <Button onClick={makePrediction} variant="contained" disabled={!selectedModel || !inputData}>
            Make Prediction
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity} onClose={() => setSnackbar({ ...snackbar, open: false })}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default AdvancedAIDashboard;
