import pandas as pd
import streamlit as st
from datetime import datetime


# -----------------------------------------------------------------------------
# Page configuration and premium styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SAR Narrative Generator with Audit Trail",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #f5f7fb;
            color: #1f2a44;
        }
        .compact-title {
            font-size: 1.45rem;
            font-weight: 700;
            color: #102a43;
            margin-bottom: 0.1rem;
        }
        .compact-subtitle {
            color: #486581;
            font-size: 0.92rem;
            margin-bottom: 0.5rem;
        }
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #d9e2ec;
            border-radius: 10px;
            padding: 0.8rem;
            box-shadow: 0 1px 3px rgba(16, 42, 67, 0.07);
        }
        .metric-label {
            color: #486581;
            font-size: 0.82rem;
            margin-bottom: 0.15rem;
        }
        .metric-value {
            color: #102a43;
            font-size: 1.25rem;
            font-weight: 700;
        }
        .status-pill {
            display: inline-block;
            background-color: #e3f9e5;
            color: #207227;
            border: 1px solid #a7f3d0;
            border-radius: 999px;
            padding: 0.15rem 0.6rem;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .context-card {
            background-color: #ffffff;
            border: 1px solid #d9e2ec;
            border-radius: 10px;
            padding: 0.6rem 0.75rem;
            margin-bottom: 0.35rem;
        }
        .context-label {
            font-size: 0.73rem;
            color: #627d98;
        }
        .context-value {
            font-size: 0.9rem;
            color: #102a43;
            font-weight: 600;
        }
        .small-muted {
            color: #627d98;
            font-size: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Static placeholder datasets
# -----------------------------------------------------------------------------
alerts_df = pd.DataFrame(
    [
        ["ALT-1024", "CASE-3401", "Sophia Williams", "High", "2026-02-12", "Open", 185000.00],
        ["ALT-1025", "CASE-3402", "Liam Johnson", "Medium", "2026-02-12", "Investigating", 94500.00],
        ["ALT-1026", "CASE-3403", "Olivia Brown", "High", "2026-02-11", "Open", 250000.00],
        ["ALT-1027", "CASE-3398", "Noah Davis", "Low", "2026-02-10", "Closed", 12000.00],
        ["ALT-1028", "CASE-3404", "Emma Wilson", "Medium", "2026-02-09", "Pending", 68000.00],
    ],
    columns=[
        "Alert ID",
        "Case ID",
        "Customer Name",
        "Risk Level",
        "Alert Date",
        "Status",
        "Suspicious Amount",
    ],
)

customer_df = pd.DataFrame(
    [
        ["Sophia Williams", "CUST-00981", "High", "Import/Export Director", "United Kingdom", "1987-06-14", "No", "No Match", "Enhanced Monitoring"],
        ["Liam Johnson", "CUST-01005", "Medium", "IT Consultant", "Ireland", "1990-09-21", "No", "No Match", "Periodic Review"],
        ["Olivia Brown", "CUST-01088", "High", "Logistics Owner", "UAE", "1985-01-03", "No", "No Match", "Enhanced Monitoring"],
        ["Noah Davis", "CUST-01120", "Low", "Retail Manager", "United States", "1992-03-19", "No", "No Match", "Standard Monitoring"],
        ["Emma Wilson", "CUST-01241", "Medium", "Property Broker", "Canada", "1988-11-05", "No", "No Match", "Periodic Review"],
    ],
    columns=[
        "Customer Name",
        "Customer ID",
        "Risk Rating",
        "Occupation",
        "Nationality",
        "Date of Birth",
        "PEP",
        "Sanctions Screening",
        "Monitoring Plan",
    ],
)

transactions_df = pd.DataFrame(
    [
        ["TXN-7781", "2026-02-10", 85000.00, "Outbound", "Blue Harbor Trading", "SG", "High"],
        ["TXN-7782", "2026-02-10", 60000.00, "Inbound", "Sterling Commodities", "AE", "Medium"],
        ["TXN-7783", "2026-02-11", 40000.00, "Outbound", "Northline Brokers", "TR", "High"],
        ["TXN-7784", "2026-02-12", 12000.00, "Inbound", "Atlas Supplies", "GB", "Low"],
        ["TXN-7785", "2026-02-12", 95000.00, "Outbound", "Redwood Logistics", "CY", "High"],
        ["TXN-7786", "2026-02-13", 31000.00, "Outbound", "Falcon Imports", "HK", "Medium"],
    ],
    columns=["Transaction ID", "Date", "Amount", "Direction", "Counterparty", "Country", "Risk Flag"],
)


# -----------------------------------------------------------------------------
# Session state setup
# -----------------------------------------------------------------------------
def init_state() -> None:
    default_case = alerts_df.iloc[0].to_dict()

    if "selected_case" not in st.session_state:
        st.session_state.selected_case = default_case

    if "selected_transactions" not in st.session_state:
        st.session_state.selected_transactions = []

    if "role" not in st.session_state:
        st.session_state.role = "Analyst"

    if "audit_log" not in st.session_state:
        st.session_state.audit_log = [
            {
                "Timestamp": "2026-02-12 09:35:00",
                "User": "m.khan",
                "Action": "Alert selected",
                "Case ID": "CASE-3401",
                "Description": "Initial alert triage completed.",
            }
        ]

    if "sar_draft" not in st.session_state:
        st.session_state.sar_draft = ""

    if "draft_version" not in st.session_state:
        st.session_state.draft_version = 0

    if "draft_last_edited" not in st.session_state:
        st.session_state.draft_last_edited = "-"

    if "draft_edited_by" not in st.session_state:
        st.session_state.draft_edited_by = "-"


# -----------------------------------------------------------------------------
# Utility helpers
# -----------------------------------------------------------------------------
def current_user() -> str:
    return "analyst.user" if st.session_state.role == "Analyst" else "reviewer.user"


def add_audit_event(action: str, description: str) -> None:
    st.session_state.audit_log.append(
        {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "User": current_user(),
            "Action": action,
            "Case ID": st.session_state.selected_case["Case ID"],
            "Description": description,
        }
    )


def selected_customer_record() -> pd.Series:
    name = st.session_state.selected_case["Customer Name"]
    return customer_df[customer_df["Customer Name"] == name].iloc[0]


def render_case_context_bar() -> None:
    case = st.session_state.selected_case
    with st.container():
        cols = st.columns(6)
        values = [
            ("Case ID", case["Case ID"]),
            ("Alert ID", case["Alert ID"]),
            ("Customer Name", case["Customer Name"]),
            ("Risk Level", case["Risk Level"]),
            ("Case Status", case["Status"]),
            ("Assigned Officer", "Mariam Khan"),
        ]
        for c, (label, value) in zip(cols, values):
            with c:
                st.markdown(
                    f'<div class="context-card"><div class="context-label">{label}</div><div class="context-value">{value}</div></div>',
                    unsafe_allow_html=True,
                )


# -----------------------------------------------------------------------------
# Core modular page renderers
# -----------------------------------------------------------------------------
def render_case_selection() -> None:
    st.subheader("Alert / Case Selection")
    st.caption("Select an alert to establish case context for evidence review and narrative drafting.")

    view_df = alerts_df[["Alert ID", "Customer Name", "Risk Level", "Alert Date", "Status", "Suspicious Amount"]]
    st.dataframe(view_df, use_container_width=True, hide_index=True)

    case_options = [f"{row['Alert ID']} | {row['Case ID']} | {row['Customer Name']}" for _, row in alerts_df.iterrows()]
    default_idx = 0
    selected_option = st.selectbox("Select Alert / Case", case_options, index=default_idx)

    selected_alert_id = selected_option.split(" | ")[0]
    selected_row = alerts_df[alerts_df["Alert ID"] == selected_alert_id].iloc[0].to_dict()

    if selected_row["Alert ID"] != st.session_state.selected_case["Alert ID"]:
        st.session_state.selected_case = selected_row
        st.session_state.selected_transactions = []
        add_audit_event("Alert selected", f"Selected {selected_row['Alert ID']} for investigation.")
        st.success("Case context updated.")


def render_customer_summary() -> None:
    st.subheader("Customer Summary")
    st.caption("Read-only profile and KYC highlights for the selected case.")

    cust = selected_customer_record()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.text_input("Customer Name", value=cust["Customer Name"], disabled=True)
    c2.text_input("Customer ID", value=cust["Customer ID"], disabled=True)
    c3.text_input("Risk Rating", value=cust["Risk Rating"], disabled=True)
    c4.text_input("Occupation", value=cust["Occupation"], disabled=True)
    c5.text_input("Nationality", value=cust["Nationality"], disabled=True)

    with st.expander("View Full KYC Details"):
        kyc_cols = st.columns(4)
        kyc_cols[0].text_input("Date of Birth", value=cust["Date of Birth"], disabled=True)
        kyc_cols[1].text_input("PEP", value=cust["PEP"], disabled=True)
        kyc_cols[2].text_input("Sanctions Screening", value=cust["Sanctions Screening"], disabled=True)
        kyc_cols[3].text_input("Monitoring Plan", value=cust["Monitoring Plan"], disabled=True)


def render_transaction_selection() -> None:
    st.subheader("Transaction Evidence Selection")
    st.caption("Select suspicious transactions and tag each with the primary suspicion reason.")

    reason_options = [
        "Structuring",
        "Layering",
        "Rapid Movement",
        "Sanctions Risk",
        "Unusual Pattern",
        "Other",
    ]

    work_df = transactions_df.copy()
    work_df["Select"] = work_df["Transaction ID"].isin(
        [tx["Transaction ID"] for tx in st.session_state.selected_transactions]
    )

    existing_reasons = {
        tx["Transaction ID"]: tx.get("Suspicion Reason", "Unusual Pattern")
        for tx in st.session_state.selected_transactions
    }
    work_df["Suspicion Reason"] = work_df["Transaction ID"].map(existing_reasons).fillna("Unusual Pattern")

    edited = st.data_editor(
        work_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Select": st.column_config.CheckboxColumn(required=False),
            "Suspicion Reason": st.column_config.SelectboxColumn(options=reason_options, required=True),
            "Amount": st.column_config.NumberColumn(format="$%.2f"),
        },
        disabled=["Transaction ID", "Date", "Amount", "Direction", "Counterparty", "Country", "Risk Flag"],
    )

    if st.button("Update Selected Evidence", use_container_width=True):
        selected_df = edited[edited["Select"]].copy()
        st.session_state.selected_transactions = selected_df[
            [
                "Transaction ID",
                "Date",
                "Amount",
                "Direction",
                "Counterparty",
                "Country",
                "Risk Flag",
                "Suspicion Reason",
            ]
        ].to_dict("records")
        add_audit_event(
            "Transactions selected",
            f"Selected {len(st.session_state.selected_transactions)} suspicious transactions.",
        )
        st.success("Evidence selection updated.")

    st.markdown("##### Evidence Summary")
    selected_tx = pd.DataFrame(st.session_state.selected_transactions)

    if selected_tx.empty:
        st.info("No suspicious transactions selected yet.")
        return

    total_amount = float(selected_tx["Amount"].sum())
    tx_count = int(selected_tx.shape[0])
    date_range = f"{selected_tx['Date'].min()} to {selected_tx['Date'].max()}"
    top_counterparties = ", ".join(selected_tx["Counterparty"].value_counts().head(3).index.tolist())

    s1, s2, s3, s4 = st.columns(4)
    cards = [
        ("Total suspicious amount", f"${total_amount:,.2f}"),
        ("Suspicious transactions", str(tx_count)),
        ("Date range", date_range),
        ("Top counterparties", top_counterparties if top_counterparties else "-"),
    ]
    for col, (label, value) in zip([s1, s2, s3, s4], cards):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="font-size:1rem;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_narrative_generator() -> None:
    st.subheader("SAR Narrative Generator")
    st.caption("Generate and manage narrative drafts from selected evidence.")

    left, right = st.columns([1, 1.3])

    with left:
        st.markdown("##### Evidence and Controls")
        template_type = st.selectbox(
            "SAR Template Type",
            ["Structuring", "Cross-border laundering", "Sanctions evasion", "Fraud", "Other"],
        )
        analyst_summary = st.text_input("Analyst Investigation Summary", placeholder="1-2 sentence summary")

        disable_generate = st.session_state.role == "Reviewer"
        if st.button("Generate SAR Draft", type="primary", disabled=disable_generate, use_container_width=True):
            selected_tx = pd.DataFrame(st.session_state.selected_transactions)
            if selected_tx.empty:
                st.warning("Select suspicious transactions before generating a draft.")
            else:
                amount = selected_tx["Amount"].sum()
                reasons = ", ".join(sorted(selected_tx["Suspicion Reason"].unique()))
                counterparties = ", ".join(selected_tx["Counterparty"].value_counts().head(3).index.tolist())
                st.session_state.sar_draft = (
                    f"SAR Template: {template_type}\n\n"
                    f"Case {st.session_state.selected_case['Case ID']} associated with alert "
                    f"{st.session_state.selected_case['Alert ID']} involves transaction behavior "
                    f"indicative of {template_type.lower()}. The review identified "
                    f"{len(selected_tx)} suspicious transactions totaling ${amount:,.2f}, "
                    f"with key counterparties including {counterparties}.\n\n"
                    f"Primary suspicion indicators include {reasons}. "
                    f"{analyst_summary if analyst_summary else 'Analyst notes pending additional detail.'}\n\n"
                    "This is a simulated frontend draft for workflow validation only."
                )
                st.session_state.draft_version += 1
                st.session_state.draft_last_edited = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.draft_edited_by = current_user()
                add_audit_event("Narrative generated", f"Draft v{st.session_state.draft_version} generated.")
                st.success("Draft generated.")

    with right:
        st.markdown("##### Editable SAR Draft")
        st.markdown(
            f"<span class='small-muted'>Version: v{st.session_state.draft_version} | "
            f"Last edited: {st.session_state.draft_last_edited} | "
            f"Edited by: {st.session_state.draft_edited_by}</span>",
            unsafe_allow_html=True,
        )

        draft_text = st.text_area(
            "Draft",
            value=st.session_state.sar_draft,
            height=280,
            key="draft_editor",
            placeholder="Generated draft appears here...",
        )

        edit_cols = st.columns(4)

        if edit_cols[0].button("Mark Draft Edited", use_container_width=True):
            st.session_state.sar_draft = draft_text
            st.session_state.draft_last_edited = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.draft_edited_by = current_user()
            add_audit_event("Draft edited", "Draft content manually edited by user.")
            st.info("Draft edit captured.")

        if edit_cols[1].button("Save Draft", use_container_width=True):
            st.session_state.sar_draft = draft_text
            st.session_state.draft_version += 1
            st.session_state.draft_last_edited = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.draft_edited_by = current_user()
            add_audit_event("Draft saved", f"Draft saved as version v{st.session_state.draft_version}.")
            st.success("Draft saved.")

        if edit_cols[2].button("Request Review", use_container_width=True):
            st.session_state.sar_draft = draft_text
            add_audit_event("Submitted for review", "Draft submitted to reviewer queue.")
            st.info("Review requested.")

        if edit_cols[3].button("Submit SAR", use_container_width=True):
            st.session_state.sar_draft = draft_text
            add_audit_event("SAR submitted", "SAR submitted to regulatory filing queue.")
            st.success("SAR submitted.")

        if st.session_state.role == "Reviewer":
            st.divider()
            r1, r2 = st.columns(2)
            if r1.button("Approve", use_container_width=True):
                add_audit_event("Review approved", "Reviewer approved SAR draft.")
                st.success("Draft approved.")
            if r2.button("Reject", use_container_width=True):
                add_audit_event("Review rejected", "Reviewer rejected SAR draft and returned to analyst.")
                st.error("Draft rejected.")


def render_audit_trail() -> None:
    st.subheader("Audit Trail")
    st.caption("Traceable event history with workflow-level filtering.")

    log_df = pd.DataFrame(st.session_state.audit_log)
    if log_df.empty:
        st.info("No audit events recorded yet.")
        return

    f1, f2 = st.columns([1.3, 1])
    with f1:
        action_filter = st.multiselect("Filter by Action", sorted(log_df["Action"].unique().tolist()))
    with f2:
        user_filter = st.selectbox("Filter by User", ["All"] + sorted(log_df["User"].unique().tolist()))

    filtered = log_df.copy()
    if action_filter:
        filtered = filtered[filtered["Action"].isin(action_filter)]
    if user_filter != "All":
        filtered = filtered[filtered["User"] == user_filter]

    st.dataframe(filtered.sort_values("Timestamp", ascending=False), use_container_width=True, hide_index=True)


def render_debug_panel() -> None:
    with st.expander("Debug Information"):
        st.write("Selected Transactions")
        st.json(st.session_state.selected_transactions)

        prompt_data = {
            "case_id": st.session_state.selected_case["Case ID"],
            "alert_id": st.session_state.selected_case["Alert ID"],
            "customer_name": st.session_state.selected_case["Customer Name"],
            "selected_transaction_count": len(st.session_state.selected_transactions),
        }
        st.write("Current prompt data structure")
        st.json(prompt_data)

        st.write("Session state")
        st.json({k: v for k, v in st.session_state.items() if k != "audit_log"})


# -----------------------------------------------------------------------------
# App shell and navigation
# -----------------------------------------------------------------------------
init_state()

with st.sidebar:
    st.markdown("### 🏦 Bank Logo")
    st.markdown("#### SAR Narrative Generator")
    st.caption("Enterprise AML & Compliance Workspace")
    st.divider()

    st.session_state.role = st.selectbox("Role", ["Analyst", "Reviewer"], index=0 if st.session_state.role == "Analyst" else 1)

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Transaction Alerts",
            "Customer Information",
            "KYC Data",
            "Account & Transaction Data",
            "Case Management",
            "Narrative Generator",
            "Audit Trail",
        ],
    )

    st.divider()
    st.markdown("**Current User**")
    st.write(f"{current_user()} ({st.session_state.role})")
    st.markdown("**System Status**")
    st.markdown('<span class="status-pill">Active</span>', unsafe_allow_html=True)

