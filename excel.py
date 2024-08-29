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
        st.dataframe(data.head())

        # 데이터 통계 정보
        if not data.empty:
            st.write("### 데이터 통계 정보")
            st.write(data.describe())

            # 시각화 선택
            st.write("### 시각화")
            plot_type = st.selectbox("시각화 유형을 선택하세요", ["히스토그램", "박스플롯", "산점도"])

            # 컬럼 선택
            numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
            
            if numeric_columns:  # 숫자형 컬럼이 있는지 확인
                selected_columns = st.multiselect("시각화할 컬럼을 선택하세요", numeric_columns)

                # 시각화
                if plot_type == "히스토그램" and selected_columns:
                    for col in selected_columns:
                        st.write(f"### {col} 히스토그램")
                        st.bar_chart(data[col])
                
                elif plot_type == "박스플롯" and selected_columns:
                    st.write("### 박스플롯")
                    st.box_chart(data[selected_columns])
                
                elif plot_type == "산점도" and len(selected_columns) == 2:
                    st.write(f"### {selected_columns[0]} vs {selected_columns[1]} 산점도")
                    st.scatter_chart(data[selected_columns])

            else:
                st.warning("선택할 수 있는 숫자형 컬럼이 없습니다.")

        else:
            st.warning("데이터가 비어 있습니다.")

    except Exception as e:
        st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")

else:
    st.info("분석할 CSV 파일을 업로드해주세요.")
