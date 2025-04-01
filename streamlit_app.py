import asyncio

import altair as alt
import pandas as pd
import streamlit as st

from map_utils import search_nearby_places

# List of allowed place types (Table 1)
ALLOWED_PLACE_TYPES = [
    "accounting", "airport", "amusement_park", "aquarium", "art_gallery",
    "atm", "bakery", "bank", "bar", "beauty_salon", "bicycle_store",
    "book_store", "bowling_alley", "bus_station", "cafe", "campground",
    "car_dealer", "car_rental", "car_repair", "car_wash", "casino", "cemetery",
    "church", "city_hall", "clothing_store", "convenience_store", "courthouse",
    "dentist", "department_store", "doctor", "drugstore", "electrician",
    "electronics_store", "embassy", "fire_station", "florist", "funeral_home",
    "furniture_store", "gas_station", "gym", "hair_care", "hardware_store",
    "hindu_temple", "home_goods_store", "hospital", "insurance_agency",
    "jewelry_store", "laundry", "lawyer", "library", "light_rail_station",
    "liquor_store", "local_government_office", "locksmith", "lodging",
    "meal_delivery", "meal_takeaway", "mosque", "movie_rental", "movie_theater",
    "moving_company", "museum", "night_club", "painter", "park", "parking",
    "pet_store", "pharmacy", "physiotherapist", "plumber", "police", "post_office",
    "primary_school", "real_estate_agency", "restaurant", "roofing_contractor",
    "rv_park", "school", "secondary_school", "shoe_store", "shopping_mall",
    "spa", "stadium", "storage", "store", "subway_station", "supermarket",
    "synagogue", "taxi_stand", "tourist_attraction", "train_station",
    "transit_station", "travel_agency", "university", "veterinary_care", "zoo"
]

st.set_page_config(page_title="Market Research Dashboard", layout="wide")

st.title("Market Research Dashboard")
st.markdown("""
This dashboard helps you analyze the market potential for your business in a specific location.
Use the sidebar to set your search parameters and analyze the competition, customer base, and market opportunities.
""")

st.sidebar.header("Search Parameters")
lat = st.sidebar.number_input("Latitude", value=13.0196719, format="%.6f")
lng = st.sidebar.number_input("Longitude", value=80.2688418, format="%.6f")
radius = st.sidebar.number_input("Radius (km)", value=2.0, min_value=0.1, step=0.1)
selected_types = st.sidebar.multiselect("Select Place Types", ALLOWED_PLACE_TYPES, default=["restaurant", "cafe"])
only_with_photo = st.sidebar.checkbox("Only show results with photo", value=False)
max_results = st.sidebar.number_input("Maximum Results", min_value=20, max_value=200, value=20, step=20)

