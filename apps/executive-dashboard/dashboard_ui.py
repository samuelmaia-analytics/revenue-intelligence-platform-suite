from __future__ import annotations

import inspect
from html import escape
from typing import Iterable

import altair as alt
import pandas as pd


def _to_html(text: object) -> str:
    return escape(str(text), quote=True)


def _stretch_kwargs(callable_obj) -> dict[str, object]:
    if "width" in inspect.signature(callable_obj).parameters:
        return {"width": "stretch"}
    return {"use_container_width": True}


def format_currency(value: float, decimals: int = 0) -> str:
    return f"${value:,.{decimals}f}"


def format_percent(value: float, decimals: int = 1, *, from_ratio: bool = True) -> str:
    scaled = value * 100 if from_ratio else value
    return f"{scaled:.{decimals}f}%"


def render_global_context(
    st_module,
    *,
    suite_label: str,
    page_title: str,
    summary: str,
    right_hint: str,
) -> None:
    st_module.markdown(
        f"""
        <section class="rip-topbar">
            <div>
                <div class="rip-topbar-label">{_to_html(suite_label)}</div>
                <div class="rip-topbar-title">{_to_html(page_title)}</div>
            </div>
            <div class="rip-topbar-summary">
                <div>{_to_html(summary)}</div>
                <span class="rip-inline-pill">{_to_html(right_hint)}</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_status_badge(text: str, tone: str = "neutral") -> str:
    tone_class = {
        "positive": "is-positive",
        "risk": "is-risk",
        "warning": "is-warning",
        "info": "is-info",
    }.get(tone, "")
    return f'<span class="rip-status-badge {tone_class}">{_to_html(text)}</span>'


def render_sidebar_nav(
    st_module,
    *,
    current_page: str,
    mode_label: str,
    mode_body: str,
    flow_label: str,
    flow_body: str,
) -> None:
    nav_items = [
        ("app.py", "Home", "home"),
        ("pages/1_Executive_KPI_Board.py", "KPI Board", "kpi_board"),
        ("pages/2_Modules_Access.py", "Modules", "modules"),
    ]
    st_module.markdown('<div class="rip-sidebar-group-label">Workspace</div>', unsafe_allow_html=True)
    for page_path, label, page_key in nav_items:
        st_module.page_link(page_path, label=label)
    st_module.markdown('<div class="rip-sidebar-divider"></div>', unsafe_allow_html=True)
    st_module.markdown('<div class="rip-sidebar-group-label">Context</div>', unsafe_allow_html=True)
    st_module.caption(mode_label)
    st_module.markdown(f'<div class="rip-sidebar-muted">{_to_html(mode_body)}</div>', unsafe_allow_html=True)
    st_module.markdown('<div class="rip-sidebar-divider"></div>', unsafe_allow_html=True)
    st_module.markdown('<div class="rip-sidebar-group-label">Read Flow</div>', unsafe_allow_html=True)
    st_module.caption(flow_label)
    st_module.markdown(f'<div class="rip-sidebar-muted">{_to_html(flow_body)}</div>', unsafe_allow_html=True)


def render_metrics_grid(st_module, metrics: Iterable[dict[str, object]]) -> None:
    metrics = list(metrics)
    if not metrics:
        return
    cols = st_module.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            st_module.markdown(
                (
                    f'<div class="rip-stat-card {"is-featured" if metric.get("featured") else ""} {"is-" + str(metric.get("tone")) if metric.get("tone") else ""}">'
                    '<div class="rip-stat-header">'
                    f'<span class="rip-stat-label">{_to_html(metric["label"])}</span>'
                    f'{render_status_badge(metric.get("context", ""), metric.get("context_tone", "neutral")) if metric.get("context") else ""}'
                    "</div>"
                    f'<div class="rip-stat-value">{_to_html(metric["value"])}</div>'
                    '<div class="rip-stat-footer">'
                    f'<span class="rip-stat-delta">{_to_html(metric.get("delta", ""))}</span>'
                    f'<span class="rip-stat-caption">{_to_html(metric.get("caption", ""))}</span>'
                    "</div>"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )


def render_insight_grid(st_module, insights: Iterable[dict[str, object]]) -> None:
    insights = list(insights)
    if not insights:
        return
    cols = st_module.columns(len(insights))
    for col, item in zip(cols, insights):
        with col:
            st_module.markdown(
                (
                    '<div class="rip-insight-card">'
                    f'<div class="rip-insight-type">{_to_html(item.get("eyebrow", "Signal"))}</div>'
                    f'<h3>{_to_html(item["title"])}</h3>'
                    f'<p>{_to_html(item["body"])}</p>'
                    f'<div class="rip-insight-action">{_to_html(item.get("action", ""))}</div>'
                    "</div>"
                ),
                unsafe_allow_html=True,
            )


def render_signal_band(st_module, signals: Iterable[dict[str, object]]) -> None:
    signals = list(signals)
    if not signals:
        return
    cols = st_module.columns(len(signals))
    for col, signal in zip(cols, signals):
        with col:
            st_module.markdown(
                (
                    '<div class="rip-signal-card">'
                    f'<div class="rip-signal-title">{_to_html(signal["title"])}</div>'
                    f'<div class="rip-signal-value">{_to_html(signal["value"])}</div>'
                    f'<p>{_to_html(signal["body"])}</p>'
                    "</div>"
                ),
                unsafe_allow_html=True,
            )


def render_kpi_note(st_module, *, title: str, body: str, tone: str = "neutral") -> None:
    tone_class = {
        "positive": "is-positive",
        "risk": "is-risk",
        "warning": "is-warning",
        "info": "is-info",
    }.get(tone, "")
    st_module.markdown(
        (
            f'<div class="rip-kpi-note {tone_class}">'
            f'<div class="rip-kpi-note-title">{_to_html(title)}</div>'
            f'<p>{_to_html(body)}</p>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def render_story_block(st_module, *, title: str, body: str, badge: str | None = None) -> None:
    badge_markup = render_status_badge(badge, "positive") if badge else ""
    st_module.markdown(
        f"""
        <section class="rip-story-block">
            <div class="rip-story-heading">
                <h3>{_to_html(title)}</h3>
                {badge_markup}
            </div>
            <p>{_to_html(body)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_module_cards(st_module, modules: Iterable[dict[str, object]]) -> None:
    modules = list(modules)
    if not modules:
        return
    for i in range(0, len(modules), 2):
        row = modules[i:i + 2]
        cols = st_module.columns(len(row))
        for col, module in zip(cols, row):
            with col:
                st_module.markdown(
                    (
                        '<div class="rip-module-card">'
                        '<div class="rip-module-header">'
                        "<div>"
                        f'<div class="rip-module-category">{_to_html(module.get("category", "Module"))}</div>'
                        f'<h3>{_to_html(module["name"])}</h3>'
                        "</div>"
                        f'{render_status_badge(module.get("status", "Live"), module.get("status_tone", "neutral"))}'
                        "</div>"
                        f'<p>{_to_html(module["role"])}</p>'
                        '<div class="rip-module-meta">'
                        f'<span>{_to_html(module.get("value", ""))}</span>'
                        f'<span>{_to_html(module.get("asset_type", ""))}</span>'
                        "</div>"
                        "</div>"
                    ),
                    unsafe_allow_html=True,
                )


def render_command_grid(st_module, items: Iterable[dict[str, object]]) -> None:
    items = list(items)
    if not items:
        return
    cols = st_module.columns(len(items))
    for col, item in zip(cols, items):
        with col:
            st_module.markdown(
                (
                    '<div class="rip-command-card">'
                    f'<div class="rip-command-label">{_to_html(item.get("label", "Command"))}</div>'
                    f'<h3>{_to_html(item["title"])}</h3>'
                    f'<p>{_to_html(item["body"])}</p>'
                    "</div>"
                ),
                unsafe_allow_html=True,
            )


def render_command_bar(st_module, items: Iterable[dict[str, object]]) -> None:
    items = list(items)
    if not items:
        return
    spec = [1.3 if item.get("primary") else 1 for item in items]
    cols = st_module.columns(spec)
    for col, item in zip(cols, items):
        with col:
            st_module.markdown(
                (
                    f'<div class="rip-command-panel {"is-primary" if item.get("primary") else ""}">'
                    f'<div class="rip-command-kicker">{_to_html(item.get("label", "Overview"))}</div>'
                    f'<div class="rip-command-title">{_to_html(item["title"])}</div>'
                    f'<div class="rip-command-value">{_to_html(item.get("value", ""))}</div>'
                    f'<div class="rip-command-note">{_to_html(item.get("note", ""))}</div>'
                    "</div>"
                ),
                unsafe_allow_html=True,
            )


def style_altair_chart(chart: alt.Chart | alt.LayerChart | alt.HConcatChart | alt.VConcatChart):
    return chart.configure_view(strokeWidth=0).configure_axis(
        domain=False,
        gridColor="#d8e1eb",
        gridOpacity=0.5,
        labelColor="#5b6474",
        labelFontSize=12,
        titleColor="#111827",
        titleFontSize=12,
        tickColor="#d8e1eb",
    ).configure_legend(
        labelColor="#5b6474",
        titleColor="#111827",
        orient="top",
        padding=6,
        symbolType="circle",
    )


def build_line_chart(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    color: str,
    y_title: str,
    tooltip: list[str],
) -> alt.Chart:
    base = alt.Chart(data).encode(
        x=alt.X(x, title=None, axis=alt.Axis(labelAngle=0, labelPadding=8)),
        y=alt.Y(y, title=y_title),
        tooltip=tooltip,
    )
    area = base.mark_area(opacity=0.10, color=color)
    line = base.mark_line(color=color, strokeWidth=3, interpolate="monotone")
    points = base.mark_circle(color=color, size=56, opacity=1)
    return style_altair_chart((area + line + points).properties(height=340))


def build_bar_chart(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    color: str,
    tooltip: list[str],
    y_title: str,
) -> alt.Chart:
    chart = (
        alt.Chart(data)
        .mark_bar(size=26, cornerRadiusEnd=6, color=color)
        .encode(
            x=alt.X(x, title=None),
            y=alt.Y(y, title=y_title, sort="-x"),
            tooltip=tooltip,
        )
        .properties(height=300)
    )
    return style_altair_chart(chart)


def render_table(st_module, df: pd.DataFrame, *, formatters: dict[str, object] | None = None) -> None:
    styler = df.style.hide(axis="index")
    if formatters:
        styler = styler.format(formatters)
    if "Priority" in df.columns:
        priority_colors = {
            "P1": "#fee2e2",
            "P2": "#ffedd5",
            "P3": "#ecfccb",
        }
        styler = styler.apply(
            lambda col: [f"background-color: {priority_colors.get(value, '#ffffff')}" for value in col]
            if col.name == "Priority"
            else ["" for _ in col],
            axis=0,
        )
    if "Status" in df.columns:
        status_colors = {
            "Approved": "#dcfce7",
            "In Progress": "#dbeafe",
            "Planned": "#fef3c7",
            "Watch": "#fee2e2",
        }
        styler = styler.apply(
            lambda col: [f"background-color: {status_colors.get(value, '#ffffff')}" for value in col]
            if col.name == "Status"
            else ["" for _ in col],
            axis=0,
        )
    styler = styler.set_table_styles(
        [
            {"selector": "th", "props": [("background-color", "#f8fafc"), ("color", "#5b6474"), ("font-size", "0.78rem"), ("font-weight", "700"), ("text-transform", "uppercase"), ("letter-spacing", "0.08em"), ("border-bottom", "1px solid #d8e1eb")]},
            {"selector": "td", "props": [("color", "#111827"), ("border-bottom", "1px solid #eef2f6"), ("font-size", "0.92rem")]},
            {"selector": "tbody tr:hover", "props": [("background-color", "#f8fbff")]},
            {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%")]},
        ]
    )
    st_module.dataframe(styler, **_stretch_kwargs(st_module.dataframe))
