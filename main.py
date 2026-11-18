import streamlit as st


# ============================================================
# 1. 화학 반응 정보 파일 읽기
# ============================================================

def read_reactions():
    # reactions.txt 파일을 읽기 모드(r)로 엽니다.
    # encoding="utf-8"은 파일에 있는 한글을 정상적으로 읽기 위한 설정입니다.
    file = open("reactions.txt", "r", encoding="utf-8")

    # 파일에서 읽어 온 화학 반응 정보를 저장할 빈 리스트입니다.
    reactions = []

    # 파일의 내용을 한 줄씩 읽으면서 반복합니다.
    for line in file:
        # strip()은 줄 양쪽의 공백과 줄바꿈 문자를 제거합니다.
        line = line.strip()

        # 빈 줄이 아니라면 해당 줄의 반응 정보를 처리합니다.
        if line != "":
            # 쉼표를 기준으로 문자열을 나눕니다.
            # 최대 3번만 나누므로 이름, 반응식, 종류, 설명의
            # 네 부분으로 구분할 수 있습니다.
            # 설명에 쉼표가 포함되어도 나머지는 설명에 남습니다.
            reaction = line.split(",", 3)

            # 나눈 반응 정보를 reactions 리스트에 추가합니다.
            reactions.append(reaction)

    # 파일 읽기가 끝났으므로 파일을 닫습니다.
    file.close()

    # 저장한 화학 반응 정보 리스트를 반환합니다.
    return reactions


# ============================================================
# 2. 화학 반응식 해석
# ============================================================

def parse_reaction(equation):
    # 반응식을 '->' 기호를 기준으로 나눕니다.
    # 예: "2H2 + O2 -> 2H2O"
    # 왼쪽은 반응물, 오른쪽은 생성물입니다.
    sides = equation.split("->")

    # 해석한 반응물과 생성물 정보를 저장할 리스트입니다.
    result = []

    # 반응물 쪽과 생성물 쪽을 차례대로 처리합니다.
    for side in sides:
        # '+' 기호를 기준으로 각 물질을 분리합니다.
        # 예: "2H2 + O2" → ["2H2 ", " O2"]
        substances = side.split("+")

        # 각 물질의 화학식과 계수를 저장할 리스트입니다.
        parsed_substances = []

        # 분리된 물질을 하나씩 확인합니다.
        for substance in substances:
            # 화학식 양쪽에 있는 불필요한 공백을 제거합니다.
            substance = substance.strip()

            # 화학식 앞에 있는 반응 계수를 저장할 문자열입니다.
            coefficient_text = ""

            # 문자열의 몇 번째 문자를 확인하고 있는지 나타냅니다.
            position = 0

            # 문자열의 앞부분이 숫자인 동안 반복합니다.
            # 예: "2H2"에서 앞의 2만 읽습니다.
            # 여러 자리 계수도 처리할 수 있습니다.
            while position < len(substance) and substance[position].isdigit():
                # 현재 숫자를 계수 문자열에 추가합니다.
                coefficient_text += substance[position]

                # 다음 문자로 이동합니다.
                position += 1

            # 화학식 앞에 숫자가 없으면 계수를 1로 설정합니다.
            # 예: O2는 계수가 생략되었으므로 1입니다.
            if coefficient_text == "":
                coefficient = 1
            else:
                # 숫자가 있으면 정수형으로 변환합니다.
                coefficient = int(coefficient_text)

            # 계수 부분을 제외하고 실제 화학식만 추출합니다.
            # 예: "2H2O" → "H2O"
            formula = substance[position:].strip()

            # [화학식, 계수] 형태로 리스트에 저장합니다.
            # 예: ["H2O", 2]
            parsed_substances.append([formula, coefficient])

        # 한쪽의 모든 물질을 해석한 결과를 저장합니다.
        result.append(parsed_substances)

    # 반응물과 생성물 정보가 들어 있는 리스트를 반환합니다.
    # result[0]에는 반응물, result[1]에는 생성물이 들어 있습니다.
    return result


# ============================================================
# 3. 화학 반응을 한 단계 진행하는 함수
# ============================================================

