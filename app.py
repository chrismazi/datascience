import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Vehicle Theft Analytics Dashboard",
    layout="wide"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    :root {
        --bg: #f7f9fb;
        --card: #ffffff;
        --muted: #6b7280;
        --accent: #1f77b4;
    }

    body, .css-1d391kg, .stApp {
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }

    .main {background-color: inherit}
    .stApp header {background-color: transparent}
    div[data-testid="stMetricValue"] {font-size: 20px}
    .streamlit-expanderHeader {background-color: #f0f2f6}
    div.css-12w0qpk.e1tzin5v1 {background-color: var(--card); padding: 20px; border-radius: 10px; box-shadow: 0 6px 18px rgba(16,24,40,0.06)}

    .title {
        font-size: 2.25rem;
        font-weight: 700;
        margin-bottom: 0.6rem;
    }

    h1, .stMarkdown h1 {font-family: 'Inter', sans-serif}

    .css-1d391kg .sidebar .stButton>button {border-radius: 8px}
    .filter-section {background-color: rgba(255,255,255,0.6); padding: 0.8rem; border-radius: 8px; margin-bottom: 0.8rem}

    </style>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state['data'] = None

COLOR_SCHEMES = {
    'primary': ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3'],
    'sequential': {
        'blues': 'Blues',
        'reds': 'Reds',
        'purples': 'Purples',
        'viridis': 'Viridis',
        'magma': 'Magma'
    }
}

COLOR_SCHEME = {
    'primary': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
    'background': 'rgba(0,0,0,0)',
    'text': 'auto'
}

import plotly.io as pio
pio.templates.default = "plotly_white"

def create_themed_chart(fig):
    fig.update_layout(
        plot_bgcolor=COLOR_SCHEME['background'],
        paper_bgcolor=COLOR_SCHEME['background'],
        margin=dict(t=30, l=10, r=10, b=10)
    )
    return fig

st.set_page_config(page_title="Vehicle Theft Analysis", layout="wide")

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .sidebar-content {
        padding: 1rem;
    }
    .filter-section {
        background-color: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_filters():
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'date_range': None,
            'makes': [],
            'types': [],
            'colors': [],
            'regions': [],
            'make_types': []
        }

def apply_filters(df):
    filtered_df = df.copy()
    if st.session_state.filters['date_range'] and len(st.session_state.filters['date_range']) == 2:
        start_date, end_date = st.session_state.filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['date_stolen'].dt.date >= start_date) & 
            (filtered_df['date_stolen'].dt.date <= end_date)
        ]
    if st.session_state.filters['makes']:
        filtered_df = filtered_df[filtered_df['make_name'].isin(st.session_state.filters['makes'])]
    
    if st.session_state.filters['types']:
        filtered_df = filtered_df[filtered_df['vehicle_type'].isin(st.session_state.filters['types'])]
        
    if st.session_state.filters['colors']:
        filtered_df = filtered_df[filtered_df['color'].isin(st.session_state.filters['colors'])]
        
    if st.session_state.filters['regions']:
        filtered_df = filtered_df[filtered_df['region'].isin(st.session_state.filters['regions'])]
        
    if st.session_state.filters['make_types']:
        filtered_df = filtered_df[filtered_df['make_type'].isin(st.session_state.filters['make_types'])]
    
    return filtered_df

def clean_categorical(df, columns):
    df_clean = df.copy()
    for col in columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('Unknown').astype(str)
    return df_clean

@st.cache_data
def load_data():
    df = pd.read_csv('stolen_vehicles_enhanced.csv')
    df['date_stolen'] = pd.to_datetime(df['date_stolen'])
    categorical_cols = ['make_name', 'vehicle_type', 'color', 'region', 'make_type']
    df = clean_categorical(df, categorical_cols)
    return df

try:
    df_f = load_data()
except FileNotFoundError:
    st.error("Please ensure 'stolen_vehicles_enhanced.csv' is in the same directory as this script.")
    st.stop()

