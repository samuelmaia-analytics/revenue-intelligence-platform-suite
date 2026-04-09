from __future__ import annotations

from html import escape


EXECUTIVE_THEME_OPTIONS = {
    "deep_navy": {
        "name": "Deep Navy Control Tower",
        "primary": "#14532d",
        "secondary": "#0f172a",
        "accent": "#0f766e",
        "surface": "#f4f7fb",
        "surface_alt": "#e8eef5",
        "surface_soft": "#fbfdff",
        "text": "#111827",
        "muted": "#5b6474",
        "border": "#d8e1eb",
        "hero_start": "#0f172a",
        "hero_end": "#123b58",
        "success": "#15803d",
        "warning": "#b45309",
        "danger": "#b91c1c",
        "info": "#1d4ed8",
        "chip_surface": "rgba(255, 255, 255, 0.12)",
    },
    "petroleum": {
        "name": "Petroleum Executive Grid",
        "primary": "#0f766e",
        "secondary": "#111827",
        "accent": "#1d4ed8",
        "surface": "#f6f8fb",
        "surface_alt": "#e5edf4",
        "surface_soft": "#fcfdff",
        "text": "#111827",
        "muted": "#667085",
        "border": "#d5dee9",
        "hero_start": "#0f172a",
        "hero_end": "#134e4a",
        "success": "#15803d",
        "warning": "#c2410c",
        "danger": "#b91c1c",
        "info": "#0f766e",
        "chip_surface": "rgba(255, 255, 255, 0.14)",
    },
    "graphite_blue": {
        "name": "Graphite Blue Boardroom",
        "primary": "#1d4ed8",
        "secondary": "#111827",
        "accent": "#0f766e",
        "surface": "#f5f7fb",
        "surface_alt": "#e9eef6",
        "surface_soft": "#ffffff",
        "text": "#0f172a",
        "muted": "#596579",
        "border": "#d7dfeb",
        "hero_start": "#111827",
        "hero_end": "#1e3a8a",
        "success": "#15803d",
        "warning": "#b45309",
        "danger": "#dc2626",
        "info": "#2563eb",
        "chip_surface": "rgba(255, 255, 255, 0.14)",
    },
}

DEFAULT_THEME_KEY = "deep_navy"


def _resolve_palette(theme_key: str = DEFAULT_THEME_KEY) -> dict[str, str]:
    return EXECUTIVE_THEME_OPTIONS.get(theme_key, EXECUTIVE_THEME_OPTIONS[DEFAULT_THEME_KEY]).copy()


