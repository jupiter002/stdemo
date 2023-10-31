import pandas as pd
import streamlit as st
import plotly.express as px

import json
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
# pip install folium
# pip install streamlit_folium


# 멀티 페이지용 제목

st.set_page_config(page_title='FestStay',
                   page_icon='🕍', layout="wide")

st.sidebar.header('당신이 원하는 축제와 숙소를 골라보세요!')
st.title('페스트스테이FestStay')
st.title('')

# 검색한 축제명으로 위도/경도/축제명/시군구명/개최장소 불러오기
def getfesdot(fesname):
    fes = pd.read_csv('./data/recom_rest/fesJN23_순위_최최종.csv')
    find = fes['축제명'] == fesname
    idx = fes[find]['좌표'].index

    x = float(fes[find]['좌표'][idx[0]].split(',')[0])
    y = float(fes[find]['좌표'][idx[0]].split(',')[1])
    name = fes[find]['축제명'][idx[0]]
    si = fes[find]['시군구명'][idx[0]]
    place = fes[find]['개최장소 '][idx[0]]
    return x,y,name, si, place
# getfesdot('구례산수유꽃축제')


# 숙소와 축제장소의 거리계산
def getdistance(fesname):
    idx = []  # 숙소의 인덱스를 담을 리스트 선언
    for i in range(len(dist_csv)):
        try:
            distance = int(dist_csv.loc[i,fesname])/1000
            print(distance)

            # 축제로부터 떨어진 숙소의 거리를 슬라이더로 지정
            # 지정한 값 이하인 거리에 해당하는 숙소만 저장
            if distance <= slider1:
                print(data[i]['좌표'], data[i]['모텔명'])
                print(distance)
                idx.append(i)
        except Exception as e:
            pass

    # 원하는 거리만큼 떨어진 숙소데이터의 인덱스 리스트 반환
    return idx
# getdistance('구례산수유꽃축제')


# 축제 csv파일 불러옴
fes = pd.read_csv('./data/recom_rest/fesJN23_순위_최최종.csv')



# 축제좌표를 지도에 뿌림
st.subheader('🎆축제 위치🎆')
fig = px.scatter_mapbox(fes, lat='위도', lon='경도', size='예산합계', color='방문객수합계',
                        color_continuous_scale= px.colors.sequential.RdBu,
                        mapbox_style='open-street-map',
                        hover_name= '축제명', hover_data={'위도':False, '경도':False, '축제명':True},
                        opacity=0.9)
fig.update_layout(mapbox_zoom=7.5, width=800, height=600,
                  mapbox_center={"lat": 34.82725246807052, "lon": 126.82132640120547})
st.plotly_chart(fig)

