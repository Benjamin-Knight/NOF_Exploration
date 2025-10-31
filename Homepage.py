# Homepage.py — NOF Dashboards (subtitle callout + greeting tweaks)
from pathlib import Path
from datetime import datetime
import streamlit as st

# Always-on sharing
st.session_state.setdefault("remember_filters", True)

st.set_page_config(
    page_title="NOF Dashboards",
    page_icon="📊",
    layout="wide",
)

# --- App meta (edit these) ---
DEV_NAME    = "David M. Oladoyin"
DEV_EMAIL   = "david.oladoyin@nhs.net"
APP_VERSION = "4.0"

# ---------- Assets ----------
ROOT_ASSETS  = Path(__file__).parents[1] / "assets"
PAGES_ASSETS = Path(__file__).parent / "assets"

def _read_text_safely(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except Exception:
            continue
    try:
        return path.read_bytes().decode("latin-1", errors="ignore")
    except Exception:
        return ""

def _find_logo() -> str:
    for candidate in (ROOT_ASSETS / "NOF_Logo.svg",
                      PAGES_ASSETS / "NOF_Logo.svg",
                      Path("assets/NOF_Logo.svg"),
                      Path("/mnt/data/NOF_Logo.svg")):
        if candidate.is_file():
            try:
                return candidate.read_text(encoding="utf-8")
            except Exception:
                return ""
    return ""

logo_svg = _find_logo()

# ---------- Minimal Material-ish CSS ----------
def _inject_css():
    # Load your ui.css first (if present)
    for p in [Path(__file__).with_name("ui.css"),
              Path(__file__).parent / "assets" / "ui.css",
              Path("ui.css"), Path("assets/ui.css"), Path("/mnt/data/ui.css")]:
        if p.exists():
            st.markdown(f"<style>{_read_text_safely(p)}</style>", unsafe_allow_html=True)
            break

    css = """
    :root{
      /* Description (subtitle) base size; page title is desc + 3px */
      --desc-size: 18px;
      --greeting-size: 60px;
    }

    .page-wrap { max-width: 1200px; margin: 0 auto; }

    /* Header */
    .app-header{ display:flex; align-items:center; gap:12px; margin: 8px 0 6px; }
    .app-logo svg{ height:34px; width:auto; display:block; }

    /* Page title exactly +3px bigger than description */
    #page-title{
      margin:0;
      font-size: calc(var(--desc-size) + 3px) !important;
      line-height: 1.25;
    }

    /* Subtitle callout */
    .home-sub{
      font-size: var(--desc-size);
      line-height: 1.45;
      color:#1E3A8A;
      margin: 10px 0 16px 0;
    }
    .home-sub.callout{
      background: #EFF6FF;            /* light yellow */
      border: 1px solid #BFDBFE;      /* soft amber border */
      border-radius: 12px;
      padding: 12px 14px;
    }

    /* Greeting + date (tight vertical rhythm) */
    .greeting{
      font-size: var(--greeting-size);
      font-weight: 300;
      letter-spacing: -1px;
      line-height: 1.2;
      margin: 4px 0 2px 0;            /* tighter gap above & below */
      color:#585858;
    }
    .greeting-date{
      font-size: 18px;
      font-weight: 600;
      color:#6B7280;
      margin: 0 0 8px 0;              /* minimal space under the date */
      line-height: 1.2;
    }

    /* Streamlit button → card style + LEFT aligned content */
    .stButton > button,
    button[kind][data-baseweb="button"]{
      width: 100% !important;
      height: auto !important;
      padding: 28px 32px !important;
      border-radius: 15px !important;
      border: 1px solid #BFDBFE !important;
      background: #EFF6FF !important;

      /* left alignment & wrapping */
      display: flex !important;
      flex-direction: column !important;
      align-items: flex-start !important;
      justify-content: flex-start !important;
      text-align: left !important;
      white-space: normal !important;

      transition: all 0.2s ease !important;
      cursor: pointer !important;
      color: #1F2937 !important;
      text-decoration: none !important;
    }

    .stButton > button:hover,
    button[kind][data-baseweb="button"]:hover{
      background: #F3F4F6 !important;
      border-color: #D1D5DB !important;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* --- Typography inside the button --- */
    .stButton > button p,
    .stButton > button span{
      font-size: 16px;
      line-height: 24px;
      opacity: 1.0;
      color: #4B5563;
      margin: 0 !important;
      text-align: left !important;
      text-decoration: none !important;
    }
    /* Only the first line acts as the button title */
    .stButton > button p:first-child,
    .stButton > button span:first-child{
      font-size: 32px !important;
      font-weight: 300 !important;
      margin-bottom: 12px !important;
      color: #1F2937 !important;
      opacity: 1 !important;
    }
    
    /* Bold in descriptions keeps normal size */
    .stButton > button strong{
      font-weight: 600;
      font-size: inherit !important;
    }
    
    /* Bottom value/credits — plain text (black & grey, no box) */
    .footer-simple{
      margin: 18px 0 10px;
      color: #585858;              /* black-ish */
      font-size: .95rem;
      line-height: 1.55;
    }
    .footer-simple .meta{
      margin-top: 8px;
      font-size: .8rem;
      color: #8E8E8E;              /* grey */
    }
    .footer-simple .meta a{
      color: inherit;               /* keep it grey like the rest of meta */
      text-decoration: underline;
    }
    
    /* Tighter footer paragraphs */
    .footer-simple{ 
      line-height: 1.4;           /* was 1.55 */
    }
    .footer-simple p{
      margin: 2px 0;              /* cut default <p> margins */
    }
    .footer-simple p + p{
      margin-top: 2px;            /* tiny gap between the 2 lines */
    }
    /* (optional) nudge the credits line up a bit too */
    .footer-simple .meta{
      margin-top: 6px;            /* was 8px */
    }

    /* Tighten the space between the divider line and the footer */
    hr.hr-thin{ 
      margin: 125px 0 0 !important;   /* was 8px 0 6px in ui.css */
    }
    hr.hr-thin + .footer-simple{
      margin-top: 6px !important;   /* was 18px in your footer */
    }
    
    /* === Force compact typography ONLY in the sidebar === */
    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] button[kind][data-baseweb="button"]{
      font-size: 0.90rem !important;     /* <- overall button text size */
      line-height: 1.2 !important;
      padding: 8px 12px !important;
    }

    /* Cancel the "first line = 32px" rule inside the sidebar */
    [data-testid="stSidebar"] .stButton > button span:first-child,
    [data-testid="stSidebar"] .stButton > button p:first-child{
      font-size: inherit !important;      /* inherit the 0.90rem above */
      font-weight: 600 !important;        /* keep it a bit bolder as a title */
      margin-bottom: 0 !important;
    }

    /* Ensure any inner spans/paragraphs also inherit the compact size */
    [data-testid="stSidebar"] .stButton > button span,
    [data-testid="stSidebar"] .stButton > button p{
      font-size: inherit !important;
      line-height: 1.2 !important;
      margin: 0 !important;
      color: inherit !important;
    }
    
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

_inject_css()

# ---------- Helpers ----------
def _ordinal(n: int) -> str:
    return "th" if 11 <= n % 100 <= 13 else {1:"st",2:"nd",3:"rd"}.get(n % 10, "th")

def _greeting(hour: int) -> str:
    if 5 <= hour < 12: return "Good Morning 🌅"
    if 12 <= hour < 17: return "Good Afternoon 🌤️"
    return "Good Evening 🌙"

# --- Global, persistent uploaders (Homepage sidebar) ---
with st.sidebar:
    st.header("📥 Upload data files")

    # Quarterly
    if "quarterly_bytes" not in st.session_state:
        up_q = st.file_uploader(
            "Upload Quarterly CSV",
            type=["csv"],
            key="home_quarterly_uploader",
            help="Columns: Quarter, Domain, Metric, Region, Provider Code, …"
        )
        if up_q is not None:
            st.session_state["quarterly_bytes"] = up_q.getvalue()
            st.session_state["quarterly_name"]  = up_q.name
            st.rerun()
    else:
        st.caption(f"Using: {st.session_state.get('quarterly_name', '(uploaded)')}")
        if st.button("Clear Quarterly", key="home_clear_quarterly"):
            st.session_state.pop("quarterly_bytes", None)
            st.session_state.pop("quarterly_name",  None)
            st.rerun()
    
    # Monthly
    if "monthly_bytes" not in st.session_state:
        up_m = st.file_uploader(
            "Upload Monthly CSV",
            type=["csv"],
            key="home_monthly_uploader",
            help="Columns: Month, Domain, Metric, Region, Provider_Code, …"
        )
        if up_m is not None:
            st.session_state["monthly_bytes"] = up_m.getvalue()
            st.session_state["monthly_name"]  = up_m.name
            st.rerun()
    else:
        st.caption(f"Using: {st.session_state.get('monthly_name', '(uploaded)')}")
        if st.button("Clear Monthly", key="home_clear_monthly"):
            st.session_state.pop("monthly_bytes", None)
            st.session_state.pop("monthly_name",  None)
            st.rerun()


# ---------- PAGE CONTENT ----------
st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

# Header
st.markdown(
    f"""
    <div class="app-header" role="banner" aria-label="Header">
      <div class="app-logo" aria-hidden="true">{logo_svg}</div>
      <h1 id="page-title">NOF Rankings App</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Subtitle in a rounded yellow callout
st.markdown(
    '<p class="home-sub callout">Cross-page filter sharing is <b>enabled</b>. '
    'Selecting a provider on one page will automatically sync it across dashboards.</p>',
    unsafe_allow_html=True,
)

# Greeting + date (bigger greeting, tighter spacing)
now = datetime.now()
st.markdown(f'<div class="greeting">{_greeting(now.hour)}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="greeting-date">{now.strftime("%A")}, {now.day}{_ordinal(now.day)} {now.strftime("%B %Y")}</div>', unsafe_allow_html=True)

st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)  # ← add space here

