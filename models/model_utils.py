from xgboost import XGBRegressor

def train_model(df):
    features = ['energy_production']
    target = 'renewables_percentage'

    X = df[features]
    y = df[target]

    # Train the model
    model = XGBRegressor()
    model.fit(X, y)
    
    return model
