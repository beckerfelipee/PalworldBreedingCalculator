import pandas as pd
import streamlit as st

# ---------------------------- Localization --------------------------------- #

GAME_VERSION = "1.0.0"

LANGUAGES = [
    {"code": "en", "name": "English"},
    {"code": "pt-BR", "name": "Português (BR)"},
    {"code": "es", "name": "Español"},
    {"code": "de", "name": "Deutsch"},
    {"code": "ja", "name": "日本語"},
]

TRANSLATIONS = {
    "en": {
        "game_version": "Game Version: {version}",
        "secondary_server": "🐢 Site slow? Try our secondary server!",
        "title": "Palworld Breeding Calculator",
        "tips_button": "Some tips!",
        "toast_wiki_tip": "You can click on the pal image to open their wiki.",
        "first_pal": "First Pal",
        "second_pal": "Second Pal",
        "result_label": "Result",
        "search_header": "Search for Pal",
        "filter_label": "Filter by parent",
        "choose_option": "Choose an option",
        "subscribe_toast": "Subscribe to {channel}'s YouTube Channel!",
        "gender_exception_toast": "In-game, this pair's result depends on parent gender (Katress Ignis or Wixen Noct). This calculator always shows Katress Ignis.",
        "whats_new_title": "🧬 New in 1.0: Mutation & Genetics",
        "whats_new_body": "**Mutation**: breeding now has a small chance to hatch a *mutated* egg, the same species, but with higher stats and a unique passive skill.\n\n**Genetic Recombination**: fuse genes from Legendary Pals to pass specific traits on to the offspring.\n\n**New cakes** change the odds. Deluxe Vegetable Cake raises mutation chance, Special Cake improves passive inheritance, and Vegetable Cake yields two eggs.\n\nℹ️ This calculator shows the **species** a pair produces. Mutation and genetics affect stats and passives, not which species hatches.",
        "coffee_dialog_title": "Enjoying the calculator?",
        "support_button": "Support",
        "coffee_dialog_body": "This tool is free and ad-free. If it saved you some time, a coffee helps keep it online and up to date!",
    },
    "pt-BR": {
        "game_version": "Versão do Jogo: {version}",
        "secondary_server": "🐢 Site lento? Tente nosso servidor secundário!",
        "title": "Calculadora de Reprodução Palworld",
        "tips_button": "Algumas dicas!",
        "toast_wiki_tip": "Você pode clicar na imagem do Pal para abrir sua wiki.",
        "first_pal": "Primeiro Pal",
        "second_pal": "Segundo Pal",
        "result_label": "Resultado",
        "search_header": "Buscar Pal",
        "filter_label": "Filtrar por progenitor",
        "choose_option": "Escolha uma opção",
        "subscribe_toast": "Se inscreva no canal do {channel} no YouTube!",
        "gender_exception_toast": "No jogo, o resultado desse par depende do sexo dos pais (Katress Ignis ou Wixen Noct). Esta calculadora sempre mostra Katress Ignis.",
        "whats_new_title": "🧬 Novo na 1.0: Mutação e Genética",
        "whats_new_body": "**Mutação**: a reprodução agora tem uma pequena chance de chocar um ovo *mutante*, a mesma espécie, mas com atributos maiores e uma habilidade passiva única.\n\n**Recombinação Genética**: combine os genes de Pals Lendários para passar características específicas para o filhote.\n\n**Novos bolos** mudam as chances: o Bolo de Vegetais Deluxe aumenta a mutação, o Bolo Especial melhora a herança de passivas e o Bolo de Vegetais dá dois ovos.\n\nℹ️ Esta calculadora mostra a **espécie** que um par gera. Mutação e genética afetam atributos e passivas, não qual espécie nasce.",
        "coffee_dialog_title": "Curtindo a calculadora?",
        "support_button": "Apoiar",
        "coffee_dialog_body": "Esta ferramenta é gratuita e sem anúncios. Se ela te economizou um tempo, um café ajuda a manter tudo no ar e atualizado!",
    },
    "es": {
        "game_version": "Versión del Juego: {version}",
        "secondary_server": "🐢 ¿Sitio lento? ¡Prueba nuestro servidor secundario!",
        "title": "Calculadora de Cría de Palworld",
        "tips_button": "¡Algunos consejos!",
        "toast_wiki_tip": "Puedes hacer clic en la imagen del Pal para abrir su wiki.",
        "first_pal": "Primer Pal",
        "second_pal": "Segundo Pal",
        "result_label": "Resultado",
        "search_header": "Buscar Pal",
        "filter_label": "Filtrar por progenitor",
        "choose_option": "Elige una opción",
        "subscribe_toast": "¡Suscríbete al canal de YouTube de {channel}!",
        "gender_exception_toast": "En el juego, el resultado de esta pareja depende del sexo de los padres (Katress Ignis o Wixen Noct). Esta calculadora siempre muestra Katress Ignis.",
        "whats_new_title": "🧬 Nuevo en 1.0: Mutación y Genética",
        "whats_new_body": "**Mutación**: la cría ahora tiene una pequeña probabilidad de eclosionar un huevo *mutado*, la misma especie, pero con mejores estadísticas y una habilidad pasiva única.\n\n**Recombinación Genética**: fusiona genes de Pals Legendarios para transmitir rasgos específicos a la cría.\n\n**Nuevos pasteles** cambian las probabilidades: el Pastel de Verduras Deluxe aumenta la mutación, el Pastel Especial mejora la herencia de pasivas y el Pastel de Verduras da dos huevos.\n\nℹ️ Esta calculadora muestra la **especie** que produce una pareja. La mutación y la genética afectan estadísticas y pasivas, no qué especie nace.",
        "coffee_dialog_title": "¿Te gusta la calculadora?",
        "support_button": "Apoyar",
        "coffee_dialog_body": "Esta herramienta es gratuita y sin anuncios. Si te ahorró algo de tiempo, ¡un café ayuda a mantenerla en línea y actualizada!",
    },
    "de": {
        "game_version": "Spielversion: {version}",
        "secondary_server": "🐢 Seite langsam? Probiere unseren Zweitserver!",
        "title": "Palworld Zucht-Rechner",
        "tips_button": "Ein paar Tipps!",
        "toast_wiki_tip": "Klicke auf das Bild eines Pals, um sein Wiki zu öffnen.",
        "first_pal": "Erster Pal",
        "second_pal": "Zweiter Pal",
        "result_label": "Ergebnis",
        "search_header": "Pal suchen",
        "filter_label": "Nach Elternteil filtern",
        "choose_option": "Option auswählen",
        "subscribe_toast": "Abonniere {channel}s YouTube-Kanal!",
        "gender_exception_toast": "Im Spiel hängt das Ergebnis dieses Paares vom Geschlecht der Eltern ab (Katress Ignis oder Wixen Noct). Dieser Rechner zeigt immer Katress Ignis.",
        "whats_new_title": "🧬 Neu in 1.0: Mutation & Genetik",
        "whats_new_body": "**Mutation**: beim Züchten gibt es jetzt eine kleine Chance, ein *mutiertes* Ei auszubrüten, dieselbe Art, aber mit höheren Werten und einer einzigartigen passiven Fähigkeit.\n\n**Genetische Rekombination**: verschmelze Gene von legendären Pals, um bestimmte Merkmale an den Nachwuchs weiterzugeben.\n\n**Neue Kuchen** verändern die Chancen: der Deluxe-Gemüsekuchen erhöht die Mutation, der Spezialkuchen verbessert die Vererbung passiver Fähigkeiten und der Gemüsekuchen liefert zwei Eier.\n\nℹ️ Dieser Rechner zeigt die **Art**, die ein Paar hervorbringt. Mutation und Genetik beeinflussen Werte und passive Fähigkeiten, nicht welche Art schlüpft.",
        "coffee_dialog_title": "Gefällt dir der Rechner?",
        "support_button": "Unterstützen",
        "coffee_dialog_body": "Dieses Tool ist kostenlos und werbefrei. Wenn es dir Zeit gespart hat, hilft ein Kaffee, es online und aktuell zu halten!",
    },
    "ja": {
        "game_version": "ゲームバージョン: {version}",
        "secondary_server": "🐢 サイトが遅い?サブサーバーをお試しください!",
        "title": "パルワールド 配合計算機",
        "tips_button": "ちょっとしたヒント!",
        "toast_wiki_tip": "パルの画像をクリックするとWikiが開きます。",
        "first_pal": "1匹目のパル",
        "second_pal": "2匹目のパル",
        "result_label": "結果",
        "search_header": "パルを検索",
        "filter_label": "親でフィルター",
        "choose_option": "オプションを選択",
        "subscribe_toast": "{channel}のYouTubeチャンネルに登録しよう!",
        "gender_exception_toast": "ゲーム内では、この組み合わせの結果は親の性別によって変わります(Katress IgnisまたはWixen Noct)。この計算機では常にKatress Ignisを表示します。",
        "whats_new_title": "🧬 1.0の新要素:突然変異と遺伝",
        "whats_new_body": "**突然変異**:配合で低確率で*変異した*卵が孵るようになりました。同じ種族ですが、ステータスが高く、固有のパッシブスキルを持ちます。\n\n**遺伝子組み換え**:伝説のパルの遺伝子を組み合わせ、特定の特性を子に受け継がせます。\n\n**新しいケーキ**が確率を変えます。デラックス野菜ケーキは変異率を上げ、スペシャルケーキはパッシブの遺伝を高め、野菜ケーキは卵を2つ生みます。\n\nℹ️ この計算機は組み合わせが生む**種族**を表示します。突然変異と遺伝はステータスとパッシブに影響しますが、どの種族が孵るかは変えません。",
        "coffee_dialog_title": "計算機は役に立ちましたか?",
        "support_button": "応援する",
        "coffee_dialog_body": "このツールは無料で広告もありません。時間の節約になったなら、コーヒー1杯でサイトの運営と更新を応援できます!",
    },
}

