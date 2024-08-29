import streamlit as st
import pandas as pd

# Streamlit 앱 설정
st.set_page_config(page_title="성적 대시보드", layout="wide")

# 파일 업로드
uploaded_file = st.file_uploader("파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    # Excel 파일 읽기
    df = pd.read_excel(uploaded_file, sheet_name=None)  # 모든 시트를 읽어옴
    sheet_names = list(df.keys())

    # 시트 선택
    sheet_select = st.sidebar.selectbox("시트를 선택하세요", sheet_names)
    data = df[sheet_select]

    # 데이터 미리보기
    st.write(f"### {sheet_select} 시트의 데이터 미리보기")
    st.dataframe(data.head())

    # 데이터 통계 정보
    st.write("### 데이터 통계 정보")
    st.write(data.describe())

    # 시각화 선택
    st.write("### 시각화")
    plot_type = st.selectbox("시각화 유형을 선택하세요", ["히스토그램", "박스플롯", "산점도"])

    # 컬럼 선택
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    selected_columns = st.multiselect("컬럼을 선택하세요", numeric_columns)

    # 시각화
    if plot_type == "히스토그램":
        for col in selected_columns:
            st.write(f"### {col} 히스토그램")
            st.bar_chart(data[col])
    elif plot_type == "박스플롯":
        st.write("### 박스플롯")
        st.box_plot(data[selected_columns])
    elif plot_type == "산점도" and len(selected_columns) == 2:
        st.write(f"### {selected_columns[0]} vs {selected_columns[1]} 산점도")
        st.scatter_chart(data[selected_columns])

else:
    st.info("분석할 파일을 업로드해주세요.")
