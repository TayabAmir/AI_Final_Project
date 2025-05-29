import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data(file_path):
    """Load and preprocess the social media addiction dataset"""
    df = pd.read_csv(file_path)
    
    print("Dataset shape:", df.shape)
    print("\nDataset info:")
    print(df.info())
    print("\nFirst few rows:")
    print(df.head())
    
    le_gender = LabelEncoder()
    le_academic = LabelEncoder()
    le_country = LabelEncoder()
    le_platform = LabelEncoder()
    le_affects = LabelEncoder()
    
    df_processed = df.copy()
    df_processed['Gender'] = le_gender.fit_transform(df['Gender'])
    df_processed['Academic_Level'] = le_academic.fit_transform(df['Academic_Level'])
    df_processed['Country'] = le_country.fit_transform(df['Country'])
    df_processed['Most_Used_Platform'] = le_platform.fit_transform(df['Most_Used_Platform'])
    df_processed['Affects_Academic_Performance'] = le_affects.fit_transform(df['Affects_Academic_Performance'])
    
    encoders = {
        'gender': le_gender,
        'academic': le_academic,
        'country': le_country,
        'platform': le_platform,
        'affects': le_affects
    }
    
    return df_processed, encoders

def train_models(X_train, X_test, y_train, y_test):
    """Train all 5 models and evaluate their performance"""
    
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'KNN': KNeighborsRegressor(n_neighbors=5),
        'SVM': SVR(kernel='rbf', C=1.0, gamma='scale'),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    results = {}
    trained_models = {}
    
    print("Training and evaluating models...")
    print("="*60)
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Use scaled data for SVM and KNN, original data for others
        if name in ['SVM', 'KNN']:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            # Cross validation on scaled data
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            # Cross validation on original data
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()
        
        results[name] = {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'R2_Score': r2,
            'CV_Mean': cv_mean,
            'CV_Std': cv_std,
            'Accuracy_Percentage': max(0, r2 * 100) 
        }
        
        trained_models[name] = model
        
        print(f"Results for {name}:")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  MAE: {mae:.4f}")
        print(f"  R² Score: {r2:.4f}")
        print(f"  Accuracy: {max(0, r2 * 100):.2f}%")
        print(f"  CV Score: {cv_mean:.4f} (±{cv_std:.4f})")
    
    return results, trained_models, scaler

def find_best_model(results):
    """Find the best performing model based on R² score"""
    best_model_name = max(results.keys(), key=lambda x: results[x]['R2_Score'])
    return best_model_name, results[best_model_name]

def save_best_model(best_model_name, trained_models, scaler, encoders):
    """Save the best model and preprocessing objects"""
    best_model = trained_models[best_model_name]
    
    model_package = {
        'model': best_model,
        'model_name': best_model_name,
        'scaler': scaler if best_model_name in ['SVM', 'KNN'] else None,
        'encoders': encoders,
        'feature_names': ['Age', 'Gender', 'Academic_Level', 'Country', 'Avg_Daily_Usage_Hours',
                         'Most_Used_Platform', 'Affects_Academic_Performance', 'Sleep_Hours_Per_Night',
                         'Mental_Health_Score', 'Conflicts_Over_Social_Media']
    }
    
    joblib.dump(model_package, 'best_addiction_model.pkl')
    print(f"\nBest model '{best_model_name}' saved as 'best_addiction_model.pkl'")
    
    return model_package

def main():
    """Main function to run the entire pipeline"""
    
    print("Loading and preprocessing data...")
    df, encoders = load_and_preprocess_data('Students_Social_Media_Addiction.csv')
    
    feature_columns = ['Age', 'Gender', 'Academic_Level', 'Country', 'Avg_Daily_Usage_Hours',
                      'Most_Used_Platform', 'Affects_Academic_Performance', 'Sleep_Hours_Per_Night',
                      'Mental_Health_Score', 'Conflicts_Over_Social_Media']
    
    X = df[feature_columns]
    y = df['Addicted_Score']
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"Target range: {y.min()} to {y.max()}")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    
    results, trained_models, scaler = train_models(X_train, X_test, y_train, y_test)
    
    print("\n" + "="*60)
    print("MODEL COMPARISON SUMMARY")
    print("="*60)
    
    for name, metrics in results.items():
        print(f"{name:20} | R²: {metrics['R2_Score']:.4f} | RMSE: {metrics['RMSE']:.4f} | Accuracy: {metrics['Accuracy_Percentage']:.2f}%")
    
    best_model_name, best_metrics = find_best_model(results)
    
    print(f"\n🏆 BEST MODEL: {best_model_name}")
    print(f"   R² Score: {best_metrics['R2_Score']:.4f}")
    print(f"   RMSE: {best_metrics['RMSE']:.4f}")
    print(f"   Accuracy: {best_metrics['Accuracy_Percentage']:.2f}%")
    print(f"   Cross-validation: {best_metrics['CV_Mean']:.4f} (±{best_metrics['CV_Std']:.4f})")
    
    model_package = save_best_model(best_model_name, trained_models, scaler, encoders)
    
    print("\n" + "="*60)
    print("TESTING SAVED MODEL")
    print("="*60)
    
    loaded_model_package = joblib.load('best_addiction_model.pkl')
    print(f"Successfully loaded model: {loaded_model_package['model_name']}")
    
    sample_data = X_test.iloc[0:1]  
    actual_value = y_test.iloc[0]
    
    if loaded_model_package['scaler'] is not None:
        sample_scaled = loaded_model_package['scaler'].transform(sample_data)
        prediction = loaded_model_package['model'].predict(sample_scaled)[0]
    else:
        prediction = loaded_model_package['model'].predict(sample_data)[0]
    
    print(f"\nSample prediction test:")
    print(f"Actual Addiction Score: {actual_value}")
    print(f"Predicted Addiction Score: {prediction:.2f}")
    print(f"Difference: {abs(actual_value - prediction):.2f}")
    
    return model_package, results

if __name__ == "__main__":
    model_package, results = main()