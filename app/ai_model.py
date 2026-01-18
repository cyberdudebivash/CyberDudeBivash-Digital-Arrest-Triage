import numpy as np
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
X = np.array([[0, 0], [1, 1], [2, 3], [3, 5]])
y = np.array([0, 0, 1, 1])
model.fit(X, y)

def calculate_risk_score(indicators: list[str]) -> float:
    num_indicators = len(indicators)
    features = np.array([[num_indicators, num_indicators * 1.5]])
    prob = model.predict_proba(features)[0][1]
    return round(prob * 100, 2)

# © 2026 CyberDudeBivash Pvt. Ltd.