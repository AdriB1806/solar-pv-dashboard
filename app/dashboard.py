import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Solar PV Energy Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2C3E50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #34495E;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    """Load and prepare the solar PV data"""
    df = pd.read_csv('data/pv_data.csv')
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Parse datetime
    df['DateTime'] = pd.to_datetime(df['Datum'] + ' ' + df['Uhrzeit'])
    
    # Calculate additional metrics
    df['Yield_Energy_kWh'] = df['Energie_Heute (kWh)']
    df['Total_DC_Power_W'] = df['Leistung_DC_1 (W)'] + df['Leistung_DC_2 (W)']
    df['AC_Power_kW'] = df['Leistung_AC (W)'] / 1000
    
    return df

# Calculate energy distribution
def calculate_energy_distribution(df):
    """Calculate energy distribution for self-power status"""
    total_yield = df['Yield_Energy_kWh'].sum()
    
    # Simulate realistic distribution based on typical solar PV systems
    direct_solar_pct = 0.48  # 48% direct use
    battery_pct = 0.35       # 35% to battery
    grid_pct = 0.17          # 17% to grid
    
    return {
        'direct_solar': direct_solar_pct * 100,
        'battery': battery_pct * 100,
        'grid': grid_pct * 100,
        'total_yield': total_yield
    }

# Calculate daily yield data
def calculate_daily_yield(df):
    """Calculate yield, exported, and self-use energy by time of day"""
    # Group by hour
    df['Hour'] = df['DateTime'].dt.hour
    hourly = df.groupby('Hour').agg({
        'Yield_Energy_kWh': 'sum',
        'AC_Power_kW': 'mean'
    }).reset_index()
    
    # Calculate exported and self-use (simulated)
    hourly['Exported_Energy_kWh'] = hourly['Yield_Energy_kWh'] * 0.40
    hourly['SelfUse_Energy_kWh'] = hourly['Yield_Energy_kWh'] * 0.60
    
    # Format time labels
    hourly['Time_Label'] = hourly['Hour'].apply(lambda x: f"{x} {'am' if x < 12 else 'pm'}")
    
    return hourly

