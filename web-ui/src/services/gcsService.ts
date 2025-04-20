interface SensorData {
  sensor_id: string;
  temperature: number;
  humidity: number;
}

export const uploadToGCS = async (data: SensorData): Promise<string> => {
  try {
    // In a real implementation, this would make an API call to your backend
    // which would then use the GCS client library to upload the file
    const response = await fetch('/api/upload', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    const result = await response.json();
    return result.filename;
  } catch (error) {
    throw new Error(`Upload failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}; 