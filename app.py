import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Set page config
st.set_page_config(
    page_title="India Road Safety Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    national_df = pd.read_csv('cleaned_road_accidents.csv')
    city_df = pd.read_csv('cleaned_road_accident_vehicle.csv')
    weather_df = pd.read_csv('cleaned_weather_type_data.csv')
    urban_rural_df = pd.read_csv('cleaned_urban_rural_data.csv')  
    return national_df, city_df, weather_df, urban_rural_df

national_df, city_df, weather_df, urban_rural_df = load_data()

national_df['years'] = national_df['years'].astype(int)
city_df['state_ut'] = city_df['state_ut'].str.replace(' city', '').str.strip()

# Initialize session state variables
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "National Overview"

if 'year_range' not in st.session_state:
    st.session_state.year_range = (2000, 2019)

if 'selected_city' not in st.session_state:
    st.session_state.selected_city = city_df['state_ut'].unique()[0]

if 'ranking_metric' not in st.session_state:
    st.session_state.ranking_metric = "Total Accidents"

if 'show_top' not in st.session_state:
    st.session_state.show_top = "Top 10"

if 'selected_vehicle' not in st.session_state:
    st.session_state.selected_vehicle = 'Two Wheeler'

if 'weather_condition' not in st.session_state:
    st.session_state.weather_condition = "Sunny/Clear"

if 'selected_state' not in st.session_state:
    st.session_state.selected_state = urban_rural_df['State/UTs'].unique()[0]   

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False



def apply_custom_style():
    # Dynamic theme based on dark mode toggle
    if st.session_state.dark_mode:
        primary_color = "#1e1e1e"
        secondary_color = "#2d2d2d"
        accent_color = "#4CAF50"
        text_color = "#ffffff"
        gradient = "linear-gradient(135deg, #1e1e1e, #2d2d2d)"
    else:
        primary_color = "#2c3e50"
        secondary_color = "#4a6491"
        accent_color = "#3498db"
        text_color = "#ffffff"
        gradient = "linear-gradient(135deg, #2c3e50, #4a6491)"
    
    st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main content styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}

    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        padding: 0 20px;
        background-color: #F0F2F6;
        border-radius: 8px 8px 0px 0px;
        font-weight: bold;
        font-family: 'Inter', sans-serif;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {primary_color};
        color: white;
    }}

    /* Enhanced Sidebar styling */
    [data-testid="stSidebar"] {{
        background: {gradient} !important;
        border-right: 3px solid {accent_color} !important;
    }}
    
    [data-testid="stSidebar"] .sidebar-content {{
        color: {text_color} !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* All sidebar text elements */
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stCheckbox label,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stButton button {{
        color: {text_color} !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* Interactive elements styling */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }}
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"]:hover {{
        background-color: rgba(255,255,255,0.2) !important;
        border-color: {accent_color} !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }}
    
    /* Radio button styling */
    [data-testid="stSidebar"] .stRadio > div {{
        background-color: rgba(255,255,255,0.05) !important;
        border-radius: 10px !important;
        padding: 10px !important;
        margin: 5px 0 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }}
    
    /* Slider styling */
    [data-testid="stSidebar"] .stSlider > div > div > div > div {{
        background-color: {accent_color} !important;
    }}
    
    /* Button styling */
    [data-testid="stSidebar"] .stButton button {{
        background: linear-gradient(45deg, {accent_color}, #27ae60) !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
    }}
    
    [data-testid="stSidebar"] .stButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
    }}
    
    /* Header styling */
    .header {{
        background: {gradient};
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        font-family: 'Inter', sans-serif;
    }}
    
    /* Custom info boxes */
    .info-box {{
        background: rgba(255,255,255,0.1);
        border-left: 4px solid {accent_color};
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
        backdrop-filter: blur(10px);
    }}
    
    /* Stats cards */
    .stat-card {{
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }}
    
    .stat-card:hover {{
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }}
    
    /* Divider styling */
    [data-testid="stSidebar"] hr {{
        border: 1px solid rgba(255,255,255,0.3) !important;
        margin: 1.5rem 0 !important;
    }}
    
    /* Expandable sections */
    .expandable-section {{
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        margin: 10px 0;
        overflow: hidden;
        transition: all 0.3s ease;
    }}
    
    /* Animation keyframes */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.5s ease-in-out;
    }}
    </style>
    """, unsafe_allow_html=True)

# Apply custom styles
apply_custom_style()

# Interactive Header with Animation
st.markdown("""
<div class="header fade-in">
    <h1 style="color:white; text-align:center; margin:0; font-size:2.5rem;">🚗 India Road Safety Dashboard</h1>
    <p style="color:#d1d5db; text-align:center; margin:0; font-size:1.1rem;">
    Analyzing road accident patterns to enhance transportation safety (1970-2019)
    </p>
