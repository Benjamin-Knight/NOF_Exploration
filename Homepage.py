# Homepage.py — NOF Dashboards (subtitle callout + greeting tweaks)
from pathlib import Path
from datetime import datetime
import streamlit as st
from io import BytesIO
import pandas as pd

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
APP_VERSION = "7.3"

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
      margin: 100px 0 0 !important;   /* was 8px 0 6px in ui.css */
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
    
    /* Make disabled buttons obviously disabled */
    .stButton > button:disabled{
      opacity: 0.45 !important;
      cursor: not-allowed !important;
      transform: none !important;
      box-shadow: none !important;
    }
    .stButton > button:disabled:hover{
      background: #EFF6FF !important;
      border-color: #BFDBFE !important;
    }
    
    """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

_inject_css()

# ==== Dialog look & feel overrides (Material-ish) ====
_DIALOG_CSS = """
/* Center the dialog vertically & horizontally */
[data-testid="stDialog"]{
  position: fixed !important;
  inset: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;

  /* overlay look */
  background: rgba(17,24,39,.35) !important;

  /* 🔴 remove any border/outline and rounding on the dark background */
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  border-radius: 0 !important;
}


/* Panel decoration */
[data-testid="stDialog"] > div{
  border-radius: 12px !important;     /* ⬅ smaller corners */
  border: 1px solid #E5E7EB !important;
  box-shadow: 0 12px 32px rgba(0,0,0,.18),
              0 6px 14px rgba(0,0,0,.10) !important;
}

/* Title weight/spacing */
[data-testid="stDialog"] h1, 
[data-testid="stDialog"] h2 {
  letter-spacing: .2px;
}

/* Close button — no border, red hover, accessible focus ring */
[data-testid="stDialog"] [aria-label="Close"]{
  border: none !important;              /* ← remove border */
  border-radius: 10px !important;
  padding: 2px 6px !important;
  background: transparent !important;
  transition: background .15s ease;
}

[data-testid="stDialog"] [aria-label="Close"]:hover{
  background: rgba(239,68,68,.5) !important;  /* red @ 50% */
  color: #fff !important;
}

[data-testid="stDialog"] [aria-label="Close"]:focus,
[data-testid="stDialog"] [aria-label="Close"]:focus-visible{
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(239,68,68,.35) !important;  /* subtle focus ring */
  border: none !important;                                /* ensure no border */
}

[data-testid="stDialog"] [aria-label="Close"]:hover{
  background: rgba(239, 68, 68, .5) !important;  /* red-500 @ 50% */
  color: #FFFFFF !important;
}

/* Inside the dialog, make buttons compact (override your global big buttons) */
[data-testid="stDialog"] .stButton > button{
  width: auto !important;                 /* not full-width */
  padding: 10px 16px !important;          /* smaller */
  border-radius: 12px !important;
  font-size: 16px !important;
  line-height: 1.2 !important;
  box-shadow: 0 3px 8px rgba(0,0,0,.10) !important;
  transform: none !important;             /* cancel global hover lift */
}
[data-testid="stDialog"] .stButton > button:hover{
  transform: none !important;
}
/* Padding for the dialog body */
.welcome-body{
  padding-left: 14px;   /* ⬅ adds left padding to the text block */
}


/* keep your red-hover */
[data-testid="stDialog"] [aria-label="Close"]:hover{
  background: rgba(239,68,68,.5) !important;  /* red @ 50% */
  color:#fff !important;
  border-color: rgba(239,68,68,.6) !important;
}

/* remove default blue ring and give a rounded focus ring that follows the radius */
[data-testid="stDialog"] [aria-label="Close"]:focus,
[data-testid="stDialog"] [aria-label="Close"]:focus-visible{
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(59,130,246,.35) !important;  /* blue focus ring */
  border-radius: 10px !important;                          /* same radius */
}

"""
st.markdown(f"<style>{_DIALOG_CSS}</style>", unsafe_allow_html=True)

# ==== One-time welcome popup (first visit only) ==============================
# Show once per browser session; close via ✕ or button (outside click also dismisses).
st.session_state.setdefault("welcome_seen_v62", False)

@st.dialog("Welcome to the NOF Rankings App")
def _welcome_popup():
    st.markdown(
        """
