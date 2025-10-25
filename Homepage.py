# Homepage.py
# -----------------------------------------------------------
# NOF Dashboards — Home
# - Persistent "Remember filters across pages" toggle
# - Modern two-card layout
# - Robust CSS loader (fixes UnicodeDecodeError on Windows)
# -----------------------------------------------------------

from pathlib import Path
import streamlit as st

# -----------------------------------------------------------
# Page config
# -----------------------------------------------------------
st.set_page_config(
    page_title="NOF Dashboards",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------
# CSS helpers
# -----------------------------------------------------------
def _read_text_safely(path: Path) -> str:
    """
    Read text with robust fallbacks for Windows encoding issues.
    Tries UTF-8 first, then UTF-8 with BOM, then cp1252, then latin-1 (ignore errors).
    """
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc, errors="strict")
        except UnicodeDecodeError:
            continue
        except Exception:
            continue
    # Last-resort: bytes decode ignoring errors
    try:
        return path.read_bytes().decode("latin-1", errors="ignore")
    except Exception:
        return ""  # fail silently; page still renders

def _inject_css():
    # Load Material Icons (optional). Safe to remove if you prefer.
    st.markdown(
        '<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">',
        unsafe_allow_html=True,
    )

    # Try a few likely locations for ui.css
    candidates = [
        Path(__file__).with_name("ui.css"),
        Path(__file__).parent / "assets" / "ui.css",
        Path("ui.css"),
        Path("assets/ui.css"),
        Path("/mnt/data/ui.css"),  # fallback for your working folder
    ]
    for p in candidates:
        if p.exists():
            css_text = _read_text_safely(p)
            if css_text:
                st.markdown(f"<style>{css_text}</style>", unsafe_allow_html=True)
            break

    # Home-only accents (kept minimal; your ui.css stays the main styling)
    home_css = """
    .home-hero{
      display:flex; align-items:center; gap:12px;
      margin: 10px 0 8px 0;
    }
    .home-sub{
      color:#4B5563; margin: 4px 0 14px 0; line-height:1.5;
    }
    .home-grid{
      display:grid; grid-template-columns: 1fr 1fr;
      gap: 22px; margin-top: 6px;
    }
    @media (max-width: 1100px){
      .home-grid{ grid-template-columns: 1fr; }
    }
    .home-card{
      background:#fff;
      border:1px solid #E5E7EB; border-radius:16px;
      padding:18px 18px;
      box-shadow:0 1px 2px rgba(0,0,0,.05);
      transition: transform .06s ease, box-shadow .2s ease;
    }
    .home-card:hover{
      transform: translateY(-2px);
      box-shadow: 0 8px 16px rgba(0,0,0,.06);
    }
    .home-card h3{
      margin:0 0 6px 0; font-weight:800; color:#111827;
    }
    .home-card p{ margin:0; color:#4B5563; }
    .home-actions{ margin-top:10px; }
    .material{
      font-family: 'Material Icons', sans-serif;
      font-weight: normal; font-style: normal;
      font-size: 20px; display:inline-block; line-height:1;
      vertical-align: -3px; margin-right:6px; opacity:.9;
    }
    """
    st.markdown(f"<style>{home_css}</style>", unsafe_allow_html=True)

_inject_css()

# -----------------------------------------------------------
# One source of truth for the Remember toggle
# -----------------------------------------------------------
st.session_state.setdefault("remember_filters", True)

def _on_remember_change():
    # When turning OFF, tidy up any cross-page shared selection
    if not st.session_state["remember_filters"]:
        st.session_state.pop("shared_provider_code", None)

# Header
st.markdown(
    """
    <div class="home-hero">
      <h1 id="page-title">NOF Dashboards</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# The global toggle (bound directly to the session key)
st.toggle("Remember filters across pages", key="remember_filters", on_change=_on_remember_change)
st.markdown(
    '<p class="home-sub">When this is on, choosing a provider on one page will preselect it on the other (if available).</p>',
    unsafe_allow_html=True,
)

# -----------------------------------------------------------
# Cards
# -----------------------------------------------------------
st.markdown('<div class="home-grid">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        """
        <div class="home-card">
          <h3><span class="material">insights</span>Quarterly Rankings</h3>
          <p>Explore provider performance by <b>quarter</b>, domain and metric. Includes rank bar chart, sticky metric panel, and KPIs.</p>
          <div class="home-actions"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Prefer page_link; fallback to switch_page or a link button if not available
    opened = False
    try:
        st.page_link("pages/1_Quarterly_Rankings.py", label="Open Quarterly Dashboard", icon="📈")
        opened = True
    except Exception:
        pass
    if not opened:
        try:
            if st.button("📈 Open Quarterly Dashboard"):
                st.switch_page("pages/1_Quarterly_Rankings.py")
            opened = True
        except Exception:
            st.link_button("📈 Open Quarterly Dashboard", "./pages/1_Quarterly_Rankings.py")

with col2:
    st.markdown(
        """
        <div class="home-card">
          <h3><span class="material">calendar_month</span>Monthly Rankings</h3>
          <p>Monthly view with KPIs, <b>rank deltas</b> vs previous month, 12-month trend, and Region vs National comparison.</p>
          <div class="home-actions"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    opened = False
    try:
        st.page_link("pages/2_Monthly_Rankings.py", label="Open Monthly Dashboard", icon="📅")
        opened = True
    except Exception:
        pass
    if not opened:
        try:
            if st.button("📅 Open Monthly Dashboard"):
                st.switch_page("pages/2_Monthly_Rankings.py")
            opened = True
        except Exception:
            st.link_button("📅 Open Monthly Dashboard", "./pages/2_Monthly_Rankings.py")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------
# Footer tip
# -----------------------------------------------------------
st.caption("Tip: toggle ‘Remember filters across pages’ here any time. It controls cross-page provider sharing.")
