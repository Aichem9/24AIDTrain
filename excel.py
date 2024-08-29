import streamlit as st
import pandas as pd

# Streamlit 앱 설정
st.set_page_config(page_title="성적 대시보드", layout="wide")

# 파일 업로드
uploaded_file = st.file_uploader("분석할 Excel 파일을 업로드하세요", type=["xlsx"])

if uploaded_file:
    try:
        # 필요한 라이브러리가 설치되었는지 확인
        import openpyxl
        
        # Excel 파일 읽기
        df = pd.read_excel(uploaded_file, sheet_name=None)  # 모든 시트를 읽어옴
        sheet_names = list(df.keys())  # 시트 이름 가져오기

        # 시트 선택
        sheet_select = st.sidebar.selectbox("분석할 시트를 선택하세요", sheet_names)
        data = df[sheet_select]  # 선택한 시트의 데이터 가져오기

        # 데이터 미리보기
        st.write(f"### '{sheet_select}' 시트의 데이터 미리보기")
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
            st.warning(f"'{sheet_select}' 시트에는 데이터가 없습니다.")

    except ImportError:
        st.error("필수 라이브러리 'openpyxl'이 설치되지 않았습니다. 터미널에서 다음 명령어를 사용하여 설치해주세요: `pip install openpyxl`")

    except Exception as e:
        st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")

else:
    st.info("분석할 파일을 업로드해주세요.")
