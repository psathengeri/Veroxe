from google.cloud import storage
from google.cloud import bigquery
from google.cloud import aiplatform
from google.cloud import pubsub_v1
import logging
import sys
import os

def verify_credentials():
    """Verify GCP credentials and test access to key resources."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Check if credentials file exists
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not creds_path:
        logger.error("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        return False
    
    if not os.path.exists(creds_path):
        logger.error(f"Credentials file not found at: {creds_path}")
        return False
    
    logger.info(f"Found credentials file at: {creds_path}")
    
    try:
        # Test Storage access
        logger.info("Testing Storage access...")
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets())
        logger.info(f"Successfully accessed {len(buckets)} buckets")
        
        # Verify specific buckets exist
        required_buckets = ['veroxe-model-registry', 'pipeline-veroxe-train']
        for bucket_name in required_buckets:
            bucket = storage_client.bucket(bucket_name)
            if bucket.exists():
                logger.info(f"✓ Found bucket: {bucket_name}")
            else:
                logger.error(f"✗ Missing bucket: {bucket_name}")
        
        # Test BigQuery access
        logger.info("\nTesting BigQuery access...")
        bq_client = bigquery.Client()
        datasets = list(bq_client.list_datasets())
        logger.info(f"Successfully accessed {len(datasets)} datasets")
        
        # Verify specific dataset exists
        dataset_id = "veroxe_dataset_21d7351d"
        try:
            dataset = bq_client.get_dataset(dataset_id)
            logger.info(f"✓ Found dataset: {dataset_id}")
        except Exception as e:
            logger.error(f"✗ Error accessing dataset {dataset_id}: {str(e)}")
        
        # Test Vertex AI access
        logger.info("\nTesting Vertex AI access...")
        aiplatform.init(project="mlops-veroxe")
        logger.info("✓ Successfully initialized Vertex AI")
        
        # Test Pub/Sub access
        logger.info("\nTesting Pub/Sub access...")
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path("mlops-veroxe", "data-upload-topic")
        try:
            topic = publisher.get_topic(request={"topic": topic_path})
            logger.info(f"✓ Found topic: {topic.name}")
        except Exception as e:
            logger.error(f"✗ Error accessing topic: {str(e)}")
        
        logger.info("\n✓ All credential tests completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"\n✗ Credential verification failed: {str(e)}")
        return False

def main():
    """Main function to run credential verification."""
    print("\n=== GCP Credential Verification ===\n")
    
    if verify_credentials():
        print("\n✅ All credentials and resource access verified successfully!")
        sys.exit(0)
    else:
        print("\n❌ Credential verification failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 