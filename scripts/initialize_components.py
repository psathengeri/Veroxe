from monitoring.model_monitoring import ModelMonitor, create_monitoring_tables
from api.client_router import ClientRouter
import logging

def initialize_components():
    try:
        # Initialize model monitoring
        monitor = ModelMonitor()
        logging.info("Model monitoring initialized successfully")

        # Initialize client router
        router = ClientRouter()
        logging.info("Client router initialized successfully")

        # Create monitoring tables
        create_monitoring_tables()
        logging.info("Monitoring tables created successfully")

        return monitor, router
    except Exception as e:
        logging.error(f"Failed to initialize components: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    monitor, router = initialize_components() 