initialize_filters()

df_original = load_data()

with st.sidebar:
    st.title(" Filters")
    with st.expander(" Vehicle Filters", expanded=True):
        st.session_state.filters['makes'] = st.multiselect(
            "Make",
            options=sorted(df_original['make_name'].unique().tolist()),
            default=st.session_state.filters['makes'],
            key="makes_filter",
            help="Select vehicle manufacturers to filter"
        )
        
        st.session_state.filters['types'] = st.multiselect(
            "Vehicle Type",
            options=sorted(df_original['vehicle_type'].unique()),
            default=st.session_state.filters['types'],
            key="types_filter"
        )
        
        st.session_state.filters['colors'] = st.multiselect(
            "Color",
            options=sorted(df_original['color'].unique()),
            default=st.session_state.filters['colors'],
            key="colors_filter"
        )
    with st.expander(" Location", expanded=True):
        st.session_state.filters['regions'] = st.multiselect(
            "Region",
            options=sorted(df_original['region'].unique()),
            default=st.session_state.filters['regions'],
            key="regions_filter"
        )
    if st.button("Reset All Filters", type="primary"):
        for key in st.session_state.filters.keys():
            st.session_state.filters[key] = [] if isinstance(st.session_state.filters[key], list) else None
        widget_keys = ["makes_filter", "types_filter", "colors_filter", "regions_filter"]
        for widget_key in widget_keys:
            if widget_key in st.session_state:
                del st.session_state[widget_key]
        st.rerun()

df_filtered = apply_filters(df_original)

with st.sidebar:
    st.markdown("---")
    st.markdown("###  Filter Summary")
    st.markdown(f"**Total Records:** {len(df_filtered):,}")
    st.markdown(f"**Filter Reduction:** {((1 - len(df_filtered)/len(df_original)) * 100):.1f}%")

