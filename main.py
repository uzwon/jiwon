
import streamlit as st


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

    reactions = read_reactions()
    reaction_names = []

    for reaction in reactions:
        reaction_names.append(reaction[0])

    if len(reaction_names) == 0:
        st.warning("reactions.txt에 반응 정보를 추가해 주세요.")
        return

    selected_name = st.sidebar.selectbox("화학 반응 선택", reaction_names)
    selected_index = reaction_names.index(selected_name)
    selected_reaction = reactions[selected_index]

    equation = selected_reaction[1]
    reactants, products = parse_reaction(equation)

    st.write("반응식: " + equation)

    # 선택한 반응의 반응물 개수만큼 입력칸을 만듭니다.
    reactant_counts = []
    for i in range(len(reactants)):
        formula = reactants[i][0]
        default_count = 2
        if i == 0:
            default_count = 4

        count = st.number_input(
            formula + " 분자 개수", min_value=0, value=default_count, step=1
        )
        reactant_counts.append(count)

    # 반응식에서 해석한 결과를 표로 보여줍니다.
    table = "| 구분 | 화학식 | 계수 |\n|---|---|---|\n"

    for reactant in reactants:
        table += "| 반응물 | " + reactant[0] + " | " + str(reactant[1]) + " |\n"

    for product in products:
        table += "| 생성물 | " + product[0] + " | " + str(product[1]) + " |\n"

    st.markdown(table)


show_screen()