# ---------- BIG CLICKABLE BUTTONS ----------
col1, col2 = st.columns(2, gap="medium")

with col1:
    button_content = """
**Quarterly Rankings**

Explore provider performance by **quarter**, domain and metric. Includes rank bar chart, sticky metric panel, and KPIs."""
    if st.button(button_content, key="quarterly_btn", use_container_width=True):
        st.switch_page("pages/1_Quarterly_Rankings.py")

with col2:
    button_content = """
**Monthly Rankings**

Monthly view with KPIs, **rank deltas** vs previous month, 12-month trends, and Region vs National comparisons."""
    if st.button(button_content, key="monthly_btn", use_container_width=True):
        st.switch_page("pages/2_Monthly_Rankings.py")

footer_html = f"""
<hr class="hr-thin">
<div class="footer-simple" role="contentinfo" aria-label="About NOF Rankings">
  <p>The NOF Rankings App turns performance data into clear comparisons across domains and providers.</p>
  <p>It helps you spot organizational change fast, focus effort, and prove improvement.</p>
  <div class="meta">
    Developed by: {DEV_NAME} · v{APP_VERSION} ·
    <a href="mailto:{DEV_EMAIL}?subject=NOF%20Rankings%20v{APP_VERSION}%20feedback">Email the developer</a>
  </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # end .page-wrap
