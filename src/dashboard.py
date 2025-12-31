import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="DAX Sentiment Analysis", layout="wide")

#Konstanten für Farben erstellen
COLORS = {
    "price": "#004b87",
    "ma20": "#ffa500",
    "ma50": "#d3d3d3",  # Hellgrau statt Weiß
    "vol_area": "rgba(200, 0, 0, 0.4)",
    "vol_line": "rgba(255, 255, 255, 0.6)"
}

@st.cache_data
def load_data():
    return pd.read_csv("data/evaluated_processed_stock_data.csv", index_col=0, parse_dates=True)


# --- 3. VISUALISIERUNGS-FUNKTIONEN ---

def render_kpi_row(df):
    """Anzeige der wichtigsten Kennzahlen in der obersten Zeile."""
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    diff = last_row['Close'] - prev_row['Close']

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("DAX Kurs", f"{last_row['Close']:,.0f} Pkt", f"{diff:,.2f}")
    c2.metric("Volatilität", f"{last_row['Volatility']:.2%}")
    # Sentiment aus der CSV (falls vorhanden) oder N/A
    sent = last_row.get('Sentiment', 0.0)
    c3.metric("Sentiment Score", f"{sent:.2f}")
    c4.metric("Handelstage", len(df))


def render_main_chart(df):
    """Erstellung des kombinierten Preis- und Volatilitäts-Charts."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Preis & MAs
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Kurs", line=dict(color=COLORS["price"])),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name="MA20", line=dict(color=COLORS["ma20"], dash='dash')),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name="MA50", line=dict(color=COLORS["ma50"], dash='dash')),
                  secondary_y=False)

    # Volatilität im Hintergrund
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Volatility'], name="Volatilität", fill='tozeroy',
        line=dict(width=0), fillcolor=COLORS["vol_area"], hoverinfo="y"
    ), secondary_y=True)

    # Layout-Feinschliff
    max_vol = df['Volatility'].max()
    fig.update_layout(
        height=500, template="plotly_white", hovermode="x unified",
        margin=dict(l=50, r=50, t=30, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis=dict(title="Kurs", showgrid=True),
        yaxis2=dict(title="Vol %", range=[0, max_vol * 3], side="right", tickformat=".1%", showgrid=False)
    )
    # WICHTIG: width='stretch' für 2026-Kompatibilität
    st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})


def render_sentiment_gauge(score):
    #Sentiment als Gauge Chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Live Sentiment-Meter", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'color': "rgba(255, 255, 255, 0.6)", 'thickness': 0.15},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [-1, -0.3], 'color': "#ff0000"}, # Kräftiges Rot
                {'range': [-0.3, 0.3], 'color': "#3e4452"}, # Dunkles Neutral für Dark Mode
                {'range': [0.3, 1], 'color': "#00ff00"}    # Frisches Grün
            ],
            # Die 'Nadel' als auffälliger Marker
            'threshold': {
                'line': {'color': "white", 'width': 5},
                'thickness': 0.8,
                'value': score
            }
        }))
    fig.update_layout(height=300, margin=dict(l=30, r=30, t=50, b=30))
    st.plotly_chart(fig, width='stretch')


def main():
    st.title("📊 SP500 Analyse-Dashboard")

    try:
        df = load_data()

        # UI Struktur
        render_kpi_row(df)

        st.markdown("---")

        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("Kurs & Trends")
            render_main_chart(df)

        with col_right:
            st.subheader("Stimmungsbild")
            current_sent = df['Sentiment'].iloc[-1] if 'Sentiment' in df.columns else 0.0
            render_sentiment_gauge(current_sent)
            st.info("Das Sentiment basiert auf einer KI-Analyse der aktuellsten News-Schlagzeilen.")

    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")
        st.info("Bitte stelle sicher, dass die Pipeline (main.py) korrekt gelaufen ist.")


if __name__ == "__main__":
    main()