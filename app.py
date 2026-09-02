import time
import streamlit as st

from src.nback_task import NBackRunner
from src.data_manager import get_next_run_number


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="N-Back Driver Experiment",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# COMPACT PROFESSIONAL UI — FITS ONE SCREEN, NO SCROLL
# ============================================================

st.markdown(
    """
    <style>

    /* Hide Streamlit chrome to reclaim vertical space */
    #MainMenu { visibility: hidden; }
    header[data-testid="stHeader"] { display: none; }
    footer { visibility: hidden; }
    div[data-testid="stToolbar"] { display: none; }
    div[data-testid="stDecoration"] { display: none; }

    /* Kill page scroll — everything must fit in viewport */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh;
    }

    .block-container {
        max-width: 1300px;
        padding-top: 0.6rem;
        padding-bottom: 0.4rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    [data-testid="stVerticalBlock"] { gap: 0.5rem; }
    [data-testid="column"] { padding: 0 6px; }

    /* Header bar */
    .header-bar {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        border-radius: 16px;
        padding: 18px 26px;
        margin-bottom: 10px;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        line-height: 1.2;
    }

    .subtitle {
        font-size: 13px;
        color: #dbeafe;
        margin: 4px 0 0 0;
    }

    .run-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        color: #ffffff;
        font-size: 13px;
        font-weight: 650;
        padding: 6px 14px;
        border-radius: 10px;
        margin-top: 6px;
    }

    /* Start screen */
    .setup-card {
        background: white;
        border: 1px solid #dbe3ec;
        border-radius: 16px;
        padding: 20px 24px;
        height: 100%;
    }

    .setup-card-title {
        font-size: 13px;
        font-weight: 700;
        color: #64748b;
        letter-spacing: 0.04em;
        margin-bottom: 12px;
    }

    .key-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0;
        border-bottom: 1px solid #eef1f5;
    }

    .key-row:last-child { border-bottom: none; }

    .key-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 750;
        flex-shrink: 0;
    }

    .key-chip.match { background: #dcfce7; color: #15803d; }
    .key-chip.nomatch { background: #fef3c7; color: #b45309; }
    .key-chip.skip { background: #e2e8f0; color: #475569; }

    .key-desc {
        font-size: 14px;
        color: #334155;
    }

    .note-row {
        display: flex;
        gap: 10px;
        align-items: flex-start;
        padding: 6px 0;
        font-size: 13.5px;
        color: #475569;
    }

    .note-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #94a3b8;
        margin-top: 7px;
        flex-shrink: 0;
    }

    .task-summary {
        display: flex;
        gap: 10px;
        margin-bottom: 4px;
    }

    .summary-pill {
        flex: 1;
        background: #f8fafc;
        border: 1px solid #e5eaf0;
        border-radius: 12px;
        padding: 10px 14px;
        text-align: center;
    }

    .summary-pill-value {
        font-size: 20px;
        font-weight: 750;
        color: #172033;
        line-height: 1.2;
    }

    .summary-pill-label {
        font-size: 11px;
        color: #64748b;
        font-weight: 600;
        letter-spacing: 0.03em;
    }

    /* Progress card */
    .progress-card {
        background: white;
        border: 1px solid #dbe3ec;
        border-radius: 14px;
        padding: 10px 20px;
        margin-top: 4px;
    }

    .progress-label {
        font-size: 14px;
        color: #475569;
        font-weight: 600;
    }

    .progress-count {
        float: right;
        font-size: 17px;
        font-weight: 750;
        color: #172033;
    }

    /* Stat cards */
    .stat-card {
        background: white;
        border: 1px solid #dbe3ec;
        border-radius: 14px;
        padding: 10px 16px;
        height: 78px;
    }

    .stat-title {
        font-size: 12px;
        color: #64748b;
        font-weight: 600;
        letter-spacing: 0.03em;
        margin-bottom: 2px;
    }

    .stat-value {
        font-size: 26px;
        font-weight: 750;
        color: #172033;
        line-height: 1.15;
    }

    .stat-value.accent-match { color: #15803d; }
    .stat-value.accent-nomatch { color: #b45309; }
    .stat-value.accent-skip { color: #64748b; }
    .stat-value.accent-acc { color: #2563eb; }

    /* Live number card */
    .live-card {
        background: #172033;
        border-radius: 14px;
        padding: 10px 20px;
        text-align: center;
    }

    .live-label {
        font-size: 12px;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    .live-number {
        font-size: 34px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1.1;
    }

    /* Response section */
    .response-title {
        font-size: 14px;
        font-weight: 650;
        color: #475569;
        margin: 4px 0 4px 0;
    }

    div.stButton > button {
        height: 48px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 650;
    }

    div.stButton > button[kind="primary"] {
        height: 52px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "runner" not in st.session_state:
    st.session_state.runner = None

if "driver_number" not in st.session_state:
    st.session_state.driver_number = 1


runner = st.session_state.runner


# ============================================================
# HEADER (always shown, compact)
# ============================================================

run_badge_html = ""
if runner is not None:
    run_badge_html = (
        f'<div class="run-badge">D{runner.driver_number} · RUN {runner.run_number:02d}</div>'
    )

st.markdown(
    f"""
    <div class="header-bar" style="display:flex; align-items:center; justify-content:space-between;">
        <div>
            <div class="main-title">N-Back Driver Experiment</div>
            <div class="subtitle">20 trials per run · 2.25 s stimulus-onset interval · number audio only</div>
        </div>
        {run_badge_html}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# START SCREEN
# ============================================================

if runner is None:

    # Driver number selector
    dcol1, dcol2 = st.columns([1, 3])
    with dcol1:
        st.session_state.driver_number = st.number_input(
            "Driver number",
            min_value=1,
            step=1,
            value=st.session_state.driver_number
        )

    next_run_number = get_next_run_number(st.session_state.driver_number)

    next_filename = (
        f"D{st.session_state.driver_number}_run{next_run_number:02d}.xlsx"
    )

    # Quick summary strip
    st.markdown(
        f"""
        <div class="task-summary">
            <div class="summary-pill">
                <div class="summary-pill-value">20</div>
                <div class="summary-pill-label">TRIALS</div>
            </div>
            <div class="summary-pill">
                <div class="summary-pill-value">2.25s</div>
                <div class="summary-pill-label">ONSET INTERVAL</div>
            </div>
            <div class="summary-pill">
                <div class="summary-pill-value">Audio</div>
                <div class="summary-pill-label">NUMBER ONLY</div>
            </div>
            <div class="summary-pill">
                <div class="summary-pill-value" style="font-size:16px;">{next_filename}</div>
                <div class="summary-pill-label">NEXT FILE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_keys, col_notes = st.columns([1, 1.2])

    with col_keys:
        st.markdown(
            """
            <div class="setup-card">
                <div class="setup-card-title">OBSERVER KEYS</div>
                <div class="key-row">
                    <span class="key-chip match">M</span>
                    <span class="key-desc">Match — number matches the target</span>
                </div>
                <div class="key-row">
                    <span class="key-chip nomatch">N</span>
                    <span class="key-desc">No match — number does not match</span>
                </div>
                <div class="key-row">
                    <span class="key-chip skip">S</span>
                    <span class="key-desc">Skip — excluded from accuracy</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_notes:
        st.markdown(
            """
            <div class="setup-card">
                <div class="setup-card-title">BEFORE YOU START</div>
                <div class="note-row"><span class="note-dot"></span>
                    Only number audio is played to the driver — M/N/S keys are completely silent.</div>
                <div class="note-row"><span class="note-dot"></span>
                    1-back: skip the first trial. 2-back: skip the first two trials.</div>
                <div class="note-row"><span class="note-dot"></span>
                    Skipped trials are excluded from the accuracy calculation.</div>
                <div class="note-row"><span class="note-dot"></span>
                    Data saves continuously to Excel after every trial.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    if st.button("▶  START 20-TRIAL RUN", type="primary", use_container_width=True):
        st.session_state.runner = NBackRunner(
            run_number=next_run_number,
            driver_number=st.session_state.driver_number
        )
        st.session_state.runner.start()
        st.rerun()


# ============================================================
# RUNNING SCREEN — compact, single-screen monitoring view
# ============================================================

elif runner.status == "running":

    completed = runner.completed_trials
    total = runner.total_trials
    progress = completed / total

    match_count = runner.match_count
    no_match_count = runner.no_match_count
    skip_count = runner.skip_count

    denominator = match_count + no_match_count
    accuracy = (match_count / denominator * 100) if denominator > 0 else 0.0

    last_number = getattr(runner, "last_number", None)

    # --------------------------------------------------------
    # PROGRESS BAR
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="progress-card">
            <span class="progress-label">Trial progress</span>
            <span class="progress-count">{completed} / {total}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(progress)

    # --------------------------------------------------------
    # LIVE STIMULUS + STATS ROW
    # --------------------------------------------------------

    c0, c1, c2, c3, c4 = st.columns([1.1, 1, 1, 1, 1])

    with c0:
        number_display = last_number if last_number is not None else "—"
        st.markdown(
            f"""
            <div class="live-card">
                <div class="live-label">CURRENT NUMBER</div>
                <div class="live-number">{number_display}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">MATCH</div>
                <div class="stat-value accent-match">{match_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">NO MATCH</div>
                <div class="stat-value accent-nomatch">{no_match_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">SKIP</div>
                <div class="stat-value accent-skip">{skip_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-title">ACCURACY</div>
                <div class="stat-value accent-acc">{accuracy:.1f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # RESPONSE BUTTONS
    # --------------------------------------------------------

    st.markdown('<div class="response-title">Observer response</div>', unsafe_allow_html=True)

    b1, b2, b3, b4 = st.columns([1, 1, 1, 1])

    with b1:
        if st.button("M — MATCH", use_container_width=True):
            runner.manual_response("M")

    with b2:
        if st.button("N — NO MATCH", use_container_width=True):
            runner.manual_response("N")

    with b3:
        if st.button("S — SKIP", use_container_width=True):
            runner.manual_response("S")

    with b4:
        if st.button("■ STOP RUN", use_container_width=True):
            runner.stop()
            st.rerun()

    # --------------------------------------------------------
    # REFRESH
    # --------------------------------------------------------

    time.sleep(0.20)
    st.rerun()


# ============================================================
# COMPLETED
# ============================================================

elif runner.status == "completed":

    match_count = runner.match_count
    no_match_count = runner.no_match_count
    skip_count = runner.skip_count

    denominator = match_count + no_match_count
    accuracy = (match_count / denominator * 100) if denominator > 0 else 0.0

    st.success("✓ RUN COMPLETED — 20 / 20 TRIALS")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-title">MATCH</div>'
            f'<div class="stat-value accent-match">{match_count}</div></div>',
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f'<div class="stat-card"><div class="stat-title">NO MATCH</div>'
            f'<div class="stat-value accent-nomatch">{no_match_count}</div></div>',
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f'<div class="stat-card"><div class="stat-title">SKIP</div>'
            f'<div class="stat-value accent-skip">{skip_count}</div></div>',
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f'<div class="stat-card"><div class="stat-title">ACCURACY</div>'
            f'<div class="stat-value accent-acc">{accuracy:.2f}%</div></div>',
            unsafe_allow_html=True
        )

    st.info(f"Data saved to: {runner.output_path}")

    if st.button("↻  RUN AGAIN", type="primary", use_container_width=True):
        st.session_state.runner = None
        st.rerun()


# ============================================================
# STOPPED
# ============================================================

elif runner.status == "stopped":

    st.warning("Run stopped by observer.")

    if runner.output_path:
        st.info(f"Data saved to: {runner.output_path}")

    if st.button("↻  RUN AGAIN", type="primary", use_container_width=True):
        st.session_state.runner = None
        st.rerun()


# ============================================================
# ERROR
# ============================================================

elif runner.status == "error":

    st.error(f"Experiment error: {runner.error}")

    if st.button("Back / Try Again", use_container_width=True):
        st.session_state.runner = None
        st.rerun()
