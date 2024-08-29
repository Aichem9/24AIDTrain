import streamlit as st
import pandas as pd

# Streamlit 앱 설정
st.set_page_config(page_title="2024 AIDT 전문가 연수 성취도 성적 분석 대시보드", layout="wide")

# 대시보드 제목 및 설명
st.title("2024 AIDT 전문가 연수 성취도 성적 분석 대시보드")
st.write("업로드한 CSV 파일을 기반으로 데이터 분석과 시각화를 제공합니다. 먼저 분석할 파일을 업로드하세요.")

# 파일 업로드
uploaded_file = st.file_uploader("분석할 CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    try:
        # CSV 파일 읽기
        data = pd.read_csv(uploaded_file, header=None)  # CSV 파일을 판다스로 읽기 (헤더 없음으로 설정)
        
        # 데이터 미리보기
        st.write("### 데이터 미리보기")
        st.dataframe(data.head(10))  # 상위 10개 데이터 미리보기

        # 1행 데이터를 기준으로 2~6행 데이터 시각화
        if len(data) >= 6:
            x_axis = data.iloc[0]  # 1행의 데이터를 X축으로 사용
            data_to_plot = data.iloc[1:6].transpose()  # 2~6행 데이터를 가져와서 열로 변환 (각 행이 시리즈로)

            # 시각화 선택
            st.write("### 시각화")
            chart_type = st.selectbox("시각화 유형을 선택하세요", ["막대 그래프", "선 그래프"])

            if chart_type == "막대 그래프":
                st.write("### 막대 그래프")
                st.bar_chart(data_to_plot.set_index(x_axis))

            elif chart_type == "선 그래프":
                st.write("### 선 그래프")
                st.line_chart(data_to_plot.set_index(x_axis))
        else:
            st.warning("시각화를 위해 데이터가 충분하지 않습니다. 최소 6행의 데이터가 필요합니다.")
        
    except Exception as e:
        st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")

else:
    st.info("분석할 CSV 파일을 업로드해주세요.")