async def search_and_display():
    if selected_types:
        with st.spinner("Analyzing market data..."):
            try:
                all_data = []
                status_summary = {}
                type_counter = {}

                for place_type in selected_types:
                    results = await search_nearby_places((lat, lng), radius, place_type, require_photo=only_with_photo, max_results=max_results)
                    status_summary[place_type] = len(results)
                    for rec in results:
                        for t in rec.get("type", []):
                            type_counter[t] = type_counter.get(t, 0) + 1
                        rec["Place Type Searched"] = place_type
                        all_data.append(rec)

                if all_data:
                    df = pd.DataFrame(all_data)
                    
                    # Market Overview Section
                    st.header("Market Overview")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Competitors", len(df))
                    with col2:
                        st.metric("Average Rating", f"{df['rating'].mean():.1f}")
                    with col3:
                        st.metric("Total Reviews", int(df['user_ratings_total'].sum()))
                    with col4:
                        st.metric("Currently Open", int(df['is_open_now'].sum()))

                    # Competition Analysis Section
                    st.header("Competition Analysis")
                    
                    # 1. Price Level Distribution
                    price_counts = df["price_level_symbols"].value_counts().sort_index().reset_index()
                    price_counts.columns = ["Price Level", "Count"]
                    # Replace empty price level with "Not Defined"
                    price_counts["Price Level"] = price_counts["Price Level"].replace("", "Not Defined")
                    bar_price = alt.Chart(price_counts).mark_bar().encode(
                        x=alt.X("Price Level:N", sort='-y'),
                        y=alt.Y("Count:Q"),
                        tooltip=["Price Level", "Count"]
                    ).properties(width=400, height=300, title="Price Level Distribution")

                    # 2. Rating vs. Price Level
                    # Create a copy of the dataframe for the scatter plot
                    scatter_df = df.copy()
                    # Replace price level 0 with "Not Defined" for visualization
                    scatter_df["price_level_display"] = scatter_df["price_level"].apply(
                        lambda x: "Not Defined" if x == 0 else f"Level {x}"
                    )
                    scatter_rating_price = alt.Chart(scatter_df).mark_circle().encode(
                        x=alt.X("price_level_display:N", title="Price Level"),
                        y=alt.Y("rating:Q", title="Rating"),
                        size=alt.Size("user_ratings_total:Q", title="Number of Reviews"),
                        color=alt.Color("Place Type Searched:N"),
                        tooltip=["name", "rating", "price_level_display", "user_ratings_total"]
                    ).properties(width=400, height=300, title="Rating vs. Price Level")

                    # 3. Business Status Distribution
                    status_counts = df["business_status"].fillna("Not Provided").value_counts().reset_index()
                    status_counts.columns = ["Business Status", "Count"]
                    pie_status = alt.Chart(status_counts).mark_arc().encode(
                        theta=alt.Theta(field="Count", type="quantitative"),
                        color=alt.Color(field="Business Status", type="nominal"),
                        tooltip=["Business Status", "Count"]
                    ).properties(width=400, height=300, title="Business Status Distribution")

                    # 4. Top Place Types
                    type_df = pd.DataFrame(list(type_counter.items()), columns=["type", "Count"])
                    type_df = type_df.sort_values("Count", ascending=False).head(10)
                    bar_types = alt.Chart(type_df).mark_bar().encode(
                        x=alt.X("type:N", sort='-y', title="Place Type"),
                        y=alt.Y("Count:Q"),
                        tooltip=["type", "Count"]
                    ).properties(width=400, height=300, title="Top 10 Place Types")

                    # Display charts in a grid
                    col1, col2 = st.columns(2)
                    with col1:
                        st.altair_chart(bar_price)
                        st.altair_chart(pie_status)
                    with col2:
                        st.altair_chart(scatter_rating_price)
                        st.altair_chart(bar_types)

                    # Market Insights Section
                    st.header("Market Insights")
                    
                    # Calculate market insights
                    avg_rating = df['rating'].mean()
                    avg_reviews = df['user_ratings_total'].mean()
                    price_levels = df['price_level'].value_counts()
                    most_common_price = price_levels.index[0] if not price_levels.empty else 0
                    undefined_price_count = len(df[df['price_level'] == 0])
                    total_businesses = len(df)
                    price_defined_percentage = ((total_businesses - undefined_price_count) / total_businesses) * 100
                    
                    insights = [
                        f"📊 Market Saturation: {'High' if len(df) > 50 else 'Medium' if len(df) > 20 else 'Low'}",
                        f"⭐ Average Rating: {avg_rating:.1f}",
                        f"📝 Average Reviews per Business: {avg_reviews:.0f}",
                        f"💰 Price Level Information: {price_defined_percentage:.1f}% of businesses have defined price levels",
                        f"🏪 Currently Open Businesses: {int(df['is_open_now'].sum())}",
                        f"📸 Businesses with Photos: {int(df['has_photos'].sum())}"
                    ]
                    
                    for insight in insights:
                        st.info(insight)

                    # Detailed Results Section
                    st.header("Detailed Results")
                    st.dataframe(df)

                    # Download button for CSV export
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Market Research Data", data=csv, file_name="market_research_data.csv", mime="text/csv")

                else:
                    st.info("No results found for the selected filters.")
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
    else:
        st.warning("Please select at least one place type.")

if st.sidebar.button("Analyze Market"):
    asyncio.run(search_and_display()) 