def apply_dashboard_theme(st_module, theme_key: str = DEFAULT_THEME_KEY) -> dict[str, str]:
    palette = _resolve_palette(theme_key)
    st_module.markdown(
        f"""
        <style>
        :root {{
            --rip-primary: {palette["primary"]};
            --rip-secondary: {palette["secondary"]};
            --rip-accent: {palette["accent"]};
            --rip-surface: {palette["surface"]};
            --rip-surface-alt: {palette["surface_alt"]};
            --rip-surface-soft: {palette["surface_soft"]};
            --rip-text: {palette["text"]};
            --rip-muted: {palette["muted"]};
            --rip-border: {palette["border"]};
            --rip-hero-start: {palette["hero_start"]};
            --rip-hero-end: {palette["hero_end"]};
            --rip-success: {palette["success"]};
            --rip-warning: {palette["warning"]};
            --rip-danger: {palette["danger"]};
            --rip-info: {palette["info"]};
            --rip-chip-surface: {palette["chip_surface"]};
            --rip-shadow-soft: 0 18px 45px rgba(15, 23, 42, 0.06);
            --rip-shadow-medium: 0 22px 55px rgba(15, 23, 42, 0.10);
            --rip-radius-xl: 28px;
            --rip-radius-lg: 22px;
            --rip-radius-md: 18px;
            --rip-radius-sm: 14px;
            --rip-space-1: 0.35rem;
            --rip-space-2: 0.6rem;
            --rip-space-3: 0.9rem;
            --rip-space-4: 1.2rem;
            --rip-space-5: 1.6rem;
            --rip-space-6: 2.2rem;
        }}

        html,
        body,
        [data-testid="stAppViewContainer"],
        [data-testid="stAppViewContainer"] > .main,
        .stApp {{
            background:
                radial-gradient(circle at top left, rgba(29, 78, 216, 0.05), transparent 24%),
                radial-gradient(circle at top right, rgba(15, 118, 110, 0.07), transparent 22%),
                linear-gradient(180deg, var(--rip-surface) 0%, #edf2f8 100%);
            color: var(--rip-text) !important;
        }}

        .stApp,
        .stApp div,
        .stApp p,
        .stApp li,
        .stApp span,
        .stApp strong,
        .stApp label,
        .stApp td,
        .stApp th,
        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6,
        .stApp ul,
        .stApp ol,
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] *,
        [data-testid="stCaptionContainer"],
        [data-testid="stAlertContent"],
        [data-testid="stText"] {{
            color: var(--rip-text) !important;
        }}

        [data-testid="stHeader"] {{
            background: rgba(244, 247, 251, 0.78);
            border-bottom: 1px solid rgba(15, 23, 42, 0.06);
            backdrop-filter: blur(12px);
        }}

        .block-container {{
            max-width: 1380px;
            padding-top: 1.15rem;
            padding-bottom: 3.2rem;
            padding-left: 1.3rem;
            padding-right: 1.3rem;
        }}

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(180deg, rgba(15, 23, 42, 0.98) 0%, rgba(16, 24, 40, 0.98) 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
            min-width: 300px;
        }}

        [data-testid="stSidebar"] *,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] li,
        [data-testid="stSidebar"] a,
        [data-testid="stSidebar"] button,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] h4,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] [data-testid="stSidebarNav"],
        [data-testid="stSidebar"] [data-testid="stSidebarNav"] *,
        [data-testid="stSidebar"] .stPageLink,
        [data-testid="stSidebar"] .stPageLink *,
        [data-testid="stSidebar"] .st-emotion-cache-16txtl3,
        [data-testid="stSidebar"] .st-emotion-cache-1cypcdb,
        [data-testid="stSidebar"] .st-emotion-cache-10oheav {{
            color: #e7edf6 !important;
            opacity: 1 !important;
        }}

        [data-testid="stSidebarUserContent"] {{
            padding-top: 0.55rem;
            padding-left: 0.55rem;
            padding-right: 0.55rem;
        }}

        [data-testid="stSidebar"] .stPageLink {{
            margin-bottom: 0.2rem;
        }}

        [data-testid="stSidebarNav"] {{
            padding-top: 0.35rem;
        }}

        [data-testid="stSidebarNav"] a {{
            border-radius: 14px;
            margin-bottom: 0.25rem;
            padding: 0.45rem 0.55rem;
            color: #e7edf6 !important;
            opacity: 1 !important;
        }}

        [data-testid="stSidebarNav"] a:hover {{
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff !important;
            opacity: 1;
        }}

        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: linear-gradient(135deg, rgba(20, 83, 45, 0.38), rgba(15, 118, 110, 0.32));
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #ffffff !important;
            opacity: 1;
        }}

        [data-testid="stSidebar"] .stPageLink a,
        [data-testid="stSidebar"] .stPageLink a * {{
            color: #e7edf6 !important;
            opacity: 1 !important;
        }}

        [data-testid="stSidebar"] .stPageLink a:hover,
        [data-testid="stSidebar"] .stPageLink a:hover * {{
            color: #ffffff !important;
        }}

        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] .rip-sidebar-muted {{
            color: rgba(231, 237, 246, 0.78) !important;
        }}

        .rip-sidebar-group-label {{
            color: #ffffff !important;
            font-size: 0.72rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            margin: 0.65rem 0 0.45rem 0;
        }}

        .rip-sidebar-divider {{
            height: 1px;
            background: rgba(255, 255, 255, 0.08);
            margin: 0.65rem 0;
        }}

        .stButton > button,
        .stLinkButton > a {{
            border-radius: 999px !important;
            border: 1px solid transparent !important;
            background: linear-gradient(135deg, var(--rip-primary) 0%, var(--rip-accent) 100%) !important;
            color: #f8fafc !important;
            font-weight: 700 !important;
            letter-spacing: 0.01em;
            min-height: 2.85rem;
            padding: 0.55rem 1rem !important;
            box-shadow: 0 14px 28px rgba(15, 23, 42, 0.14);
            transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease;
        }}

        .stButton > button:hover,
        .stLinkButton > a:hover {{
            transform: translateY(-1px);
            filter: brightness(1.03);
            box-shadow: 0 18px 32px rgba(15, 23, 42, 0.18);
        }}

        .stButton > button:focus,
        .stLinkButton > a:focus {{
            outline: none !important;
            box-shadow: 0 0 0 4px rgba(29, 78, 216, 0.14), 0 18px 32px rgba(15, 23, 42, 0.18) !important;
        }}

        .stSelectbox > div[data-baseweb="select"] > div,
        .stMultiSelect > div[data-baseweb="select"] > div,
        .stTextInput > div > div > input,
        .stNumberInput input,
        .stDateInput input {{
            border-radius: 14px !important;
            border: 1px solid var(--rip-border) !important;
            background: rgba(255, 255, 255, 0.92) !important;
            box-shadow: none !important;
        }}

        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stMultiSelect label,
        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stNumberInput label,
        [data-testid="stSidebar"] .stTextInput label {{
            color: #f8fafc !important;
            font-weight: 600 !important;
        }}

        [data-testid="stSidebar"] .stSelectbox > div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] .stMultiSelect > div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] .stTextInput > div > div > input,
        [data-testid="stSidebar"] .stNumberInput input,
        [data-testid="stSidebar"] .stDateInput input {{
            background: #f8fafc !important;
            color: #111827 !important;
            border: 1px solid rgba(255, 255, 255, 0.10) !important;
        }}

        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span,
        [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] span,
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div,
        [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] div {{
            color: #111827 !important;
        }}

        .stSlider [data-baseweb="slider"] {{
            padding-top: 0.4rem;
        }}

        .stSlider [role="slider"] {{
            box-shadow: 0 0 0 4px rgba(29, 78, 216, 0.12);
            background: var(--rip-primary);
        }}

        .stSlider [data-testid="stTickBarMin"],
        .stSlider [data-testid="stTickBarMax"] {{
            background: var(--rip-primary);
        }}

        div[data-testid="stAlert"] {{
            border-radius: var(--rip-radius-md);
            border: 1px solid var(--rip-border);
            background: rgba(255, 255, 255, 0.92) !important;
            box-shadow: var(--rip-shadow-soft);
        }}

        div[data-baseweb="notification"] {{
            border-radius: var(--rip-radius-md);
            background: rgba(255, 255, 255, 0.95) !important;
        }}

        div[data-testid="stDataFrame"] {{
            border-radius: var(--rip-radius-md);
            overflow: hidden;
            border: 1px solid var(--rip-border);
            background: rgba(255, 255, 255, 0.95);
            box-shadow: var(--rip-shadow-soft);
        }}

        div[data-testid="stTabs"] button {{
            border-radius: 999px;
            padding: 0.55rem 0.95rem;
            border: 1px solid transparent;
            color: var(--rip-muted);
            font-weight: 600;
        }}

        div[data-testid="stTabs"] button[aria-selected="true"] {{
            background: rgba(20, 83, 45, 0.10);
            border-color: rgba(20, 83, 45, 0.16);
            color: var(--rip-primary);
        }}

        .rip-intro-banner {{
            padding: var(--rip-space-5);
            border-radius: var(--rip-radius-xl);
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.96) 0%, rgba(250, 252, 255, 0.94) 100%);
            border: 1px solid rgba(15, 23, 42, 0.06);
            box-shadow: var(--rip-shadow-soft);
            margin-bottom: 0.2rem;
        }}

        .rip-intro-eyebrow,
        .rip-section-label {{
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            width: fit-content;
            padding: 0.26rem 0.62rem;
            border-radius: 999px;
            background: rgba(29, 78, 216, 0.06);
            color: var(--rip-info) !important;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 0.7rem;
        }}

        .rip-intro-banner h1 {{
            margin: 0;
            color: var(--rip-secondary) !important;
            font-size: clamp(2rem, 4vw, 3.35rem);
            line-height: 0.98;
            letter-spacing: -0.03em;
        }}

        .rip-intro-subtitle {{
            margin: 0.85rem 0 0 0;
            color: var(--rip-muted) !important;
            font-size: 1.02rem;
            line-height: 1.7;
            max-width: 58rem;
        }}

        .rip-intro-notice {{
            margin-top: 1rem;
            border-radius: var(--rip-radius-sm);
            padding: 0.9rem 1rem;
            background: linear-gradient(135deg, rgba(29, 78, 216, 0.06), rgba(15, 118, 110, 0.06));
            border: 1px solid rgba(29, 78, 216, 0.10);
            color: var(--rip-secondary) !important;
            font-size: 0.92rem;
            line-height: 1.55;
        }}

        .rip-topbar {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            padding: 1rem 1.15rem;
            border-radius: var(--rip-radius-lg);
            border: 1px solid var(--rip-border);
            background: rgba(255, 255, 255, 0.76);
            box-shadow: var(--rip-shadow-soft);
        }}

        .rip-topbar-label {{
            color: var(--rip-muted) !important;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 0.35rem;
        }}

        .rip-topbar-title {{
            color: var(--rip-secondary) !important;
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}

        .rip-topbar-summary {{
            max-width: 40rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.7rem;
            align-items: center;
            justify-content: flex-end;
            color: var(--rip-muted) !important;
            font-size: 0.94rem;
            line-height: 1.6;
            text-align: right;
        }}

        .rip-hero {{
            padding: 1.45rem 1.55rem;
            border-radius: var(--rip-radius-xl);
            background:
                radial-gradient(circle at top right, rgba(255, 255, 255, 0.11), transparent 24%),
                linear-gradient(135deg, var(--rip-hero-start) 0%, #102c43 52%, var(--rip-hero-end) 100%);
            color: #f8fafc !important;
            box-shadow: var(--rip-shadow-medium);
        }}

        .rip-hero h1,
        .rip-hero h2,
        .rip-hero h3,
        .rip-hero p,
        .rip-hero div,
        .rip-hero span {{
            color: #f8fafc !important;
        }}

        .rip-kicker {{
            color: rgba(248, 250, 252, 0.72) !important;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            margin-bottom: 0.7rem;
        }}

        .rip-title {{
            margin: 0;
            font-size: clamp(1.7rem, 2.6vw, 2.5rem);
            line-height: 1.02;
            letter-spacing: -0.03em;
            color: #f8fafc !important;
        }}

        .rip-subtitle {{
            margin-top: 0.9rem;
            max-width: 56rem;
            font-size: 1rem;
            line-height: 1.7;
            color: rgba(248, 250, 252, 0.82) !important;
        }}

        .rip-chip-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            margin-top: 1rem;
        }}

        .rip-chip,
        .rip-inline-pill,
        .rip-status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            border-radius: 999px;
            padding: 0.32rem 0.68rem;
            font-size: 0.78rem;
            font-weight: 700;
            white-space: nowrap;
        }}

        .rip-chip {{
            background: var(--rip-chip-surface);
            border: 1px solid rgba(255, 255, 255, 0.14);
            color: #f8fafc !important;
        }}

        .rip-inline-pill {{
            background: rgba(29, 78, 216, 0.06);
            border: 1px solid rgba(29, 78, 216, 0.10);
            color: var(--rip-info) !important;
        }}

        .rip-status-badge {{
            background: rgba(148, 163, 184, 0.10);
            border: 1px solid rgba(148, 163, 184, 0.16);
            color: var(--rip-muted) !important;
        }}

        .rip-status-badge.is-positive {{
            background: rgba(21, 128, 61, 0.10);
            border-color: rgba(21, 128, 61, 0.14);
            color: var(--rip-success) !important;
        }}

        .rip-status-badge.is-risk {{
            background: rgba(185, 28, 28, 0.10);
            border-color: rgba(185, 28, 28, 0.14);
            color: var(--rip-danger) !important;
        }}

        .rip-status-badge.is-warning {{
            background: rgba(180, 83, 9, 0.10);
            border-color: rgba(180, 83, 9, 0.14);
            color: var(--rip-warning) !important;
        }}

        .rip-status-badge.is-info {{
            background: rgba(29, 78, 216, 0.10);
            border-color: rgba(29, 78, 216, 0.14);
            color: var(--rip-info) !important;
        }}

        .rip-stat-grid,
        .rip-insight-grid,
        .rip-signal-grid,
        .rip-module-grid,
        .rip-command-grid,
        .rip-command-bar {{
            display: grid;
            gap: 1rem;
            margin-bottom: 0.25rem;
        }}

        .rip-stat-grid {{
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }}

        .rip-insight-grid,
        .rip-signal-grid {{
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }}

        .rip-module-grid {{
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }}

        .rip-command-grid {{
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }}

        .rip-command-bar {{
            grid-template-columns: 1.3fr 1fr 1fr 1fr;
        }}

        .rip-stat-card,
        .rip-insight-card,
        .rip-story-block,
        .rip-module-card,
        .rip-card,
        .rip-command-card {{
            border-radius: var(--rip-radius-lg);
            border: 1px solid rgba(15, 23, 42, 0.06);
            background: rgba(255, 255, 255, 0.94);
            box-shadow: var(--rip-shadow-soft);
        }}

        .rip-stat-card {{
            padding: 1.05rem 1.05rem 1rem 1.05rem;
            position: relative;
            overflow: hidden;
        }}

        .rip-stat-card::before {{
            content: "";
            position: absolute;
            inset: 0 0 auto 0;
            height: 4px;
            background: linear-gradient(90deg, var(--rip-primary), var(--rip-accent));
            opacity: 0.92;
        }}

        .rip-stat-card.is-featured {{
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(244, 247, 251, 0.98) 100%);
            box-shadow: var(--rip-shadow-medium);
        }}

        .rip-stat-card.is-featured .rip-stat-value {{
            color: var(--rip-secondary) !important;
            font-size: 2.35rem;
        }}

        .rip-stat-card.is-risk::before {{
            background: linear-gradient(90deg, #f97316, var(--rip-danger));
        }}

        .rip-stat-card.is-opportunity::before {{
            background: linear-gradient(90deg, var(--rip-primary), var(--rip-success));
        }}

        .rip-stat-card.is-governance::before {{
            background: linear-gradient(90deg, var(--rip-info), var(--rip-accent));
        }}

        .rip-stat-header,
        .rip-module-header,
        .rip-story-heading {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 0.75rem;
        }}

        .rip-stat-header {{
            margin-bottom: 0.9rem;
        }}

        .rip-stat-label,
        .rip-module-category,
        .rip-insight-type {{
            color: var(--rip-muted) !important;
            font-size: 0.77rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.11em;
        }}

        .rip-stat-value {{
            color: var(--rip-primary) !important;
            font-size: 2rem;
            line-height: 1;
            letter-spacing: -0.03em;
            font-weight: 800;
            margin-bottom: 0.65rem;
        }}

        .rip-stat-footer {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }}

        .rip-stat-delta {{
            color: var(--rip-secondary) !important;
            font-weight: 700;
            font-size: 0.92rem;
        }}

        .rip-stat-caption,
        .rip-insight-action,
        .rip-card-muted,
        .rip-module-meta,
        .rip-footer {{
            color: var(--rip-muted) !important;
            line-height: 1.55;
        }}

        .rip-insight-card,
        .rip-story-block,
        .rip-module-card,
        .rip-card,
        .rip-command-card {{
            padding: 1.15rem;
        }}

        .rip-insight-card h3,
        .rip-story-heading h3,
        .rip-module-card h3,
        .rip-card h3 {{
            margin: 0 0 0.55rem 0;
            color: var(--rip-secondary) !important;
            font-size: 1.1rem;
            letter-spacing: -0.02em;
        }}

        .rip-insight-card p,
        .rip-story-block p,
        .rip-module-card p {{
            margin: 0.3rem 0 0 0;
            color: var(--rip-text) !important;
            line-height: 1.65;
        }}

        .rip-insight-action {{
            margin-top: 0.8rem;
            padding-top: 0.8rem;
            border-top: 1px solid rgba(15, 23, 42, 0.08);
            font-weight: 600;
        }}

        .rip-signal-card {{
            border-radius: var(--rip-radius-lg);
            padding: 1.05rem 1.1rem;
            background:
                radial-gradient(circle at top right, rgba(255, 255, 255, 0.08), transparent 24%),
                linear-gradient(150deg, var(--rip-secondary) 0%, #14324d 60%, var(--rip-primary) 100%);
            box-shadow: var(--rip-shadow-medium);
        }}

        .rip-signal-card .rip-signal-title {{
            color: rgba(248, 250, 252, 0.66) !important;
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 0.55rem;
        }}

        .rip-signal-card .rip-signal-value {{
            color: #f8fafc !important;
            font-size: 1.5rem;
            line-height: 1.02;
            letter-spacing: -0.03em;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }}

        .rip-signal-card p,
        .rip-signal-card div,
        .rip-signal-card span {{
            margin: 0;
            color: rgba(248, 250, 252, 0.78) !important;
            line-height: 1.6;
            font-size: 0.92rem;
        }}

        .rip-module-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            padding-top: 0.75rem;
            margin-top: 0.75rem;
            border-top: 1px solid rgba(15, 23, 42, 0.08);
            font-size: 0.9rem;
        }}

        .rip-command-card {{
            position: relative;
            overflow: hidden;
        }}

        .rip-command-card::before {{
            content: "";
            position: absolute;
            inset: 0 0 auto 0;
            height: 3px;
            background: linear-gradient(90deg, var(--rip-info), var(--rip-accent));
        }}

        .rip-command-label {{
            color: var(--rip-muted) !important;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.10em;
            margin-bottom: 0.65rem;
        }}

        .rip-command-card h3 {{
            margin: 0 0 0.45rem 0;
            color: var(--rip-secondary) !important;
            font-size: 1.08rem;
            letter-spacing: -0.02em;
        }}

        .rip-command-card p {{
            margin: 0;
            color: var(--rip-muted) !important;
            line-height: 1.6;
        }}

        .rip-command-panel {{
            border-radius: var(--rip-radius-lg);
            border: 1px solid rgba(15, 23, 42, 0.06);
            background: rgba(255, 255, 255, 0.95);
            box-shadow: var(--rip-shadow-soft);
            padding: 1rem 1.05rem;
            min-height: 100%;
        }}

        .rip-command-panel.is-primary {{
            background:
                radial-gradient(circle at top right, rgba(255, 255, 255, 0.10), transparent 28%),
                linear-gradient(135deg, var(--rip-secondary) 0%, #16324a 55%, var(--rip-primary) 100%);
            box-shadow: var(--rip-shadow-medium);
        }}

        .rip-command-panel.is-primary h1,
        .rip-command-panel.is-primary h2,
        .rip-command-panel.is-primary h3,
        .rip-command-panel.is-primary p,
        .rip-command-panel.is-primary div,
        .rip-command-panel.is-primary span {{
            color: #f8fafc !important;
        }}

        .rip-command-kicker {{
            color: var(--rip-muted) !important;
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.11em;
            margin-bottom: 0.55rem;
        }}

        .rip-command-panel.is-primary .rip-command-kicker {{
            color: rgba(248, 250, 252, 0.70) !important;
        }}

        .rip-command-title {{
            color: var(--rip-secondary) !important;
            font-size: 1.02rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.2rem;
        }}

        .rip-command-panel.is-primary .rip-command-title {{
            color: #f8fafc !important;
        }}

        .rip-command-value {{
            color: var(--rip-primary) !important;
            font-size: 1.65rem;
            line-height: 1.05;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin-bottom: 0.35rem;
        }}

        .rip-command-panel.is-primary .rip-command-value {{
            color: #f8fafc !important;
        }}

        .rip-command-note {{
            color: var(--rip-muted) !important;
            font-size: 0.9rem;
            line-height: 1.55;
        }}

        .rip-command-panel.is-primary .rip-command-note {{
            color: rgba(248, 250, 252, 0.78) !important;
        }}

        .rip-kpi-note {{
            border-radius: var(--rip-radius-md);
            border: 1px solid rgba(15, 23, 42, 0.08);
            background: rgba(255, 255, 255, 0.92);
            box-shadow: var(--rip-shadow-soft);
            padding: 0.9rem 1rem;
            min-height: 100%;
        }}

        .rip-kpi-note-title {{
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.10em;
            margin-bottom: 0.4rem;
            color: var(--rip-muted) !important;
        }}

        .rip-kpi-note p {{
            margin: 0;
            color: var(--rip-text) !important;
            line-height: 1.6;
            font-size: 0.94rem;
        }}

        .rip-kpi-note.is-risk {{
            border-left: 4px solid var(--rip-danger);
        }}

        .rip-kpi-note.is-positive {{
            border-left: 4px solid var(--rip-success);
        }}

        .rip-kpi-note.is-warning {{
            border-left: 4px solid var(--rip-warning);
        }}

        .rip-kpi-note.is-info {{
            border-left: 4px solid var(--rip-info);
        }}

        .rip-footer {{
            margin-top: 1.6rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(15, 23, 42, 0.08);
            font-size: 0.9rem;
        }}

        @media (max-width: 1080px) {{
            .rip-stat-grid,
            .rip-insight-grid,
            .rip-signal-grid,
            .rip-module-grid,
            .rip-command-grid,
            .rip-command-bar {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}

            .rip-topbar {{
                flex-direction: column;
            }}

            .rip-topbar-summary {{
                justify-content: flex-start;
                text-align: left;
            }}
        }}

        @media (max-width: 720px) {{
            .block-container {{
                padding-left: 0.95rem;
                padding-right: 0.95rem;
            }}

            .rip-stat-grid,
            .rip-insight-grid,
            .rip-signal-grid,
            .rip-module-grid,
            .rip-command-grid,
            .rip-command-bar {{
                grid-template-columns: 1fr;
            }}

            .rip-intro-banner,
            .rip-hero,
            .rip-topbar {{
                padding: 1rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    return palette


def render_intro_banner(st_module, *, title: str, subtitle: str, notice: str, eyebrow: str | None = None) -> None:
    eyebrow_markup = f'<div class="rip-intro-eyebrow">{escape(eyebrow)}</div>' if eyebrow else ""
    st_module.markdown(
        f"""
        <section class="rip-intro-banner">
            {eyebrow_markup}
            <h1>{escape(title)}</h1>
            <p class="rip-intro-subtitle">{escape(subtitle)}</p>
            <div class="rip-intro-notice">{escape(notice)}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_hero(st_module, *, title: str, subtitle: str, kicker: str, chips: list[str] | None = None) -> None:
    chips_markup = ""
    if chips:
        chips_markup = '<div class="rip-chip-row">' + "".join(
            f'<span class="rip-chip">{escape(chip)}</span>' for chip in chips
        ) + "</div>"
    st_module.markdown(
        f"""
        <section class="rip-hero">
            <div class="rip-kicker">{escape(kicker)}</div>
            <h1 class="rip-title">{escape(title)}</h1>
            <div class="rip-subtitle">{escape(subtitle)}</div>
            {chips_markup}
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_section_label(st_module, text: str) -> None:
    st_module.markdown(
        f'<div class="rip-section-label">{escape(text)}</div>',
        unsafe_allow_html=True,
    )


def render_card(st_module, title: str, body: str) -> None:
    st_module.markdown(
        f"""
        <section class="rip-card">
            <h3>{escape(title)}</h3>
            <p class="rip-card-muted">{escape(body)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_footer(st_module, text: str) -> None:
    st_module.markdown(
        f'<div class="rip-footer">{text}</div>',
        unsafe_allow_html=True,
    )
