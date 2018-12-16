import pandas as pd

def get_binary_from_raw(filename: str = 'btc'):
    df = pd.read_csv(f'../dataset/raw/{filename}.csv')
    df['difference'] = df['Close Price'].shift(-1) - df['Close Price']
    df.loc[df['difference'] > 0, 'binary'] = 1
    df.loc[df['difference'] <= 0, 'binary'] = 0
    df = df.loc[:df.shape[0]-2]
    df['binary'] = df['binary'].astype(int)

    # print(df)
    # print(df.columns)
    # print(list(df['binary']))
    return list(df['binary'])


def get_normal_random_dataset(size=1000):
    import numpy as np
    dataset = np.random.choice([0, 1], size=(size,), p=[1./2, 1./2])
    return dataset

def get_static_dataset():
    dataset = [0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,]
    print(dataset)
    return dataset
