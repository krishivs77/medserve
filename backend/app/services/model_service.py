import torch

from app.core.config import MODEL_PATH


class ModelService:
    def __init__(self):
        self.model = None
        self.metadata = None
        self.device = self._get_device()
    
    def _get_device(self):
        if torch.backends.mps.is_available():
            return torch.device("mps")
        
        if torch.cuda.is_available():
            return torch.device("cuda")
        
        return torch.device("cpu")
    
    def load_model(self):
        checkpoint = torch.load(
            MODEL_PATH,
            map_location=self.device
        )

        self.metadata = {
            "model_name": checkpoint.get("model_name"),
            "class_names": checkpoint.get("class_names"),
            "image_size": checkpoint.get("image_size"),
            "validation_accuracy": checkpoint.get("validation_accuracy"),
            "test_accuracy": checkpoint.get("test_accuracy"),
            "notes": checkpoint.get("notes"),
            "checkpoint_path": str(MODEL_PATH)
        }

        return self.metadata
    
    def get_model_info(self):
        if self.metadata is None:
            self.load_model()
        
        return self.metadata
    

model_service = ModelService()