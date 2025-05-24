from google.cloud import aiplatform
from google.cloud.aiplatform import Model
from google.cloud.aiplatform import ModelRegistry
import json
from typing import Dict, List, Optional
import logging

class ModelGovernance:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        self.registry = ModelRegistry(project=project_id, location=location)
        
    def register_model(
        self,
        model_path: str,
        display_name: str,
        client_id: str,
        version: str,
        risk_level: str,
        metadata: Optional[Dict] = None
    ) -> Model:
        """Register a model with governance metadata."""
        # Prepare model metadata
        model_metadata = {
            "client_id": client_id,
            "version": version,
            "risk_level": risk_level,
            "compliance_status": "pending_review"
        }
        
        if metadata:
            model_metadata.update(metadata)
            
        # Register model
        model = self.registry.register_model(
            model_path=model_path,
            display_name=display_name,
            metadata=model_metadata
        )
        
        return model
    
    def update_model_metadata(
        self,
        model_id: str,
        metadata_updates: Dict
    ):
        """Update model metadata."""
        model = self.registry.get_model(model_id)
        current_metadata = model.metadata or {}
        current_metadata.update(metadata_updates)
        
        model.update(metadata=current_metadata)
        
    def list_models_by_client(self, client_id: str) -> List[Model]:
        """List all models for a specific client."""
        filter_query = f"metadata.client_id={client_id}"
        return list(self.registry.list_models(filter=filter_query))
    
    def list_models_by_risk_level(self, risk_level: str) -> List[Model]:
        """List all models with a specific risk level."""
        filter_query = f"metadata.risk_level={risk_level}"
        return list(self.registry.list_models(filter=filter_query))
    
    def export_model_metadata(self, model_id: str, output_path: str):
        """Export model metadata to JSON file."""
        model = self.registry.get_model(model_id)
        metadata = {
            "model_id": model_id,
            "display_name": model.display_name,
            "metadata": model.metadata,
            "create_time": model.create_time.isoformat(),
            "update_time": model.update_time.isoformat()
        }
        
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    def integrate_with_mlmd(self, model_id: str):
        """Integrate model with ML Metadata Store."""
        try:
            model = self.registry.get_model(model_id)
            
            # Create MLMD context
            context = {
                "name": f"model_{model_id}",
                "properties": {
                    "model_id": model_id,
                    "client_id": model.metadata.get("client_id"),
                    "version": model.metadata.get("version"),
                    "risk_level": model.metadata.get("risk_level")
                }
            }
            
            # Store in MLMD
            # Note: This is a placeholder for MLMD integration
            # Actual implementation would depend on your MLMD setup
            logging.info(f"MLMD context created for model {model_id}")
            
        except Exception as e:
            logging.error(f"Failed to integrate with MLMD: {str(e)}")
            raise 