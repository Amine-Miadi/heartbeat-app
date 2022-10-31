
df = pd.read_csv('echocardiogram.data', sep=",", header=None)
df.columns = ["survival", "still-alive", "age-at-heart-attack", "pericardial-effusion", "fractional-shortening",
            "epss", "lvdd", "wall-motion-score", "wall-motion-index", "mult", "name", "group", "alive-at-1"]
            
df.replace('?', np.nan, inplace=True)
df.head()   

df.columns[df.isna().any()].tolist()


df.drop(['alive-at-1', 'mult', 'group', 'name','wall-motion-score'], axis = 1, inplace = True)
df.columns


for column in df:
    df[column] = pd.to_numeric(df[column])

df.info()

print(df)