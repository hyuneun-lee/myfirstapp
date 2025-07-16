import streamlit as st
import pandas as pd
import altair as alt
import os

# CSV 파일 경로 (현재 폴더에 있다고 가정)
CSV_PATH = "countriesMBTI_16types.csv"

# 제목
st.title("🌍 국가별 MBTI 유형 상위 3개 분석기")

# 파일 존재 여부 확인
if not os.path.exists(CSV_PATH):
    st.error("❌ 데이터 파일(countriesMBTI_16types.csv)을 찾을 수 없습니다. 이 앱과 같은 폴더에 있어야 합니다.")
else:
    # 데이터 불러오기
    @st.cache_data
    def load_data():
        return pd.read_csv(CSV_PATH)

    df = load_data()

    # 국가 선택
    country_list = df['Country'].tolist()
    selected_country = st.selectbox("국가를 선택하세요:", country_list)

    if selected_country:
        # 선택한 국가의 데이터
        country_row = df[df['Country'] == selected_country].iloc[0]
        
        # MBTI 점수만 추출
        mbti_scores = country_row.drop(labels="Country")
        
        # 상위 3개 MBTI
        top_mbti = mbti_scores.sort_values(ascending=False).head(3)

        st.subheader(f"📊 {selected_country}에서 가장 높은 MBTI 3종")

        # 리스트 출력
        for i, (mbti, value) in enumerate(top_mbti.items(), 1):
            st.write(f"{i}. **{mbti}** : {value:.2%}")

        # Altair 차트
        chart_df = pd.DataFrame({
            "MBTI": top_mbti.index,
            "비율": top_mbti.values
        })

        chart = alt.Chart(chart_df).mark_bar(color="#4c78a8").encode(
            x=alt.X("MBTI", sort="-y"),
            y=alt.Y("비율", title="비율 (%)", scale=alt.Scale(domain=[0, chart_df["비율"].max() + 0.05])),
            tooltip=["MBTI", alt.Tooltip("비율", format=".2%")]
        ).properties(
            width=500,
            height=300,
            title=f"{selected_country}의 MBTI Top 3"
        )

        st.altair_chart(chart, use_container_width=True)
