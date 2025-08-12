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
  Paper,
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
  Snackbar,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemIcon
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
  CheckCircle,
  ModelTraining,
  Insights,
  Timeline
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
}

interface AIPrediction {
  prediction_id: string;
  model_id: string;
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
  actionable_recommendations: string[];
  impact_score: number;
  created_date: string;
}

const AdvancedAIDashboard: React.FC = () => {
  const theme = useTheme();
  const [models, setModels] = useState<AIModel[]>([]);
  const [predictions, setPredictions] = useState<AIPrediction[]>([]);
  const [insights, setInsights] = useState<AIInsight[]>([]);
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
      
      // Simulated AI data for demonstration
      const mockModels: AIModel[] = [
        {
          model_id: '1',
          name: 'BERT-Prostate-Cancer-Classifier',
          model_type: 'bert',
          task_type: 'text_classification',
          version: '2.0.0',
          accuracy: 0.95,
          is_active: true
        },
        {
          model_id: '2',
          name: 'GPT-Mens-Health-Sentiment',
          model_type: 'gpt',
          task_type: 'sentiment_analysis',
          version: '3.5.0',
          accuracy: 0.92,
          is_active: true
        },
        {
          model_id: '3',
          name: 'LSTM-Health-Trend-Predictor',
          model_type: 'lstm',
          task_type: 'prediction',
          version: '1.5.0',
          accuracy: 0.88,
          is_active: true
        }
      ];

      const mockPredictions: AIPrediction[] = [
        {
          prediction_id: '1',
          model_id: '1',
          output_data: { predicted_category: 'prostate_cancer', confidence: 0.95 },
          confidence_score: 0.95,
          processing_time: 0.15,
          timestamp: new Date().toISOString(),
          metadata: {
            model_name: 'BERT-Prostate-Cancer-Classifier',
            model_type: 'bert',
            task_type: 'text_classification'
          }
        }
      ];

      const mockInsights: AIInsight[] = [
        {
          insight_id: '1',
          title: 'Advanced Prostate Cancer Detection Patterns',
          description: 'AI analysis reveals new patterns in early detection methods with 95% accuracy improvement potential.',
          category: 'prostate_cancer',
          confidence_level: 0.92,
          actionable_recommendations: [
            'Implement AI-powered screening protocols',
            'Enhance early detection algorithms'
          ],
          impact_score: 0.88,
          created_date: new Date().toISOString()
        }
      ];

      setModels(mockModels);
      setPredictions(mockPredictions);
      setInsights(mockInsights);

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
      // Simulated prediction
      const mockResult = {
        predicted_category: 'prostate_cancer',
        confidence: 0.95,
        processing_time: 0.15,
        model_type: 'BERT'
      };

      setPredictionResult(mockResult);
      setSnackbar({ open: true, message: 'Prediction completed successfully!', severity: 'success' });
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
      'transformer': theme.palette.warning.main
    };
    return colors[modelType.toLowerCase()] || theme.palette.grey[500];
  };

  const getTaskTypeIcon = (taskType: string) => {
    const icons: { [key: string]: React.ReactNode } = {
      'text_classification': <Psychology />,
      'sentiment_analysis': <TrendingUp />,
      'prediction': <Timeline />,
      'recommendation': <Insights />
    };
    return icons[taskType.toLowerCase()] || <Science />;
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
                  {models.length}
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
                  {predictions.length}
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
                  {((models.reduce((acc, model) => acc + model.accuracy, 0) / models.length) * 100).toFixed(1)}%
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
                  {insights.length}
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
        {insights.map((insight) => (
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

                <Typography variant="body2" fontWeight="bold" gutterBottom>
                  Recommendations:
                </Typography>
                <List dense>
                  {insight.actionable_recommendations.map((rec, index) => (
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
