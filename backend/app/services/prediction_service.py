import json

from app.db.models import Prediction


class PredictionService:
    def create_prediction(
        self,
        db,
        filename,
        predicted_class,
        confidence,
        probabilities,
        model_version,
        latency_ms,
        image_width,
        image_height,
        file_size_kb,
        low_confidence_flag
    ):
        prediction = Prediction(
            filename=filename,
            predicted_class=predicted_class,
            confidence=confidence,
            probabilities_json=json.dumps(probabilities),
            model_version=model_version,
            latency_ms=latency_ms,
            image_width=image_width,
            image_height=image_height,
            file_size_kb=file_size_kb,
            low_confidence_flag=low_confidence_flag
        )

        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        return prediction
    
    def get_predictions(self, db, limit=50):
        return (
            db.query(Prediction)
            .order_by(Prediction.created_at.desc())
            .limit(limit)
            .all()
        )
    
    def get_prediction_by_id(self, db, prediction_id):
        return (
            db.query(Prediction)
            .filter(Prediction.id == prediction_id)
            .first()
        )
    
    def update_prediction_review(
        self,
        db,
        prediction_id,
        review_status=None,
        true_label=None,
        notes=None
    ):
        prediction = self.get_prediction_by_id(
            db=db,
            prediction_id=prediction_id
        )

        if prediction is None:
            return None
        
        if review_status is not None:
            prediction.review_status = review_status
        
        if true_label is not None:
            prediction.true_label = true_label
            prediction.correct = (
                true_label == prediction.predicted_class
            )
        
        if notes is not None:
            prediction.notes = notes
        
        db.commit()
        db.refresh(prediction)

        return prediction


prediction_service = PredictionService()