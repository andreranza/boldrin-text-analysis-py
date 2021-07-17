import pandas as pd

# load data
df = pd.read_csv('data/boldrin-df.csv')

# informations
print(df)
print(df.info())
print(df.shape)
print(df.head())
print(df.iloc[:9])

# select
print(df[['video_id', 'views', 'comments']])
print(df.loc[:, 'views':'comments'])

# select and filter
print(df[['video_id', 'views', 'comments']].query('views > 10000 & comments > 200'))
print(df.loc[(df['views'] > 10000) & (df['comments'] > 200), ['video_id', 'views', 'comments']])

# drop column
print('Drop column "language"')
print(df.drop('language', axis = 1))
to_drop = ['language', 'definition']
print(df.drop(to_drop, axis = 1))

# drop duplicates
print(df[['video_id']].drop_duplicates())

# sample
print(df.sample(n = 3))
print(df.sample(frac = 0.01))

# arrange
print(df[['video_id', 'views']].sort_values('views', ascending = False))

# rename
print(df[['video_id', 'views']].rename(columns = {'views' : 'n_views'}))

# mutate
print(df[['video_id', 'views']].assign(views = df['views']*1000))
print(df[['video_id', 'views', 'likes']].assign(ratio = df['likes']/df['views']*100))

# summary
print(df.describe())

# group_by
grouped = df.groupby(by = 'definition')
print(grouped.sum())
print(grouped.agg({'definition' : 'count'}))


# method chaining
print(df[['video_id', 'views', 'comments']].query('views > 10000 & comments > 200'))

df2 = (df.rename(columns = {'views' : 'n_views'})
         .rename(columns = {'comments' : 'n_comments'})
         .query('n_views > 2000')
         .drop('language', axis = 1)
         .loc[:, 'n_views':'n_comments']
         )

print(df2)