</div>
""", unsafe_allow_html=True)

# Enhanced Interactive Sidebar
with st.sidebar:
    # Dashboard Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">📊 Dashboard Controls</h2>
        <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">Configure your analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme Toggle
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🌙 Dark" if not st.session_state.dark_mode else "☀️ Light"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset"):
            for key in list(st.session_state.keys()):
                if key not in ['dark_mode']:
                    del st.session_state[key]
            st.rerun()
    
    st.markdown("---")
    
    
    st.markdown("### 🧭 Navigation")
    tab_options = {
        "🏁 National Overview": "National Overview",
        "🏙️ City/State Analysis": "City/State Analysis", 
        "🚗 Vehicle Type Impact": "Vehicle Type Impact",
        "🌦️ Weather Impact": "Weather Impact",
        "🏘️ Urban vs Rural": "Urban vs Rural"
    }
    
    actual_tab = st.radio(
        "Select Analysis View",
        list(tab_options.keys()),
        index=0,
        label_visibility="collapsed"
    )
    
    actual_tab = tab_options[actual_tab]
    
    st.markdown("---")
    st.markdown("### Filters")
    
    
    if actual_tab == "National Overview":
        year_range = st.slider(
            "Select Year Range",
            min_value=1970,
            max_value=2019,
            value=(2000, 2019),
            step=1
        )
    
    elif actual_tab == "City/State Analysis":
        selected_city = st.selectbox(
            "Select City/State",
            city_df['state_ut'].unique(),
            index=0
        )
    
    elif actual_tab == "Vehicle Type Impact":
        selected_vehicle = st.selectbox(
            "Select Vehicle Type",
            ['Two Wheeler', 'Pedestrian', 'Car', 'Bus', 'Truck', 'Auto', 'Bicycle', 'E-Rickshaw', 'Others'],
            index=0
        )
    

if actual_tab == "National Overview":
    tab1, tab2= st.tabs(["📈 Trends", "📊 Metrics"])
    
    with tab1:
        
        filtered_df = national_df[(national_df['years'] >= year_range[0]) & 
                                (national_df['years'] <= year_range[1])]
        
        
        st.subheader(f"Key Performance Indicators ({year_range[0]}-{year_range[1]})")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_accidents = filtered_df['total_number_of_road_accidents_in_numbers'].mean()
            st.metric(
                "Average Accidents",
                f"{avg_accidents:,.0f}",
                help=f"Average annual accidents from {year_range[0]} to {year_range[1]}"
            )
        
        with col2:
            avg_deaths = filtered_df['total_number_of_persons_killed_in_numbers'].mean()
            st.metric(
                "Average Deaths",
                f"{avg_deaths:,.0f}",
                help=f"Average annual fatalities from {year_range[0]} to {year_range[1]}"
            )
        
        with col3:
            avg_injuries = filtered_df['total_number_of_persons_injured_in_numbers'].mean()
            st.metric(
                "Average Injuries",
                f"{avg_injuries:,.0f}",
                help=f"Average annual injuries from {year_range[0]} to {year_range[1]}"
            )
        
        st.markdown("---")
        
        # Area Chart
        st.subheader("Cumulative Trend of Accidents, Deaths and Injuries")
        fig_area = px.area(
            filtered_df,
            x='years',
            y=['total_number_of_persons_killed_in_numbers', 
               'total_number_of_persons_injured_in_numbers',
               'total_number_of_road_accidents_in_numbers'],
            labels={
                'value': 'Count', 
                'variable': 'Metric',
                'years': 'Year'
            },
            color_discrete_map={
                'total_number_of_persons_killed_in_numbers': '#e74c3c',
                'total_number_of_persons_injured_in_numbers': '#f39c12',
                'total_number_of_road_accidents_in_numbers': '#3498db'
            }
        )
        fig_area.update_layout(
            hovermode="x unified",
            legend_title_text='Category'
        )
        st.plotly_chart(fig_area, use_container_width=True)
        
        st.markdown("---")
        
        
        st.subheader(f"Comparison: Deaths vs Injuries vs Accidents ({year_range[0]}-{year_range[1]})")
        
        # Calculate averages for the period
        avg_values = {
            'Deaths': filtered_df['total_number_of_persons_killed_in_numbers'].mean(),
            'Injuries': filtered_df['total_number_of_persons_injured_in_numbers'].mean(),
            'Accidents': filtered_df['total_number_of_road_accidents_in_numbers'].mean()
        }
        
        fig_bar = px.bar(
            x=list(avg_values.keys()),
            y=list(avg_values.values()),
            color=list(avg_values.keys()),
            color_discrete_map={
                'Deaths': '#e74c3c',
                'Injuries': '#f39c12',
                'Accidents': '#3498db'
            },
            labels={'y': 'Average Count', 'x': 'Category'},
            text=[f"{v:,.0f}" for v in avg_values.values()]
        )
        
        fig_bar.update_traces(textposition='outside')
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("---")
        
        
        st.subheader("Detailed Normalized Trends")
        
        normalize_by = st.radio(
            "Normalize Metrics By",
            ["None", "Per Lakh Population", "Per 10k Vehicles", "Per 10k km Roads"],
            index=0,
            horizontal=True
        )
        
        if normalize_by == "Per Lakh Population":
            accident_metric = 'number_of_accidents_per_lakh_population'
            fatality_metric = 'number_of_persons_killed_per_lakh_population'
            injury_metric = 'number_of_persons_injured_per_lakh_population'
            y_title = "Per Lakh Population"
        elif normalize_by == "Per 10k Vehicles":
            accident_metric = 'number_of_accidents_per_ten_thousand_vehicles'
            fatality_metric = 'number_of_persons_killed_per_ten_thousand_vehicles'
            injury_metric = 'number_of_persons_injured_per_ten_thousand_vehicles'
            y_title = "Per 10,000 Vehicles"
        elif normalize_by == "Per 10k km Roads":
            accident_metric = 'number_of_accidents_per_ten_thousand_kms_of_roads'
            fatality_metric = 'number_of_persons_killed_per_ten_thousand_kms_of_roads'
            injury_metric = 'number_of_persons_injured_per_ten_thousand_kms_of_roads'
            y_title = "Per 10,000 km Roads"
        else:
            accident_metric = 'total_number_of_road_accidents_in_numbers'
            fatality_metric = 'total_number_of_persons_killed_in_numbers'
            injury_metric = 'total_number_of_persons_injured_in_numbers'
            y_title = "Total Count"
        
        fig = make_subplots(rows=2, cols=2, 
                          subplot_titles=("Road Accidents", "Fatalities", "Injuries", "Vehicle Growth"),
                          specs=[[{"type": "xy"}, {"type": "xy"}], [{"type": "xy"}, {"type": "xy"}]])
        
        fig.add_trace(
            go.Scatter(x=filtered_df['years'], y=filtered_df[accident_metric], 
                     name="Accidents", line=dict(color='#3498db')),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=filtered_df['years'], y=filtered_df[fatality_metric], 
                     name="Fatalities", line=dict(color='#e74c3c')),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=filtered_df['years'], y=filtered_df[injury_metric], 
                     name="Injuries", line=dict(color='#f39c12')),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=filtered_df['years'], 
                     y=filtered_df['total_number_of_registered_motor_vehicles_in_thousands']*1000,
                     name="Registered Vehicles", line=dict(color='#2ecc71')),
            row=2, col=2
        )
        
        fig.update_layout(
            height=700,
            showlegend=True,
            hovermode="x unified",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_yaxes(title_text=y_title, row=1, col=1)
        fig.update_yaxes(title_text=y_title, row=1, col=2)
        fig.update_yaxes(title_text=y_title, row=2, col=1)
        fig.update_yaxes(title_text="Number of Vehicles", row=2, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
    
 
    
    with tab2:
        st.subheader("Key National Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Total Accidents (2019)",
                value=f"{national_df[national_df['years'] == 2019]['total_number_of_road_accidents_in_numbers'].values[0]:,}",
                delta=f"{national_df['total_number_of_road_accidents_in_numbers'].pct_change().iloc[-1]*100:.1f}% from previous year"
            )
        
        with col2:
            st.metric(
                label="Total Fatalities (2019)",
                value=f"{national_df[national_df['years'] == 2019]['total_number_of_persons_killed_in_numbers'].values[0]:,}",
                delta=f"{national_df['total_number_of_persons_killed_in_numbers'].pct_change().iloc[-1]*100:.1f}% from previous year"
            )
        
        with col3:
            st.metric(
                label="Total Injuries (2019)",
                value=f"{national_df[national_df['years'] == 2019]['total_number_of_persons_injured_in_numbers'].values[0]:,}",
                delta=f"{national_df['total_number_of_persons_injured_in_numbers'].pct_change().iloc[-1]*100:.1f}% from previous year"
            )
        
        st.markdown("---")
        
        # Severity analysis
        st.subheader("Accident Severity Over Time")
        
        national_df['fatality_rate'] = (national_df['total_number_of_persons_killed_in_numbers'] / 
                                      national_df['total_number_of_road_accidents_in_numbers']) * 100
        national_df['injury_rate'] = (national_df['total_number_of_persons_injured_in_numbers'] / 
                                     national_df['total_number_of_road_accidents_in_numbers']) * 100
        
        fig_severity = px.line(national_df, x='years', y=['fatality_rate', 'injury_rate'],
                             labels={'value': 'Percentage', 'variable': 'Metric'},
                             title="Fatality and Injury Rates per Accident",
                             color_discrete_map={'fatality_rate': '#e74c3c', 'injury_rate': '#f39c12'})
        
        st.plotly_chart(fig_severity, use_container_width=True)
    
   
elif actual_tab == "City/State Analysis":
    tab1, tab2 = st.tabs(["🏙️ City Profile", "🏆 City Rankings"])
    
    with tab1:
        st.subheader(f"Road Safety Profile: {selected_city}")
        
        
        city_data = city_df[city_df['state_ut'] == selected_city].iloc[0]
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_accidents = city_data.iloc[1::4].sum()
            st.metric("Total Accidents", f"{total_accidents:,}")
        
        with col2:
            total_fatalities = city_data.iloc[2::4].sum()
            st.metric("Total Fatalities", f"{total_fatalities:,}")
        
        with col3:
            fatality_rate = (total_fatalities / total_accidents) * 100
            st.metric("Fatality Rate", f"{fatality_rate:.1f}%")
        
        st.markdown("---")
        
        # Vehicle type distribution
        st.subheader("Accident Distribution by Vehicle Type")
        
        vehicle_types = [
            'Pedestrian', 'Bicycle', 'Two Wheeler', 'Auto', 
            'Car', 'Truck', 'Bus', 'E-Rickshaw', 'Others'
        ]
        
        accidents = [
            city_data['pedestrian_accidents'],
            city_data['bicycles_accidents'],
            city_data['two_wheelers_accidents'],
            city_data['auto_accidents'],
            city_data['cars_accidents'],
            city_data['trucks_accidents'],
            city_data['buses_accidents'],
            city_data['e_rickshaw_accidents'],
            city_data['others_accidents']
        ]
        
        fatalities = [
            city_data['pedestrian_killed'],
            city_data['bicycles_killed'],
            city_data['two_wheelers_killed'],
            city_data['auto_killed'],
            city_data['cars_killed'],
            city_data['trucks_killed'],
            city_data['buses_killed'],
            city_data['e_rickshaw_killed'],
            city_data['others_killed']
        ]
        
        
        city_df_vis = pd.DataFrame({
            'Vehicle Type': vehicle_types,
            'Accidents': accidents,
            'Fatalities': fatalities,
            'Fatality Rate': [(f/a)*100 if a > 0 else 0 for f, a in zip(fatalities, accidents)]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_accidents = px.pie(city_df_vis, names='Vehicle Type', values='Accidents',
                                 title="Accidents by Vehicle Type",
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_accidents, use_container_width=True)
        
        with col2:
            fig_fatalities = px.pie(city_df_vis, names='Vehicle Type', values='Fatalities',
                                  title="Fatalities by Vehicle Type",
                                  color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_fatalities, width="stretch")
        
        st.markdown("---")
        
        # Fatality rates by vehicle type
        st.subheader("Fatality Rates by Vehicle Type")
        
        fig_fatality_rate = px.bar(city_df_vis.sort_values('Fatality Rate', ascending=False), 
                                 x='Vehicle Type', y='Fatality Rate',
                                 color='Fatality Rate',
                                 color_continuous_scale='reds',
                                 title="Fatality Rate (%) by Vehicle Type")
        
        st.plotly_chart(fig_fatality_rate, use_container_width=True)
    
    
    
    with tab2:
        st.subheader("Ranking Options")
        ranking_metric = st.selectbox(
            "Rank Cities By",
            ["Total Accidents", "Total Fatalities", "Fatality Rate", "Pedestrian Accidents", 
            "Two Wheeler Accidents", "Car Accidents", "Bus Accidents"],
            index=0
        )
        
        
        show_top = st.radio(
            "Show",
            ["Top 10", "Bottom 10"],
            index=0
        )
        
        
        # Calculate city-level metrics 
        city_metrics = city_df.copy()
        city_metrics['Total Accidents'] = city_metrics.iloc[:, 1::4].sum(axis=1)
        city_metrics['Total Fatalities'] = city_metrics.iloc[:, 2::4].sum(axis=1)
        city_metrics['Fatality Rate'] = (city_metrics['Total Fatalities'] / city_metrics['Total Accidents']) * 100
            
        # Map selection to column
        if ranking_metric == "Total Accidents":
            sort_col = 'Total Accidents'
        elif ranking_metric == "Total Fatalities":
            sort_col = 'Total Fatalities'
        elif ranking_metric == "Fatality Rate":
            sort_col = 'Fatality Rate'
        elif ranking_metric == "Pedestrian Accidents":
            sort_col = 'pedestrian_accidents'
        elif ranking_metric == "Two Wheeler Accidents":
            sort_col = 'two_wheelers_accidents'
        elif ranking_metric == "Car Accidents":
            sort_col = 'cars_accidents'
        elif ranking_metric == "Bus Accidents":
            sort_col = 'buses_accidents'
            
        # Sort based on selection
        ascending_order = False if show_top == "Top 10" else True
        sorted_cities = city_metrics.sort_values(sort_col, ascending=ascending_order)
            
        # Get top or bottom 10 cities
        ranked_cities = sorted_cities.head(10)
            
        # Create bar chart visualization 
        fig = px.bar(
            ranked_cities,
            x='state_ut', 
            y=sort_col,    
            color=sort_col,
            color_continuous_scale='reds' if show_top == "Top 10" else 'greens',
            title=f"{show_top} Cities by {ranking_metric}",
            labels={sort_col: ranking_metric, 'state_ut': 'City/State'}
        )
            
        # Adjust layout for vertical bars
        fig.update_layout(
            xaxis={'categoryorder': 'total descending'},  
            height=500
        )
        
        # Rotate x-axis labels for better readability
        fig.update_xaxes(tickangle=45)
        
        st.plotly_chart(fig, use_container_width=True)
        
        
        st.markdown("---")
            
            
        st.subheader("Regional Comparisons")
            
        
        tab_a, tab_b = st.tabs(["📊 Top 10 States", "📊 Safest States"])
        
       
        
        with tab_a:
            st.subheader("Top 10 States by Key Metrics")
            
            # Calculate top 10 states for each metric
            top_accidents = city_metrics.sort_values('Total Accidents', ascending=False).head(10)
            top_fatalities = city_metrics.sort_values('Total Fatalities', ascending=False).head(10)
            top_fatality_rate = city_metrics[city_metrics['Total Accidents'] > 100].sort_values('Fatality Rate', ascending=False).head(10)
            
            # 1. Accidents chart 
            fig1 = px.bar(
                top_accidents,
                x='state_ut',
                y='Total Accidents',
                title='Top 10 States by Total Accidents',
                color='Total Accidents',
                color_continuous_scale=[(0, "#1565C0"), (0.5, "#0D47A1"), (1, "#002171")],
                labels={'state_ut': 'State/UT', 'Total Accidents': 'Number of Accidents'}
            )
            fig1.update_layout(
                height=500,
                xaxis={'categoryorder':'total descending', 'tickangle': 45},
                yaxis_title="Number of Accidents",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig1.update_traces(
                marker_line_color='#003366',
                marker_line_width=1.5,
                opacity=0.9
            )
            st.plotly_chart(fig1, use_container_width=True)
            
           
            st.write("")
            
            # 2. Fatalities chart 
            fig2 = px.bar(
                top_fatalities,
                x='state_ut',
                y='Total Fatalities',
                title='Top 10 States by Total Fatalities',
                color='Total Fatalities',
                color_continuous_scale=[(0, "#C62828"), (0.5, "#B71C1C"), (1, "#7F0000")],  
                labels={'state_ut': 'State/UT', 'Total Fatalities': 'Number of Fatalities'}
            )
            fig2.update_layout(
                height=500,
                xaxis={'categoryorder':'total descending', 'tickangle': 45},
                yaxis_title="Number of Fatalities",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig2.update_traces(
                marker_line_color='#800000',
                marker_line_width=1.5,
                opacity=0.9
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            
            st.write("")
            
            # 3. Fatality Rate chart 
            fig3 = px.bar(
                top_fatality_rate,
                x='state_ut',
                y='Fatality Rate',
                title='Top 10 States by Fatality Rate (min 100 accidents)',
                color='Fatality Rate',
                color_continuous_scale=[(0, "#EF6C00"), (0.5, "#E65100"), (1, "#BF360C")],  
                labels={'state_ut': 'State/UT', 'Fatality Rate': 'Fatality Rate (%)'}
            )
            fig3.update_layout(
                height=500,
                xaxis={'categoryorder':'total descending', 'tickangle': 45},
                yaxis_title="Fatality Rate (%)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig3.update_traces(
                marker_line_color='#993300',
                marker_line_width=1.5,
                opacity=0.9
            )
            st.plotly_chart(fig3, use_container_width=True)
                
        with tab_b:
            st.subheader("10 Safest States (Least Accidents)")
            
            # Get safest states 
            safest_states = city_metrics.sort_values('Total Accidents').head(10)
            
            # Create horizontal bar chart
            fig = px.bar(
                safest_states,
                x='Total Accidents',
                y='state_ut',
                orientation='h',
                color='Total Accidents',
                color_continuous_scale='greens',
                title="States with Fewest Accidents",
                labels={'Total Accidents': 'Number of Accidents', 'state_ut': 'State'}
            )
            
            # Adjust layout
            fig.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Safest State",
                    safest_states.iloc[0]['state_ut'],
                    f"{safest_states.iloc[0]['Total Accidents']} accidents"
                )
            
            with col2:
                avg_fatality_rate = safest_states['Fatality Rate'].mean()
                st.metric(
                    "Average Fatality Rate",
                    f"{avg_fatality_rate:.1f}%",
                    "Among safest 10 states"
                )
elif actual_tab == "Vehicle Type Impact":
    tab1, tab2 = st.tabs(["🚦 Vehicle Analysis", "📊 Comparative Impact"])
    
    with tab1:
        st.subheader(f"{selected_vehicle} Accident Analysis")
        
        # Map selection to column names
        vehicle_map = {
            'Pedestrian': ('pedestrian_accidents', 'pedestrian_killed', 'pedestrian_grievous_inj', 'pedestrian_minor_inj'),
            'Bicycle': ('bicycles_accidents', 'bicycles_killed', 'bicycles_grievous_inj', 'bicycles_minor_inj'),
            'Two Wheeler': ('two_wheelers_accidents', 'two_wheelers_killed', 'two_wheelers_grievous_inj', 'two_wheelers_minor_inj'),
            'Auto': ('auto_accidents', 'auto_killed', 'auto_grievous_inj', 'auto_minor_inj'),
            'Car': ('cars_accidents', 'cars_killed', 'cars_grievous_inj', 'cars_minor_inj'),
            'Truck': ('trucks_accidents', 'trucks_killed', 'trucks_grievous_inj', 'trucks_minor_inj'),
            'Bus': ('buses_accidents', 'buses_killed', 'buses_grievous_inj', 'buses_minor_inj'),
            'E-Rickshaw': ('e_rickshaw_accidents', 'e_rickshaw_killed', 'e_rickshaw_grievous_inj', 'e_rickshaw_minor_inj'),
            'Others': ('others_accidents', 'others_killed', 'others_grievous_inj', 'others_minor_inj')
        }
        
        col_accident, col_fatality, col_grievous, col_minor = vehicle_map[selected_vehicle]
        
        # Get top 15 cities for selected vehicle type
        top_cities = city_df.sort_values(col_accident, ascending=False).head(15)
        
        # Accident Bar Chart with custom colors
        fig1 = px.bar(
            top_cities, 
            x='state_ut', 
            y=col_accident,
            title=f"Top Cities by {selected_vehicle} Accidents",
            color=col_accident,
            color_continuous_scale=[
                [0, "#C6E6F5"],
                [0.5, '#4FC3F7'],
                [1, '#01579B']
            ]
        )
        fig1.update_traces(
            marker_line_color='#0288D1',
            marker_line_width=1.5,
            opacity=0.9
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig1, use_container_width=True)
        
            
        fig2 = px.bar(
            top_cities,
            x='state_ut',
            y=col_fatality,
            title=f"Top Cities by {selected_vehicle} Fatalities",
            color=col_fatality,
            color_continuous_scale=[
                [0, "#F9C3CB"],
                [0.5, '#E57373'],
                [1, '#B71C1C']
            ]
        )
        fig2.update_traces(
            marker_line_color='#C62828',
            marker_line_width=1.5,
            opacity=0.9
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        #Severity Analysis
        st.subheader(f"{selected_vehicle} Severity Analysis")
        
        # Calculate injury breakdown for selected city
        severity_data = {
            'Category': ['Fatalities', 'Grievous Injuries', 'Minor Injuries'],
            'Count': [
                city_df[col_fatality].sum(),
                city_df[col_grievous].sum(),
                city_df[col_minor].sum()
            ]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for severity distribution
            fig_severity = px.pie(
                pd.DataFrame(severity_data),
                names='Category',
                values='Count',
                title=f"{selected_vehicle} Accident Severity Distribution",
                color='Category',
                color_discrete_map={
                    'Fatalities': '#e74c3c',
                    'Grievous Injuries': '#f39c12',
                    'Minor Injuries': '#3498db'
                }
            )
            st.plotly_chart(fig_severity, use_container_width=True)
        
        with col2:
            # Bar chart for severity comparison
            fig_severity_bar = px.bar(
                pd.DataFrame(severity_data),
                x='Category',
                y='Count',
                title=f"{selected_vehicle} Severity Breakdown",
                color='Category',
                color_discrete_map={
                    'Fatalities': '#e74c3c',
                    'Grievous Injuries': '#f39c12',
                    'Minor Injuries': '#3498db'
                }
            )
            st.plotly_chart(fig_severity_bar, use_container_width=True)
        
        st.markdown("---")
     
        # Calculate national totals
        total_accidents = city_df[col_accident].sum()
        total_fatalities = city_df[col_fatality].sum()
        total_grievous = city_df[col_grievous].sum()
        total_minor = city_df[col_minor].sum()
        fatality_rate = (total_fatalities / total_accidents) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label=f"Total {selected_vehicle} Accidents",
                value=f"{total_accidents:,}"
            )
        
        with col2:
            st.metric(
                label=f"Total {selected_vehicle} Fatalities",
                value=f"{total_fatalities:,}"
            )
        
        with col3:
            st.metric(
                label=f"Total Grievous Injuries",
                value=f"{total_grievous:,}"
            )
        
        with col4:
            st.metric(
                label=f"Total Minor Injuries",
                value=f"{total_minor:,}"
            )
    
    with tab2:
        st.subheader("Comparative Vehicle Impact Analysis")
        
        # Prepare data for all vehicle types
        vehicle_types = [
            'Pedestrian', 'Bicycle', 'Two Wheeler', 'Auto', 
            'Car', 'Truck', 'Bus', 'E-Rickshaw', 'Others'
        ]
        
        accidents = [
            city_df['pedestrian_accidents'].sum(),
            city_df['bicycles_accidents'].sum(),
            city_df['two_wheelers_accidents'].sum(),
            city_df['auto_accidents'].sum(),
            city_df['cars_accidents'].sum(),
            city_df['trucks_accidents'].sum(),
            city_df['buses_accidents'].sum(),
            city_df['e_rickshaw_accidents'].sum(),
            city_df['others_accidents'].sum()
        ]
        
        fatalities = [
            city_df['pedestrian_killed'].sum(),
            city_df['bicycles_killed'].sum(),
            city_df['two_wheelers_killed'].sum(),
            city_df['auto_killed'].sum(),
            city_df['cars_killed'].sum(),
            city_df['trucks_killed'].sum(),
            city_df['buses_killed'].sum(),
            city_df['e_rickshaw_killed'].sum(),
            city_df['others_killed'].sum()
        ]
        
        injuries = [
            city_df['pedestrian_grievous_inj'].sum() + city_df['pedestrian_minor_inj'].sum(),
            city_df['bicycles_grievous_inj'].sum() + city_df['bicycles_minor_inj'].sum(),
            city_df['two_wheelers_grievous_inj'].sum() + city_df['two_wheelers_minor_inj'].sum(),
            city_df['auto_grievous_inj'].sum() + city_df['auto_minor_inj'].sum(),
            city_df['cars_grievous_inj'].sum() + city_df['cars_minor_inj'].sum(),
            city_df['trucks_grievous_inj'].sum() + city_df['trucks_minor_inj'].sum(),
            city_df['buses_grievous_inj'].sum() + city_df['buses_minor_inj'].sum(),
            city_df['e_rickshaw_grievous_inj'].sum() + city_df['e_rickshaw_minor_inj'].sum(),
            city_df['others_grievous_inj'].sum() + city_df['others_minor_inj'].sum()
        ]
        
        fatality_rates = [(f/a)*100 if a > 0 else 0 for f, a in zip(fatalities, accidents)]
        
    
        comparison_df = pd.DataFrame({
            'Vehicle Type': vehicle_types,
            'Accidents': accidents,
            'Fatalities': fatalities,
            'Injuries': injuries,
            'Fatality Rate': fatality_rates
        })
        
        # Grouped Bar Chart
        st.subheader("Accidents, Fatalities & Injuries by Vehicle Type")
        fig_grouped = px.bar(
            comparison_df,
            x='Vehicle Type',
            y=['Accidents', 'Fatalities', 'Injuries'],
            barmode='group',
            title="Comparative Impact by Vehicle Type",
            labels={'value': 'Count', 'variable': 'Metric'},
            color_discrete_map={
                'Accidents': '#3498db',
                'Fatalities': '#e74c3c',
                'Injuries': '#f39c12'
            }
        )
        st.plotly_chart(fig_grouped, use_container_width=True)
        
        # Pie Chart for Death Share
        st.subheader("Share of Deaths by Vehicle Type")
        fig_pie = px.pie(
            comparison_df,
            names='Vehicle Type',
            values='Fatalities',
            title="Proportion of Total Fatalities by Vehicle Type",
            color='Vehicle Type',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        #Existing Fatality Rate Comparison
        st.subheader("Fatality Rate Comparison Across Vehicle Types")
        fig_fatality = px.bar(
            comparison_df.sort_values('Fatality Rate', ascending=False), 
            x='Vehicle Type', 
            y='Fatality Rate',
            color='Fatality Rate',
            color_continuous_scale='reds',
            title="Fatality Rate (%) by Vehicle Type"
        )
        st.plotly_chart(fig_fatality, use_container_width=True)
        
        #Histogram of Deaths/Injuries
        st.subheader("Distribution of Fatalities Across Vehicle Types")
        fig_hist = px.histogram(
            comparison_df,
            x='Vehicle Type',
            y='Fatalities',
            histfunc='sum',
            title="Fatalities Distribution by Vehicle Type",
            color='Vehicle Type'
        )
        st.plotly_chart(fig_hist, use_container_width=True)

elif actual_tab == "Weather Impact":
    st.subheader("Weather Conditions and Accident Analysis")
    
    # Clean up the weather data
    weather_df = weather_df[weather_df['States/UTs'] != 'Total']  # Remove total row
    
    tab1, tab2 = st.tabs(["🌦️ Weather Conditions", "📊 Comparative Analysis"])
    
    with tab1:
        st.subheader("Accidents by Weather Condition")
        
        # Calculate totals for each weather condition
        weather_totals = {
            'Sunny/Clear': weather_df['Sunny/Clear - Total Accidents - Number'].sum(),
            'Rainy': weather_df['Rainy - Total Accidents'].sum(),
            'Foggy/Misty': weather_df['Foggy and Misty - Total Accidents'].sum(),
            'Hail/Sleet': weather_df['Hail/Sleet - Total Accidents'].sum(),
            'Others': weather_df['Others - Total Accidents'].sum()
        }
        
        # Create pie chart
        fig_pie = px.pie(
            names=list(weather_totals.keys()),
            values=list(weather_totals.values()),
            title="Distribution of Accidents by Weather Condition",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        # Top cities for each weather condition
        weather_condition = st.selectbox(
            "Select Weather Condition to Analyze",
            ["Sunny/Clear", "Rainy", "Foggy/Misty", "Hail/Sleet", "Others"],
            index=0
        )
        
        if weather_condition == "Sunny/Clear":
            col = 'Sunny/Clear - Total Accidents - Number'
            title = "Cities with Most Accidents in Sunny/Clear Conditions"
        elif weather_condition == "Rainy":
            col = 'Rainy - Total Accidents'
            title = "Cities with Most Accidents in Rainy Conditions"
        elif weather_condition == "Foggy/Misty":
            col = 'Foggy and Misty - Total Accidents'
            title = "Cities with Most Accidents in Foggy/Misty Conditions"
        elif weather_condition == "Hail/Sleet":
            col = 'Hail/Sleet - Total Accidents'
            title = "Cities with Most Accidents in Hail/Sleet Conditions"
        else:
            col = 'Others - Total Accidents'
            title = "Cities with Most Accidents in Other Weather Conditions"
        
        top_cities = weather_df.sort_values(col, ascending=False).head(10)
        
        fig_bar = px.bar(
            top_cities,
            x='States/UTs',
            y=col,
            title=title,
            color=col,
            color_continuous_scale='blues'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        st.subheader("Comparative Analysis by Weather Condition")
        
        # Prepare data for comparison
        weather_comparison = pd.DataFrame({
            'Weather Condition': ['Sunny/Clear', 'Rainy', 'Foggy/Misty', 'Hail/Sleet', 'Others'],
            'Total Accidents': [
                weather_df['Sunny/Clear - Total Accidents - Number'].sum(),
                weather_df['Rainy - Total Accidents'].sum(),
                weather_df['Foggy and Misty - Total Accidents'].sum(),
                weather_df['Hail/Sleet - Total Accidents'].sum(),
                weather_df['Others - Total Accidents'].sum()
            ],
            'Total Fatalities': [
                weather_df['Sunny/Clear - Persons Killed - Number'].sum(),
                weather_df['Rainy - Persons Killed'].sum(),
                weather_df['Foggy and Misty - Persons Killed'].sum(),
                weather_df['Hail/Sleet - Persons Killed'].sum(),
                weather_df['Others - Persons Killed'].sum()
            ],
            'Total Injuries': [
                weather_df['Sunny/Clear - Persons Injured - Total Injured '].sum(),  
                weather_df['Rainy - Persons Injured - Total Injured '].sum(),      
                weather_df['Foggy and Misty - Persons Injured - Total Injured '].sum(), 
                weather_df['Hail/Sleet - Persons Injured - Total Injured '].sum(),    
                weather_df['Others - Persons Injured - Total Injured '].sum()     
            ]
        })
        
        # Calculate fatality rates
        weather_comparison['Fatality Rate'] = (weather_comparison['Total Fatalities'] / weather_comparison['Total Accidents']) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Accidents by Weather Condition")
            fig_acc = px.bar(
                weather_comparison,
                x='Weather Condition',
                y='Total Accidents',
                color='Weather Condition',
                title="Total Accidents by Weather Condition"
            )
            st.plotly_chart(fig_acc, use_container_width=True)
            
        with col2:
            st.subheader("Fatalities by Weather Condition")
            fig_fat = px.bar(
                weather_comparison,
                x='Weather Condition',
                y='Total Fatalities',
                color='Weather Condition',
                title="Total Fatalities by Weather Condition"
            )
            st.plotly_chart(fig_fat, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("Fatality Rate by Weather Condition")
        fig_rate = px.bar(
            weather_comparison.sort_values('Fatality Rate', ascending=False),
            x='Weather Condition',
            y='Fatality Rate',
            color='Fatality Rate',
            color_continuous_scale='reds',
            title="Fatality Rate (%) by Weather Condition"
        )
        st.plotly_chart(fig_rate, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("Injury Severity by Weather Condition")
        
        # Prepare injury severity data
        injury_data = pd.DataFrame({
            'Weather Condition': ['Sunny/Clear', 'Rainy', 'Foggy/Misty', 'Hail/Sleet', 'Others'],
            'Grievous Injuries': [
                weather_df['Sunny/Clear - Persons Injured - Greviously Injured'].sum(),
                weather_df['Rainy - Persons Injured - Greviously Injured'].sum(),
                weather_df['Foggy and Misty - Persons Injured - Greviously Injured'].sum(),
                weather_df['Hail/Sleet - Persons Injured - Greviously Injured'].sum(),
                weather_df['Others - Persons Injured - Greviously Injured'].sum()
            ],
            'Minor Injuries': [
                weather_df['Sunny/Clear - Persons Injured - Minor Injury'].sum(),
                weather_df['Rainy - Persons Injured - Minor Injury'].sum(),
                weather_df['Foggy and Misty - Persons Injured - Minor Injury'].sum(),
                weather_df['Hail/Sleet - Persons Injured - Minor Injury'].sum(),
                weather_df['Others - Persons Injured - Minor Injury'].sum()
            ]
        })
        
        fig_inj = px.bar(
            injury_data,
            x='Weather Condition',
            y=['Grievous Injuries', 'Minor Injuries'],
            barmode='group',
            title="Injury Severity by Weather Condition",
            labels={'value': 'Number of Injuries', 'variable': 'Injury Type'},
            color_discrete_map={
                'Grievous Injuries': '#e74c3c',
                'Minor Injuries': '#f39c12'
            }
        )
        st.plotly_chart(fig_inj, use_container_width=True)

elif actual_tab == "Urban vs Rural":
    st.subheader("Urban vs Rural Accident Analysis")
    

    urban_rural_df = urban_rural_df[urban_rural_df['State/UTs'] != '0']
    urban_rural_df = urban_rural_df[urban_rural_df['Total'] > 0]
    
    
    urban_rural_df.columns = urban_rural_df.columns.str.strip().str.lower()
    
    tab1, tab2 = st.tabs(["📊 State-wise Analysis", "🌆 Comparative Analysis"])
    
    with tab1:
        st.subheader("State-wise Urban vs Rural Accident Distribution")
        
        
        sorted_df = urban_rural_df.sort_values('total', ascending=False)
        
    
        selected_state = st.selectbox(
            "Select State/UT",
            sorted_df['state/uts'].unique(),
            index=0
        )
        
        
        state_data = urban_rural_df[urban_rural_df['state/uts'] == selected_state].iloc[0]
        
        # Create metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Accidents", f"{state_data['total']:,}")
        with col2:
            st.metric("Urban Accidents", f"{state_data['urban']:,}", 
                     f"{state_data['urban']/state_data['total']*100:.1f}%")
        with col3:
            st.metric("Rural Accidents", f"{state_data['rural']:,}", 
                     f"{state_data['rural']/state_data['total']*100:.1f}%")
        
        # Create pie chart
        fig_pie = px.pie(
            names=['Urban', 'Rural'],
            values=[state_data['urban'], state_data['rural']],
            title=f"Urban vs Rural Accidents in {selected_state}",
            color_discrete_sequence=['#3498db', '#2ecc71']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        # Top states by urban and rural accidents
        st.subheader("Top States by Accident Type")
        
        top_urban = urban_rural_df.sort_values('urban', ascending=False).head(10)
        fig_urban = px.bar(
                top_urban,
                x='state/uts',
                y='urban',
                title="Top 10 States by Urban Accidents",
                color='urban',
                color_continuous_scale='blues'
            )
        st.plotly_chart(fig_urban, use_container_width=True)
        
        
        top_rural = urban_rural_df.sort_values('rural', ascending=False).head(10)
        fig_rural = px.bar(
                top_rural,
                x='state/uts',
                y='rural',
                title="Top 10 States by Rural Accidents",
                color='rural',
                color_continuous_scale='greens'
            )
        st.plotly_chart(fig_rural, use_container_width=True)
    
    with tab2:
        st.subheader("Comparative Analysis: Urban vs Rural")
        
        # Calculate national totals
        total_urban = urban_rural_df['urban'].sum()
        total_rural = urban_rural_df['rural'].sum()
        total_all = urban_rural_df['total'].sum()
        
        # National metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Accidents", f"{total_all:,}")
        with col2:
            st.metric("Urban Accidents", f"{total_urban:,}", 
                     f"{total_urban/total_all*100:.1f}% of total")
        with col3:
            st.metric("Rural Accidents", f"{total_rural:,}", 
                     f"{total_rural/total_all*100:.1f}% of total")
        
        # National pie chart
        fig_national_pie = px.pie(
            names=['Urban', 'Rural'],
            values=[total_urban, total_rural],
            title="National Urban vs Rural Accident Distribution",
            color_discrete_sequence=['#3498db', '#2ecc71']
        )
        st.plotly_chart(fig_national_pie, use_container_width=True)
        
        st.markdown("---")
        
        # Urban-Rural ratio analysis
        urban_rural_df['urban_ratio'] = urban_rural_df['urban'] / urban_rural_df['total']
        urban_rural_df['rural_ratio'] = urban_rural_df['rural'] / urban_rural_df['total']
        
        st.subheader("States with Highest Urban/Rural Accident Ratios")
        
        top_urban_ratio = urban_rural_df.sort_values('urban_ratio', ascending=False).head(10)
        fig_urban_ratio = px.bar(
                top_urban_ratio,
                x='state/uts',
                y='urban_ratio',
                title="Top 10 States by Urban Accident Ratio",
                labels={'urban_ratio': 'Urban Accident Ratio'},
                color='urban_ratio',
                color_continuous_scale='blues'
            )
        fig_urban_ratio.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig_urban_ratio, use_container_width=True)
        
        
        top_rural_ratio = urban_rural_df.sort_values('rural_ratio', ascending=False).head(10)
        fig_rural_ratio = px.bar(
                top_rural_ratio,
                x='state/uts',
                y='rural_ratio',
                title="Top 10 States by Rural Accident Ratio",
                labels={'rural_ratio': 'Rural Accident Ratio'},
                color='rural_ratio',
                color_continuous_scale='greens'
            )
        fig_rural_ratio.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig_rural_ratio, use_container_width=True)
        
        