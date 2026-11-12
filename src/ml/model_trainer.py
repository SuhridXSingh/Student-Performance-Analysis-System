from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import os
import joblib
DEFAULT_MODEL_PATH = os.path.join("models", "student_model.pkl")

class StudentPerformanceModel:
    def __init__(self, df, model_type = "linear"):
        self.df = df
        self.model_type = model_type
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def prep_data(self):
        feature_cols = ['weekly_self_study_hours', 'attendance_percentage', 'class_participation']
        hours_col = "weekly_self_study_hours" if "weekly_self_study_hours" in self.df.columns else "study_hours"
        score_col = "total_score" if "total_score" in self.df.columns else "score"
        X = self.df[[hours_col, 'attendance_percentage', 'class_participation']]
        y = self.df[score_col]

        stratify_col = self.df['grade'] if 'grade' in self.df.columns else None

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
        X, y, test_size=0.2,stratify=stratify_col, random_state=42)

        return self.X_train, self.X_test, self.y_train, self.y_test

    def train(self):
        if self.model_type == "random_forest":
            self.model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
        else:
            self.model = LinearRegression()
        
        self.model.fit(self.X_train, self.y_train)
        return self.model
    
    def evaluate(self):
        y_pred = self.model.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        rmse = root_mean_squared_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)

        metrics = {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2": round(r2, 4)
        }
        print(f"\n---Model Evaluation({self.model_type})---")
        for k, v in metrics.items():
            print(f"{k}:{v}")

        return metrics

    def predict_student(self, study_hours, attendance, participation):
            if self.model is None:
                raise ValueError("Model is not trained yet. Call train() first.")

            feature_names = (
                self.X_train.columns 
                if self.X_train is not None 
                else getattr(self.model, "feature_names_in_", ['weekly_self_study_hours', 'attendance_percentage', 'class_participation']))
            input_data = pd.DataFrame([[study_hours, attendance, participation]], columns=feature_names)
        
            raw_score = float(self.model.predict(input_data)[0])

            score = max(0.0, min(100.0, round(raw_score, 1)))

            thresholds = [(85, "A"), (70, "B"), (55, "C"), (40, "D")]
            grade = next(filter(lambda t: score >= t[0], thresholds), (0, "F"))[1]

            return {
                "predicted_score": score,
                "predicted_grade": grade
            }
    
    def save_model(self, filepath=DEFAULT_MODEL_PATH):
        """Saves the trained model to disk so it doesn't need to be retrained."""
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath=DEFAULT_MODEL_PATH):
        """Loads a pre-trained model from disk in ~0.001 seconds."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No saved model found at {filepath}. Please train first.")
        
        self.model = joblib.load(filepath)
        print(f"Model loaded from {filepath}")
        return self.model