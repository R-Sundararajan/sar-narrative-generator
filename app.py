import pandas as pd
import streamlit as st


# -----------------------------------------------------------------------------
# Page configuration and global styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SAR Narrative Generator with Audit Trail",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for premium banking dashboard look-and-feel
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f5f7fb;
            color: #1f2a44;
        }
        .main-title {
            font-size: 2rem;
            font-weight: 700;
            color: #102a43;
            margin-bottom: 0.25rem;
        }
        .subtitle {
            color: #486581;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #d9e2ec;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(16, 42, 67, 0.08);
        }
        .metric-label {
            color: #486581;
            font-size: 0.9rem;
            margin-bottom: 0.2rem;
        }
        .metric-value {
            color: #102a43;
            font-size: 1.6rem;
            font-weight: 700;
        }
        .status-pill {
            display: inline-block;
            background-color: #e3f9e5;
            color: #207227;
            border: 1px solid #a7f3d0;
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .timeline-item {
            background-color: #ffffff;
            border-left: 3px solid #1f4b99;
            border-radius: 8px;
            padding: 0.8rem 1rem;
            margin-bottom: 0.7rem;
            box-shadow: 0 1px 2px rgba(16, 42, 67, 0.06);
        }
        .generated-narrative {
            background-color: #ffffff;
            border: 1px solid #c3dafe;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(16, 42, 67, 0.08);
            white-space: pre-wrap;
        }
        .small-muted {
            color: #627d98;
            font-size: 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Session state initialization
# -----------------------------------------------------------------------------
if "selected_alert" not in st.session_state:
    st.session_state.selected_alert = "ALT-1024"

if "generated_narrative" not in st.session_state:
    st.session_state.generated_narrative = ""

if "case_status" not in st.session_state:
    st.session_state.case_status = "Under Review"


# -----------------------------------------------------------------------------
# Placeholder datasets for all pages
# -----------------------------------------------------------------------------
alerts_df = pd.DataFrame(
    [
        ["ALT-1024", "2026-02-12", "Sophia Williams", "High", 185000.00, "Open"],
        ["ALT-1025", "2026-02-12", "Liam Johnson", "Medium", 94500.00, "Investigating"],
        ["ALT-1026", "2026-02-11", "Olivia Brown", "High", 250000.00, "Open"],
        ["ALT-1027", "2026-02-10", "Noah Davis", "Low", 12000.00, "Closed"],
        ["ALT-1028", "2026-02-09", "Emma Wilson", "Medium", 68000.00, "Pending"],
    ],
    columns=["Alert ID", "Date", "Customer Name", "Risk Level", "Amount", "Status"],
)

recent_alerts_df = alerts_df[["Alert ID", "Date", "Customer Name", "Risk Level", "Status"]]

transaction_history_df = pd.DataFrame(
    [
        ["TXN-7781", "2026-02-10", "Wire Transfer", 85000.00, "Outbound"],
        ["TXN-7782", "2026-02-10", "Cash Deposit", 60000.00, "Inbound"],
        ["TXN-7783", "2026-02-11", "International Transfer", 40000.00, "Outbound"],
        ["TXN-7784", "2026-02-12", "ACH Credit", 12000.00, "Inbound"],
    ],
    columns=["Transaction ID", "Date", "Type", "Amount", "Direction"],
)

audit_trail_df = pd.DataFrame(
    [
        ["2026-02-12 09:35", "m.khan", "Alert escalated", "CASE-3401", "Open"],
        ["2026-02-12 10:12", "a.patel", "KYC details updated", "CASE-3401", "In Progress"],
        ["2026-02-12 11:04", "r.chen", "Narrative draft generated", "CASE-3402", "Pending Review"],
        ["2026-02-12 12:26", "m.khan", "Case assigned", "CASE-3403", "Assigned"],
        ["2026-02-12 13:48", "a.patel", "SAR report submitted", "CASE-3398", "Completed"],
    ],
    columns=["Timestamp", "User", "Action", "Case ID", "Status"],
)


# -----------------------------------------------------------------------------
# Sidebar: navigation and system information
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏦 Bank Logo")
    st.markdown("#### SAR Narrative Generator")
    st.caption("Enterprise AML & Compliance Workspace")

    st.divider()

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
    st.write("Compliance Officer (placeholder)")
    st.markdown("**System Status**")
    st.markdown('<span class="status-pill">Active</span>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Shared page header
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">SAR Narrative Generator with Audit Trail</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Professional frontend prototype for banking compliance workflows.</div>',
    unsafe_allow_html=True,
)
st.divider()


# -----------------------------------------------------------------------------
# Page: Dashboard
# -----------------------------------------------------------------------------
if page == "Dashboard":
    # Summary metric cards
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("Total Alerts", "128"),
        ("High Risk Cases", "37"),
        ("Pending Narratives", "22"),
        ("Completed Reports", "69"),
    ]

    for col, (label, value) in zip([col1, col2, col3, col4], metrics):
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

    # Recent alerts table and activity timeline
    left, right = st.columns([1.8, 1.2])

    with left:
        st.subheader("Recent Alerts")
        st.dataframe(recent_alerts_df, use_container_width=True, hide_index=True)

    with right:
        st.subheader("Activity Timeline")
        timeline_items = [
            "09:35 - Alert ALT-1024 escalated to Level 2 review.",
            "10:12 - KYC profile updated for customer CUST-00981.",
            "11:04 - Draft narrative generated for CASE-3402.",
            "12:26 - New case CASE-3403 assigned to compliance team.",
        ]
        for item in timeline_items:
            st.markdown(f'<div class="timeline-item">{item}</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Page: Transaction Alerts
# -----------------------------------------------------------------------------
elif page == "Transaction Alerts":
    st.subheader("Transaction Alerts")
    st.caption("Monitor and review flagged transactions.")

    st.dataframe(alerts_df, use_container_width=True, hide_index=True)

    selected = st.selectbox("Select an Alert", alerts_df["Alert ID"].tolist(), index=0)
    st.session_state.selected_alert = selected

    selected_row = alerts_df[alerts_df["Alert ID"] == selected].iloc[0]
    st.info(
        f"Selected Alert: {selected_row['Alert ID']} | "
        f"Customer: {selected_row['Customer Name']} | "
        f"Risk: {selected_row['Risk Level']} | "
        f"Status: {selected_row['Status']}"
    )


# -----------------------------------------------------------------------------
# Page: Customer Information
# -----------------------------------------------------------------------------
elif page == "Customer Information":
    st.subheader("Customer Information")
    st.caption("Centralized customer profile details.")

    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            customer_name = st.text_input("Customer Name", value="Sophia Williams")
            customer_id = st.text_input("Customer ID", value="CUST-00981")
        with col2:
            dob = st.date_input("Date of Birth")
            nationality = st.text_input("Nationality", value="United Kingdom")
        with col3:
            risk_rating = st.selectbox("Risk Rating", ["Low", "Medium", "High"], index=2)
            occupation = st.text_input("Occupation", value="Import/Export Director")

    st.divider()
    st.markdown("##### Profile Summary")
    st.write(
        {
            "Customer Name": customer_name,
            "Customer ID": customer_id,
            "Date of Birth": str(dob),
            "Nationality": nationality,
            "Risk Rating": risk_rating,
            "Occupation": occupation,
        }
    )


# -----------------------------------------------------------------------------
# Page: KYC Data
# -----------------------------------------------------------------------------
elif page == "KYC Data":
    st.subheader("KYC Data")
    st.caption("Structured KYC review with expandable sections.")

    with st.expander("Identity Information", expanded=True):
        st.write("- Full Name: Sophia Williams")
        st.write("- National ID: UK-9283-1846")
        st.write("- Date of Birth: 1987-06-14")

    with st.expander("Address Information"):
        st.write("- Registered Address: 24 Sterling Lane, London")
        st.write("- Country: United Kingdom")
        st.write("- Postal Code: SW1A 2AA")

    with st.expander("Document Verification"):
        st.write("- Passport: Verified")
        st.write("- Utility Bill: Verified")
        st.write("- Company Registration: Pending Review")

    with st.expander("Risk Assessment"):
        st.write("- Overall KYC Risk: High")
        st.write("- Politically Exposed Person (PEP): No")
        st.write("- Sanctions Screening: No Match")


# -----------------------------------------------------------------------------
# Page: Account & Transaction Data
# -----------------------------------------------------------------------------
elif page == "Account & Transaction Data":
    st.subheader("Account & Transaction Data")
    st.caption("Account profile and historical transaction records.")

    col1, col2, col3 = st.columns(3)
    col1.text_input("Account Number", value="AC-55201984")
    col2.selectbox("Account Type", ["Corporate Checking", "Savings", "Investment"], index=0)
    col3.text_input("Balance", value="$1,248,765.42")

    st.divider()
    st.markdown("##### Transaction History")
    st.dataframe(transaction_history_df, use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# Page: Case Management
# -----------------------------------------------------------------------------
elif page == "Case Management":
    st.subheader("Case Management")
    st.caption("Manage investigation lifecycle and ownership.")

    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Case ID", value="CASE-3401")
            case_status = st.selectbox(
                "Case Status",
                ["Open", "Under Review", "Escalated", "Pending Approval", "Closed"],
                index=1,
            )
            st.session_state.case_status = case_status
        with c2:
            st.text_input("Assigned Officer", value="Mariam Khan")
            st.markdown('<div class="small-muted">Last Updated: 2026-02-12 13:48</div>', unsafe_allow_html=True)

    notes = st.text_area(
        "Notes",
        value=(
            "Initial review indicates unusual cross-border transfers and rapid movement "
            "of funds across related accounts. Pending enhanced due diligence."
        ),
        height=160,
    )

    st.info(f"Current case status: {st.session_state.case_status}")
    st.caption(f"Notes character count: {len(notes)}")


# -----------------------------------------------------------------------------
# Page: Narrative Generator (core feature)
# -----------------------------------------------------------------------------
elif page == "Narrative Generator":
    st.subheader("Narrative Generator")
    st.caption("Generate SAR narrative drafts from investigation context.")

    # Tabs provide structured data entry for narrative inputs
    tab1, tab2 = st.tabs(["Input Details", "Generated Output"])

    with tab1:
        suspicious_summary = st.text_area(
            "Suspicious Activity Summary",
            height=120,
            placeholder="Describe suspicious patterns observed...",
        )
        transaction_details = st.text_area(
            "Transaction Details",
            height=120,
            placeholder="Include key transaction dates, amounts, counterparties...",
        )
        customer_background = st.text_area(
            "Customer Background",
            height=120,
            placeholder="Summarize customer profile, risk category, and business activity...",
        )
        additional_notes = st.text_area(
            "Additional Notes",
            height=100,
            placeholder="Any relevant compliance observations...",
        )

        if st.button("Generate SAR Narrative", type="primary", use_container_width=True):
            st.session_state.generated_narrative = (
                "[PLACEHOLDER GENERATED NARRATIVE]\n\n"
                "Based on the provided case inputs, the subject account demonstrates a pattern of "
                "transactions inconsistent with the expected customer profile and stated source of funds. "
                "A series of high-value transfers were observed across multiple jurisdictions within a "
                "compressed time window, with layering indicators and limited economic rationale.\n\n"
                "The customer background review indicates elevated risk characteristics requiring enhanced "
                "monitoring. Internal controls triggered alert escalation following threshold breaches and "
                "behavioral anomalies.\n\n"
                "This narrative is a frontend placeholder output only and is not generated by a live AI model."
            )

    with tab2:
        if st.session_state.generated_narrative:
            st.success("Narrative generated successfully (placeholder).")
            st.markdown(
                f'<div class="generated-narrative">{st.session_state.generated_narrative}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.info("No narrative generated yet. Complete input fields and click the generate button.")


# -----------------------------------------------------------------------------
# Page: Audit Trail
# -----------------------------------------------------------------------------
elif page == "Audit Trail":
    st.subheader("Audit Trail")
    st.caption("Traceable record of user actions and case updates.")

    st.dataframe(audit_trail_df, use_container_width=True, hide_index=True)
