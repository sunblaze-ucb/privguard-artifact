from os import path

def run(data_folder, **kwargs):

    lgb = kwargs.get('lightgbm')
    metrics = kwargs.get('metrics')
    model_selection = kwargs.get('model_selection')
    np = kwargs.get('numpy')
    pd = kwargs.get('pandas')
    random = kwargs.get('random')
    roc_auc_score = metrics.roc_auc_score
    KFold = model_selection.KFold

    train = pd.read_csv(path.join(data_folder, 'train/data.csv'))
    test = pd.read_csv(path.join(data_folder, 'test/data.csv'))

    features = [c for c in train.columns if c not in ['ID_code', 'target']]

    target = train['target']
    train = train.drop(["ID_code", "target"], axis=1)

    def augment(x,y,t=2):
        xs,xn = [],[]
        for i in range(t):
            mask = y > 0
            x1 = x[mask].copy()
            ids = np.arange(x1.shape[0])
            for c in range(train.shape[1]):
                np.random.shuffle(ids)
                x1[:,c] = x1[ids][:,c]
            xs.append(x1)

        for i in range(t//2):
            mask = y==0
            x1 = x[mask].copy()
            ids = np.arange(x1.shape[0])
            for c in range(train.shape[1]):
                np.random.shuffle(ids)
                x1[:,c] = x1[ids][:,c]
            xn.append(x1)

        xs = np.vstack(xs)
        xn = np.vstack(xn)
        ys = np.ones(xs.shape[0])
        yn = np.zeros(xn.shape[0])
        x = np.vstack([x,xs,xn])
        y = np.concatenate([y,ys,yn])
        return x,y

    param = {
        'bagging_freq': 5,
        'bagging_fraction': 0.335,
        'boost_from_average':'false',
        'boost': 'gbdt',
        'feature_fraction': 0.041,
        'learning_rate': 0.0083,
        'max_depth': -1,
        'metric':'auc',
        'min_data_in_leaf': 80,
        'min_sum_hessian_in_leaf': 10.0,
        'num_leaves': 13,
        'num_threads': 8,
        'tree_learner': 'serial',
        'objective': 'binary', 
        'verbosity': -1
    }

    num_folds = 11
    features = [c for c in train.columns if c not in ['ID_code', 'target']]

    folds = KFold(n_splits=num_folds, random_state=2319)
    oof = np.zeros(train.shape[0])
    predictions = np.zeros(target.shape[0])

    folds.split(train.values, target.values)

    for fold_, (trn_idx, val_idx) in enumerate(folds.split(train.values, target.values)):  
        X_train, y_train = train.iloc[trn_idx][features], target.iloc[trn_idx]
        X_valid, y_valid = train.iloc[val_idx][features], target.iloc[val_idx] 
        X_tr, y_tr = augment(X_train.values, y_train.values)
        X_tr = pd.DataFrame(data=X_tr)
        print("Fold idx:{}".format(fold_ + 1))
        trn_data = lgb.Dataset(X_tr, label=y_tr)
        val_data = lgb.Dataset(X_valid, label=y_valid)
        clf = lgb.train(param, trn_data, 1000000, valid_sets = [trn_data, val_data], verbose_eval=5000, early_stopping_rounds = 4000)
        oof[val_idx] = clf.predict(train.iloc[val_idx][features], num_iteration=clf.best_iteration) 
        predictions += clf.predict(test[features], num_iteration=clf.best_iteration) / folds.n_splits
    return roc_auc_score(target, oof)
