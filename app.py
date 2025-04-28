import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

# Paths
MODEL_PATH = "artifacts/models/lgbm_model.pkl"
DATA_PATH = "artifacts/raw/raw.csv"

# Load model and data
model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH)

# Create Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Layout
app.layout = html.Div([
    ##### Side Bar #####
    html.Div([
        html.Div([
            html.H2("Hotel Reservation Form", className="sidebar-title"),

            html.Label("Lead Time"),
            dcc.Input(id="lead_time", type="number", placeholder="Days", className="input"),

            html.Label("No. of Special Requests"),
            dcc.Input(id="special_requests", type="number", placeholder="0-10", className="input"),

            html.Label("Avg Price per Room"),
            dcc.Input(id="price", type="number", placeholder="$", className="input"),

            html.Label("Arrival Month"),
            dcc.Dropdown(
                id="arrival_month",
                options=[{"label": month, "value": idx} for idx, month in enumerate(
                    ["January", "February", "March", "April", "May", "June",
                     "July", "August", "September", "October", "November", "December"], 1)],
                value=1,
                className="dropdown"
            ),

            html.Label("Arrival Date"),
            dcc.Input(id="arrival_date", type="number", placeholder="1-31", className="input"),

            html.Label("Market Segment Type"),
            dcc.Dropdown(
                id="market_segment_type",
                options=[
                    {'label': 'Aviation', 'value': 0},
                    {'label': 'Complementary', 'value': 1},
                    {'label': 'Corporate', 'value': 2},
                    {'label': 'Offline', 'value': 3},
                    {'label': 'Online', 'value': 4}
                ],
                value=4,
                className="dropdown"
            ),

            html.Label("No. of Week Nights"),
            dcc.Input(id="week_nights", type="number", placeholder="Nights", className="input"),

            html.Label("No. of Weekend Nights"),
            dcc.Input(id="weekend_nights", type="number", placeholder="Weekend Nights", className="input"),

            html.Label("Room Type Reserved"),
            dcc.Dropdown(
                id="room_type_reserved",
                options=[{'label': f"Room Type {i+1}", 'value': i} for i in range(7)],
                value=0,
                className="dropdown"
            ),

            html.Label("Type of Meal Plan"),
            dcc.Dropdown(
                id="type_of_meal_plan",
                options=[
                    {'label': 'Meal Plan 1', 'value': 0},
                    {'label': 'Meal Plan 2', 'value': 1},
                    {'label': 'Meal Plan 3', 'value': 2},
                    {'label': 'No Meal Plan', 'value': 3}
                ],
                value=0,
                className="dropdown"
            ),

            html.Button("Predict", id="predict_btn", n_clicks=0, className="button"),

            html.Div(id="prediction_result")

        ], className="sidebar"),
        
    ##### Main content ########
    html.Div([
    html.H1("Hotel Reservation", style={"textAlign": "center", "marginBottom": "30px"}),

    html.Div([
        html.Div([dcc.Graph(id="eda_booking_status_bar")], className="graph-card"),
        html.Div([dcc.Graph(id="eda_market_segment_bar")], className="graph-card"),
    ], className="graph-row"),

    html.Div([
        html.Div([dcc.Graph(id="eda_arrival_month_bar")], className="graph-card"),
        html.Div([dcc.Graph(id="eda_price_histogram")], className="graph-card"),
    ], className="graph-row"),

    html.Div([
        html.Button("Download EDA Report (PDF)", id="download_button", className="button", n_clicks=0),
        dcc.Download(id="download_pdf")
    ], style={"marginTop": "30px", "textAlign": "center"})

], className="main-content")

    ], style={"display": "flex", "flexDirection": "row"})
])
# Callback for Prediction
@app.callback(
    Output('prediction_result', 'children'),
    Input('predict_btn', 'n_clicks'),
    State('lead_time', 'value'),
    State('special_requests', 'value'),
    State('price', 'value'),
    State('arrival_month', 'value'),
    State('arrival_date', 'value'),
    State('market_segment_type', 'value'),
    State('week_nights', 'value'),
    State('weekend_nights', 'value'),
    State('room_type_reserved', 'value'),
    State('type_of_meal_plan', 'value')
)
def predict_reservation(n_clicks, lead_time, special_requests, price,
                        arrival_month, arrival_date, market_segment_type,
                        week_nights, weekend_nights, room_type_reserved, type_of_meal_plan):
    if n_clicks > 0:
        features = np.array([[lead_time, special_requests, price,
                              arrival_month, arrival_date, market_segment_type,
                              week_nights, weekend_nights,
                              room_type_reserved, type_of_meal_plan]])
        prediction = model.predict(features)

        if prediction[0] == 1:
            return html.Div("✅ Customer is not likely to cancel!", className="result-success")
        else:
            return html.Div("🚫 Customer is likely to cancel!", className="result-fail")
    return ""

# Callback for EDA Graphs
@app.callback(
    Output('eda_price_histogram', 'figure'),
    Output('eda_market_segment_bar', 'figure'),
    Output('eda_arrival_month_bar', 'figure'),
    Output('eda_booking_status_bar', 'figure'),
    Input('predict_btn', 'n_clicks')  # Optional, to refresh graphs
)
def update_eda_graphs(n_clicks):
    # 1. Distribution of Average Room Price
    fig1 = px.histogram(df, x="avg_price_per_room", nbins=50, title="Distribution of Average Room Prices",
                        color_discrete_sequence=["#3498db"])

    # 2. Market Segment Type (Grouped)
    market_segment_counts = df['market_segment_type'].value_counts().reset_index()
    market_segment_counts.columns = ['market_segment_type', 'count']
    fig2 = px.bar(market_segment_counts, x='market_segment_type', y='count', title="Market Segment Distribution",
                  color_discrete_sequence=["#2ecc71"])

    # 3. Arrival Month (Grouped)
    arrival_month_counts = df['arrival_month'].value_counts().sort_index().reset_index()
    arrival_month_counts.columns = ['arrival_month', 'count']
    fig3 = px.bar(arrival_month_counts, x='arrival_month', y='count', title="Arrival Month Distribution",
                  color_discrete_sequence=["#9b59b6"])

    # 4. Booking Status (Grouped)
    booking_status_counts = df['booking_status'].value_counts().reset_index()
    booking_status_counts.columns = ['booking_status', 'count']
    fig4 = px.bar(booking_status_counts, x='booking_status', y='count', title="Booking Status Distribution",
                  color_discrete_sequence=["#e74c3c"])

    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run(debug=True)