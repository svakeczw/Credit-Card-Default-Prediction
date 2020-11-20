import pandas as pd


data = pd.read_csv('data/UCI_Credit_Card.csv')
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 40)
pd.set_option('display.width', 1000)
data = data.drop(labels='ID', axis=1)


def norm(data):
    data = (data - data.mean()) / (data.max() - data.min())
    return data


def onehot_pay(data_col, data, i):
    data = data.join(pd.get_dummies(data_col, prefix='PAY_' + str(i)))
    return data


# Normalize data
data['LIMIT_BAL'] = norm(data['LIMIT_BAL'])
for i in range(11,23):
    data.iloc[:,i] = norm(data.iloc[:,i])

# Binning 'AGE'
data.loc[(data['AGE'] > 20) & (data['AGE'] < 30), 'AgeBin'] = 1
data.loc[(data['AGE'] >= 30) & (data['AGE'] < 40), 'AgeBin'] = 2
data.loc[(data['AGE'] >= 40) & (data['AGE'] < 50), 'AgeBin'] = 3
data.loc[(data['AGE'] >= 50) & (data['AGE'] < 60), 'AgeBin'] = 4
data.loc[(data['AGE'] >= 60) & (data['AGE'] < 70), 'AgeBin'] = 5
data.loc[(data['AGE'] >= 70), 'AgeBin'] = 6
data['AgeBin'] = pd.cut(data['AGE'], 6, labels=[1, 2, 3, 4, 5, 6])
data = data.drop(labels='AGE', axis=1)

# One-Hot data
for i in range(4, 10):
    j = i-3
    data = onehot_pay(data.iloc[:, i], data, j)
data = data.drop(labels=['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6'], axis=1)

data = data.join(pd.get_dummies(data.SEX, prefix='Sex'))
data = data.join(pd.get_dummies(data.EDUCATION, prefix='Education'))
data = data.join(pd.get_dummies(data.MARRIAGE, prefix='Marriage'))
data = data.join(pd.get_dummies(data.AgeBin, prefix='AgeBin'))

data = data.drop(labels=['SEX', 'EDUCATION', 'MARRIAGE', 'AgeBin'], axis=1)

order_li = data.columns.values

true_label = data['default.payment.next.month']
data = data.drop(labels='default.payment.next.month', axis=1)
data.insert(96, 'default.payment.next.month', true_label)

data.to_csv('data/credit_data.csv')
