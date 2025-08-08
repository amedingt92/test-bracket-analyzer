"""Streamlit dashboard implementation (minimal placeholder)."""

from __future__ import annotations

import streamlit as st


def run_dashboard(db_path: str, snapshots_dir: str) -> None:
    """
    Launch a Streamlit dashboard for exploring backtests, brackets and matchups.
    Placeholder implementation shows basic information.
    """
    st.title("March Madness Dashboard")
    st.write("Database path:", db_path)
    st.write("Snapshots directory:", snapshots_dir)
    st.write(
        "This dashboard is under construction. Backtest results and bracket visualisations "
        "will appear here once implemented."
    )
