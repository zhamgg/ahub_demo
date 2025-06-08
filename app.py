import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="AHUB 2.0 - Analytics Hub Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Great Gray branding
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-good {
        color: #10b981;
        font-weight: bold;
    }
    .status-warning {
        color: #f59e0b;
        font-weight: bold;
    }
    .status-error {
        color: #ef4444;
        font-weight: bold;
    }
    .layer-header {
        background: #f8fafc;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border-left: 4px solid #64748b;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Generate realistic synthetic data for demo purposes"""
    
    # Data sources simulation
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    # Northern Trust data
    nt_data = []
    for i, date in enumerate(dates[:90]):  # Last 90 days
        for account in ['FUND001', 'FUND002', 'FUND003', 'FUND004', 'FUND005']:
            nt_data.append({
                'date': date,
                'account_id': account,
                'nav': 100 + np.random.normal(0, 2) + i * 0.01,
                'total_assets': np.random.uniform(50000000, 200000000),
                'shares_outstanding': np.random.uniform(500000, 2000000),
                'source': 'Northern Trust'
            })
    
    # State Street data
    ss_data = []
    for i, date in enumerate(dates[:90]):
        for account in ['FUND001', 'FUND002', 'FUND003']:
            ss_data.append({
                'date': date,
                'account_id': account,
                'market_value': np.random.uniform(45000000, 190000000),
                'cash_balance': np.random.uniform(1000000, 5000000),
                'accrued_income': np.random.uniform(100000, 500000),
                'source': 'State Street'
            })
    
    # FactSet data
    fs_data = []
    for i, date in enumerate(dates[:90]):
        for account in ['FUND001', 'FUND002', 'FUND004', 'FUND005']:
            fs_data.append({
                'date': date,
                'account_id': account,
                'benchmark_return': np.random.normal(0.0008, 0.02),
                'risk_score': np.random.uniform(1, 10),
                'expense_ratio': np.random.uniform(0.005, 0.025),
                'source': 'FactSet'
            })
    
    return pd.DataFrame(nt_data), pd.DataFrame(ss_data), pd.DataFrame(fs_data)

def create_unified_dataset(nt_df, ss_df, fs_df):
    """Simulate the Silver layer unified data"""
    
    # Create unified fund data
    unified_data = []
    
    for date in nt_df['date'].unique():
        for account in nt_df['account_id'].unique():
            nt_row = nt_df[(nt_df['date'] == date) & (nt_df['account_id'] == account)]
            ss_row = ss_df[(ss_df['date'] == date) & (ss_df['account_id'] == account)]
            fs_row = fs_df[(fs_df['date'] == date) & (fs_df['account_id'] == account)]
            
            if not nt_row.empty:
                unified_row = {
                    'date': date,
                    'fund_id': account,
                    'nav_per_share': nt_row.iloc[0]['nav'],
                    'total_net_assets': nt_row.iloc[0]['total_assets'],
                    'shares_outstanding': nt_row.iloc[0]['shares_outstanding'],
                    'market_value': ss_row.iloc[0]['market_value'] if not ss_row.empty else nt_row.iloc[0]['total_assets'] * 0.95,
                    'cash_balance': ss_row.iloc[0]['cash_balance'] if not ss_row.empty else nt_row.iloc[0]['total_assets'] * 0.05,
                    'benchmark_return': fs_row.iloc[0]['benchmark_return'] if not fs_row.empty else np.random.normal(0.0008, 0.02),
                    'risk_score': fs_row.iloc[0]['risk_score'] if not fs_row.empty else np.random.uniform(1, 10),
                    'data_quality_score': np.random.uniform(85, 99)
                }
                unified_data.append(unified_row)
    
    return pd.DataFrame(unified_data)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AHUB 2.0 - Analytics Hub Demo</h1>
        <p>From Spreadsheets to AI: Transforming Retirement Technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    demo_sections = [
        "🏠 Overview",
        "📥 Source Data Ingestion", 
        "🥉 Bronze Layer - Raw Staging",
        "🥈 Silver Layer - Data Vault",
        "🥇 Gold Layer - Business Intelligence",
        "📊 Real-time Monitoring",
        "💼 Business Impact"
    ]
    
    selected_section = st.sidebar.selectbox("Select Demo Section:", demo_sections)
    
    # Generate sample data
    if 'data_generated' not in st.session_state:
        with st.spinner("Generating sample data..."):
            st.session_state.nt_data, st.session_state.ss_data, st.session_state.fs_data = generate_sample_data()
            st.session_state.unified_data = create_unified_dataset(
                st.session_state.nt_data, 
                st.session_state.ss_data, 
                st.session_state.fs_data
            )
            st.session_state.data_generated = True
    
    # Section routing
    if selected_section == "🏠 Overview":
        show_overview()
    elif selected_section == "📥 Source Data Ingestion":
        show_source_ingestion()
    elif selected_section == "🥉 Bronze Layer - Raw Staging":
        show_bronze_layer()
    elif selected_section == "🥈 Silver Layer - Data Vault":
        show_silver_layer()
    elif selected_section == "🥇 Gold Layer - Business Intelligence":
        show_gold_layer()
    elif selected_section == "📊 Real-time Monitoring":
        show_monitoring()
    elif selected_section == "💼 Business Impact":
        show_business_impact()

def show_overview():
    st.header("📋 AHUB 2.0 Architecture Overview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Key Differentiators")
        
        differentiators = [
            ("🔄 Unified Data", "Single source of truth for all retirement data"),
            ("⚡ Process Automation", "Intelligent workflows that minimize manual intervention"),
            ("🔮 Predictive Intelligence", "AI that anticipates and prevents issues"),
            ("👥 Stakeholder Design", "Personalized experiences for each industry stakeholder"),
            ("🛡️ Compliance Automation", "Proactive monitoring and reporting"),
            ("🤖 Self-Optimizing Systems", "Systems that learn and improve autonomously"),
            ("🔗 Seamless Integrations", "Seamless connections to industry platforms")
        ]
        
        for title, description in differentiators:
            with st.container():
                st.markdown(f"**{title}**")
                st.write(description)
                st.markdown("---")
    
    with col2:
        st.subheader("📊 Current Status")
        
        # Status metrics
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Data Sources", "5", "↗️ +2")
            st.metric("Data Quality", "96.2%", "↗️ +12%")
        with col_b:
            st.metric("Processing Speed", "0.88s", "🔽 -75%")
            st.metric("Automation", "85%", "↗️ +68%")
        
        st.subheader("🏗️ Architecture Layers")
        layers = ["🥇 Gold - Business Intelligence", "🥈 Silver - Data Vault", "🥉 Bronze - Raw Staging", "📥 Source Data"]
        
        for i, layer in enumerate(layers):
            if i < len(layers) - 1:
                st.write(f"{layer} ⬇️")
            else:
                st.write(layer)

def show_source_ingestion():
    st.header("📥 Source Data Ingestion")
    
    st.write("""
    AHUB 2.0 connects to multiple data sources across the retirement ecosystem, 
    automatically identifying and processing new data as it becomes available.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    # Data source simulation
    sources = [
        {"name": "Northern Trust", "status": "✅ Connected", "last_sync": "2 min ago", "records": 1247},
        {"name": "State Street", "status": "✅ Connected", "last_sync": "5 min ago", "records": 892},
        {"name": "FactSet", "status": "✅ Connected", "last_sync": "1 min ago", "records": 1056},
        {"name": "BoardingPass", "status": "✅ Connected", "last_sync": "3 min ago", "records": 2341},
        {"name": "Morningstar", "status": "⏳ Syncing", "last_sync": "Now", "records": 0}
    ]
    
    for i, source in enumerate(sources):
        col = [col1, col2, col3][i % 3]
        with col:
            with st.container():
                st.markdown(f"### {source['name']}")
                st.write(f"**Status:** {source['status']}")
                st.write(f"**Last Sync:** {source['last_sync']}")
                st.write(f"**Records:** {source['records']:,}")
                
                if "Syncing" in source['status']:
                    progress = st.progress(0)
                    for j in range(100):
                        time.sleep(0.01)
                        progress.progress(j + 1)
                    st.success("Sync completed!")
    
    st.subheader("📁 Sample Raw Data")
    
    # Show sample raw data from different sources
    source_tabs = st.tabs(["Northern Trust", "State Street", "FactSet"])
    
    with source_tabs[0]:
        st.write("**Fund Accounting Valuation Details**")
        sample_nt = st.session_state.nt_data.head(10)[['date', 'account_id', 'nav', 'total_assets', 'shares_outstanding']]
        st.dataframe(sample_nt, use_container_width=True)
    
    with source_tabs[1]:
        st.write("**Custody and Settlement Data**")
        sample_ss = st.session_state.ss_data.head(10)[['date', 'account_id', 'market_value', 'cash_balance', 'accrued_income']]
        st.dataframe(sample_ss, use_container_width=True)
    
    with source_tabs[2]:
        st.write("**Market Data and Analytics**")
        sample_fs = st.session_state.fs_data.head(10)[['date', 'account_id', 'benchmark_return', 'risk_score', 'expense_ratio']]
        st.dataframe(sample_fs, use_container_width=True)

def show_bronze_layer():
    st.header("🥉 Bronze Layer - Raw Data Staging")
    
    st.markdown("""
    <div class="layer-header">
        <h4>🎯 Purpose: Initial staging and validation of raw data</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📊 Staging Tables Overview")
        
        # Simulate staging table stats
        staging_stats = pd.DataFrame({
            'Source': ['Northern Trust', 'State Street', 'FactSet', 'BoardingPass', 'Morningstar'],
            'Records Ingested': [1247, 892, 1056, 2341, 0],
            'Quality Score': [98.2, 96.7, 99.1, 97.4, 0],
            'Processing Time (s)': [0.8, 0.6, 0.9, 1.2, 0],
            'Status': ['✅ Complete', '✅ Complete', '✅ Complete', '✅ Complete', '⏳ Processing']
        })
        
        st.dataframe(staging_stats, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Performance")
        st.metric("Avg Processing Time", "0.88s", "🔽 -75%")
        st.metric("Success Rate", "99.97%", "↗️ +0.12%")
        st.metric("Data Volume", "5.5GB", "↗️ +15%")
    
    st.subheader("🔍 Data Validation Results")
    
    # Data quality checks
    quality_checks = pd.DataFrame({
        'Check Type': ['Schema Validation', 'Null Value Check', 'Data Type Validation', 'Range Validation', 'Duplicate Detection'],
        'Northern Trust': ['✅ Pass', '✅ Pass', '✅ Pass', '⚠️ 2 outliers', '✅ Pass'],
        'State Street': ['✅ Pass', '✅ Pass', '✅ Pass', '✅ Pass', '✅ Pass'],
        'FactSet': ['✅ Pass', '✅ Pass', '✅ Pass', '✅ Pass', '✅ Pass'],
        'BoardingPass': ['✅ Pass', '⚠️ 5 nulls', '✅ Pass', '✅ Pass', '❌ 12 dupes']
    })
    
    st.dataframe(quality_checks, use_container_width=True)
    
    # Show transformation example
    st.subheader("🔄 Data Transformation Example")
    
    transformation_tabs = st.tabs(["Before", "After", "Changes"])
    
    with transformation_tabs[0]:
        st.write("**Raw Northern Trust Data**")
        raw_sample = pd.DataFrame({
            'Account ID (FA)': ['FUND001', 'FUND002'],
            'Total MV Securities (Base)': ['$50,000,000.00', '$75,000,000.00'],
            'NAV (8 Precision)': ['100.12345678', '98.87654321'],
            'As of Date': ['2024-01-15', '2024-01-15']
        })
        st.dataframe(raw_sample, use_container_width=True)
    
    with transformation_tabs[1]:
        st.write("**Cleaned Staging Data**")
        clean_sample = pd.DataFrame({
            'account_id': ['FUND001', 'FUND002'],
            'total_market_value': [50000000.00, 75000000.00],
            'nav_per_share': [100.12345678, 98.87654321],
            'valuation_date': ['2024-01-15', '2024-01-15'],
            'source_system': ['Northern Trust', 'Northern Trust'],
            'ingestion_timestamp': ['2024-01-15 09:30:00', '2024-01-15 09:30:00']
        })
        st.dataframe(clean_sample, use_container_width=True)
    
    with transformation_tabs[2]:
        st.write("**Applied Transformations:**")
        st.write("✅ Removed special characters from column names")
        st.write("✅ Converted currency strings to numeric values")
        st.write("✅ Standardized date formats")
        st.write("✅ Added audit fields (source_system, ingestion_timestamp)")
        st.write("✅ Applied data type validations")

def show_silver_layer():
    st.header("🥈 Silver Layer - Data Vault")
    
    st.markdown("""
    <div class="layer-header">
        <h4>🎯 Purpose: Unified data integration and business rule application</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Show the medallion architecture progress
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🥉 Bronze → 🥈 Silver")
        st.write("✅ Raw data vault created")
        st.write("✅ Business rules applied")
        st.write("✅ Data quality improved")
    
    with col2:
        st.markdown("### 📊 Integration Stats")
        st.metric("Sources Unified", "5", "↗️ +2")
        st.metric("Data Quality", "96.2%", "↗️ +12%")
        st.metric("Records Matched", "98.7%", "↗️ +8%")
    
    with col3:
        st.markdown("### ⚙️ Business Rules")
        st.write("✅ Master Data Management")
        st.write("✅ Cross-source validation")
        st.write("✅ Calculated fields added")
    
    st.subheader("🔗 Data Vault Model")
    
    # Show unified data sample
    st.write("**Unified Fund Data (Business Data Vault)**")
    unified_sample = st.session_state.unified_data.head(10)
    st.dataframe(unified_sample, use_container_width=True)
    
    # Data lineage visualization
    st.subheader("🔍 Data Lineage & Integration")
    
    lineage_data = pd.DataFrame({
        'Fund ID': ['FUND001', 'FUND001', 'FUND002', 'FUND002'],
        'Source System': ['Northern Trust', 'State Street', 'Northern Trust', 'FactSet'],
        'Data Element': ['NAV', 'Market Value', 'NAV', 'Benchmark Return'],
        'Last Updated': ['2024-01-15 09:30', '2024-01-15 09:32', '2024-01-15 09:30', '2024-01-15 09:28'],
        'Quality Score': [99.2, 97.8, 98.9, 99.5]
    })
    
    st.dataframe(lineage_data, use_container_width=True)
    
    # Show data quality improvements
    st.subheader("📈 Data Quality Improvements")
    
    # Create before/after quality comparison
    quality_comparison = pd.DataFrame({
        'Metric': ['Completeness', 'Accuracy', 'Consistency', 'Timeliness', 'Validity'],
        'Before (Bronze)': [87.2, 91.5, 78.3, 85.7, 89.1],
        'After (Silver)': [96.8, 98.2, 95.4, 97.1, 98.9],
        'Improvement': ['+9.6%', '+6.7%', '+17.1%', '+11.4%', '+9.8%']
    })
    
    fig = px.bar(quality_comparison, x='Metric', y=['Before (Bronze)', 'After (Silver)'], 
                 title="Data Quality: Bronze vs Silver Layer",
                 barmode='group',
                 color_discrete_map={'Before (Bronze)': '#ef4444', 'After (Silver)': '#10b981'})
    
    st.plotly_chart(fig, use_container_width=True)

def show_gold_layer():
    st.header("🥇 Gold Layer - Business Intelligence")
    
    st.markdown("""
    <div class="layer-header">
        <h4>🎯 Purpose: Business-ready data for analytics and reporting</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics dashboard
    st.subheader("📊 Executive Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate some business metrics
    total_aum = st.session_state.unified_data['total_net_assets'].sum() / 1e9
    avg_nav = st.session_state.unified_data['nav_per_share'].mean()
    avg_risk = st.session_state.unified_data['risk_score'].mean()
    quality_score = st.session_state.unified_data['data_quality_score'].mean()
    
    with col1:
        st.metric("Total AUM", f"${total_aum:.1f}B", "↗️ +5.2%")
    with col2:
        st.metric("Avg NAV", f"${avg_nav:.2f}", "↗️ +0.8%")
    with col3:
        st.metric("Avg Risk Score", f"{avg_risk:.1f}/10", "🔽 -0.3")
    with col4:
        st.metric("Data Quality", f"{quality_score:.1f}%", "↗️ +2.1%")
    
    # Fund performance visualization
    st.subheader("📈 Fund Performance Analysis")
    
    # Create performance chart
    daily_performance = st.session_state.unified_data.groupby(['date', 'fund_id']).agg({
        'nav_per_share': 'mean',
        'total_net_assets': 'sum'
    }).reset_index()
    
    fig = px.line(daily_performance, x='date', y='nav_per_share', color='fund_id',
                  title="NAV Performance by Fund",
                  labels={'nav_per_share': 'NAV per Share ($)', 'date': 'Date'})
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Risk Distribution")
        risk_dist = st.session_state.unified_data.groupby('fund_id')['risk_score'].mean().reset_index()
        
        fig_risk = px.bar(risk_dist, x='fund_id', y='risk_score',
                         title="Average Risk Score by Fund",
                         color='risk_score',
                         color_continuous_scale='RdYlGn_r')
        
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        st.subheader("💰 Asset Allocation")
        asset_allocation = st.session_state.unified_data.groupby('fund_id')['total_net_assets'].sum().reset_index()
        
        fig_assets = px.pie(asset_allocation, values='total_net_assets', names='fund_id',
                           title="AUM Distribution by Fund")
        
        st.plotly_chart(fig_assets, use_container_width=True)
    
    # Automated reports section
    st.subheader("📄 Automated Reports")
    
    report_tabs = st.tabs(["Daily Summary", "Risk Report", "Compliance Check"])
    
    with report_tabs[0]:
        st.write("**Daily Fund Summary Report - Generated Automatically**")
        daily_summary = st.session_state.unified_data.groupby('fund_id').agg({
            'nav_per_share': ['mean', 'std'],
            'total_net_assets': 'sum',
            'risk_score': 'mean',
            'data_quality_score': 'mean'
        }).round(2)
        
        daily_summary.columns = ['Avg NAV', 'NAV Volatility', 'Total Assets', 'Risk Score', 'Data Quality']
        st.dataframe(daily_summary, use_container_width=True)
    
    with report_tabs[1]:
        st.write("**Risk Monitoring Report**")
        
        # Risk alerts
        high_risk_funds = st.session_state.unified_data[st.session_state.unified_data['risk_score'] > 7]
        if not high_risk_funds.empty:
            st.warning(f"⚠️ {len(high_risk_funds)} funds showing elevated risk levels")
            st.dataframe(high_risk_funds[['fund_id', 'risk_score', 'date']].head(), use_container_width=True)
        else:
            st.success("✅ All funds within acceptable risk parameters")
    
    with report_tabs[2]:
        st.write("**Compliance Monitoring**")
        
        compliance_checks = pd.DataFrame({
            'Check': ['Data Completeness', 'Regulatory Reporting', 'NAV Validation', 'Risk Limits', 'Documentation'],
            'Status': ['✅ Pass', '✅ Pass', '✅ Pass', '⚠️ Review', '✅ Pass'],
            'Last Check': ['09:30 AM', '09:28 AM', '09:31 AM', '09:29 AM', '09:27 AM']
        })
        
        st.dataframe(compliance_checks, use_container_width=True)

def show_monitoring():
    st.header("📊 Real-time Monitoring & Alerts")
    
    st.markdown("""
    <div class="layer-header">
        <h4>🎯 Purpose: Proactive monitoring and self-optimizing systems</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # System health metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🖥️ System Health")
        st.metric("Uptime", "99.97%", "↗️ +0.02%")
        st.metric("Response Time", "0.88s", "🔽 -0.45s")
        st.metric("Throughput", "1.2M rec/hr", "↗️ +15%")
    
    with col2:
        st.subheader("🔄 Pipeline Status")
        st.metric("Active Pipelines", "12", "→ 0")
        st.metric("Success Rate", "99.8%", "↗️ +0.3%")
        st.metric("Avg Processing", "2.1 min", "🔽 -30s")
    
    with col3:
        st.subheader("🛡️ Security & Compliance")
        st.metric("Access Violations", "0", "→ 0")
        st.metric("Data Leakage Alerts", "0", "→ 0")
        st.metric("Compliance Score", "98.5%", "↗️ +1.2%")
    
    # Real-time alerts
    st.subheader("🚨 Active Alerts & Notifications")
    
    # Simulate real-time alerts
    alerts_data = pd.DataFrame({
        'Time': ['09:31:23', '09:28:45', '09:25:12', '09:22:33'],
        'Type': ['INFO', 'WARNING', 'SUCCESS', 'INFO'],
        'Component': ['Data Quality', 'Processing', 'Integration', 'Security'],
        'Message': [
            'FUND004 data quality score improved to 99.2%',
            'Processing time for State Street feed increased by 15%',
            'FactSet integration completed successfully - 1,056 records',
            'Daily security scan completed - no issues found'
        ],
        'Action': ['None', 'Monitor', 'None', 'None']
    })
    
    # Color code alerts
    def style_alerts(row):
        if row['Type'] == 'WARNING':
            return ['background-color: #fef3c7'] * len(row)
        elif row['Type'] == 'SUCCESS':
            return ['background-color: #d1fae5'] * len(row)
        else:
            return ['background-color: #f0f9ff'] * len(row)
    
    styled_alerts = alerts_data.style.apply(style_alerts, axis=1)
    st.dataframe(styled_alerts, use_container_width=True)
    
    # Data quality monitoring
    st.subheader("📈 Data Quality Trends")
    
    # Generate quality trend data
    dates = pd.date_range(start='2024-01-01', end='2024-01-15', freq='D')
    quality_trends = pd.DataFrame({
        'Date': dates,
        'Overall Quality': [85 + i + np.random.normal(0, 2) for i in range(len(dates))],
        'Completeness': [88 + i * 0.5 + np.random.normal(0, 1) for i in range(len(dates))],
        'Accuracy': [90 + i * 0.3 + np.random.normal(0, 1.5) for i in range(len(dates))],
        'Timeliness': [85 + i * 0.8 + np.random.normal(0, 1) for i in range(len(dates))]
    })
    
    fig_quality = px.line(quality_trends, x='Date', y=['Overall Quality', 'Completeness', 'Accuracy', 'Timeliness'],
                         title="Data Quality Trends (Last 15 Days)",
                         labels={'value': 'Quality Score (%)', 'variable': 'Metric'})
    
    st.plotly_chart(fig_quality, use_container_width=True)
    
    # Predictive alerts
    st.subheader("🔮 Predictive Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Predicted Issues (Next 24 Hours)**")
        predictions = pd.DataFrame({
            'Risk Level': ['🟡 Medium', '🟢 Low', '🟡 Medium', '🟢 Low'],
            'Component': ['State Street Feed', 'Data Quality', 'Processing Load', 'Storage Capacity'],
            'Prediction': [
                'Processing time may increase by 20%',
                'Quality scores expected to remain stable',
                'Peak load expected at 2 PM EST',
                'Storage utilization normal'
            ],
            'Confidence': ['85%', '92%', '78%', '94%']
        })
        st.dataframe(predictions, use_container_width=True)
    
    with col2:
        st.write("**Auto-Optimization Actions**")
        optimizations = pd.DataFrame({
            'Time': ['09:15', '09:20', '09:25', '09:30'],
            'Action': [
                'Increased processing capacity for peak load',
                'Optimized query execution plan',
                'Adjusted data quality thresholds',
                'Balanced workload across clusters'
            ],
            'Impact': ['+15% throughput', '-0.3s latency', '+2% accuracy', '+8% efficiency']
        })
        st.dataframe(optimizations, use_container_width=True)

def show_business_impact():
    st.header("💼 Business Impact & ROI")
    
    st.markdown("""
    <div class="layer-header">
        <h4>🎯 Purpose: Demonstrating tangible business value and competitive advantage</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # ROI Metrics
    st.subheader("💰 Return on Investment")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Time Savings", "75%", "↗️ Manual → Auto")
        st.write("*Process automation*")
    
    with col2:
        st.metric("Error Reduction", "88%", "🔽 Data inconsistencies")
        st.write("*Quality improvements*")
    
    with col3:
        st.metric("Faster Insights", "10x", "↗️ Hours → Minutes")
        st.write("*Real-time analytics*")
    
    with col4:
        st.metric("Cost Reduction", "$2.1M", "🔽 Annual savings")
        st.write("*Operational efficiency*")
    
    # Before vs After comparison
    st.subheader("📊 Before vs After AHUB 2.0")
    
    comparison_data = pd.DataFrame({
        'Metric': [
            'Report Generation Time',
            'Data Quality Issues',
            'Manual Interventions',
            'Data Latency',
            'Compliance Violations',
            'System Downtime'
        ],
        'Before AHUB 2.0': ['4-6 hours', '15-20 per week', '40+ per day', '2-4 hours', '2-3 per month', '8 hours/month'],
        'After AHUB 2.0': ['5-10 minutes', '1-2 per week', '3-5 per day', '< 5 minutes', '0 per month', '< 1 hour/month'],
        'Improvement': ['95% faster', '90% reduction', '87% reduction', '95% faster', '100% reduction', '87% reduction']
    })
    
    st.dataframe(comparison_data, use_container_width=True)
    
    # Stakeholder benefits
    st.subheader("👥 Stakeholder Benefits")
    
    stakeholder_tabs = st.tabs(["Plan Sponsors", "Advisors", "Participants", "Operations"])
    
    with stakeholder_tabs[0]:
        st.write("**Plan Sponsors**")
        benefits = [
            "🔍 **Real-time visibility** into plan performance and health",
            "📊 **Automated compliance** reporting and monitoring", 
            "💰 **Cost reduction** through operational efficiency",
            "🛡️ **Risk mitigation** through predictive analytics",
            "📈 **Better outcomes** for plan participants"
        ]
        for benefit in benefits:
            st.markdown(benefit)
    
    with stakeholder_tabs[1]:
        st.write("**Advisors**")
        benefits = [
            "⚡ **Faster proposal** generation (hours → minutes)",
            "🎯 **Personalized recommendations** based on comprehensive data",
            "📊 **Enhanced client** presentations with real-time data",
            "🔄 **Automated follow-up** scheduling and reminders",
            "💡 **Predictive insights** for proactive client management"
        ]
        for benefit in benefits:
            st.markdown(benefit)
    
    with stakeholder_tabs[2]:
        st.write("**Plan Participants**")
        benefits = [
            "📱 **Real-time account** information and updates",
            "🎯 **Personalized retirement** planning recommendations",
            "📊 **Clear, visual** performance tracking",
            "🔔 **Proactive notifications** about important changes",
            "💼 **Seamless experience** across all touchpoints"
        ]
        for benefit in benefits:
            st.markdown(benefit)
    
    with stakeholder_tabs[3]:
        st.write("**Operations Teams**")
        benefits = [
            "🤖 **85% automation** of manual processes",
            "🔍 **Proactive issue** detection and resolution",
            "📈 **Improved data quality** and consistency",
            "⚡ **Faster processing** and reduced latency",
            "🛡️ **Enhanced security** and compliance monitoring"
        ]
        for benefit in benefits:
            st.markdown(benefit)
    
    # Competitive advantages
    st.subheader("🏆 Competitive Advantages")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Industry Challenges AHUB 2.0 Solves:**")
        challenges = [
            "❌ Siloed data across multiple systems",
            "❌ Manual, error-prone processes", 
            "❌ Delayed reporting and insights",
            "❌ Compliance and regulatory challenges",
            "❌ Poor data quality and consistency",
            "❌ Reactive vs. proactive management"
        ]
        for challenge in challenges:
            st.write(challenge)
    
    with col2:
        st.write("**Our Solution:**")
        solutions = [
            "✅ Unified data platform - single source of truth",
            "✅ AI-powered automation and optimization",
            "✅ Real-time insights and predictive analytics", 
            "✅ Automated compliance monitoring",
            "✅ Statistical process control for data quality",
            "✅ Predictive intelligence prevents issues"
        ]
        for solution in solutions:
            st.write(solution)
    
    # Future roadmap
    st.subheader("🚀 Future Roadmap")
    
    roadmap_data = pd.DataFrame({
        'Quarter': ['Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026'],
        'Feature': [
            'Advanced AI Workflows',
            'Predictive Participant Behavior',
            'Natural Language Queries', 
            'Full Ecosystem Integration'
        ],
        'Impact': [
            'Further automation of complex processes',
            'Personalized participant engagement',
            'Self-service analytics for all users',
            'Seamless data flow across all products'
        ]
    })
    
    st.dataframe(roadmap_data, use_container_width=True)
    
    # Call to action
    st.markdown("""
    ---
    ### 🎯 Ready to Transform Your Retirement Technology?
    
    **AHUB 2.0 represents the future of retirement data management** - moving from reactive spreadsheets 
    to proactive, AI-powered intelligence that drives better outcomes for everyone in the ecosystem.
    
    **Contact us to learn more about implementing AHUB 2.0 for your organization.**
    """)

if __name__ == "__main__":
    main()
