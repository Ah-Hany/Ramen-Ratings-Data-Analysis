import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df=pd.read_csv(r"C:\Users\Ahmed Hany\Downloads\ramen-ratings.csv")

#pd.set_option('display.max_rows',None)
#pd.set_option('display.max_columns',None)
#pd.set_option('display.width',None)
#print(df)
print(df.shape)
print(df.info())
print(df.describe(include='all').T)
print(df.nunique())
print(df['Brand'])
df.columns.str.strip()
df.columns=df.columns.str.strip().str.lower()

text_cols=['review #' ,'brand','variety','style','country','stars','top ten']

for i in text_cols:
    df[i]=df[i].astype(str).str.strip()
    df[i]=df[i].replace('nan',np.nan)
    df[i] = df[i].str.title()
print(df)

df['review #']=pd.to_numeric(df['review #'],errors='coerce').astype('int64')
df['stars']=pd.to_numeric(df['stars'],errors='coerce').astype('float')

df['stars']=df.groupby('brand')['stars'].transform(lambda X:X.fillna(X.median()))
df['stars']=df['stars'].fillna(df['stars'].median())
df=df.dropna(subset=['brand','country'])

dup_review=df[df.duplicated(subset=['review #'])]
df=df.drop_duplicates(subset=['review #'])

country_stats=df.groupby('country')['stars'].agg(['mean','count'])
top_stats=country_stats[country_stats['count']>10].sort_values(by='mean',ascending=False).head(10)

style_analysis = df.groupby('style')['stars'].agg(['mean','count']).sort_values(by='mean',ascending=False)

brands_stats= df.groupby('brand')['stars'].agg(['mean','count'])
top_brand=brands_stats[brands_stats['count']>5].sort_values(by='mean',ascending=False).head(10)

market_analysis = df.groupby('country').agg(AVg_Rating=('stars','mean'),Total_products=('brand','nunique'))

investment_opportunities = market_analysis[(market_analysis['AVg_Rating'] > 4) & (market_analysis['Total_products'] < 10)].sort_values(by='AVg_Rating',ascending=False)

brand_reliability = df.groupby('brand')['stars'].agg(['mean','std','count'])

Top_reliable_brands = brand_reliability[brand_reliability['count'] > 10].sort_values(by='std')

df['is_winner'] = df['top ten'].notna()

success_by_style= df.groupby('style')['is_winner'].mean() * 100

success_by_country= df.groupby('country')['is_winner'].mean() * 100


print(f"Dear Client, Here are the Top 10 Countries by Rating :\n {top_stats} ")
print(f"\n market Analysis - Best Investment Opportunities : \n {investment_opportunities}")
print(f"\n Product Packaging Insights (Style Analysis) : \n {style_analysis}")
print(f"\n Top 10 Performing Brands in the Market : \n {top_brand}")
print(f"\n Reliability Report - Most Consistent Brands (Low Std) : \n {Top_reliable_brands.head(10)}")
print(f"\n Success Rate for reaching 'Top Ten' by Country : \n {success_by_country.sort_values(ascending=False).head(10)}")


top_stats['mean'].plot(kind='bar',color='royalblue', figsize=(10,5))
plt.title('Top 10 Countries by Rating')
plt.ylabel('Average Stars')
plt.savefig('top_countries.png')
plt.show()


style_analysis['mean'].sort_values().plot(kind='barh',color='seagreen',figsize=(8,4))
plt.title('Best Packaging Styles')
plt.xlabel('Rating')
plt.savefig('packaging_styles.png')
plt.show()


market_analysis.plot(kind='scatter', x='Total_products',y='AVg_Rating', color='red',figsize=(10,6))
plt.title('Market saturation vs Quality')
plt.grid(True , linestyle='--',alpha=0.5)
plt.savefig('market_analysis.png')
plt.show()

