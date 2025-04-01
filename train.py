import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
import itertools

data = {
    "mood": [3, 7, 5, 2, 8, 4, 6, 1, 3, 5],
    "sleepQuality": ["disturbed", "adequate", "irregular", "disturbed", "restful", "irregular", "adequate", "disturbed", "restful", "adequate"],
    "hobbies": ["yes", "no", "yes", "yes", "no", "yes", "no", "yes", "no", "yes"],
    "social": ["no", "yes", "no", "no", "yes", "no", "yes", "no", "yes", "yes"],
    "focus": ["yes", "no", "yes", "yes", "no", "yes", "no", "yes", "no", "yes"],
    "stressLevel": ["high", "low", "moderate", "high", "low", "moderate", "high", "low", "moderate", "high"],
    "recentChanges": ["yes", "no", "yes", "no", "yes", "no", "yes", "no", "yes", "no"],
    "mentalHealthCategory": ["Anxiety", "Depression", "Stress", "PTSD", "Depression", "Anxiety", "Stress", "PTSD", "Depression", "Anxiety"]
}

df = pd.DataFrame(data)

df.replace({"yes": 1, "no": 0, "high": 2, "moderate": 1, "low": 0, "disturbed": 2, "irregular": 1, "adequate": 0, "restful": 0}, inplace=True)

possible_values = {
    "mood": range(1, 11),
    "sleepQuality": [0, 1, 2],
    "hobbies": [0, 1],
    "social": [0, 1],
    "focus": [0, 1],
    "stressLevel": [0, 1, 2],
    "recentChanges": [0, 1],
    "mentalHealthCategory": ["Anxiety", "Depression", "Stress", "PTSD"]
}

combinations = list(itertools.product(*[possible_values[col] for col in possible_values.keys()]))

expanded_df = pd.DataFrame(combinations, columns=possible_values.keys())

X = expanded_df.drop("mentalHealthCategory", axis=1)
y = expanded_df["mentalHealthCategory"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

with open("mental_health_model.pkl", "wb") as f:
    pickle.dump(clf, f)
