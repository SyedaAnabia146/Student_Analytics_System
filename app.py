import streamlit as st
import os
import pandas as pd

# Purani files se functions import
from data_manager import load_data, save_data, SUBJECT_COLS
from analytics import enrich_records, subject_wise_average, get_top_performers

# 1.PAGE CONFIG 
st.set_page_config(
    page_title="Teyzix Core | Advanced Analytics Dashboard",
    page_icon="🎓",
    layout="wide"
)

#  2. PREMIUM JET-BLACK CSS LAYER
st.markdown("""
    <style>
    /* Google Fonts Import for Elite Typography */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;800&family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* Deep Rich True Jet-Black Background */
    .stApp {
        background: #05070C !important;
        color: #F3F4F6 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Giga Title with Classy Executive Font & Sleek Typography */
    .giga-title {
        font-family: 'Cinzel', 'Playfair Display', serif !important;
        font-size: 42px !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        letter-spacing: 2px !important;
        margin-top: -30px !important;
        margin-bottom: 2px !important;
        text-align: left !important;
    }

    /* Creator Signature Badge - Corrected to Miss Anabia */
    .creator-badge {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #00F2FE !important;
        background: rgba(0, 242, 254, 0.08) !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        padding: 4px 12px !important;
        border-radius: 20px !important;
        display: inline-block !important;
        margin-bottom: 20px !important;
        letter-spacing: 0.5px !important;
    }

    /* Subtitle Layout */
    .sub-title {
        font-size: 16px !important;
        color: #9CA3AF !important;
        margin-bottom: 30px !important;
        font-weight: 400 !important;
        letter-spacing: 0.5px !important;
    }

    /* Responsive KPI Metrics Box Optimization */
    div[data-testid="stMetric"] {
        background: rgba(13, 18, 30, 0.8) !important;
        border: 1px solid rgba(0, 242, 254, 0.12) !important;
        border-radius: 14px !important;
        padding: 15px 18px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1) !important;
        overflow: hidden !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px) !important;
        border-color: #00F2FE !important;
        box-shadow: 0 12px 35px rgba(0, 242, 254, 0.2) !important;
    }

    /* Metric Header Text Size Reduction */
    div[data-testid="stMetricLabel"] p {
        color: #9CA3AF !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        white-space: nowrap !important;
    }
    
    /* Metric Main Numerical Value Font Adjustment */
    div[data-testid="stMetricValue"] div {
        color: #FFFFFF !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        white-space: nowrap !important;
    }

    /* Section Cards Custom Glassmorphism */
    .glass-card {
        background: rgba(13, 18, 30, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        padding: 25px !important;
        border-radius: 18px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6) !important;
        margin-top: 20px !important;
    }

    /* Input Field Modifications */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #0D121E !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
    }

    /* Submit Button with Dynamic Glow Gradient */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.2) !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4) !important;
        background: linear-gradient(90deg, #4FACFE 0%, #00F2FE 100%) !important;
    }

    /* Progress Fill Accent */
    .stProgress > div > div > div > div {
        background-color: #00F2FE !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. DATA PERSISTENCE LAYER 
records = load_data()
enriched = enrich_records(records)
df_display = pd.DataFrame(enriched) if enriched else pd.DataFrame()

# 4. SIDEBAR PANEL
with st.sidebar:
    st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#00F2FE; font-weight:700; font-size:26px; margin-bottom:5px;'>📝 Registration</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9CA3AF; font-size:13px; margin-bottom:20px;'>Deploy new student profile to core ledger.</p>", unsafe_allow_html=True)
    
    with st.form("add_student_form", clear_on_submit=True):
        s_id = st.text_input("🆔 Student ID", placeholder="e.g. S011")
        s_name = st.text_input("👤 Full Name", placeholder="Enter student name")
        s_class = st.selectbox("🏫 Assigned Class", ["10A", "10B", "11A", "11B", "12A"])
        
        st.markdown("<p style='color:#00F2FE; font-weight:600; margin-top:12px; margin-bottom:5px;'>📊 Academic Scores</p>", unsafe_allow_html=True)
        marks = {}
        cols = st.columns(2)
        for i, sub in enumerate(SUBJECT_COLS):
            with cols[i % 2]:
                marks[sub] = st.number_input(f"{sub.capitalize()}", 0, 100, 0)
        
        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("Secure Record")
        
        if submit_btn:
            if any(r['student_id'] == s_id for r in records):
                st.error("Error: Duplicate ID.")
            elif not s_id or not s_name:
                st.warning("Error: Credentials required.")
            else:
                new_student = {"student_id": s_id, "name": s_name, "class": s_class}
                for sub in SUBJECT_COLS: new_student[sub] = int(marks[sub])
                records.append(new_student)
                save_data(records)
                st.success("Record Authenticated!")
                st.rerun()

# 5. EXECUTIVE HERO HEADER
st.markdown('<h1 class="giga-title">STUDENT ANALYTICS HUB</h1>', unsafe_allow_html=True)
st.markdown('<div class="creator-badge">⚡ Developed by Miss Anabia</div>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Advanced Modular Intelligence Platform for Teyzix Core Execution Framework.</p>', unsafe_allow_html=True)

# High-Gloss KPI Metric Layout
if not df_display.empty:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Enrolled", f"{len(df_display)} Students")
    m2.metric("Cumulative Average", f"{round(df_display['percentage'].mean(), 1)}%")
    m3.metric("Highest Grade", "A+")
    m4.metric("Monitored Cohorts", f"{df_display['class'].nunique()} Classes")

st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)

# 6. NAV INTERFACE 
tab1, tab2, tab3 = st.tabs(["📁 Database Explorer", "📊 Performance Analytics", "🎨 Visual Gallery"])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#00F2FE; font-weight:700; margin-bottom:15px;'>🖥️ Real-time Data Grid Master View</h3>", unsafe_allow_html=True)
    if not df_display.empty:
        st.dataframe(
            df_display.style.set_properties(**{
                'background-color': '#0D121E',
                'color': '#FFFFFF',
                'border-color': 'rgba(0, 242, 254, 0.08)'
            }),
            use_container_width=True
        )
    else:
        st.info("System Engine Online. Awaiting dataset configuration.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    if not df_display.empty:
        col_a, col_b = st.columns([5, 4])
        
        with col_a:
            st.markdown("<h3 style='color:#00F2FE; font-weight:700; margin-bottom:15px;'>⭐ Elite Performers Panel</h3>", unsafe_allow_html=True)
            top_students = get_top_performers(enriched)
            if top_students:
                st.dataframe(pd.DataFrame(top_students)[['name', 'class', 'percentage', 'grade']], use_container_width=True)
            else:
                st.write("No candidates currently meeting elite thresholds.")
        
        with col_b:
            st.markdown("<h3 style='color:#00F2FE; font-weight:700; margin-bottom:15px;'>📚 Metrics & Target Indicators</h3>", unsafe_allow_html=True)
            sub_avgs = subject_wise_average(enriched)
            for sub, avg in sub_avgs.items():
                st.markdown(f"<div style='display:flex; justify-content:space-between; font-weight:600; margin-bottom:2px;'><span>{sub.upper()}</span><span style='color:#00F2FE;'>{avg}%</span></div>", unsafe_allow_html=True)
                st.progress(avg / 100)
    else:
        st.info("Analytics engine suspended due to lack of records.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#00F2FE; font-weight:700; margin-bottom:25px;'>🏆 Live Executive Visual Gallery</h3>", unsafe_allow_html=True)
    
    if not df_display.empty:
        import matplotlib.pyplot as plt
        
        img_cols = st.columns(3)
        
        #  CHART 1: Subject Performance Index
        with img_cols[0]:
            st.markdown("<div style='background: rgba(13, 18, 30, 0.9); padding: 12px; border-radius: 10px; border: 1px solid rgba(0, 242, 254, 0.08); text-align:center; font-weight:700; color:#FFFFFF; margin-bottom:12px;'>📊 Subject Performance Index</div>", unsafe_allow_html=True)
            
            sub_avgs = subject_wise_average(enriched)
            subjects = [s.upper() for s in sub_avgs.keys()]
            values = list(sub_avgs.values())
            
            fig1, ax1 = plt.subplots(figsize=(5, 4))
            fig1.patch.set_facecolor('#05070C')
            ax1.set_facecolor('#0D121E')
            
            bars1 = ax1.bar(subjects, values, color="#00F2FE", edgecolor="white", width=0.5)
            ax1.set_ylim(0, 110)
            ax1.tick_params(colors='white', labelsize=10)
            ax1.spines['bottom'].set_color('white')
            ax1.spines['left'].set_color('white')
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.grid(axis='y', linestyle='--', alpha=0.1)
            
            for bar in bars1:
                yval = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{round(yval,1)}%", ha='center', va='bottom', color='white', fontsize=8)
                
            st.pyplot(fig1)
            
        # CHART 2: Class Performance Distribution 
        with img_cols[1]:
            st.markdown("<div style='background: rgba(13, 18, 30, 0.9); padding: 12px; border-radius: 10px; border: 1px solid rgba(0, 242, 254, 0.08); text-align:center; font-weight:700; color:#FFFFFF; margin-bottom:12px;'>🏫 Cohort Performance Distribution</div>", unsafe_allow_html=True)
            
            class_groups = df_display.groupby('class')['percentage'].mean().reset_index()
            
            fig2, ax2 = plt.subplots(figsize=(5, 4))
            fig2.patch.set_facecolor('#05070C')
            ax2.set_facecolor('#0D121E')
            
            bars2 = ax2.bar(class_groups['class'], class_groups['percentage'], color="#4FACFE", edgecolor="white", width=0.5)
            ax2.set_ylim(0, 110)
            ax2.tick_params(colors='white', labelsize=10)
            ax2.spines['bottom'].set_color('white')
            ax2.spines['left'].set_color('white')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.grid(axis='y', linestyle='--', alpha=0.1)
            
            for bar in bars2:
                yval = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{round(yval,1)}%", ha='center', va='bottom', color='white', fontsize=8)
                
            st.pyplot(fig2)
            
        #  CHART 3: Academic Merit Matrix
        with img_cols[2]:
            st.markdown("<div style='background: rgba(13, 18, 30, 0.9); padding: 12px; border-radius: 10px; border: 1px solid rgba(0, 242, 254, 0.08); text-align:center; font-weight:700; color:#FFFFFF; margin-bottom:12px;'>🏆 Academic Merit Matrix</div>", unsafe_allow_html=True)
            
            top_students = get_top_performers(enriched)
            if top_students:
                top_df = pd.DataFrame(top_students).head(5)
                names = [s['name'].split()[0] for s in top_students[:5]]
                percentages = [s['percentage'] for s in top_students[:5]]
                
                fig3, ax3 = plt.subplots(figsize=(5, 4))
                fig3.patch.set_facecolor('#05070C')
                ax3.set_facecolor('#0D121E')
                
                bars3 = ax3.barh(names, percentages, color="teal", edgecolor="white")
                ax3.set_xlim(0, 115)
                ax3.tick_params(colors='white', labelsize=10)
                ax3.invert_yaxis()
                ax3.spines['bottom'].set_color('white')
                ax3.spines['left'].set_color('white')
                ax3.spines['top'].set_visible(False)
                ax3.spines['right'].set_visible(False)
                
                for bar in bars3:
                    xval = bar.get_width()
                    ax3.text(xval + 2, bar.get_y() + bar.get_height()/2, f"{round(xval,1)}%", ha='left', va='center', color='white', fontsize=8)
                    
                st.pyplot(fig3)
            else:
                st.write("No elite performers found yet.")
    else:
        st.info("No live data available to render visual graphs.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# 7. FOOTER PLATFORM AUDIT
st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: rgba(255,255,255,0.03);'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563; font-size: 12px; font-weight:600;'>ENGINE CONFIG: STREAMLIT SAAS CORE PLATFORM EDITION V3.0 | DESIGNED BY MISS ANABIA FOR TEYZIX CORE INTERNSHIP AUDIT</p>", unsafe_allow_html=True)
