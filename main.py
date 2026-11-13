import streamlit as st


def show_screen():
    st.title("🧪 화학 반응 단계별 시뮬레이터")

    # 첫 단계에서는 물 생성 반응의 반응물 개수만 입력합니다.
    h2_count = st.number_input("수소(H2) 분자 개수", min_value=0, value=4, step=1)
    o2_count = st.number_input("산소(O2) 분자 개수", min_value=0, value=2, step=1)


show_screen()

