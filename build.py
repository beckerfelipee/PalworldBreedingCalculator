import pandas as pd
import streamlit as st

# Start Webpage
st.set_page_config(page_title="Palworld Breeding Calculator", page_icon="🐣", layout="wide")


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


@st.cache_data
def load_wikis_url():
    sources = pd.read_csv(r'Data/Wikis.csv', sep=',', header=None)
    return sources


# start Data
df_pals, n_pals = load_pals()
df_all_combos = load_all_combinations()
img_sources = load_images_src()
wikis_url = load_wikis_url()


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
    if pal in img_sources[0].values:
        row = img_sources[img_sources[0] == pal].index[0]
        image_src = img_sources[1][row]
        return image_src
    else:
        row = img_sources[img_sources[0] == "No Image"].index[0]
        no_image_src = img_sources[1][row]
        return no_image_src


def get_wiki(pal):
    if pal in wikis_url[0].values:
        row = wikis_url[wikis_url[0] == pal].index[0]
        url = wikis_url[1][row]
        return url
    else:
        return False


def image_with_wiki(pal, next_pal=None, place=st, width=200):
    if not next_pal:
        href = get_wiki(pal)
        src = get_image(pal)
        place.markdown(f'''
            <a href="{href}">
                <img src="{src}" width="{width}" height="{width}" style="margin-left: 0px;"/>
            </a>''', unsafe_allow_html=True)
    else:
        # Create a Combination Card
        href1 = get_wiki(pal)
        src1 = get_image(pal)
        href2 = get_wiki(next_pal)
        src2 = get_image(next_pal)
        place.markdown(f'''
            <div style="text-align: center; height: 150px;">
                <figure style="display: inline-block; margin-right: 20px;">
                    <figcaption style="font-size: 15px; margin-bottom: 10px;">{pal}</figcaption>
                    <a href="{href1}">
                        <img align="left" src="{src1}" width="{width}" height="{width}"/>
                    </a>
                </figure>
                <div style="display: inline-block; transform: translateY(250%);">
                    ➕
                </div>
                <figure style="display: inline-block; margin-bottom: 50px; margin-left: 20px;">
                    <figcaption style="font-size: 15px; margin-bottom: 10px;">{next_pal}</figcaption>
                    <a href="{href2}">
                        <img align="right" src="{src2}" width="{width}" height="{width}"/>
                    </a>
                </figure>
            </div>
        ''', unsafe_allow_html=True)


# ---------------------------- Web App Build -------------------------- #

# Header
with st.container():
    c1, c2, c3, c4 = st.columns([2, 1, 3, 3])
    c1.text("Game Version: 0.1.4.0")
    c1.write("[https://github.com/beckerfelipee](https://github.com/beckerfelipee)")
    if c3.button("🚀 Coming soon... ", use_container_width=True):
        st.toast("New website for finding the best pals to work is on its way!!", icon='🤚')
    c3.title('Palworld Breeding :blue[Calculator]', anchor=False)
    c1.link_button("Buy me a coffee!", "https://www.buymeacoffee.com/beckerfelipee")

# Calculator Area

with st.container(border=True):
    left, space1, center1, space2, center2, space3, center3, space4, right = st.columns([3, 1, 2, 1, 2, 1, 2, 1, 3])
    pals_list = get_pals_list()

    # Tips
    if left.button('Some tips!'):
        st.toast('You can click on "Search for Pal" to view all combinations for breeding a pal.', icon='👀')
        st.toast('You can click on the pal image to open their wiki.', icon='🚀')
        st.toast('Switch light and dark themes by clicking Settings in the top right corner.', icon='🌃')

    # Parent 1
    center1.header("Parent 1", anchor=False)
    pal1 = center1.selectbox("pal1", pals_list, label_visibility="hidden")
    image_with_wiki(pal1, place=center1)

    # Parent 2
    center2.header("Parent 2", anchor=False)
    pal2 = center2.selectbox("pal2", pals_list, label_visibility="hidden")
    image_with_wiki(pal2, place=center2)

    # Result
    center3.header("Result", anchor=False)
    center3.text("")
    pal3 = get_children(pal1, pal2)
    center3.code(pal3)
    image_with_wiki(pal3, place=center3)

    # Some Easter Egg (Subscribe to Gaubss)
    if pal1 == "Bushi" and pal2 == "Penking":
        st.toast('Subscribe to Gaubss Youtube Channel!', icon='🔺')

    # space
    st.title("")
    st.title("")

# Search by Result
with st.container(border=True):
    st.header("Search for Pal", anchor=False)
    l, s1, r1, s2, r2, s3, r3, s4, r4, = st.columns([7, 1, 9, 1, 9, 1, 9, 1, 9])

    # Pal for Search
    pal4 = l.selectbox("pal4", pals_list, label_visibility="hidden")

    # Some Easter Egg (Subscribe to Zackstabz)
    if pal4 == "Orserk":
        st.toast('Subscribe to Zackstabz Youtube Channel!', icon='🔺')

    # get combinations
    result = get_combinations(pal4)

    # Create Filter
    possible_pals = []
    for c in result:
        if not c[0] in possible_pals:
            possible_pals.append(c[0])
        if not c[1] in possible_pals:
            possible_pals.append(c[1])

    filter_option = l.selectbox("Filter by parent", possible_pals, index=None)

    # Pal Image
    image_with_wiki(pal4, place=l)
    l.divider()

    with st.container():
        # Return combinations
        r_list = [r1, r2, r3, r4]
        index = 0
        for c in result:
            if filter_option:
                if filter_option in c:
                    with r_list[index].container(border=True):
                        couple = f"{c[0]} + {c[1]}"
                        image_with_wiki(c[0], next_pal=c[1], width=90)
                        index = (index + 1) % len(r_list)
            else:
                with r_list[index].container(border=True):
                    couple = f"{c[0]} + {c[1]}"
                    image_with_wiki(c[0], next_pal=c[1], width=90)
                    index = (index + 1) % len(r_list)
