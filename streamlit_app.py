import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

import matplotlib.font_manager as fm


#import platform
#from matplotlib import font_manager, rc
#plt.rcParams['axes.unicode_minus'] = False
#if platform.system() == 'Windows':
#    rc('font', family='NanumGothic')

@st.cache_data
def fontRegistered():
    fm.fontManager.addfont('fonts/IBMPlexSansKR-Text.ttf')
    fm._load_fontmanager(try_read_cache=False)
    plt.rc('font', family='IBM Plex Sans KR')


# 멀티 페이지용 제목
st.set_page_config(page_title='FestStay',
                   page_icon='🕍', layout="wide")

fontRegistered()


st.sidebar.header('축제데이터 분석!')
st.title('축제데이터 분석 페이지예요!')
st.title('')

fes = pd.read_csv('./data/festival_2023_or_합계확인_최종.csv')


fes_name_count=fes.groupby('시도명')['방문객수합계'].sum().sort_values(ascending=False)

fes_budget=fes.groupby('시도명')['예산합계'].sum().sort_values(ascending=False)


colors = sns.color_palette('hls', len(fes_budget))
fig, ax = plt.subplots(figsize=(10, 4))
fes_budget.plot.bar(stacked=True, color=colors, rot=0, fontsize=10, ax=ax)
#sns.barplot(x='시도명',data=fes_name_count, errwidth=False)
ax.set_xlabel('', fontsize=15)
ax.set_ylabel('축제 시도별 예산합계', fontsize=10)

ax.set_title('2022년 전국 축제 예산합계', fontsize=20, pad=15)
ax.legend(loc='upper left', fontsize=8)
ax.grid(visible=False)



st.pyplot(fig)



st.write('')
st.write('')
st.write('')
st.write('')
st.write('')

#plt.figure(figsize=(16,12))
#plt.xticks(fontsize=15)
#plt.yticks(fontsize=15)
#plt.title('2023년 지역별 축제 수', fontsize=30, pad=30)
#colors = sns.color_palette('hls',len(fes_name_counts))
#plt.bar(fes_sido_count, fes_name_counts, color = colors)
#for i in range(len(fes_name_counts)):
#    plt.text(fes_sido_count[i], fes_name_counts[i], fes_name_counts[i], ha='center', va='bottom', fontsize=15)
#plt.grid(visible=False)
#plt.tight_layout()

for i in range(len(fes_name_count)):
    fes_name_count[i] = fes_name_count[i] / 100






colors = sns.color_palette('hls', len(fes_name_count))
fig, ax = plt.subplots(figsize=(10, 4))
fes_name_count.plot.bar(stacked=True, color=colors, rot=0, fontsize=10, ax=ax)

ax.set_xlabel('', fontsize=1)
ax.set_ylabel('축제 시도별 방문객수합계', fontsize=10)

ax.set_title('2022년 전국 축제 방문객수합계 (단위:100명)', fontsize=20, pad=15)
ax.legend(loc='upper left', fontsize=15)
ax.grid(visible=False)



st.pyplot(fig)


fes = './data/recom_rest/fesJN23_순위_최최종.csv'

fesJ = pd.read_csv(fes)


fesJ_category = fesJ.축제종류.value_counts()
fesJ_categories = fesJ_category.index.tolist()


df = pd.read_csv('./data/fesJN2023_월별 축제종류 개최수.csv')


#pivot_df = df.pivot(index='월', columns='축제종류', values='개최수')
#pivot_df = pivot_df[['생태자연','문화예술','특산물','전통역사','기타(주민화합등)']].copy()
#pivot_df.info()

#colors = sns.color_palette('hls',len(fesJ_categories))
## pivot_df.plot.bar(stacked=True, figsize=(16,12), color=colors, rot=0, fontsize=15)
#fig = pivot_df.plot.bar(stacked=True, figsize=(16,12), color=colors, rot=0, fontsize=15, xlabel='월', ylabel='축제개최수')
#plt.title('2023년 전라남도 월별 축제 종류', fontsize=30, pad=30)
#plt.legend(loc='upper left', fontsize=20)
#plt.grid(visible=False)
#plt.tight_layout()


# Streamlit File *.py

st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')
pivot_df = df.pivot(index='월', columns='축제종류', values='개최수')
selected_categories = ['생태자연', '문화예술', '특산물', '전통역사', '기타(주민화합등)']

selected_categories = st.selectbox('',['생태자연','문화예술','특산물','전통역사','기타(주민화합등)'])
st.title(f'2023년 전라남도의 {selected_categories}축제는 이 정도 있어요!')
st.write('')
st.write('')
st.write('')
st.write('')
st.write('')

pivot_df = pivot_df[selected_categories].copy()

colors = sns.color_palette('hls', len(selected_categories))
fig, ax = plt.subplots(figsize=(10, 4))
pivot_df.plot.bar(stacked=True, color=colors, rot=0, fontsize=10, ax=ax)
ax.set_xlabel('월', fontsize=15)
ax.set_ylabel('축제 개최 수', fontsize=15)
ax.set_title('2023년 전라남도 월별 축제 종류', fontsize=20, pad=15)
ax.legend(loc='upper left', fontsize=8)
ax.grid(visible=False)


st.pyplot(fig)
