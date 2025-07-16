import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("mlb_hitting_stats_cleaned.csv")

# Calculate derived columns if needed
df["homeRunRate"] = df["homeRuns"] / df["atBats"]

# Sidebar navigation
st.sidebar.title("MLB Hitting Stats Explorer")
menu = st.sidebar.radio("Select Analysis Type:", ["Univariate Analysis", "Bivariate Analysis"])

st.title("⚾ MLB Hitting Stats Dashboard")

if menu == "Univariate Analysis":
    st.header("Univariate Analysis")
    plot_type = st.sidebar.selectbox("Choose Plot Type:", ["Histogram", "Boxplot", "Bar Chart"])

    if plot_type == "Histogram":
        numeric_col = st.selectbox("Select numerical column:", df.select_dtypes(include='number').columns)
        fig = px.histogram(df, x=numeric_col, nbins=30, title=f"Distribution of {numeric_col}")
        st.plotly_chart(fig)

    elif plot_type == "Boxplot":
        numeric_col = st.selectbox("Select numerical column:", df.select_dtypes(include='number').columns)
        fig = px.box(df, y=numeric_col, title=f"Boxplot of {numeric_col}")
        st.plotly_chart(fig)

    elif plot_type == "Bar Chart":
        cat_col = st.selectbox("Select categorical column:", df.select_dtypes(include='object').columns)
        bar_data = df[cat_col].value_counts().reset_index()
        bar_data.columns = [cat_col, "count"]
        fig = px.bar(bar_data, x=cat_col, y="count", title=f"Bar Chart of {cat_col}")
        st.plotly_chart(fig)

elif menu == "Bivariate Analysis":
    st.header("Bivariate Analysis")
    analysis_option = st.sidebar.selectbox("Select Analysis Question:", [
        "Average Stolen Base Percentage by Team",
        "Stolen Bases vs Games Played",
        "Top 10 Power Hitters",
        "Batting Average vs On-Base Percentage"
    ])

    if analysis_option == "Average Stolen Base Percentage by Team":
        team_sb_eff = df.groupby("team")["stolenBasePercentage"].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(team_sb_eff, x="team", y="stolenBasePercentage",
                     title="Average Stolen Base Percentage by Team",
                     labels={"stolenBasePercentage": "Stolen Base %"})
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig)

    elif analysis_option == "Stolen Bases vs Games Played":
        fig = px.scatter(df, x="gamesPlayed", y="stolenBases",
                         hover_name="player", color="team",
                         title="Stolen Bases vs Games Played")
        st.plotly_chart(fig)

    elif analysis_option == "Top 10 Power Hitters":
        top_power_hitters = df[df["atBats"] > 100].sort_values("homeRunRate", ascending=False).head(10)
        fig = px.bar(top_power_hitters, x="player", y="homeRunRate", color="team",
                     title="Top 10 Power Hitters (HR Rate, Min 100 AB)")
        st.plotly_chart(fig)

    elif analysis_option == "Batting Average vs On-Base Percentage":
        fig = px.scatter(df, x="avg", y="obp", 
                         color="team", hover_name="player",
                         title="Batting Average vs On-Base Percentage")
        st.plotly_chart(fig) 