col1, col2, col3 = st.columns([1.5, 1, 1.5])
with col2:
    try:
        st.image("logo.webp", width=250)
    except:
        st.markdown("<h2 style='text-align: center;'>CENFRI</h2>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 1rem 0; border-bottom: 2px solid #1f77b4; margin-bottom: 2rem;'>
        <h1 style='margin: 0.5rem 0; font-size: 2.5rem; font-weight: 700;'> Motor Vehicle Theft Analysis Dashboard</h1>
        <p style='margin: 0.5rem 0; font-size: 1.1rem; opacity: 0.8;'>Data Science Assessment - November 2025</p>
        <p style='margin: 0; font-size: 1rem; font-weight: 500;'>Prepared by: <span style='color: #1f77b4;'>Prince Chris Mazimpaka</span></p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.title(' Dashboard Controls')

st.sidebar.markdown("###  Key Metrics")
total_thefts = len(df_filtered)
unique_makes = df_filtered['make_name'].nunique()
st.sidebar.metric("Total Incidents", f"{total_thefts:,}")
st.sidebar.metric("Unique Makes", f"{unique_makes:,}")

st.markdown("### Analysis of Vehicle Theft")

col1, col2, col3, col4 = st.columns(4)
with col1:
    total_luxury = len(df_filtered[df_filtered['make_type'] == 'Luxury'])
    st.metric("Luxury Vehicles", f"{total_luxury:,}")
with col2:
    avg_age = (pd.Timestamp.now().year - df_filtered['model_year'].mean()).round(1)
    st.metric("Avg Vehicle Age", f"{avg_age:.1f} years")
with col3:
    most_stolen = df_filtered['make_name'].mode()[0]
    st.metric("Most Stolen Make", most_stolen)
with col4:
    df_filtered['population'] = pd.to_numeric(df_filtered['population'].astype(str).str.replace(',', ''), errors='coerce')

    avg_population = df_filtered['population'].mean()
    if pd.notnull(avg_population) and avg_population > 0:
        theft_rate = (total_thefts / avg_population * 100000).round(2)
        st.metric("Thefts per 100k", f"{theft_rate:.2f}")
    else:
        st.metric("Thefts per 100k", "N/A")

st.markdown("### Detailed Analysis")

st.subheader(" Most Frequently Stolen Vehicle Models")

model_count = df_filtered['vehicle_desc'].value_counts().reset_index()
model_count.columns = ['model', 'count']

fig_models = px.bar(
    model_count.head(20).sort_values('count', ascending=True),
    x='count',
    y='model',
    orientation='h',
    title='Top 20 Most Frequently Stolen Vehicle Models',
    color='count',
    color_continuous_scale='viridis'
)

fig_models.update_layout(
    margin=dict(l=150, r=20, t=40, b=20),
    yaxis={
        'categoryorder': 'total descending',
        'automargin': True
    },
    height=600,
    xaxis_title="Number of Thefts",
    yaxis_title="Vehicle Model"
)

fig_models.update_traces(marker_colorbar=dict(
    title=dict(text='Number of Thefts'),
    thickness=18,
    len=0.75,
    outlinewidth=1,
    outlinecolor='rgba(128,128,128,0.3)'
))

st.plotly_chart(fig_models, width='stretch')

st.subheader(" Vehicle Makes Analysis")
col5, col6 = st.columns(2)

with col5:
    top_makes = (
        df_filtered.groupby(['make_name', 'make_type'])
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
        .head(15)
    )
    
    fig = px.bar(
        top_makes,
        x='make_name',
        y='count',
        color='make_type',
        title='Top 15 Most Stolen Vehicle Makes by Category',
        barmode='group'
    )
    fig.update_layout(xaxis_tickangle=45, showlegend=True)
    st.plotly_chart(fig, width='stretch')

with col6:
    make_type_counts = df_filtered['make_type'].value_counts()
    if 'Unknown' in make_type_counts.index:
        make_type_counts = make_type_counts[make_type_counts.index != 'Unknown']

    fig = go.Figure(data=[go.Pie(
        labels=make_type_counts.index,
        values=make_type_counts.values,
        hole=.7,
        marker_colors=['#66b3ff', '#ff9999'][:len(make_type_counts)]
    )])
    fig.update_layout(
        title='Luxury vs Standard Vehicle Thefts',
        annotations=[dict(text='Vehicle<br>Types', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    st.plotly_chart(fig, width='stretch')

st.subheader(" Regional Theft Analysis")
col3, col4 = st.columns(2)

with col3:
    location_counts = (
        df_filtered['region']
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )
    location_counts.columns = ['region', 'theft_count']
    
    fig = px.bar(
        location_counts,
        x='region', 
        y='theft_count',
        title='Top 10 Locations for Vehicle Theft',
        color='theft_count',
        color_continuous_scale='viridis'
    )
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, width='stretch')

with col4:
    top_models = df_filtered['vehicle_desc'].value_counts().head(10).index
    subset_df = df_filtered[df_filtered['vehicle_desc'].isin(top_models)]

    fig = px.histogram(
        subset_df,
        x='region',
        color='vehicle_desc',
        title='Top 10 Stolen Vehicle Models by Region',
        barmode='group'
    )
    fig.update_layout(
        xaxis_tickangle=45,
        legend_title="Vehicle Model",
        showlegend=True
    )
    st.plotly_chart(fig, width='stretch')

st.subheader(" Theft Trends Over Time")
col_time1, col_time2 = st.columns(2)

with col_time1:
    df_filtered['date_stolen'] = pd.to_datetime(df_filtered['date_stolen'], errors='coerce')
    quarterly_counts = (
        df_filtered
        .set_index('date_stolen')
        .resample('Q')
        .size()
        .reset_index(name='theft_count')
    )
    quarterly_counts['quarter_label'] = quarterly_counts['date_stolen'].dt.to_period('Q').astype(str)
    
    fig = px.line(
        quarterly_counts,
        x='quarter_label',
        y='theft_count',
        title='Quarterly Vehicle Theft Trend',
        markers=True
    )
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, width='stretch')

with col_time2:
    model_years = (
        df_filtered['model_year']
        .dropna()
        .astype(int)
        .value_counts()
        .sort_index()
        .reset_index()
    )
    model_years.columns = ['model_year', 'theft_count']

    fig = px.line(
        model_years,
        x='model_year',
        y='theft_count',
        title='Number of Cars Stolen by Model Year',
        markers=True
    )
    fig.update_layout(
        xaxis_title="Model Year",
        yaxis_title="Number of Thefts"
    )
    st.plotly_chart(fig, width='stretch')

st.subheader(" Vehicle Demographics")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### Vehicle Colors Analysis")
    color_counts = (
        df_filtered['color']
        .dropna()
        .value_counts()
        .reset_index()
    )
    color_counts.columns = ['color', 'theft_count']

    fig_colors = px.bar(
        color_counts,
        x='color',
        y='theft_count',
        title='Total Count of Stolen Vehicles by Color',
        labels={'color': 'Color', 'theft_count': 'Number of Thefts'},
        color='theft_count',
        color_continuous_scale='viridis',
        template='plotly_white'
    )
    fig_colors.update_traces(hovertemplate="<b>%{x}</b><br>Thefts: %{y}<extra></extra>", marker=dict(showscale=True))
    fig_colors.update_traces(marker_colorbar=dict(
        title=dict(text='Number of Thefts'),
        thickness=18,
        len=0.75,
        outlinewidth=1,
        outlinecolor='rgba(128,128,128,0.3)'
    ))
    fig_colors.update_layout(
        xaxis=dict(
            tickangle=45,
            title=dict(text='Color')
        ),
        yaxis=dict(
            title=dict(text='Number of Thefts'),
            gridcolor='rgba(128,128,128,0.2)'
        ),
        height=420,
        margin=dict(t=40, l=10, r=10, b=40),
        showlegend=False
    )
    fig_colors = create_themed_chart(fig_colors)
    st.plotly_chart(fig_colors, width='stretch')

with col2:
    st.markdown("#### Top Vehicle Types")
    type_counts = (
        df_filtered['vehicle_type']
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )
    type_counts.columns = ['vehicle_type', 'theft_count']

    fig_types = px.bar(
        type_counts,
        x='vehicle_type',
        y='theft_count',
        title='Top 10 Stolen Vehicle Types',
        labels={'vehicle_type': 'Vehicle Type', 'theft_count': 'Number of Thefts'},
        template='plotly_white',
        color_discrete_sequence=[COLOR_SCHEME['primary'][0]]
    )
    fig_types.update_traces(hovertemplate="<b>%{x}</b><br>Thefts: %{y}<extra></extra>")
    fig_types.update_layout(
        xaxis=dict(tickangle=45, title=dict(text='Vehicle Type')),
        yaxis=dict(title=dict(text='Number of Thefts'), gridcolor='rgba(128,128,128,0.2)'),
        height=420,
        margin=dict(t=40, l=10, r=10, b=40),
        showlegend=False
    )
    fig_types = create_themed_chart(fig_types)
    st.plotly_chart(fig_types, width='stretch')

st.subheader(" Vehicle Age Analysis")
model_years = (
    df_filtered['model_year']
    .dropna()
    .astype(int)
    .value_counts()
    .sort_index()
    .reset_index()
)
df_filtered['vehicle_age'] = datetime.now().year - df_filtered['model_year']
age_type_trend = (
    df_filtered[(df_filtered['vehicle_age'] >= 0) & (df_filtered['vehicle_age'] < 100)]
    .groupby(['vehicle_age', 'make_type'])
    .size()
    .reset_index(name='count')
)

fig = px.line(
    age_type_trend,
    x='vehicle_age',
    y='count',
    color='make_type',
    title='Vehicle Age vs Theft Count by Type',
    markers=True
)
fig.update_layout(
    xaxis_title="Vehicle Age (years)",
    yaxis_title="Number of Thefts"
)
st.plotly_chart(fig, width='stretch')

st.subheader(" Vehicle Make & Color Distribution")
col7, col8 = st.columns([2, 1])

with col7:
    maker_color_counts = (
        df_filtered.groupby(['make_name', 'color'])
        .size()
        .reset_index(name='theft_count')
    )
    
    top10_makers = df_filtered['make_name'].value_counts().head(10).index
    filtered_data = maker_color_counts[maker_color_counts['make_name'].isin(top10_makers)]
    
    fig = px.bar(
        filtered_data,
        x='theft_count',
        y='make_name',
        color='color',
        orientation='h',
        title='Top 10 Vehicle Makers — Thefts by Color',
        color_discrete_sequence=px.colors.qualitative.Set3,
        barmode='stack'
    )
    
    fig.update_layout(
        showlegend=True,
        legend_title="Vehicle Color",
        yaxis={'categoryorder': 'total ascending'},
        height=600
    )
    st.plotly_chart(fig, width='stretch')

st.subheader(" Population Density Impact Analysis")

region_thefts = df_filtered.groupby('region')['vehicle_id'].count().reset_index()
region_thefts.rename(columns={'vehicle_id': 'theft_count'}, inplace=True)
region_info = df_filtered[['region', 'population', 'density']].drop_duplicates()
region_data = region_thefts.merge(region_info, on='region', how='left')
corr_value = region_data['theft_count'].corr(region_data['density'])

fig = px.scatter(
    region_data,
    x='density',
    y='theft_count',
    trendline="ols",
    title=f'Correlation Between Vehicle Thefts and Population Density (r = {corr_value:.2f})',
    color_discrete_sequence=['#636EFA'],
    labels={
        'density': 'Population Density',
        'theft_count': 'Number of Thefts'
    }
)

fig.update_traces(marker=dict(size=8, opacity=0.6))
fig.update_layout(height=500)
st.plotly_chart(fig, width='stretch')

def clean_population(value):
    if pd.isna(value):
        return None
    try:
        return str(value).replace(',', '')
    except:
        return None

region_data['population'] = pd.to_numeric(
    region_data['population'].apply(clean_population), 
    errors='coerce'
)

region_data['thefts_per_10k_pop'] = (region_data['theft_count'] / region_data['population']) * 10000

def format_number(x):
    if isinstance(x, (int, float)):
        return f"{x:,.2f}" if x % 1 else f"{int(x):,}"
    return str(x)

col9, col10 = st.columns(2)

with col9:
    st.subheader("Highest Per-Capita Theft Rates")
    top5 = region_data.nlargest(5, 'thefts_per_10k_pop')[
        ['region', 'theft_count', 'thefts_per_10k_pop']
    ]
    
    # Format the data
    top5_formatted = top5.copy()
    for col in top5_formatted.columns:
        top5_formatted[col] = top5_formatted[col].apply(format_number)
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Region", "Total Thefts", "Thefts per 10k"],
            fill_color='#636EFA',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[top5_formatted[k].tolist() for k in top5_formatted.columns],
            fill_color=['rgba(99, 110, 250, 0.1)'] * len(top5_formatted),
            align='left',
            font=dict(size=11),
            height=30
        )
    )])
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, width='stretch')

with col10:
    st.subheader("Lowest Per-Capita Theft Rates")
    bottom5 = region_data.nsmallest(5, 'thefts_per_10k_pop')[
        ['region', 'theft_count', 'thefts_per_10k_pop']
    ]
    
    # Format the data
    bottom5_formatted = bottom5.copy()
    for col in bottom5_formatted.columns:
        bottom5_formatted[col] = bottom5_formatted[col].apply(format_number)
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Region", "Total Thefts", "Thefts per 10k"],
            fill_color='#EF553B',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[bottom5_formatted[k].tolist() for k in bottom5_formatted.columns],
            fill_color=['rgba(239, 85, 59, 0.1)'] * len(bottom5_formatted),
            align='left',
            font=dict(size=11),
            height=30
        )
    )])
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, width='stretch')
