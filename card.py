import pandas as pd
import streamlit as st

GAME_VERSION = "1.0.0"

st.set_page_config(page_title="Palworld Working Pal Cards", page_icon="🐣", layout="wide")

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

    /* Only .st-key-filter_area tilts: each card in the results grid also
       tilts on hover, and tilting the panel and the card together compounded
       their transforms and made it jitter. */
    .st-key-filter_area, .st-key-cards_area {
        background: rgba(255, 255, 255, .55);
        border: 1px solid rgba(255, 45, 120, .18);
        border-radius: 22px;
        padding: 1.5rem 1.6rem;
        box-shadow: 0 10px 34px rgba(255, 45, 120, .08);
        backdrop-filter: blur(6px);
        margin-bottom: 1.2rem;
    }
    .st-key-filter_area {
        will-change: transform;
        transition: transform .15s ease-out, box-shadow .25s ease;
    }
    .st-key-filter_area:hover {
        box-shadow: 0 16px 40px rgba(255, 45, 120, .16);
    }

    .pal-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
        gap: 16px;
        width: 100%;
    }
    .pal-card {
        display: flex;
        flex-direction: column;
        align-items: center;
        background: rgba(255, 255, 255, .80);
        border: 1px solid rgba(255, 45, 120, .16);
        border-radius: 18px;
        padding: 14px 12px 16px 12px;
        box-shadow: 0 4px 14px rgba(67, 48, 94, .06);
        text-decoration: none !important;
        color: #43305E !important;
        /* 'backwards': a 'both' fill would hold `transform` forever and
           override the JS tilt's inline style below */
        animation: fade-up .45s ease backwards;
        animation-delay: calc(var(--i, 0) * 35ms);
        will-change: transform;
        transition: transform .12s ease-out, box-shadow .25s ease, border-color .2s ease;
    }
    .pal-card:hover {
        border-color: rgba(255, 45, 120, .55);
        box-shadow: 0 12px 26px rgba(255, 45, 120, .18);
    }
    @keyframes fade-up {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .pal-card .pal-name {
        font-family: 'Bebas Neue', sans-serif;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 1.3rem;
        color: var(--accent, #FF2D78);
        margin-bottom: 2px;
        text-align: center;
    }
    .pal-card img {
        width: min(120px, 100%);
        aspect-ratio: 1 / 1.2;
        object-fit: contain;
        margin: 4px auto 10px auto;
        transition: transform .2s ease;
        filter: drop-shadow(0 8px 14px rgba(67, 48, 94, .18));
    }
    .pal-card:hover img { transform: scale(1.06); }

    .stat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px 14px;
        width: 100%;
    }
    .stat-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
        font-size: .8rem;
        padding: 3px 8px;
        border-radius: 8px;
        background: rgba(67, 48, 94, .04);
    }
    .stat-item.is-empty { opacity: .35; }
    .stat-item .stat-label {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .stat-item .stat-value {
        font-weight: 700;
        color: var(--accent, #FF2D78);
        flex: 0 0 auto;
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
</style>
''', unsafe_allow_html=True)


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


@st.cache_data
def load_work_suitability():
    sources = pd.read_csv(r'Data/WorkSuitability.csv', sep=',', header=None)
    return sources


df_pals = load_pals()[0]
img_sources = load_images_src()
wikis_url = load_wikis_url()
work_suitability = load_work_suitability()


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


def get_stats(pal):
    """Returns the 12 work-suitability levels for a pal, in the same order as STAT_FIELDS."""
    if pal in work_suitability[0].values:
        row = work_suitability[work_suitability[0] == pal].index[0]
        return [int(work_suitability[col][row]) for col in range(1, 13)]
    return [0] * 12


# ---------------------------- Web App Functions -------------------------- #

STAT_FIELDS = [
    ("🔥", "Kindling"), ("💧", "Watering"), ("🌱", "Planting"), ("⚡", "Eletricity"),
    ("✋", "Handiwork"), ("🥬", "Gathering"), ("🪵", "Lumbering"), ("⛏️", "Mining"),
    ("🥣", "Medicine"), ("❄️", "Cooling"), ("📦", "Transporting"), ("🧺", "Farming"),
]


def generate_card(accent_color, pal, url, image, values, index=0):
    items = ''
    for (icon, label), value in zip(STAT_FIELDS, values):
        is_empty = value == 0
        shown = "—" if is_empty else value
        items += (
            f'<div class="stat-item{" is-empty" if is_empty else ""}">'
            f'<span class="stat-label">{icon} {label}</span>'
            f'<span class="stat-value">{shown}</span>'
            f'</div>'
        )

    inner = (
        f'<span class="pal-name">{pal}</span>'
        f'<img src="{image}" alt="{pal}" loading="lazy"/>'
        f'<div class="stat-grid">{items}</div>'
    )

    delay = min(index, 20)
    style = f'--i:{delay}; --accent:{accent_color};'
    if url:
        return f'<a class="pal-card" style="{style}" href="{url}" target="_blank" rel="noopener">{inner}</a>'
    return f'<div class="pal-card" style="{style}">{inner}</div>'


# ---------------------------- Web App Build -------------------------- #

# Header
with st.container():
    c1, c2, c3 = st.columns([2, 5, 2])

    c1.write("[https://github.com/beckerfelipee](https://github.com/beckerfelipee)")
    c1.link_button("🧮 Breeding Calculator", "https://breeding-calculator-palworld.streamlit.app/",
                    key="nav_btn")

    c2.markdown('<div class="neon-title">Find Your Best Working Pal</div>', unsafe_allow_html=True)

    c3.text(f"Game Version: {GAME_VERSION}", width="stretch", text_alignment="right")

# Filter
with st.container(key="filter_area"):
    options = ["Must Have", "Optional", "Exclude"]

    f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12 = st.columns(12)
    f_kindling = f1.selectbox("🔥 Kindling", options, index=1, key="f_kindling")
    f_watering = f2.selectbox("💧 Watering", options, index=1, key="f_watering")
    f_planting = f3.selectbox("🌱 Planting", options, index=1, key="f_planting")
    f_eletricity = f4.selectbox("⚡ Eletricity", options, index=1, key="f_eletricity")
    f_handiwork = f5.selectbox("✋ Handiwork", options, index=1, key="f_handiwork")
    f_gathering = f6.selectbox("🥬️ Gathering", options, index=1, key="f_gathering")
    f_lumbering = f7.selectbox("🪵 Lumbering", options, index=1, key="f_lumbering")
    f_mining = f8.selectbox("⛏️ Mining", options, index=1, key="f_mining")
    f_medicine = f9.selectbox("🥣 Medicine", options, index=1, key="f_medicine")
    f_cooling = f10.selectbox("❄️ Cooling", options, index=1, key="f_cooling")
    f_transporting = f11.selectbox("📦 Transporting", options, index=1, key="f_transporting")
    f_farming = f12.selectbox("🧺 Farming", options, index=1, key="f_farming")

# Filters in the same order as STAT_FIELDS / get_stats()
filters = [
    f_kindling, f_watering, f_planting, f_eletricity, f_handiwork, f_gathering,
    f_lumbering, f_mining, f_medicine, f_cooling, f_transporting, f_farming,
]


def pal_matches(stats):
    for value, choice in zip(stats, filters):
        if choice == "Must Have" and value == 0:
            return False
        if choice == "Exclude" and value > 0:
            return False
    return True


# Cards
with st.container(key="cards_area"):
    st.subheader("Result", anchor=False)

    matches = [(p, get_stats(p)) for p in get_pals_list()]
    matches = [(p, stats) for p, stats in matches if pal_matches(stats)]

    if not matches:
        st.info("No Pal matches the current filters.")
    else:
        cards = ''.join(
            generate_card("#FF2D78", p, get_wiki(p), get_image(p), stats, i)
            for i, (p, stats) in enumerate(matches)
        )
        st.markdown(f'<div class="pal-grid">{cards}</div>', unsafe_allow_html=True)

# BMC floating widget (same approach as build.py): an external <script src>
# won't run when injected as HTML, so build it in an inline script.
st.html('''
<style>
    /* Shrink the panel the widget opens so it takes less of the screen. Only
       the panel, not the button, to keep the button's Manage app clearance.
       zoom, not transform, since the widget animates open via transform:scale. */
    #bmc-iframe { zoom: 0.85; }
</style>
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
    // Raised (default 18) to clear Streamlit Community Cloud's bottom-right
    // "Manage app" button.
    s.setAttribute('data-y_margin', '60');
    // The widget builds on window "DOMContentLoaded", which already fired;
    // re-fire it on load so the button actually builds.
    s.onload = function () { window.dispatchEvent(new Event('DOMContentLoaded')); };
    document.body.appendChild(s);
})();
</script>
''', unsafe_allow_javascript=True)

# Same 3D tilt behavior as build.py: no "run once" guard since Streamlit
# reruns this script in the same browser tab on every rerun, so handlers are
# always removed and reattached rather than locked in behind a stale boolean.
st.html('''
<script>
    (function() {
        const TILT_CONFIGS = [
            { selector: '.pal-card', maxDeg: 14, lift: -3 },
            { selector: '.st-key-filter_area', maxDeg: 2, lift: 0 },
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
</script>
''', unsafe_allow_javascript=True)