def react_once(reactant_counts, product_counts, parsed_reaction):
    # 해석한 반응식에서 반응물과 생성물 정보를 가져옵니다.
    reactants = parsed_reaction[0]
    products = parsed_reaction[1]

    # 먼저 반응에 필요한 반응물이 충분한지 확인합니다.
    for i in range(len(reactants)):
        # 각 반응물의 반응 계수를 가져옵니다.
        coefficient = reactants[i][1]

        # 현재 분자 수가 반응 계수보다 작으면
        # 해당 반응물은 한 번의 반응에도 필요한 양이 부족합니다.
        if reactant_counts[i] < coefficient:
            # 반응을 진행할 수 없으므로 False를 반환합니다.
            return False

    # 모든 반응물이 충분하면 실제 반응을 진행합니다.
    for i in range(len(reactants)):
        coefficient = reactants[i][1]

        # 반응물의 현재 개수에서 반응 계수만큼 뺍니다.
        # 예: 2H2 + O2 -> 2H2O에서
        # H2는 2개, O2는 1개 감소합니다.
        reactant_counts[i] -= coefficient

    # 반응이 일어나면 생성물의 개수를 증가시킵니다.
    for i in range(len(products)):
        coefficient = products[i][1]

        # 생성물의 현재 개수에 반응 계수만큼 더합니다.
        # 예: H2O는 한 번의 반응에서 2개 생성됩니다.
        product_counts[i] += coefficient

    # 반응이 정상적으로 한 번 진행되었다는 의미입니다.
    return True


# ============================================================
# 4. 반응물과 생성물의 화학식 및 계수 표 출력
# ============================================================

def show_table(title, substances):
    # 표의 제목을 화면에 표시합니다.
    # title에는 "반응물" 또는 "생성물"이 들어갑니다.
    st.subheader(title)

    # 마크다운 표의 제목 행과 구분선을 작성합니다.
    # \n은 줄바꿈을 의미합니다.
    table = "| 화학식 | 계수 |\n| --- | --- |\n"

    # 물질의 화학식과 계수를 하나씩 가져옵니다.
    for substance in substances:
        # 물질 정보의 첫 번째 값은 화학식입니다.
        formula = substance[0]

        # 두 번째 값은 반응 계수입니다.
        coefficient = substance[1]

        # 표에 한 행씩 추가합니다.
        # str()은 숫자를 문자열로 변환하는 함수입니다.
        table += "| " + formula + " | " + str(coefficient) + " |\n"

    # 완성된 마크다운 표를 Streamlit 화면에 표시합니다.
    st.markdown(table)


# ============================================================
# 5. 단계별 분자 수 변화 표 출력
# ============================================================

def show_history_table(reactants, products, history):
    # 단계별 반응 결과를 표시하는 제목입니다.
    st.subheader("단계별 분자 수")

    # 반응물과 생성물 리스트를 하나로 합칩니다.
    # 표에서 반응물과 생성물의 개수를 함께 보여주기 위해서입니다.
    substances = reactants + products

    # 표의 첫 번째 열은 반응 단계입니다.
    table = "| 단계 |"

    # 각 물질의 화학식을 표의 열 제목에 추가합니다.
    for substance in substances:
        table += " " + substance[0] + " |"

    # 마크다운 표에 필요한 구분선을 작성합니다.
    table += "\n| --- |"

    # 물질의 개수만큼 구분선을 추가합니다.
    for substance in substances:
        table += " --- |"

    # 구분선 작성 후 줄을 바꿉니다.
    table += "\n"

    # history 리스트에 저장된 단계 수만큼 반복합니다.
    # 0단계는 반응하기 전 초기 상태를 의미합니다.
    for step in range(len(history)):
        # 현재 단계 번호를 표에 추가합니다.
        table += "| " + str(step) + " |"

        # 현재 단계의 반응물 및 생성물 개수를 차례대로 추가합니다.
        for count in history[step]:
            table += " " + str(count) + " |"

        # 한 단계의 분자 수 기록이 끝나면 줄을 바꿉니다.
        table += "\n"

    # 완성된 단계별 분자 수 변화 표를 화면에 출력합니다.
    st.markdown(table)


# ============================================================
# 6. 화학 반응의 최종 결과 분석 및 출력
# ============================================================

