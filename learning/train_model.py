from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np
import joblib
from learning.dataset import load_dataset

MODEL_PATH = "learning/models/card_policy_500iter_v1.pkl"

def main():
    print("Loading dataset")
    X, y = load_dataset()
    print(f"Dataset size: {len(X)}")

    print("Unique targets (first 20):", np.unique(y)[:20])
    print("Target count:", len(np.unique(y)))

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, 
        y,
        test_size=100_000,
        random_state=18,
        stratify=y
    )

    print("Training model")
    model = LogisticRegression(
        max_iter=500,
        n_jobs=-1,
        multi_class="multinomial",
        solver="lbfgs",
        verbose=1
    )

    
    lengths = {len(x) for x in X}
    print(lengths)
    
    model.fit(X_train, Y_train)

    print("Evaluating")
    preds = model.predict(X_test)
    acc = accuracy_score(Y_test, preds)

    print(f"Accuracy: {acc:.4f}")
    print("Saving model")
    
    joblib.dump(model, MODEL_PATH)
    
    print("Done")

if __name__ == "__main__":
    main()