# This script is based on the content from: 
# 1. https://www.kaggle.com/dott1718/922-in-3-minutes by @dott1718
# 2. https://www.kaggle.com/titericz/giba-single-model-public-0-9245-private-0-9234
# 3. https://www.kaggle.com/nawidsayed/lightgbm-and-cnn-3rd-place-solution

def run(data_folder, **kwargs):

    np = kwargs.get('numpy')
    pd = kwargs.get('pandas')
    lgb = kwargs.get('lightgbm')
    scipy = kwargs.get('scipy')

    train_df = pd.read_csv(data_folder + 'train/data.csv')

    features = train_df[[x for x in train_df.columns if x.startswith("var")]]
    target = train_df["target"]

    model = lgb.LGBMClassifier(**{ 'learning_rate':0.06, 'max_bin': 165, 'max_depth': 5, 'min_child_samples': 153,
            'min_child_weight': 0.1, 'min_split_gain': 0.0018, 'n_estimators': 41, 'num_leaves': 6, 'reg_alpha': 2.1,
            'reg_lambda': 2.54, 'objective': 'binary', 'n_jobs': -1})
        
    model = model.fit(features.values, target.values)

    return model
