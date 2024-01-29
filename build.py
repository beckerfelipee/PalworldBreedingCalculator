import pandas as pd
import streamlit as st

# Start Webpage
st.set_page_config(layout="wide")

# ---------------------------- Retrieve Data ------------------------------- #

@st.cache_data
def load_pals():
    pals = pd.read_csv(r'Data/Pals.csv', header=None)
    number_of_pals = len(pals[0])
    return pals, number_of_pals

@st.cache_data
def load_all_combinations():
    all_combos = pd.read_csv(r'Data/AllCombos.csv', sep=';', header=None)
    return all_combos

@st.cache_data
def load_images_src():
    sources = pd.read_csv(r'Data/Images.csv', sep=',', header=None)
    return sources


# start Data
df_pals, n_pals = load_pals()
df_all_combos = load_all_combinations()
img_sources = load_images_src()


# ---------------------------- Data Functions ------------------------- #

def search_number(pal):
    number = df_pals[df_pals[0] == pal].index[0]
    return number

def search_pal(number):
    pal = df_pals[0][number]
    return pal

def get_pals_list():
    pals = []
    for pal in df_pals[0]:
        pals.append(pal)
    return pals

def get_children(parent1, parent2):
    column = search_number(parent1)
    row = search_number(parent2)
    children = df_all_combos[column][row]
    return children

def get_combinations(pal):
    combinations = []
    for column in range(n_pals):
        for row, p in enumerate(df_all_combos[column].values):
            if p == pal:
                parent1 = search_pal(column)
                parent2 = search_pal(row)
                parents = [parent1, parent2]
                if not [parent2, parent1] in combinations:
                    combinations.append(parents)
    return combinations

def get_image(pal):
    # Exception
    if pal == "Gumoss (Special)":
        pal = "Gumoss"

    # Code
    if pal in img_sources[0].values:
        row = img_sources[img_sources[0] == pal].index[0]
        image_src = img_sources[1][row]
        return image_src
    else:
        row = img_sources[img_sources[0] == "No Image"].index[0]
        no_image_src = img_sources[1][row]
        return no_image_src


# ---------------------------- Web App Build -------------------------- #

# Header
with st.container():
    c1, c2, c3 = st.columns(3)
    c1.text("Game Version: 0.1.3.0")
    c1.write("[https://github.com/beckerfelipee](https://github.com/beckerfelipee)")
    c1.link_button("Buy me a coffee!", "https://www.buymeacoffee.com/beckerfelipee")
    c2.title('Palworld Breeding :blue[Calculator]', anchor=False)
    c3.text("")

# Calculator
with st.container():
    st.divider()
    left, space1, center1, space2, center2, space3, center3, space4, right = st.columns([3, 1, 2, 1, 2, 1, 2, 1, 3])
    pals_list = get_pals_list()

    # Parent 1
    center1.header("Parent 1", anchor=False)
    pal1 = center1.selectbox("---", pals_list)
    src_pal1 = get_image(pal1)
    center1.image(src_pal1)

    # Parent 2
    center2.header("Parent 2", anchor=False)
    pal2 = center2.selectbox("--- ---", pals_list)
    src_pal2 = get_image(pal2)
    center2.image(src_pal2)

    # Result
    center3.header("Result", anchor=False)
    center3.markdown("")
    pal3 = get_children(pal1, pal2)
    center3.code(pal3)
    src_pal3 = get_image(pal3)
    center3.image(src_pal3)
    st.divider()

# Search by Result
with st.expander("Search by Result"):
    st.divider()
    st.markdown("<h2 style='text-align: left'>Search by Result</h2>", unsafe_allow_html=True)
    l, s1, r1, s2, r2, s3, r3, s4, r4 = st.columns([3, 1, 3, 1, 3, 1, 3, 1, 3])

    # Pal for Search
    pal4 = l.selectbox("--- --- ---", pals_list)
    src_pal4 = get_image(pal4)
    l.image(src_pal4)

    # get and return combinations
    result = get_combinations(pal4)
    r_list = [r1, r2, r3, r4]
    index = 0
    for c in result:
        couple = f"{c[0]} + {c[1]}"
        r_list[index].code(couple)
        index = (index + 1) % len(r_list)
