
import streamlit as st


# 화면 설정 (화학 반응 데이터와 계산 로직은 변경하지 않습니다.)
st.set_page_config(
    page_title="화학 반응 단계별 시뮬레이터",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_styles():
    # 다크 모드와 카드 디자인만 담당하는 함수입니다.
    st.markdown(
        """
        <style>
        :root {
            --bg: #151B25;
            --card: #252D3A;
            --accent: #66A9BE;
            --text: #E3E8EF;
            --muted: #A8B6C6;
            --line: #3B485A;
        }

        html, body, .stApp, [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background: var(--bg) !important;
            color: var(--text) !important;
        }
        [data-testid="stHeader"] { background: transparent !important; }
        .block-container {
            max-width: 1150px !important;
            padding: 3rem 2.2rem 4rem !important;
        }
        [data-testid="stSidebar"] {
            background: #1B2430 !important;
            border-right: 1px solid var(--line) !important;
        }
        [data-testid="stSidebar"] * { color: var(--text); }
        h1, h2, h3, p, label { color: var(--text); }
        h1 {
            font-size: 2.15rem !important;
            font-weight: 750 !important;
            letter-spacing: -0.04em !important;
        }
        h3 { font-size: 1.25rem !important; letter-spacing: -0.02em !important; }
        [data-testid="stCaptionContainer"] p {
            color: var(--muted) !important;
            line-height: 1.6 !important;
        }

        /* 상단 브랜드 및 영역 번호 */
        .sidebar-brand {
            border-bottom: 1px solid var(--line);
            padding: 0.4rem 0 1.4rem;
            margin-bottom: 1.5rem;
        }
        .sidebar-brand strong { font-size: 1.15rem; }
        .sidebar-brand p { color: var(--muted) !important; font-size: 0.85rem; }
        .section-number {
            color: var(--accent);
            font-size: 0.75rem;
            font-weight: 750;
            letter-spacing: 0.14em;
            margin-bottom: 0.2rem;
        }

        /* 실제 Streamlit 컨테이너를 카드로 표시 */
        .st-key-conditions_card,
        .st-key-simulation_card,
        .st-key-results_card {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1.5rem 1.7rem;
            margin-top: 1.25rem;
            box-shadow: 0 10px 26px rgba(5, 12, 21, 0.13);
        }
        .st-key-simulation_card {
            background: linear-gradient(120deg, #2A3A4A, var(--card));
            border-color: #477588;
            border-left: 4px solid var(--accent);
            box-shadow: 0 12px 32px rgba(5, 12, 21, 0.24);
        }
        .st-key-equation_display {
            background: #192430;
            border: 1px solid #49677A;
            border-radius: 12px;
            padding: 1.15rem 1.35rem;
        }
        .st-key-equation_display [data-testid="stMarkdownContainer"] p {
            font-size: 1.3rem !important;
            font-weight: 650 !important;
            line-height: 1.65;
            overflow-wrap: anywhere;
        }

        /* 숫자 입력창과 증감 버튼 */
        [data-testid="stNumberInput"] [data-baseweb="input"],
        [data-testid="stNumberInput"] input {
            background: #192430 !important;
            color: var(--text) !important;
        }
        [data-testid="stNumberInput"] [data-baseweb="input"] {
            border: 1px solid #526174 !important;
            border-radius: 10px !important;
            overflow: hidden;
        }
        [data-testid="stNumberInput"] [data-baseweb="input"]:focus-within {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px rgba(102, 169, 190, 0.2) !important;
        }
        [data-testid="stNumberInput"] button {
            background: #334355 !important;
            color: var(--text) !important;
            border-left: 1px solid #526174 !important;
        }
        [data-testid="stNumberInput"] button:hover {
            background: #466D7C !important;
        }

        /* 사이드바의 반응 선택 메뉴 */
        [data-testid="stSelectbox"] [data-baseweb="select"] > div {
            background: var(--card) !important;
            color: var(--text) !important;
            border: 1px solid #526174 !important;
            border-radius: 10px !important;
        }
        [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover,
        [data-testid="stSelectbox"] [data-baseweb="select"]:focus-within > div {
            border-color: var(--accent) !important;
        }
        [data-baseweb="popover"], [role="listbox"], [role="option"] {
            background: var(--card) !important;
            color: var(--text) !important;
        }
        [role="option"]:hover, [role="option"][aria-selected="true"] {
            background: #355063 !important;
        }

        /* 반응물·생성물 분석 결과 표 */
        .st-key-results_card table {
            width: 100% !important;
            border: 1px solid var(--line) !important;
            border-collapse: separate !important;
            border-spacing: 0 !important;
            border-radius: 12px !important;
            overflow: hidden;
        }
        .st-key-results_card th {
            background: #344458 !important;
            color: var(--text) !important;
            font-weight: 700 !important;
        }
        .st-key-results_card td {
            background: var(--card) !important;
            color: var(--text) !important;
        }
        .st-key-results_card th, .st-key-results_card td {
            padding: 0.8rem 1rem !important;
            text-align: left !important;
            border-bottom: 1px solid var(--line) !important;
        }
        .st-key-results_card tbody tr:hover td {
            background: #304052 !important;
        }
        .st-key-results_card tr:last-child td { border-bottom: none !important; }

        /* 버튼, 마우스 오버, 키보드 포커스 */
        .stButton button {
            background: var(--accent) !important;
            color: var(--bg) !important;
            border-radius: 10px !important;
        }
        .stButton button:hover { background: #86BECB !important; }
        button:focus-visible, input:focus-visible {
            outline: 2px solid var(--accent) !important;
            outline-offset: 2px;
        }
        @media (max-width: 760px) {
            .block-container { padding: 1.5rem 1rem 3rem !important; }
            .st-key-conditions_card, .st-key-simulation_card,
            .st-key-results_card { padding: 1rem; border-radius: 14px; }
            h1 { font-size: 1.65rem !important; }
            .st-key-equation_display [data-testid="stMarkdownContainer"] p {
                font-size: 1rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def read_reactions():
    reactions = []

    with open("reactions.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line != "":
                parts = line.split(",", 3)
                if len(parts) == 4:
                    reactions.append(parts)

    return reactions


def parse_reaction(equation):
    sides = equation.split("->")
    result = []

    for side in sides:
        substances = []

        for item in side.split("+"):
            item = item.strip()
            number = ""

            for character in item:
                if character.isdigit():
                    number += character
                else:
                    break

            if number == "":
                coefficient = 1
            else:
                coefficient = int(number)

            formula = item[len(number):].strip()
            substances.append([formula, coefficient])

        result.append(substances)

    return result[0], result[1]


def show_screen():
    st.title("🧪 화학 반응 단계별 시뮬레이터")
    st.caption("화학 반응식을 확인하고 반응물의 초기 분자 개수를 설정하는 공간")

    reactions = read_reactions()
    reaction_names = []

    for reaction in reactions:
        reaction_names.append(reaction[0])

    if len(reaction_names) == 0:
        st.warning("reactions.txt에 반응 정보를 추가해 주세요.")
        return

    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="section-number">SCIENTIFIC DASHBOARD</div>
            <strong>⚗ Reaction Lab</strong>
            <p>화학 반응 선택 및 실험 설정</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_name = st.sidebar.selectbox("화학 반응 선택", reaction_names)
    selected_index = reaction_names.index(selected_name)
    selected_reaction = reactions[selected_index]

    equation = selected_reaction[1]
    reactants, products = parse_reaction(equation)

    # 실험 조건 설정 영역
    with st.container(key="conditions_card"):
        st.markdown('<div class="section-number">01 / EXPERIMENT SETUP</div>', unsafe_allow_html=True)
        st.markdown("### 실험 조건 설정")
        st.caption("선택한 반응에 필요한 반응물의 초기 분자 개수를 입력하세요.")

        # 선택한 반응의 반응물 개수만큼 입력칸을 만듭니다.
        reactant_counts = []
        input_columns = st.columns(2, gap="large")
        for i in range(len(reactants)):
            formula = reactants[i][0]
            default_count = 2
            if i == 0:
                default_count = 4

            with input_columns[i % 2]:
                count = st.number_input(
                    formula + " 분자 개수", min_value=0, value=default_count, step=1
                )
            reactant_counts.append(count)

    # 시뮬레이션 영역: 현재는 기존 반응식 표시만 합니다.
    with st.container(key="simulation_card"):
        st.markdown('<div class="section-number">02 / REACTION SIMULATION</div>', unsafe_allow_html=True)
        st.markdown("### 화학 반응 시뮬레이션")
        st.caption("현재는 반응식 분석 단계입니다. 실제 반응 계산은 아직 구현되지 않았습니다.")
        with st.container(key="equation_display"):
            st.write("반응식: " + equation)

    # 실험 결과 영역: 기존의 반응식 해석 결과 표를 유지합니다.
    with st.container(key="results_card"):
        st.markdown('<div class="section-number">03 / ANALYSIS RESULTS</div>', unsafe_allow_html=True)
        st.markdown("### 실험 결과")
        st.caption("반응물과 생성물의 화학식 및 계수를 분석한 결과입니다.")

        # 반응식에서 해석한 결과를 표로 보여줍니다.
        table = "| 구분 | 화학식 | 계수 |\n|---|---|---|\n"

        for reactant in reactants:
            table += "| 반응물 | " + reactant[0] + " | " + str(reactant[1]) + " |\n"

        for product in products:
            table += "| 생성물 | " + product[0] + " | " + str(product[1]) + " |\n"

        st.markdown(table)


apply_styles()
show_screen()