def show_result(reactants, products, history):
    # history에 초기 상태만 저장되어 있다면
    # 실제 화학 반응이 한 번도 진행되지 않았다는 뜻입니다.
    if len(history) == 1:
        st.write("반응물이 부족하여 반응하지 않았습니다")
        return

    # history의 마지막 항목은 반응이 끝난 후의 분자 수입니다.
    # -1은 리스트의 마지막 요소를 의미합니다.
    final_counts = history[-1]

    # 완전히 소모되어 개수가 0이 된 반응물을 저장합니다.
    exhausted = []

    # 다음 반응을 진행하기에 개수가 부족한 반응물을 저장합니다.
    insufficient = []

    # 반응이 끝난 후에도 남아 있는 반응물을 저장합니다.
    remaining = []

    # 반응을 통해 생성된 생성물의 개수를 저장합니다.
    created = []

    # 각 반응물의 최종 상태를 확인합니다.
    for i in range(len(reactants)):
        # 현재 확인 중인 반응물의 화학식입니다.
        formula = reactants[i][0]

        # 한 번의 반응에 필요한 해당 반응물의 계수입니다.
        coefficient = reactants[i][1]

        # 최종 상태에서 해당 반응물의 개수입니다.
        count = final_counts[i]

        # 반응물의 개수가 0이면 완전히 소모된 것입니다.
        if count == 0:
            exhausted.append(formula)

        # 남은 개수가 반응 계수보다 작으면
        # 다음 반응을 한 번 더 진행하기에 부족합니다.
        if count < coefficient:
            insufficient.append(formula)

        # 반응물이 1개 이상 남아 있으면
        # 화학식과 남은 개수를 함께 저장합니다.
        if count > 0:
            remaining.append(formula + " " + str(count) + "개")

    # 각 생성물의 최종 개수를 확인합니다.
    for i in range(len(products)):
        # 생성물의 화학식을 가져옵니다.
        formula = products[i][0]

        # history에는 반응물 개수가 먼저 저장되고
        # 그다음 생성물 개수가 저장되어 있습니다.
        # 따라서 반응물의 개수만큼 인덱스를 이동하여
        # 해당 생성물의 최종 개수를 가져옵니다.
        count = final_counts[len(reactants) + i]

        # 생성물의 화학식과 최종 개수를 저장합니다.
        created.append(formula + " " + str(count) + "개")

    # 완전히 소모된 반응물이 하나인 경우입니다.
    if len(exhausted) == 1:
        st.write(exhausted[0] + "가 먼저 모두 소모되었습니다.")

    # 완전히 소모된 반응물이 여러 개인 경우입니다.
    elif len(exhausted) > 1:
        st.write(", ".join(exhausted) + "가 동시에 모두 소모되었습니다.")

    # 어떤 반응물도 완전히 소모되지 않은 경우입니다.
    else:
        st.write("완전히 소모된 반응물은 없습니다.")

    # 다음 반응을 진행하기에 부족한 물질을 알려줍니다.
    # join()은 리스트의 문자열들을 쉼표로 연결합니다.
    st.write(
        "다음 반응에 필요한 "
        + ", ".join(insufficient)
        + "의 개수가 부족하여 반응이 멈췄습니다."
    )

    # 반응이 끝난 후 남아 있는 반응물의 정보를 출력합니다.
    if len(remaining) > 0:
        st.write("남은 반응물은 " + ", ".join(remaining) + "입니다.")
    else:
        st.write("남은 반응물은 없습니다.")

    # 최종적으로 생성된 물질의 개수를 출력합니다.
    st.write("생성물은 " + ", ".join(created) + " 만들어졌습니다.")


# ============================================================
# 7. Streamlit 프로그램 화면 구성
# ============================================================