st.markdown('<div class="compact-title">SAR Narrative Generator with Audit Trail</div>', unsafe_allow_html=True)
st.markdown('<div class="compact-subtitle">Evidence-first analyst workflow for case triage, transaction selection, and narrative lifecycle management.</div>', unsafe_allow_html=True)

render_case_context_bar()
st.divider()

if page == "Dashboard":
    c1, c2, c3, c4 = st.columns(4)
    selected_tx = pd.DataFrame(st.session_state.selected_transactions)
    total_suspicious = f"${selected_tx['Amount'].sum():,.2f}" if not selected_tx.empty else "$0.00"
    metrics = [
        ("Open Alerts", str(alerts_df[alerts_df["Status"] != "Closed"].shape[0])),
        ("High Risk Alerts", str(alerts_df[alerts_df["Risk Level"] == "High"].shape[0])),
        ("Selected Evidence Tx", str(selected_tx.shape[0])),
        ("Selected Evidence Amount", total_suspicious),
    ]
    for col, (label, value) in zip([c1, c2, c3, c4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()
    render_case_selection()

elif page == "Transaction Alerts":
    render_case_selection()

elif page == "Customer Information":
    render_customer_summary()

elif page == "KYC Data":
    render_customer_summary()

elif page == "Account & Transaction Data":
    render_transaction_selection()

elif page == "Case Management":
    st.subheader("Case Management")
    st.caption("Read-only case controls and assignment context.")
    c1, c2, c3 = st.columns(3)
    c1.text_input("Case ID", value=st.session_state.selected_case["Case ID"], disabled=True)
    c2.text_input("Case Status", value=st.session_state.selected_case["Status"], disabled=True)
    c3.text_input("Assigned Officer", value="Mariam Khan", disabled=True)
    st.info("Case actions are logged through the Narrative Generator controls.")

elif page == "Narrative Generator":
    render_narrative_generator()

elif page == "Audit Trail":
    render_audit_trail()

st.divider()
render_debug_panel()
