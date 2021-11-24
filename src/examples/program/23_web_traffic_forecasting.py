""" Web Traffic Forecasting. """

from os import path
import re

def run(data_folder, **kwargs):

    # Load the libraries.
    np = kwargs.get('numpy')
    pd = kwargs.get('pandas')
    arm = kwargs.get('arima')

    train = pd.read_csv(path.join(data_folder, 'data.csv')).fillna(0)

    def get_language(page):
        res = re.search('[a-z][a-z].wikipedia.org',page)
        if res:
            return res[0][0:2]
        return 'na'

    train['lang'] = train.Page.map(get_language)

    lang_sets = {}
    lang_sets['en'] = train[train.lang=='en'].iloc[:,0:-1]
    lang_sets['ja'] = train[train.lang=='ja'].iloc[:,0:-1]
    lang_sets['de'] = train[train.lang=='de'].iloc[:,0:-1]
    lang_sets['na'] = train[train.lang=='na'].iloc[:,0:-1]
    lang_sets['fr'] = train[train.lang=='fr'].iloc[:,0:-1]
    lang_sets['zh'] = train[train.lang=='zh'].iloc[:,0:-1]
    lang_sets['ru'] = train[train.lang=='ru'].iloc[:,0:-1]
    lang_sets['es'] = train[train.lang=='es'].iloc[:,0:-1]

    sums = {}
    for key in lang_sets:
        sums[key] = lang_sets[key].iloc[:,1:].sum(axis=0) / lang_sets[key].shape[0]

    # Top Pages
    top_pages = {}
    for key in lang_sets:
        sum_set = lang_sets[key][['Page']]
        sum_set['total'] = lang_sets[key].sum(axis=1)
        sum_set = sum_set.sort_values('total',ascending=False)
        top_pages[key] = sum_set.index[0]

    # ARIMA
    cols = train.columns[1:-1]
    model_list = []
    for key in top_pages:
        data = np.array(train.loc[top_pages[key],cols],'f')
        arima = arm.ARIMA(data,[2,1,4])
        model_list.append(arima.fit(disp=False))

    return model_list
        
