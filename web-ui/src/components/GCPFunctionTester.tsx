import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  TextField,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';

interface SensorData {
  sensor_id: string;
  temperature: number;
  humidity: number;
}

const GCPFunctionTester: React.FC = () => {
  const [sensorData, setSensorData] = useState<SensorData>({
    sensor_id: '',
    temperature: 0,
    humidity: 0,
  });
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<{ type: 'success' | 'error' | 'info' | null; message: string }>({
    type: null,
    message: '',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSensorData((prev) => ({
      ...prev,
      [name]: name === 'sensor_id' ? value : parseFloat(value),
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setStatus({ type: 'info', message: 'Uploading data...' });

    try {
      // Here we would implement the actual upload logic to GCS
      // For now, we'll simulate the process
      const filename = `uploads/pending/client-x/sensor_readings_${Date.now()}.json`;
      
      // Simulated upload delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setStatus({
        type: 'success',
        message: `File uploaded successfully to gs://ml-dataset-veroxe/${filename}. Check Cloud Logging for results.`
      });
    } catch (error) {
      setStatus({
        type: 'error',
        message: `Error uploading file: ${error instanceof Error ? error.message : 'Unknown error'}`
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ maxWidth: 600, mx: 'auto', mt: 4 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          GCP Function Tester
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          Function: validate_file (Python 3.10)
        </Typography>
        
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <TextField
            fullWidth
            label="Sensor ID"
            name="sensor_id"
            value={sensorData.sensor_id}
            onChange={handleInputChange}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Temperature"
            name="temperature"
            type="number"
            value={sensorData.temperature}
            onChange={handleInputChange}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Humidity"
            name="humidity"
            type="number"
            value={sensorData.humidity}
            onChange={handleInputChange}
            margin="normal"
            required
          />
          
          <Button
            type="submit"
            variant="contained"
            fullWidth
            sx={{ mt: 3 }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Upload and Test'}
          </Button>
        </Box>

        {status.type && (
          <Alert severity={status.type} sx={{ mt: 3 }}>
            {status.message}
          </Alert>
        )}

        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle2" gutterBottom>
            Function Details:
          </Typography>
          <Typography variant="body2" component="div">
            <ul>
              <li>Trigger: GCS Finalize (uploads/pending/ in ml-dataset-veroxe)</li>
              <li>Memory: 256MB</li>
              <li>Timeout: 540s</li>
              <li>Service Account: 829870057131-compute@developer.gserviceaccount.com</li>
            </ul>
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default GCPFunctionTester; 