import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


years = list(map(str,range(1980,2014)))
# loading data 
@st.cache_data
def load_data():
   df = pd.read_excel('Canada.xlsx', sheet_name=1 ,skiprows=20 ,skipfooter=2)
   cols_to_rename = {
    'OdName':'country',
    'AreaName':'continent',
    'RegName' : 'region',
    'DevName'  : 'development'
    }
   df= df.rename(columns=cols_to_rename)
   cols_to_drop = ['AREA','Type','Coverage']
   df =df.drop(columns=cols_to_drop)
   df = df.set_index('country')
   df.columns = [str(name).lower() for name in df.columns.tolist()]
   df['total']= df[years].sum(axis=1)
   df = df.sort_values(by='total',ascending=False)
   return df


#configure the layout 
st.set_page_config(
   layout='wide',
   page_title=' Immigration data Analysis',
   page_icon='📊'
)

#loading the data 
with st.spinner("loading data...."):
  df = load_data()
  st.sidebar.success("data loaded sucessfully")

# creating the interface
c1,c2,c3 = st.columns(3)
c1.title("immigration Analysis")
c2.header("summary of data")
total_row = df.shape[0]
total_imig =df.total.sum()
max_imig = df.total.max()
max_imig_country =df.total.idxmax()
c2.metric("total country",total_row)
c2.metric("totalyear",len(years))
c2.metric("total imigration",f"{total_imig/1000000:.2f}M")
c2.metric("max imigration",f"{max_imig/1000000:.2f}M",
          f"{max_imig_country}")
c3.header("Top 10 country")
top_10 =df.head(10)
c3.dataframe(top_10,use_container_width=True)
fig = px.bar(top_10,x=top_10.index, y='total')
c3.plotly_chart(fig,use_container_width=True)

#country wise visualization 
countries =df.index.tolist()
country =c1.selectbox("select a country",countries)
imig =df.loc[country,years]
fig =px.area(imig,x=imig.index,y=imig.values,
             title ="imigration trend")
c1.plotly_chart(fig,use_container_width=True)
fig2 =px.histogram(imig ,x=imig.values,nbins=10,marginal="box")

max_imig_country=imig.max()
max_year=imig.idxmax()
c2.metric(f"max imigration for{country}",
          f"{max_imig_country/1000000:.2f}K",
          f"{max_year}")
c1, c2 =st.columns(2)
c1.plotly_chart(fig2,use_container_width=True)
c2.plotly_chart(fig2,use_container_width=True)
st.header("Continent wise analysis")
c1,c2,c3 = st.columns(3)
continents =df['continent'].unique().tolist()
cdf =df.groupby('continent')[years].sum()
cdf['total']=cdf.sum(axis=1)
c1.dataframe(cdf,use_container_width=True)
figcontinent =px.bar(cdf, x=cdf.index, y ='total',
                         title="Total imigration by continent")
c2.plotly_chart(figcontinent,use_container_width=True)

figMap = px.choropleth(df,
                       locations=df.index,
                       locationmode='country names',
                       color='total',
                       title='World map',
                       projection='natural earth',
                       width=1000,height=700,
                       template='plotly',)
st.plotly_chart(figMap,use_container_width=True)