def show_screen():
    # Streamlit 메인 화면에 프로그램 제목을 표시합니다.
    st.title("화학 반응 시뮬레이터")

    # reactions.txt에서 화학 반응 정보를 읽어 옵니다.
    reactions = read_reactions()

    # 사용자가 선택할 수 있는 반응 이름을 저장할 리스트입니다.
    reaction_names = []

    # 각 반응 정보에서 첫 번째 항목인 반응 이름만 가져옵니다.
    for reaction in reactions:
        reaction_names.append(reaction[0])

    # 사이드바에 화학 반응 선택 메뉴를 생성합니다.
    # 사용자는 reactions.txt에 등록된 반응 중 하나를 선택합니다.
    selected_name = st.sidebar.selectbox("반응 선택", reaction_names)

    # 사용자가 선택한 반응이 리스트의 몇 번째에 있는지 찾습니다.
    selected_index = reaction_names.index(selected_name)

    # 선택한 반응의 전체 정보를 가져옵니다.
    selected_reaction = reactions[selected_index]

    # 선택한 반응 정보의 두 번째 항목은 화학 반응식입니다.
    equation = selected_reaction[1]

    # 반응식을 해석하여 반응물과 생성물 정보를 분리합니다.
    parsed_reaction = parse_reaction(equation)

    # 반응식에서 반응물 정보를 가져옵니다.
    reactants = parsed_reaction[0]

    # 반응식에서 생성물 정보를 가져옵니다.
    products = parsed_reaction[1]

    # 선택한 반응의 반응식, 종류, 설명을 화면에 표시합니다.
    st.write("반응식: " + equation)
    st.write("종류: " + selected_reaction[2])
    st.write("설명: " + selected_reaction[3])

    # 사용자가 입력한 반응물의 초기 개수를 저장할 리스트입니다.
    reactant_counts = []

    # 반응물의 종류만큼 숫자 입력칸을 자동으로 생성합니다.
    for reactant in reactants:
        # 현재 반응물의 화학식을 가져옵니다.
        formula = reactant[0]

        # 사용자가 반응물의 분자 수를 입력할 수 있도록 합니다.
        # min_value=0은 음수 입력을 제한합니다.
        # value=0은 초기 입력값을 0으로 설정합니다.
        # step=1은 숫자가 1씩 변하도록 설정합니다.
        count = st.number_input(
            formula + " 분자 수",
            min_value=0,
            value=0,
            step=1
        )

        # 사용자가 입력한 분자 수를 리스트에 추가합니다.
        reactant_counts.append(count)

    # 현재 선택한 반응 이름, 반응식, 입력된 분자 수를
    # 하나의 리스트로 저장합니다.
    # 이전 입력값과 비교하여 변경 여부를 확인하는 데 사용합니다.
    current_inputs = [selected_name, equation] + reactant_counts

    # session_state는 Streamlit에서 화면이 다시 실행되어도
    # 특정 데이터를 유지할 수 있도록 하는 저장 공간입니다.

    # 이전 입력값을 저장하는 항목이 없다면 빈 리스트를 생성합니다.
    if "previous_inputs" not in st.session_state:
        st.session_state.previous_inputs = []

    # 단계별 반응 결과를 저장하는 항목이 없다면
    # 빈 리스트를 생성합니다.
    if "history" not in st.session_state:
        st.session_state.history = []

    # 현재 입력값과 이전 입력값을 비교합니다.
    # 반응 선택이나 분자 수가 바뀌면 이전 결과를 초기화합니다.
    if current_inputs != st.session_state.previous_inputs:
        st.session_state.history = []

        # 현재 입력값을 새로운 이전 입력값으로 저장합니다.
        st.session_state.previous_inputs = current_inputs

    # 반응물의 화학식과 계수를 표로 표시합니다.
    show_table("반응물", reactants)

    # 생성물의 화학식과 계수를 표로 표시합니다.
    show_table("생성물", products)

    # 사이드바의 실행 버튼을 누르면
    # 아래 화학 반응 계산 과정이 시작됩니다.
    if st.sidebar.button("실행"):
        # 생성물의 초기 개수를 저장할 리스트입니다.
        product_counts = []

        # 모든 생성물의 초기 개수를 0으로 설정합니다.
        for product in products:
            product_counts.append(0)

        # 단계별 분자 수 변화를 기록할 리스트입니다.
        history = []

        # 반응이 시작되기 전의 초기 상태를 0단계로 저장합니다.
        # 반응물 개수와 생성물 개수를 하나의 리스트로 합칩니다.
        history.append(reactant_counts + product_counts)

        # react_once()가 True를 반환하는 동안
        # 화학 반응을 한 단계씩 반복해서 진행합니다.
        # 반응물이 부족하면 False가 반환되어 반복이 종료됩니다.
        while react_once(reactant_counts, product_counts, parsed_reaction):
            # 한 번의 반응이 끝날 때마다
            # 변경된 반응물과 생성물의 개수를 기록합니다.
            history.append(reactant_counts + product_counts)

        # 모든 단계의 반응 기록을 session_state에 저장합니다.
        # 이를 통해 화면이 다시 실행되어도 결과를 유지할 수 있습니다.
        st.session_state.history = history

    # 저장된 반응 기록이 하나 이상 있는 경우
    # 단계별 표와 최종 결과를 표시합니다.
    if len(st.session_state.history) > 0:
        # 반응이 진행되는 동안 변화한 분자 수를
        # 단계별 표로 출력합니다.
        show_history_table(
            reactants,
            products,
            st.session_state.history
        )

        # 반응 종료 후 소모된 반응물, 부족한 반응물,
        # 남은 반응물, 생성물의 개수를 분석하여 출력합니다.
        show_result(
            reactants,
            products,
            st.session_state.history
        )


# ============================================================
# 8. 프로그램 실행
# ============================================================

# 위에서 정의한 show_screen() 함수를 호출하여
# Streamlit 프로그램의 전체 화면을 표시합니다.
show_screen()
