import torch
import torch.nn as nn
from torchvision import models

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
    
    def _build_model(self, num_classes):
        weights = models.ResNet18_Weights.DEFAULT
        model = models.resnet18(weights=weights)

        num_features = model.fc.in_features

        model.fc = nn.Sequential(
            nn.Linear(num_features, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )

        return model
    
    def load_model(self):
        if self.model is not None and self.metadata is not None:
            return self.model, self.metadata
        
        checkpoint = torch.load(
            MODEL_PATH,
            map_location=self.device
        )

        class_names = checkpoint.get("class_names")

        self.model = self._build_model(
            num_classes=len(class_names)
        )

        self.model.load_state_dict(
            checkpoint["model_state_dict"]
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        self.metadata = {
            "model_name": checkpoint.get("model_name"),
            "class_names": class_names,
            "image_size": checkpoint.get("image_size"),
            "validation_accuracy": checkpoint.get("validation_accuracy"),
            "test_accuracy": checkpoint.get("test_accuracy"),
            "notes": checkpoint.get("notes"),
            "checkpoint_path": str(MODEL_PATH)
        }

        return self.model, self.metadata
    
    def get_model_info(self):
        _, metadata = self.load_model()
        
        return metadata
    
    def predict(self, input_tensor):
        model, metadata = self.load_model()

        input_tensor = input_tensor.to(self.device)

        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)[0]

        predicted_index = probabilities.argmax().item()
        predicted_class = metadata["class_names"][predicted_index]
        confidence = probabilities[predicted_index].item()

        class_probabilities = {
            class_name: probabilities[index].item()
            for index, class_name in enumerate(metadata["class_names"])
        }

        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "probabilities": class_probabilities,
            "model_version": metadata["model_name"]
        }
    

model_service = ModelService()