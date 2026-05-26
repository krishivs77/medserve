from io import BytesIO

from PIL import Image
from torchvision import transforms


class ImageService:
    def __init__(self):
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),

            transforms.Grayscale(
                num_output_channels=3
            ),

            transforms.ToTensor(),

            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def load_image(self, image_bytes):
        image = Image.open(
            BytesIO(image_bytes)
        )

        return image.convert("RGB")

    def preprocess_image(self, image):
        tensor = self.transform(image)
        
        return tensor.unsqueeze(0)


image_service = ImageService()