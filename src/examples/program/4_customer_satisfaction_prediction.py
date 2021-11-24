""" Customer Satisfaction. Based on https://www.kaggle.com/yuansun/lb-0-84-for-starters """ 

from os import path

def run(data_folder, **kwargs):

    cross_validation = kwargs.get('cross_validation')
    metrics = kwargs.get('metrics')
    np = kwargs.get('numpy')
    pd = kwargs.get('pandas')
    xgb = kwargs.get('xgboost')
    train_test_split = cross_validation.train_test_split
    roc_auc_score = metrics.roc_auc_score
    
    # load data
    df_train = pd.read_csv(path.join(data_folder, 'train/data.csv'), schema=['ID', 'var3', 'var15', 'TARGET'])

    y_train = df_train['TARGET'].values
    X_train = df_train.drop(['ID','TARGET'], axis=1).values

    # classifier
    clf = xgb.XGBClassifier(missing=np.nan, max_depth=5, n_estimators=350, learning_rate=0.03, nthread=4, subsample=0.95, colsample_bytree=0.85, seed=4242)

    X_fit, X_eval, y_fit, y_eval= cross_validation.train_test_split(X_train, y_train, test_size=0.3)

    # fitting
    clf.fit(X_train, y_train, early_stopping_rounds=20, eval_metric="auc", eval_set=[(X_eval, y_eval)])

    return metrics.roc_auc_score(y_train, clf.predict_proba(X_train)[:,1])
