import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class PredictiveMaintenanceAI:
    def __init__(self, model_path="panel_rf_model.pkl"):
        self.model_path = model_path
        # Initialize an industry-standard Random Forest model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.load_model()

    def load_model(self):
        """Attempts to load a pre-trained model from disk."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            print("🧠 AI Engine: Pre-trained Random Forest model loaded successfully.")
        else:
            print("🧠 AI Engine: No existing model found. Ready for training initialization.")

    def generate_synthetic_training_data(self):
        """
        Generates standard power systems behavioral datasets based on 
        ETAP parameters to train your AI model initially before field deployment.
        """
        print("🧠 AI Engine: Synthesizing baseline machine learning datasets...")
        np.random.seed(42)
        n_samples = 1000
        
        data = []
        for _ in range(n_samples):
            # Pick a random scenario to train on
            scenario = np.random.choice([0, 1, 2, 3], p=[0.7, 0.1, 0.1, 0.1])
            
            if scenario == 0: # NORMAL OPERATING MODE
                v_avg = np.random.uniform(215, 230)
                v_unbalance = np.random.uniform(0.1, 1.5)
                c_max = np.random.uniform(5, 15)
                pf = np.random.uniform(0.85, 0.98)
                thd = np.random.uniform(1.0, 4.0)
                temp = np.random.uniform(25, 45)
                label = 0
                
            elif scenario == 1: # OVERLOAD FAULT
                v_avg = np.random.uniform(200, 215) # Voltage drops slightly during overload
                v_unbalance = np.random.uniform(0.5, 2.0)
                c_max = np.random.uniform(32, 45)  # Heavy overcurrent trip territory
                pf = np.random.uniform(0.70, 0.84)
                thd = np.random.uniform(3.0, 7.0)
                temp = np.random.uniform(45, 58)
                label = 1
                
            elif scenario == 2: # PHASE UNBALANCE FAULT
                v_avg = np.random.uniform(210, 225)
                v_unbalance = np.random.uniform(5.5, 12.0) # High unbalance percent
                c_max = np.random.uniform(10, 25)
                pf = np.random.uniform(0.80, 0.90)
                thd = np.random.uniform(2.0, 5.0)
                temp = np.random.uniform(30, 48)
                label = 2
                
            else: # CRITICAL THERMAL OVERHEATING
                v_avg = np.random.uniform(215, 230)
                v_unbalance = np.random.uniform(0.1, 1.5)
                c_max = np.random.uniform(10, 20) # Normal current, but loose contact terminal
                pf = np.random.uniform(0.85, 0.95)
                thd = np.random.uniform(2.0, 6.0)
                temp = np.random.uniform(62, 85) # Extreme hotspot signature
                label = 3
                
            data.append([v_avg, v_unbalance, c_max, pf, thd, temp, label])
            
        columns = ['v_avg', 'v_unbalance', 'c_max', 'power_factor', 'thd', 'temperature', 'label']
        df = pd.DataFrame(data, columns=columns)
        
        # Split into training features and targets
        X = df.drop(columns=['label'])
        y = df['label']
        
        # Train the model
        self.model.fit(X, y)
        self.is_trained = True
        joblib.dump(self.model, self.model_path)
        print("🎉 Model trained successfully on baseline datasets and saved as panel_rf_model.pkl!")

    def predict_status(self, v_avg, v_unbalance, c_max, power_factor, thd, temperature):
        """
        Accepts real-time extracted features and classifies panel health state.
        """
        if not self.is_trained:
            self.generate_synthetic_training_data()
            
        # Format metrics as an input array for the estimator
        features = np.array([[v_avg, v_unbalance, c_max, power_factor, thd, temperature]])
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        confidence = float(np.max(probabilities) * 100)
        
        status_map = {
            0: "Normal Operation",
            1: "Overload Fault Detected",
            2: "Phase Unbalance Tripped",
            3: "Critical Hotspot Overheating"
        }
        
        return status_map.get(prediction, "Unknown Status"), confidence