# 월별 선택
month = st.selectbox("📅축제가 열리는 달을 선택해주세요", ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"])
smonth = 1 if month=='1월' else 2 if month=='2월' else 3 if month=='3월' else \
    4 if month=='4월' else 5 if month=='5월' else 6 if month=='6월' else \
        7 if month=='7월' else 8 if month=='8월' else 9 if month=='9월' else \
            10 if month=='10월' else 11 if month=='11월' else 12

st.subheader('🎆축제리스트🎆')
# 선택한 '월'을 조건에 넣기
findm = fes['시작월'] == smonth
fes1 = pd.DataFrame(fes[findm],
                    columns=['시군구명','축제명','축제종류',' 개최방식',
                             '기간','개최주소'])
st.dataframe(fes1)


fesname=st.text_input("🔍축제명을 검색해주세요")
st.write('입력내용:', fesname)

st.write('')

st.write('🚗원하는 거리의 범위를 선택해주세요')
slider1=st.slider('단위(Km)', 0, 100)

st.write('')

select2=st.selectbox("🏡모텔, 펜션중에 선택해주세요", ["모텔", "펜션"])

ps = './data/recom_rest/ps_list_last.json'
mt = './data/recom_rest/motel_list_last (1).json'



# 모텔을 선택할시
if select2 == '모텔':
    with open(mt, 'r', encoding='utf-8') as f:
        rest = f.read()
    rest_csv = pd.read_csv('./data/recom_rest/motel_list_last (1).csv')
    dist_csv = pd.read_csv('./data/recom_rest/festival_to_motel.csv')
    df2 = pd.read_csv('./data/recom_rest/모텔_list_추천여부최종최종2.csv')

# 펜션을 선택할시
else:
    with open(ps, 'r', encoding='utf-8') as f:
        rest = f.read()
    rest_csv = pd.read_csv('./data/recom_rest/ps_list_last.csv')
    dist_csv = pd.read_csv('./data/recom_rest/festival_to_pension.csv')
    df2 = pd.read_csv('./data/recom_rest/펜션_list_추천여부최종최종2.csv')

data = json.loads(rest)

df = pd.DataFrame()



#getfesdot('거문도백도은빛바다체험행사')
#getdistance('거문도백도은빛바다체험행사')

a = []
try:
    # 검색한 축제의 좌표를 지도 중앙으로 하기 위해서 가져옴
    lat, lon, name, si, place = getfesdot(fesname)

    a = getdistance(fesname)
    # 검색한 축제 근처의 숙소들을 지도에 보여줌

    for idx in a:
        df = df._append(rest_csv.loc[idx], ignore_index=True)

    # 컬럼 설정
    left_column, right_column = st.columns(2)

    # 지도 출력 (left_column에 배치)
    with left_column:
        st.subheader('🌏축제 및 숙소 위치🌏')
        # Folium 지도 생성
        m = folium.Map(location=[lat, lon], zoom_start=10.5)

        # 숙소 마커들을 클러스터로 그룹화
        marker_cluster = MarkerCluster().add_to(m)

        # 숙소별 이름, 좌표 가져오기
        for _, row in df.iterrows():
            motel_name = row['모텔명']
            motel_addr = row['주소']
            motel_lat = float(row['좌표/위도'])
            motel_lon = float(row['좌표/경도'])

            # 숙소 마커 추가
            folium.Marker([motel_lat, motel_lon], tooltip=f'{motel_name}, {motel_addr}', icon=folium.Icon(color='blue')).add_to(marker_cluster)

        # 중심 마커 추가
        folium.Marker([lat, lon], tooltip=name, icon=folium.Icon(color='red')).add_to(m)

        folium_static(m)
        # 범례 추가
        # folium.LayerControl().add_to(m)


    # 두 데이터프레임을 모텔명을 기준으로 병합합니다.
    merged_df = pd.merge(df, df2, on='모텔명')

    # 데이터프레임 출력 (right_column에 배치)
    with right_column:
        # 모텔 선택시
        if select2 == '모텔':
            option1 = st.radio("", ['추천순', '친절도순', '청결도순', '편의성순', '비품만족도순'])
            opt = '전체평점_x' if option1 == '추천순' else \
                '평점순/친절도순_x' if option1 == '친절도순' else \
                    '평점순/청결도순_x' if option1 == '청결도순' else \
                        '평점순/편의성순_x' if option1 == '편의성순' else \
                            '평점순/비품만족도순_x'
        # 펜션 선택시
        else:
            option1 = st.radio("", ['추천순', '친절도순', '청결도순', '편의성순', '주변여행순'])
            opt = '전체평점_x' if option1 == '추천순' else \
                '평점순/친절도순_x' if option1 == '친절도순' else \
                    '평점순/청결도순_x' if option1 == '청결도순' else \
                        '평점순/편의성순_x' if option1 == '편의성순' else \
                            '평점순/주변여행순_x'


        # '추천여부_최종'을 기준으로 내림차순 정렬, 그 다음 '평점'을 큰 순서대로 정렬
        sorted_df = merged_df.sort_values(by=['추천여부_최종2', opt], ascending=[False, False])
        # '추천여부_최종'이 '비추천'이 아닌 것만 담기
        sorted_df = sorted_df[sorted_df['추천여부_최종2'] != 1]

        # st.write('🏠숙소 리스트🏠')
        st.subheader('🏠숙소 리스트🏠')
        showdf = sorted_df[['모텔명', '주소_x', '전체평점_x']]  # '모텔명', '주소', '전체평점'만 담기

        # 열이름 변경
        showdf = showdf.rename(columns={'모텔명': '숙소명', '주소_x': '주소', '전체평점_x': '전체평점'})

        st.write(showdf)

except Exception as e:
    

    if fesname == '':
        st.warning('축제명이 입력되지 않았습니다😢')
    elif 'name' not in globals():
        st.error('검색하신 축제명을 다시 확인해주세요😯')
    elif name and (slider1 == 0 or len(a) == 0):
        st.error('축제장소에서 숙소까지의 원하는 거리를 선택해주세요😊')

    print(e)