VALID_LANG_CODES = {entry["code"] for entry in LANGUAGES}


def persist_lang():
    # Persist the language in the URL (?lang=xx) so it survives a reload.
    st.query_params["lang"] = st.session_state.lang


if "lang" not in st.session_state:
    saved = st.query_params.get("lang")
    st.session_state.lang = saved if saved in VALID_LANG_CODES else "en"


def t(key, **kwargs):
    text = TRANSLATIONS[st.session_state.lang][key]
    return text.format(**kwargs) if kwargs else text


st.set_page_config(page_title=t("title"), page_icon="🐣", layout="wide")

# ---------------------------- Retrowave Miami Theme ----------------------- #

st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Righteous&family=Bebas+Neue&display=swap');

    .stApp {
        background:
            radial-gradient(1100px 600px at 88% -10%, rgba(255, 139, 61, .25), transparent 60%),
            radial-gradient(1000px 700px at -10% 15%, rgba(255, 45, 120, .18), transparent 55%),
            radial-gradient(900px 550px at 50% 115%, rgba(155, 93, 229, .18), transparent 60%),
            linear-gradient(175deg, #FFFDFA 0%, #FFF1F6 45%, #FFE9F0 100%);
        background-attachment: fixed;
    }
    [data-testid="stHeader"] { background: transparent; }

    h1, h2, h3 {
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    .neon-title {
        display: block;
        text-align: center;
        font-family: 'Righteous', sans-serif;
        letter-spacing: .4px;
        font-size: 2.7rem;
        line-height: 1.15;
        margin: 0;
        background: linear-gradient(90deg, #FF2D78, #FF8B3D, #FFC93D, #FF2D78);
        background-size: 300% 100%;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-slide 8s linear infinite;
    }
    @keyframes gradient-slide {
        0%   { background-position: 0% 50%; }
        100% { background-position: 300% 50%; }
    }

    /* Column is kept as wide as the coffee-button column so the language
       selectbox (which always stretches to its column's full width) can be
       capped back down and pushed to the right edge via max-width + margin. */
    .st-key-lang {
        max-width: 180px;
        margin-left: auto;
    }

    .st-key-calculator_area, .st-key-search_area {
        background: rgba(255, 255, 255, .55);
        border: 1px solid rgba(255, 45, 120, .18);
        border-radius: 22px;
        padding: 1.5rem 1.6rem;
        box-shadow: 0 10px 34px rgba(255, 45, 120, .08);
        backdrop-filter: blur(6px);
        margin-bottom: 1.2rem;
    }
    .st-key-calculator_area, .st-key-search_area {
        will-change: transform;
        transition: transform .15s ease-out, box-shadow .25s ease;
    }
    .st-key-calculator_area:hover, .st-key-search_area:hover {
        box-shadow: 0 16px 40px rgba(255, 45, 120, .16);
    }

    .pal-float {
        display: block;
        width: min(170px, 100%);
        aspect-ratio: 1 / 1.2;
        margin: 0 auto;
        animation: floaty 5s ease-in-out infinite;
    }
    .pal-float img {
        display: block;
        width: 100%;
        height: 100%;
        object-fit: contain;
        object-position: center;
        transition: transform .25s ease;
        filter: drop-shadow(0 10px 18px rgba(255, 45, 120, .20));
    }
    .pal-float:hover img { transform: scale(1.05); }
    @keyframes floaty {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-3px); }
    }

    .combo-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 14px;
        width: 100%;
    }
    .combo-card {
        display: flex;
        align-items: center;
        justify-content: space-evenly;
        gap: 4px;
        background: rgba(255, 255, 255, .80);
        border: 1px solid rgba(255, 45, 120, .16);
        border-radius: 16px;
        padding: 14px 8px 10px 8px;
        box-shadow: 0 4px 14px rgba(67, 48, 94, .06);
        /* 'backwards': a 'both' fill would hold `transform` forever and
           override the JS tilt's inline style below */
        animation: fade-up .45s ease backwards;
        animation-delay: calc(var(--i, 0) * 35ms);
        will-change: transform;
        transition: transform .12s ease-out, box-shadow .25s ease, border-color .2s ease;
    }
    .combo-card:hover {
        border-color: rgba(255, 45, 120, .55);
        box-shadow: 0 12px 26px rgba(255, 45, 120, .18);
    }
    @keyframes fade-up {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .combo-pal {
        flex: 1 1 0;
        min-width: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        text-decoration: none !important;
        color: #43305E !important;
    }
    .combo-pal .name {
        font-size: .85rem;
        font-weight: 600;
        max-width: 100%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        text-align: center;
    }
    .combo-pal img {
        width: min(92px, 100%);
        aspect-ratio: 1 / 1;
        object-fit: contain;
        transition: transform .2s ease;
        filter: drop-shadow(0 4px 8px rgba(67, 48, 94, .15));
    }
    a.combo-pal:hover img { transform: scale(1.1) rotate(-2deg); }
    .combo-plus {
        flex: 0 0 auto;
        font-size: 1.3rem;
        font-weight: 700;
        padding-top: 1.4rem;
        background: linear-gradient(135deg, #FF2D78, #FF8B3D);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stButton button, .stLinkButton a {
        border-radius: 999px !important;
        transition: transform .15s ease, box-shadow .2s ease, border-color .2s ease !important;
    }
    .stButton button:hover, .stLinkButton a:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(255, 45, 120, .28);
    }

    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #FF2D78, #FF8B3D, transparent) !important;
    }

    /* Hidden until the auto-fit script below sizes and reveals it via
       .fit-fade, avoiding a flash of unsized/wrapped text on load or
       language switch. */
    .st-key-parent1_wrap h1, .st-key-parent1_wrap h2, .st-key-parent1_wrap h3,
    .st-key-parent2_wrap h1, .st-key-parent2_wrap h2, .st-key-parent2_wrap h3,
    .st-key-result_wrap h1, .st-key-result_wrap h2, .st-key-result_wrap h3,
    .st-key-search_header_wrap h1, .st-key-search_header_wrap h2, .st-key-search_header_wrap h3,
    .st-key-secondary_btn button, .st-key-secondary_btn a,
    .st-key-tips_btn button, .st-key-tips_btn a,
    .st-key-filter_select label,
    .neon-title {
        opacity: 0;
    }
    .fit-fade {
        animation: fit-fade-in .35s ease forwards;
    }
    /* `animation` is a shorthand, so .fit-fade alone would replace
       .neon-title's own gradient-slide instead of running both. */
    .neon-title.fit-fade {
        animation: gradient-slide 8s linear infinite, fit-fade-in .35s ease forwards;
    }
    @keyframes fit-fade-in {
        from { opacity: 0; transform: translateY(5px); }
        to   { opacity: 1; transform: translateY(0); }
    }
