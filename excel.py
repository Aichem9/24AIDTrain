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
        data = pd.read_csv(uploaded_file)  # CSV 파일을 판다스로 읽기
        
        # 데이터 미리보기
        st.write("### 데이터 미리보기")
        st.dataframe(data.head(10))  # 상위 10개 데이터 미리보기

        # 1열의 데이터를 X축으로 사용
        if len(data.columns) > 1:
            x_axis = data.iloc[:, 0]  # 1열의 데이터를 X축으로 사용
            y_columns = data.columns[1:]  # 2열부터 마지막 열까지의 데이터 선택 가능

            # 시각화할 데이터 선택
            selected_columns = st.multiselect("시각화할 데이터를 선택하세요", y_columns)

            if selected_columns:
                # 선택한 데이터를 시각화하기 위해 새로운 DataFrame 생성
                data_to_plot = data[selected_columns]
                data_to_plot.index = x_axis  # X축을 1열의 데이터로 설정
                
                # 시각화 선택
                st.write("### 시각화")
                chart_type = st.selectbox("시각화 유형을 선택하세요", ["막대 그래프", "선 그래프"])

                if chart_type == "막대 그래프":
                    st.write("### 막대 그래프")
                    st.bar_chart(data_to_plot)

                elif chart_type == "선 그래프":
                    st.write("### 선 그래프")
                    st.line_chart(data_to_plot)
            else:
                st.warning("시각화할 데이터를 선택하세요.")
        else:
            st.warning("데이터에 시각화할 열이 충분하지 않습니다. 2개 이상의 열이 필요합니다.")

    except Exception as e:
        st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")

else:
    st.info("분석할 CSV 파일을 업로드해주세요.")
