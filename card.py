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
def load_images_src():
    sources = pd.read_csv(r'Data/Images.csv', sep=',', header=None)
    return sources


@st.cache_data
def load_wikis_url():
    sources = pd.read_csv(r'Data/Wikis.csv', sep=',', header=None)
    return sources


# Start data
df_pals = load_pals()[0]
img_sources = load_images_src()
wikis_url = load_wikis_url()


# ---------------------------- Data Functions ------------------------- #

def get_pals_list():
    pals = []
    for pal in df_pals[0]:
        pals.append(pal)
    return pals


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


# ---------------------------- Web App Functions -------------------------- #

def generate_card(card_color, table_color, pal, url, image, values):
    new_values = [" " if value == "0" else value for value in values]

    kindling, watering, planting, eletricity, handiwork, gathering, \
    lumbering, mining, medicine, cooling, transporting, farming = new_values

    size = "140"
    card = f'''
            <style>
                .card:hover {{
                    transform: scale(1.03);
                    transition: all 0.3s ease;
                }}
            </style>
            <a href="{url}" style="text-decoration: none; color: inherit;">
                <div class="card" style="background-color: {card_color}; margin-top: 25px; margin-bottom: 25px; 
                padding: 8px; border-radius: 10px; text-align: center; box-shadow: 0px 0px 10px #444;">
                    <p style="font-size: 28px; font-weight: bold;margin-bottom: 0px;">{pal}</p>
                    <img height={size} width={size} src="{image}">
                    <p style="font-size: 16px; margin-bottom: 20px;">
                    <table style="width:98%; margin-top: 20px; margin-bottom: 10px;
                    margin-left: auto; margin-right: auto; font-size: 14px; 
                    background-color: {table_color};">
                        <tr>
                            <td style="text-align: left;">🔥 Kindling:</td>
                            <td style="text-align: center;">{kindling}</td>
                            <td style="text-align: left;">💧 Watering:</td>
                            <td style="text-align: center;">{watering}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left;">🌱 Planting:</td>
                            <td style="text-align: center;">{planting}</td>
                            <td style="text-align: left;">⚡ Eletricity:</td>
                            <td style="text-align: center;">{eletricity}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left;">✋ Handiwork:</td>
                            <td style="text-align: center;">{handiwork}</td>
                            <td style="text-align: left;">🥬️ Gathering:</td>
                            <td style="text-align: center;">{gathering}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left;">🪵 Lumbering:</td>
                            <td style="text-align: center;">{lumbering}</td>
                            <td style="text-align: left;">⛏️ Mining:</td>
                            <td style="text-align: center;">{mining}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left;">🥣 Medicine:</td>
                            <td style="text-align: center;">{medicine}</td>
                            <td style="text-align: left;">❄️ Cooling:</td>
                            <td style="text-align: center;">{cooling}</td>
                        </tr>
                        <tr>
                            <td style="text-align: left;">📦 Transporting:</td>
                            <td style="text-align: center;">{transporting}</td>
                            <td style="text-align: left;">🧺 Farming:</td>
                            <td style="text-align: center;">{farming}</td>
                        </tr>
                    </table>
                </div>
            </a>'''
    return card


# ---------------------------- Web App Build -------------------------- #

# Header
with st.container():
    h1, h2, h3 = st.columns([4, 3, 4])
    h1.text("Game Version: 0.1.4.0")
    h1.write("[https://github.com/beckerfelipee](https://github.com/beckerfelipee)")
    h1.link_button("Buy me a coffee!", "https://www.buymeacoffee.com/beckerfelipee")
    h2.link_button("Palworld Breeding Calculator", "https://breeding-calculator-palworld.streamlit.app/",
                   use_container_width=True)
    h2.title('Find your best :green[Working Pal]', anchor=False)
# st.divider()

# Filter
with st.container(border=True):
    options = ["Must Have", "Optional", "Exclude"]

    f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12 = st.columns(12)
    f_kindling = f1.selectbox("🔥 Kindling", options, index=1)
    f_watering = f2.selectbox("💧 Watering", options, index=1)
    f_planting = f3.selectbox("🌱 Planting", options, index=1)
    f_eletricity = f4.selectbox("⚡ Eletricity", options, index=1)
    f_handiwork = f5.selectbox("✋ Handiwork", options, index=1)
    f_gathering = f6.selectbox("🥬️ Gathering", options, index=1)
    f_lumbering = f7.selectbox("🪵 Lumbering", options, index=1)
    f_mining = f8.selectbox("⛏️ Mining", options, index=1)
    f_medicine = f9.selectbox("🥣 Medicine", options, index=1)
    f_cooling = f10.selectbox("❄️ Cooling", options, index=1)
    f_transporting = f11.selectbox("📦 Transporting", options, index=1)
    f_farming = f12.selectbox("🧺 Farming", options, index=1)

# Cards
with st.container(border=True):
    # Header
    rc = st.columns([9, 2])
    rc[0].subheader("Result: ", anchor=False)
    with rc[1].expander("Customize"):
        card_bg = st.color_picker("Change Cards background!", "#1A9BE4")
        # table_bg = st.color_picker("Change Tables background!", "#1A9BE4")

    # Cards Body
    n = 8
    l, s1, r1, s2, r2, s3, r3, s4, r4 = st.columns([n, 1, n, 1, n, 1, n, 1, n])
    r_list = [l, r1, r2, r3, r4]
    pals = get_pals_list()
    values = ["0", "2", "0", "0", "2", "0", "0", "2", "0", "2", "2", "0"]
    index = 0
    for p in pals:
        wiki = get_wiki(p)
        image = get_image(p)
        c = r_list[index]
        with c.container():
            c.markdown(generate_card(card_bg, card_bg, p, wiki, image, values), unsafe_allow_html=True)
            # c.divider()
            index = (index + 1) % len(r_list)