# Main dashboard
def main():
    # Header with icon
    st.markdown('<div class="main-header">⚡ Dashboard to monitor solar PV systems energy flow</div>', 
                unsafe_allow_html=True)
    st.markdown("*The purpose of this slide is to highlight dashboard for solar PV systems energy flow monitoring. It includes various elements such as yield daily, self power status, exported energy, direct self use, etc.*")
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    # Calculate metrics
    energy_dist = calculate_energy_distribution(df)
    daily_yield = calculate_daily_yield(df)
    
    # Today's metrics
    total_yield = df['Yield_Energy_kWh'].sum()
    total_exported = total_yield * 0.40
    total_self_use = total_yield * 0.60
    
    # Monthly metrics (simulated as 30x daily)
    monthly_multiplier = 30
    monthly_yield = total_yield * monthly_multiplier
    monthly_exported = total_exported * monthly_multiplier
    monthly_self_use = total_self_use * monthly_multiplier
    
    # Top section: Daily Yield, Status, and Meter
    col1, col2, col3 = st.columns([2, 2, 1.5])
    
    with col1:
        st.markdown('<div class="section-header">Daily yield</div>', unsafe_allow_html=True)
        
        # Create bar chart for daily yield
        fig_yield = go.Figure()
        
        # Sample time points for display
        display_hours = [6, 8, 10, 12, 14, 16, 18]
        display_data = daily_yield[daily_yield['Hour'].isin(display_hours)]
        
        fig_yield.add_trace(go.Bar(
            name='Yield energy',
            x=display_data['Time_Label'],
            y=display_data['Yield_Energy_kWh'],
            marker_color='#2E7D32',
            text=display_data['Yield_Energy_kWh'].round(1),
            textposition='none'
        ))
        
        fig_yield.add_trace(go.Bar(
            name='Exported energy',
            x=display_data['Time_Label'],
            y=display_data['Exported_Energy_kWh'],
            marker_color='#FFA726',
            text=display_data['Exported_Energy_kWh'].round(1),
            textposition='none'
        ))
        
        fig_yield.add_trace(go.Bar(
            name='Selfuse energy',
            x=display_data['Time_Label'],
            y=display_data['SelfUse_Energy_kWh'],
            marker_color='#C8E6C9',
            text=display_data['SelfUse_Energy_kWh'].round(1),
            textposition='none'
        ))
        
        fig_yield.update_layout(
            barmode='group',
            height=250,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(
                orientation="h",
                yanchor="top",
                y=1.15,
                xanchor="left",
                x=0
            ),
            yaxis=dict(title="kWh", range=[0, 6]),
            xaxis=dict(title=""),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        # Display metrics above chart
        met_col1, met_col2, met_col3 = st.columns(3)
        met_col1.metric("Yield energy", f"{total_yield:.1f} kWh", delta=None)
        met_col2.metric("Exported energy", f"{total_exported:.1f} kWh", delta=None)
        met_col3.metric("Selfuse energy", f"{total_self_use:.1f} kWh", delta=None)
        
        st.plotly_chart(fig_yield, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">Status of self power</div>', unsafe_allow_html=True)
        
        # Create donut chart
        labels = ['Direct solar', 'Battery', 'Grid']
        values = [energy_dist['direct_solar'], energy_dist['battery'], energy_dist['grid']]
        colors = ['#2E7D32', '#FFA726', '#E0E0E0']
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker=dict(colors=colors),
            textposition='inside',
            textinfo='percent',
            hovertemplate='%{label}: %{percent}<extra></extra>'
        )])
        
        fig_donut.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="right",
                x=1.3
            ),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)
    
    with col3:
        st.markdown('<div class="section-header">Meter (smartenergy)</div>', unsafe_allow_html=True)
        
        # Gauge chart for current power
        current_power = df['AC_Power_kW'].iloc[-1]
        max_power = 5.0
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_power,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': ""},
            gauge={
                'axis': {'range': [None, max_power], 'tickwidth': 1},
                'bar': {'color': "#FFA726"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, max_power * 0.5], 'color': '#E8F5E9'},
                    {'range': [max_power * 0.5, max_power], 'color': '#C8E6C9'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_power * 0.9
                }
            }
        ))
        
        fig_gauge.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Display energy and cost
        st.markdown(f"""
        <div style='text-align: center; margin-top: -20px;'>
            <p style='margin: 5px 0;'><strong>Energy</strong><br>{total_yield:.2f} kWh</p>
            <p style='margin: 5px 0;'><strong>Cost</strong><br>USD$ {total_yield * 0.12:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Bottom section: Today and This Month
    col_today, col_month = st.columns(2)
    
    with col_today:
        st.markdown('<div class="section-header">Today</div>', unsafe_allow_html=True)
        
        # Create horizontal bar chart for today
        today_data = pd.DataFrame({
            'Metric': ['Energy exported', 'Direct self use', 'Yield energy'],
            'Value': [total_exported, total_self_use, total_yield],
            'Color': ['#2E7D32', '#2E7D32', '#2E7D32']
        })
        
        fig_today = go.Figure()
        
        for idx, row in today_data.iterrows():
            fig_today.add_trace(go.Bar(
                y=[row['Metric']],
                x=[row['Value']],
                orientation='h',
                marker=dict(color=row['Color']),
                text=[f"{row['Value']:.2f}kWh"],
                textposition='outside',
                showlegend=False,
                hovertemplate=f"{row['Metric']}: {row['Value']:.2f}kWh<extra></extra>"
            ))
        
        fig_today.update_layout(
            height=250,
            margin=dict(l=150, r=20, t=20, b=20),
            xaxis=dict(title="", range=[0, total_yield * 1.2]),
            yaxis=dict(title="", autorange="reversed"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            barmode='overlay'
        )
        
        st.plotly_chart(fig_today, use_container_width=True)
    
    with col_month:
        st.markdown('<div class="section-header">This month</div>', unsafe_allow_html=True)
        
        # Create horizontal bar chart for this month
        month_data = pd.DataFrame({
            'Metric': ['Energy exported', 'Direct self use', 'Add test here'],
            'Value': [monthly_exported, monthly_self_use, monthly_yield * 0.85],
            'Color': ['#FFA726', '#FFA726', '#FFA726']
        })
        
        fig_month = go.Figure()
        
        for idx, row in month_data.iterrows():
            fig_month.add_trace(go.Bar(
                y=[row['Metric']],
                x=[row['Value']],
                orientation='h',
                marker=dict(color=row['Color']),
                text=[f"{row['Value']:.2f}kWh"],
                textposition='outside',
                showlegend=False,
                hovertemplate=f"{row['Metric']}: {row['Value']:.2f}kWh<extra></extra>"
            ))
        
        fig_month.update_layout(
            height=250,
            margin=dict(l=150, r=20, t=20, b=20),
            xaxis=dict(title="", range=[0, monthly_yield * 1.2]),
            yaxis=dict(title="", autorange="reversed"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            barmode='overlay'
        )
        
        st.plotly_chart(fig_month, use_container_width=True)
    
    # Footer note
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #7F8C8D; font-size: 0.9rem; padding: 20px;'>
        <p>💡 This graph/chart is linked to excel, and changes automatically based on data. Just left click on it and select "Edit Data"</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
