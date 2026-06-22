import streamlit as st

def metric_card(label, value, color):
    st.markdown(f"""
        <div style="
            background-color: {color};
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        ">
            <p style="color: white; font-size: 14px; margin: 0;">{label}</p>
            <h2 style="color: white; margin: 0;">{value}</h2>
        </div>
    """, unsafe_allow_html=True)

def analytics_card(title, headline, details, color):
    details_html = "".join(f"<li>{detail}</li>" for detail in details)

    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}, #1f2937);
            padding: 22px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
            color: white;
            height: 100%;
        ">
            <p style="margin: 0 0 8px 0; font-size: 13px; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.75;">{title}</p>
            <h2 style="margin: 0 0 14px 0; color: white; font-size: 32px; line-height: 1.1;">{headline}</h2>
            <ul style="margin: 0; padding-left: 18px; line-height: 1.7; font-size: 15px; opacity: 0.96;">
                {details_html}
            </ul>
        </div>
    """, unsafe_allow_html=True)