<div class="welcome-body">
  <p><strong>What you can do here</strong></p>
  <ul>
    <li>Upload <strong>Monthly</strong> or <strong>Quarterly</strong> CSVs from the left sidebar.</li>
    <li>Explore <strong>Monthly</strong> and <strong>Quarterly</strong> rankings with KPIs &amp; distributions.</li>
    <li>Use <strong>Compare Providers</strong> for side-by-side analysis.</li>
    <li>Set a <strong>default provider</strong> that syncs across pages.</li>
    <li>See trends with <strong>regional (dashed)</strong> and <strong>national (dotted)</strong> weighted averages.</li>
    <li>Visit the <strong>Foundation Group</strong> page to <em>stack multiple providers</em>, view distribution &amp; trend together, and scan domain cards in one place.</li>
  </ul>
</div>
        """,
        unsafe_allow_html=True
    )

# Open the dialog exactly once per session
if not st.session_state["welcome_seen_v62"]:
    st.session_state["welcome_seen_v62"] = True   # mark as shown for this session
    _welcome_popup()
    
# ============================================================================

# ---------- Helpers ----------
def _ordinal(n: int) -> str:
    return "th" if 11 <= n % 100 <= 13 else {1:"st",2:"nd",3:"rd"}.get(n % 10, "th")

def _greeting(hour: int) -> str:
    if 5 <= hour < 12: return "Good Morning 🌅"
    if 12 <= hour < 17: return "Good Afternoon 🌤️"
    return "Good Evening 🌙"

# --- Pull provider codes from an uploaded CSV (fast + robust) ---
def _provider_codes_from_bytes(raw: bytes) -> list[str]:
    """
    Reads only the provider code column from the CSV (if present).
    Handles both 'Provider Code' (Quarterly) and 'Provider_Code' (Monthly).
    Returns a sorted unique list of non-empty strings.
    """
    if not raw:
        return []
    # Read header only to find the correct column name
    try:
        header = pd.read_csv(BytesIO(raw), nrows=0)
    except Exception:
        return []
    cols = list(header.columns)

    # Try likely column names in order
    candidates = [
        "Provider Code", "Provider_Code", "Provider code",
        "ProviderCode", "Provider", "Provider_ID", "Provider Id"
    ]
    target = next((c for c in candidates if c in cols), None)
    if not target:
        return []

    # Read just that column
    try:
        ser = pd.read_csv(BytesIO(raw), usecols=[target], dtype={target: "string"})[target]
    except Exception:
        return []

    ser = ser.fillna("").str.strip()
    codes = sorted(x for x in ser.unique().tolist() if x)
    return codes

@st.cache_data(show_spinner=False)
def _codes_and_names_from_bytes(file_bytes: bytes) -> pd.DataFrame:
    """Return a DataFrame with columns: Provider_Code, Provider_Name."""
    if not file_bytes:
        return pd.DataFrame(columns=["Provider_Code", "Provider_Name"])
    try:
        df = pd.read_csv(BytesIO(file_bytes), dtype=str)
    except Exception:
        return pd.DataFrame(columns=["Provider_Code", "Provider_Name"])

    # Normalise columns: "Provider Code" / "Provider_Code" → provider_code, etc.
    norm = {c: c.strip().lower().replace(" ", "_") for c in df.columns}
    df = df.rename(columns=norm)

    if "provider_code" not in df.columns:
        return pd.DataFrame(columns=["Provider_Code", "Provider_Name"])
    if "provider_name" not in df.columns:
        df["provider_name"] = ""

    out = df[["provider_code", "provider_name"]].copy()
    out = out.rename(columns={"provider_code": "Provider_Code", "provider_name": "Provider_Name"})
    for c in out.columns:
        out[c] = out[c].astype(str).str.strip()

    out = (out.dropna(subset=["Provider_Code"])
               .drop_duplicates()
               .sort_values(["Provider_Code", "Provider_Name"]))
    return out[["Provider_Code", "Provider_Name"]]


def _build_provider_labels_and_map() -> tuple[list[str], dict[str, str]]:
    """
    Combine Monthly + Quarterly uploads, de-dupe by code, prefer first non-empty name.
    Returns:
      - labels: ["CODE — NAME", ...] (or "CODE" if name empty)
      - label_to_code: mapping from label to CODE
    """
    frames = []
    if "quarterly_bytes" in st.session_state:
        frames.append(_codes_and_names_from_bytes(st.session_state["quarterly_bytes"]))
    if "monthly_bytes" in st.session_state:
        frames.append(_codes_and_names_from_bytes(st.session_state["monthly_bytes"]))

    if not frames:
        return [], {}

    df = pd.concat(frames, ignore_index=True)
    df = (df.sort_values(["Provider_Code", "Provider_Name"], ascending=[True, True])
            .groupby("Provider_Code", as_index=False)
            .agg(Provider_Name=("Provider_Name", "first")))

    labels, label_to_code = [], {}
    for _, r in df.iterrows():
        code = (r["Provider_Code"] or "").strip()
        name = (r["Provider_Name"] or "").strip()
        label = f"{code} — {name}" if name else code
        labels.append(label)
        label_to_code[label] = code
    return labels, label_to_code


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
            
    st.markdown("---")
    st.subheader("🎯 Default provider")

    labels, label_to_code = _build_provider_labels_and_map()

    if labels:
        # Preselect currently remembered code if present
        current_code = st.session_state.get("shared_provider_code")
        if current_code:
            try:
                default_idx = next(i for i, lab in enumerate(labels) if label_to_code[lab] == current_code)
            except StopIteration:
                default_idx = 0
        else:
            default_idx = 0

        chosen_label = st.selectbox(
            "Set the default provider for the app",
            labels,
            index=default_idx,
            key="home_default_provider_select",
            help="This applies across all pages. You can still change it on each page."
        )

        # Persist only the CODE for cross-page use
        st.session_state["shared_provider_code"] = label_to_code[chosen_label]

        # Optional: quick clear
        if st.button("Clear default", key="home_clear_default_provider"):
            st.session_state.pop("shared_provider_code", None)
            st.rerun()
    else:
        st.caption("Upload a Monthly or Quarterly CSV to set a default provider.")


# ---------- PAGE CONTENT ----------
# Header (moved OUTSIDE the page-wrap for consistent alignment)
st.markdown(
    f"""
    <div class="app-header" role="banner" aria-label="Header">
      <div class="app-logo" aria-hidden="true">{logo_svg}</div>
      <h1 id="page-title">NOF Rankings App</h1>
    </div>
    """, unsafe_allow_html=True,
)

# Now open the optional content wrapper
st.markdown('<div class="page-wrap">', unsafe_allow_html=True)


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
show_compare = ("monthly_bytes" in st.session_state) or ("quarterly_bytes" in st.session_state)

col1, col2 = st.columns(2, gap="medium")

with col1:
    # --- Quarterly (top-left)
    q_btn = """
