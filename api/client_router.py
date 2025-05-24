from google.cloud import storage
from google.cloud import pubsub_v1
import json
import os
from typing import Dict, Optional
import logging

# Project configuration
PROJECT_ID = "mlops-veroxe"
BUCKET_NAME = "veroxe-model-registry"
PUBSUB_TOPIC = "data-upload-topic"

class ClientRouter:
    def __init__(self, project_id: str = PROJECT_ID, bucket_name: str = BUCKET_NAME):
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)
        
    def get_client_schema(self, client_id: str) -> Dict:
        """Retrieve client-specific schema from GCS."""
        schema_path = f"schemas/{client_id}/schema.json"
        blob = self.bucket.blob(schema_path)
        
        try:
            schema_content = blob.download_as_string()
            return json.loads(schema_content)
        except Exception as e:
            logging.error(f"Failed to retrieve schema for client {client_id}: {str(e)}")
            raise
            
    def route_file(
        self,
        file_path: str,
        client_id: Optional[str] = None,
        pubsub_attributes: Optional[Dict] = None
    ) -> str:
        """Route incoming file based on client ID or Pub/Sub attributes."""
        # Determine client ID from either direct input or Pub/Sub attributes
        if not client_id and pubsub_attributes:
            client_id = pubsub_attributes.get('client_id')
            
        if not client_id:
            # Try to determine client ID from file path
            # Example: gs://bucket/client_id/filename.csv
            path_parts = file_path.split('/')
            if len(path_parts) > 1:
                client_id = path_parts[0]
                
        if not client_id:
            raise ValueError("Could not determine client ID from input")
            
        # Get client schema
        schema = self.get_client_schema(client_id)
        
        # Create client-specific destination path
        file_name = os.path.basename(file_path)
        destination_path = f"processed/{client_id}/{file_name}"
        
        # Copy file to client-specific location
        source_blob = self.bucket.blob(file_path)
        destination_blob = self.bucket.blob(destination_path)
        
        try:
            destination_blob.rewrite(source_blob)
            logging.info(f"Successfully routed file to {destination_path}")
            return destination_path
        except Exception as e:
            logging.error(f"Failed to route file: {str(e)}")
            raise
            
    def publish_routing_event(
        self,
        topic_name: str = PUBSUB_TOPIC,
        file_path: str = None,
        client_id: str = None,
        status: str = None
    ):
        """Publish routing event to Pub/Sub."""
        if not all([file_path, client_id, status]):
            raise ValueError("All parameters must be provided")
            
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(self.project_id, topic_name)
        
        message = {
            "file_path": file_path,
            "client_id": client_id,
            "status": status,
            "timestamp": "CURRENT_TIMESTAMP()"
        }
        
        try:
            future = publisher.publish(
                topic_path,
                json.dumps(message).encode('utf-8')
            )
            future.result()
            logging.info(f"Published routing event for {file_path}")
        except Exception as e:
            logging.error(f"Failed to publish routing event: {str(e)}")
            raise
            
    def validate_file_against_schema(
        self,
        file_path: str,
        client_id: str
    ) -> bool:
        """Validate file against client schema."""
        schema = self.get_client_schema(client_id)
        blob = self.bucket.blob(file_path)
        
        try:
            # Download and validate file
            # This is a placeholder - implement actual validation logic
            content = blob.download_as_string()
            # Add your validation logic here
            return True
        except Exception as e:
            logging.error(f"File validation failed: {str(e)}")
            return False 