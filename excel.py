import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

        # 1열의 데이터를 X축으로 사용하고 2~6열의 데이터를 16열에 대한 비율로 계산
        if len(data.columns) >= 16:
            x_axis = data.iloc[:, 0]  # 1열의 데이터를 X축으로 사용
            y_data = data.iloc[:, 1:6].div(data.iloc[:, 15], axis=0)  # 2~6열을 16열의 데이터로 나눔
            column_15 = data.iloc[:, 14]  # 15열의 데이터 (강조할 데이터)
            
            # 선택한 데이터를 시각화하기 위해 새로운 DataFrame 생성
            y_data.index = x_axis  # X축을 1열의 데이터로 설정
            
            # 시각화 선택
            st.write("### 시각화")
            chart_type = st.selectbox("시각화 유형을 선택하세요", ["막대 그래프", "선 그래프"])

            # 시각화 생성
            if chart_type == "막대 그래프":
                st.write("### 막대 그래프")

                # 기본 막대 그래프 그리기
                fig, ax = plt.subplots()
                y_data.plot(kind='bar', ax=ax)

                # 15열 데이터를 강조된 색으로 추가
                ax.plot(x_axis, column_15, color='red', marker='o', linestyle='-', linewidth=2, label='15열 데이터 강조')

                st.pyplot(fig)

            elif chart_type == "선 그래프":
                st.write("### 선 그래프")

                # 기본 선 그래프 그리기
                fig, ax = plt.subplots()
                y_data.plot(ax=ax)

                # 15열 데이터를 강조된 색으로 추가
                ax.plot(x_axis, column_15, color='red', marker='o', linestyle='-', linewidth=2, label='15열 데이터 강조')

                st.pyplot(fig)
        else:
            st.warning("데이터에 시각화할 열이 충분하지 않습니다. 최소 16개의 열이 필요합니다.")

    except Exception as e:
        st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")

else:
    st.info("분석할 CSV 파일을 업로드해주세요.")