**Quarterly Rankings**

Explore provider performance by **quarter**, domain and metric. Includes rank bar chart, sticky metric panel, and KPIs."""
    if st.button(q_btn, key="quarterly_btn", use_container_width=True):
        st.switch_page("pages/1_Quarterly_Rankings.py")

    # Small spacer between stacked buttons
    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

    # --- Compare Providers (under Quarterly)
    c_btn = """
**Compare Providers**

Side-by-side view of two providers across **Monthly** or **Quarterly** data with KPIs, distribution, and domain cards."""
    if st.button(c_btn, key="compare_btn", use_container_width=True):
        st.switch_page("pages/3_Compare_Providers.py")

with col2:
    # --- Monthly (right column)
    m_btn = """
**Monthly Rankings**

Monthly view with KPIs, **rank deltas** vs previous month, 12-month trends, and Region vs National comparisons."""
    if st.button(m_btn, key="monthly_btn", use_container_width=True):
        st.switch_page("pages/2_Monthly_Rankings.py")
        
    # Small spacer between stacked buttons
    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

    # --- Compare Providers (under Quarterly)
    fg_btn = """
**Foundation Group**

A Foundation level overview across **Monthly** or **Quarterly** data with KPIs, distribution, and domain cards."""
    if st.button(fg_btn, key="foundation_group_btn", use_container_width=True):
        st.switch_page("pages/4_Foundation_Group.py")


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