</style>
''', unsafe_allow_html=True)


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


def image_with_wiki(pal, place=st, width=200):
    href = get_wiki(pal)
    src = get_image(pal)
    img = f'<img src="{src}" width="{width}" height="{round(width * 1.2)}" alt="{pal}"/>'
    if href:
        body = f'<a class="pal-float" href="{href}" target="_blank" rel="noopener">{img}</a>'
    else:
        body = f'<span class="pal-float">{img}</span>'
    place.markdown(body, unsafe_allow_html=True)


def combo_card_html(pal1, pal2, index=0):
    """A parent-pair card that scales fluidly inside the combo grid."""
    def side(pal):
        src = get_image(pal)
        url = get_wiki(pal)
        inner = f'<span class="name">{pal}</span><img src="{src}" alt="{pal}" loading="lazy"/>'
        if url:
            return f'<a class="combo-pal" href="{url}" target="_blank" rel="noopener">{inner}</a>'
        return f'<div class="combo-pal">{inner}</div>'

    delay = min(index, 20)
    return f'<div class="combo-card" style="--i:{delay}">{side(pal1)}<span class="combo-plus">+</span>{side(pal2)}</div>'


# ---------------------------- Web App Build -------------------------- #

# One-shot coffee popup: shown once per session (so once per visit/reload).
@st.dialog(t("coffee_dialog_title"))
def coffee_dialog():
    st.markdown(
        '<style>'
        '.bmc-support{display:inline-flex;align-items:center;gap:8px;background:#FF813F;'
        'padding:10px 22px;border-radius:999px;font-weight:600;'
        'box-shadow:0 4px 12px rgba(255,129,63,.35);'
        'transition:transform .15s ease,box-shadow .2s ease;}'
        # !important: Streamlit's link color/underline is more specific.
        '.bmc-support, .bmc-support span{color:#fff !important;text-decoration:none !important;}'
        '.bmc-support:hover{transform:translateY(-2px);box-shadow:0 8px 18px rgba(255,129,63,.45);}'
        '</style>'
        '<div style="display:flex;justify-content:center;margin-bottom:.6rem;">'
        '<a class="bmc-support" href="https://www.buymeacoffee.com/beckerfelipee" '
        'target="_blank" rel="noopener">'
        '<img src="https://cdn.buymeacoffee.com/widget/assets/coffee%20cup.svg" alt="" '
        'style="height:22px;width:22px;">'
        f'<span>{t("support_button")}</span></a></div>',
        unsafe_allow_html=True)
    st.markdown(t("coffee_dialog_body"))

if "coffee_popup_shown" not in st.session_state:
    st.session_state.coffee_popup_shown = True
    coffee_dialog()

# BMC floating widget: an external <script src> won't run when injected as HTML,
# so build it in an inline script. The guard avoids duplicates on rerun.
st.html('''
<script>
(function () {
    if (window.__bmcWidgetInjected) return;
    window.__bmcWidgetInjected = true;
    const s = document.createElement('script');
    s.setAttribute('data-name', 'BMC-Widget');
    s.setAttribute('data-cfasync', 'false');
    s.src = 'https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js';
    s.setAttribute('data-id', 'beckerfelipee');
    s.setAttribute('data-description', 'Support me on Buy me a coffee!');
    s.setAttribute('data-message', '');
    s.setAttribute('data-color', '#FF813F');
    s.setAttribute('data-position', 'Right');
    s.setAttribute('data-x_margin', '18');
    s.setAttribute('data-y_margin', '18');
    // The widget builds on window "DOMContentLoaded", which already fired;
    // re-fire it on load so the button actually builds.
    s.onload = function () { window.dispatchEvent(new Event('DOMContentLoaded')); };
    document.body.appendChild(s);
})();
</script>
''', unsafe_allow_javascript=True)

# Header
with st.container():
    # Bottom-aligned so the GitHub link lines up with the language selectbox.
    c1, c2, c3 = st.columns([2, 5, 2], vertical_alignment="bottom")

    c1.write("[https://github.com/beckerfelipee](https://github.com/beckerfelipee)")

    # A <div>, not a heading tag: Streamlit auto-attaches an anchor icon to
    # any h1-h6, which throws off centering across languages of varying length.
    c2.markdown(f'<div class="neon-title">{t("title")}</div>', unsafe_allow_html=True)

    c3.text(t("game_version", version=GAME_VERSION), width="stretch", text_alignment="right")
    lang_codes = [entry["code"] for entry in LANGUAGES]
    name_by_code = {entry["code"]: entry["name"] for entry in LANGUAGES}
    # Bound via `key` (format_func only controls the label) rather than an
    # `index=` computed from session_state: without a stable key Streamlit
    # can't tell "user just picked something" from "default changed", so
    # the first click only registers on the next rerun.
    c3.selectbox("", lang_codes, format_func=lambda code: name_by_code[code],
                 key="lang", on_change=persist_lang)

with st.expander(t("whats_new_title")):
    st.markdown(t("whats_new_body"))

# Calculator Area

with st.container(key="calculator_area"):
    left, space1, center1, space2, center2, space3, center3, space4, right = st.columns([3, 1, 2, 1, 2, 1, 2, 1, 3])
    pals_list = get_pals_list()

    # Tips
    if left.button(t("tips_button"), key="tips_btn"):
        st.toast(t("toast_wiki_tip"), icon='🚀')

    # Parent 1
    with center1.container(key="parent1_wrap"):
        st.header(t("first_pal"), anchor=False, text_alignment="center")
    pal1 = center1.selectbox("pal1", pals_list, label_visibility="hidden")
    image_with_wiki(pal1, place=center1)

    # Parent 2
    with center2.container(key="parent2_wrap"):
        st.header(t("second_pal"), anchor=False, text_alignment="center")
    pal2 = center2.selectbox("pal2", pals_list, label_visibility="hidden")
    image_with_wiki(pal2, place=center2)

    # Result
    with center3.container(key="result_wrap"):
        st.header(t("result_label"), anchor=False, text_alignment="center")
    center3.text("")
    pal3 = get_children(pal1, pal2)
    center3.code(pal3)
    image_with_wiki(pal3, place=center3)

    if pal1 == "Bushi" and pal2 == "Penking":
        st.toast(t("subscribe_toast", channel="Gaubss"), icon='🔺')

    # Katress + Wixen's real result depends on parent gender, which this
    # calculator's single-outcome-per-pair data can't represent.
    if {pal1, pal2} == {"Katress", "Wixen"}:
        st.toast(t("gender_exception_toast"), icon='🧬')

    st.title("")

# Search by Result
with st.container(key="search_area"):
    with st.container(key="search_header_wrap"):
        st.header(t("search_header"), anchor=False)
    l, s1, results_area = st.columns([7, 1, 37])

    pal4 = l.selectbox("pal4", pals_list, label_visibility="hidden")

    if pal4 == "Orserk":
        st.toast(t("subscribe_toast", channel="Zackstabz"), icon='🔺')

    result = get_combinations(pal4)

    possible_pals = []
    for c in result:
        if not c[0] in possible_pals:
            possible_pals.append(c[0])
        if not c[1] in possible_pals:
            possible_pals.append(c[1])

    filter_option = l.selectbox(
        t("filter_label"),
        possible_pals, index=None, placeholder=t("choose_option"), key="filter_select")

    image_with_wiki(pal4, place=l)
    l.divider()

    combos = [c for c in result if not filter_option or filter_option in c]
    grid = '<div class="combo-grid">' + ''.join(
        combo_card_html(a, b, i) for i, (a, b) in enumerate(combos)) + '</div>'
    results_area.markdown(grid, unsafe_allow_html=True)

    st.title("")

# Subtle 3D tilt following the mouse. st.html injects straight into the main
# document (no iframe), so one delegated listener reaches every tiltable
# element. No "run once" guard: Streamlit reruns this script in the same
# browser tab on every rerun, so handlers are always removed and reattached
# rather than locked in behind a stale boolean.
st.html('''
<script>
    (function() {
        const TILT_CONFIGS = [
            { selector: '.combo-card', maxDeg: 16, lift: -3 },
            { selector: '.st-key-calculator_area', maxDeg: 2, lift: 0 },
            { selector: '.st-key-search_area', maxDeg: 0, lift: 0 },
        ];
        let current = null;

        function findTarget(target) {
            if (!target || !target.closest) return null;
            for (const cfg of TILT_CONFIGS) {
                const el = target.closest(cfg.selector);
                if (el) return { el, cfg };
            }
            return null;
        }

        function onMove(e) {
            const found = findTarget(e.target);
            if (current && (!found || found.el !== current.el)) {
                current.el.style.transform = '';
            }
            current = found;
            if (current) {
                const { el, cfg } = current;
                const r = el.getBoundingClientRect();
                const px = (e.clientX - r.left) / r.width - 0.5;
                const py = (e.clientY - r.top) / r.height - 0.5;
                const rx = (-py * cfg.maxDeg).toFixed(2);
                const ry = (px * cfg.maxDeg).toFixed(2);
                el.style.transform =
                    `perspective(1400px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(${cfg.lift}px)`;
            }
        }

        function onLeave() {
            if (current) { current.el.style.transform = ''; current = null; }
        }

        if (window.__tiltMouseMove) {
            document.removeEventListener('mousemove', window.__tiltMouseMove);
            document.removeEventListener('mouseleave', window.__tiltMouseLeave);
        }
        window.__tiltMouseMove = onMove;
        window.__tiltMouseLeave = onLeave;
        document.addEventListener('mousemove', onMove, {passive: true});
        document.addEventListener('mouseleave', onLeave);
    })();

    // Shrinks translated labels to the largest font that fits on one line
    // instead of wrapping, by measuring real rendered width (a char-count
    // guess can't work across fonts/kerning/CJK glyph widths).
    (function() {
        const FIT_TARGETS = [
            { key: 'parent1_wrap', tags: ['h1', 'h2', 'h3'] },
            { key: 'parent2_wrap', tags: ['h1', 'h2', 'h3'] },
            { key: 'result_wrap', tags: ['h1', 'h2', 'h3'] },
            { key: 'search_header_wrap', tags: ['h1', 'h2', 'h3'] },
            { key: 'secondary_btn', tags: ['button', 'a'] },
            { key: 'tips_btn', tags: ['button', 'a'] },
            { key: 'filter_select', tags: ['label'] },
        ];
        const MIN_SCALE = 0.5;

        function fitOne(el) {
            // Cache the CSS-default size once so repeated passes shrink
            // from the same baseline instead of compounding.
            if (!el.dataset.fitBase) {
                el.style.fontSize = '';
                el.dataset.fitBase = parseFloat(getComputedStyle(el).fontSize) || 16;
            }
            const base = parseFloat(el.dataset.fitBase);
            el.style.whiteSpace = 'nowrap';
            let size = base;
            el.style.fontSize = size + 'px';
            const minSize = base * MIN_SCALE;
            let guard = 0;
            while (el.scrollWidth > el.clientWidth + 1 && size > minSize && guard < 40) {
                size -= Math.max(size * 0.04, 0.3);
                el.style.fontSize = size + 'px';
                guard++;
            }

            const text = el.textContent;
            if (el.dataset.fitText !== text) {
                el.classList.remove('fit-fade');
                void el.offsetWidth; // force reflow so the animation restarts
                el.classList.add('fit-fade');
            }
            el.dataset.fitText = text;
        }

        function fitAll() {
            for (const { key, tags } of FIT_TARGETS) {
                const root = document.querySelector('.st-key-' + key);
                if (!root) continue;
                for (const tag of tags) {
                    root.querySelectorAll(tag).forEach(fitOne);
                }
            }
            document.querySelectorAll('.neon-title').forEach(fitOne);
        }

        let debounceHandle = null;
        function scheduleFit() {
            if (debounceHandle) clearTimeout(debounceHandle);
            debounceHandle = setTimeout(fitAll, 60);
        }

        if (window.__fitObserver) window.__fitObserver.disconnect();
        if (window.__fitResizeHandler) window.removeEventListener('resize', window.__fitResizeHandler);

        window.__fitObserver = new MutationObserver(scheduleFit);
        window.__fitObserver.observe(document.body, {
            childList: true, subtree: true, characterData: true,
        });
        window.__fitResizeHandler = scheduleFit;
        window.addEventListener('resize', window.__fitResizeHandler);

        scheduleFit();
    })();
</script>
''', unsafe_allow_javascript=True)
