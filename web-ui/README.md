# GCP Function Tester UI

A web interface for testing the GCP Cloud Function that validates and processes sensor data files.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The application will be available at http://localhost:3000

## Usage

1. Fill in the sensor data form with:
   - Sensor ID
   - Temperature
   - Humidity

2. Click "Upload and Test" to submit the data

3. The function will:
   - Create a JSON file with your data
   - Upload it to GCS bucket: `gs://ml-dataset-veroxe/uploads/pending/`
   - Trigger the Cloud Function
   - Display the results

## Function Details

- Name: validate_file
- Runtime: Python 3.10
- Trigger: GCS Finalize (uploads/pending/ in ml-dataset-veroxe)
- Memory: 256MB
- Timeout: 540s
- Service Account: 829870057131-compute@developer.gserviceaccount.com

## Monitoring Results

After uploading a file:
1. Check Cloud Logging for function execution logs
2. If validation fails, check the BigQuery table in veroxe_dataset
3. If validation passes, the file will be moved to: uploads/processed/client-x/sensor_readings.json 