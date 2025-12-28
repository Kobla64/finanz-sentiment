import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Seiteneinstellungen
st.set_page_config(page_title="DAX Sentiment Analysis", layout="wide")
st.title("📊 DAX seit 2023: Kurs & Analyse")


# 2. Daten laden
@st.cache_data  # Sorgt dafür, dass die Daten nicht bei jedem Klick neu geladen werden
def load_data():
    df = pd.read_csv("data/processed_stock_data.csv", index_col=0, parse_dates=True)
    return df


try:
    df = load_data()

    # 3. Key Metrics (KPIs) ganz oben anzeigen
    last_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2]
    diff = last_price - prev_price

    col1, col2, col3 = st.columns(3)
    col1.metric("Aktueller Kurs", f"{last_price:,.0f} Pkt", f"{diff:,.2f}")
    col2.metric("Letzte Volatilität", f"{df['Volatility'].iloc[-1]:.2%}")
    col3.metric("Handelstage", len(df))

    # 4. Der Haupt-Chart mit Kurs MAs und Volatilität
    st.subheader("Kursverlauf mit Moving Averages & Volatilität")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Schlusskurs", line=dict(color="#004b87"),hoverinfo="x+y"))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA20'], name="MA20 Trend", line=dict(color="#ffa500", dash='dash'),hoverinfo="x+y"))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name="MA50 Trend", line=dict(color="#ffffff", dash='dash'),hoverinfo="x+y"))
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['Volatility'],
            name="Volatilität",
            fill='tozeroy',  # Füllt die Fläche bis zur Null-Linie
            mode='lines',  # Zeichnet eine Linie (oder 'none' für nur Fläche)
            line=dict(width=0, color='rgba(200, 0, 0, 0.4)'),  # Dünne rote Oberkante
            fillcolor='rgba(200, 0, 0, 0.2)',  # Sehr transparente Füllung
            hoverinfo="y",
        ),
        secondary_y=True,
    )

    max_vol = df['Volatility'].max()
    # Ein kleiner Puffer, falls max_vol 0 ist (verhindert Fehler)
    top_limit = max_vol * 3 if max_vol > 0 else 0.1

    fig.update_layout(
        height=500,
        template="plotly_white",
        hovermode="x unified",  # Ein gemeinsames Hover-Fenster für alle Infos
        legend=dict(
            orientation="h",  # Horizontale Legende oben, spart Platz
            yanchor="bottom", y=1.02,
            xanchor="right", x=1
        ),
        # Linke Achse (Preis)
        yaxis=dict(
            title="Kurs in Punkten",
            showgrid=True,
            fixedrange=True
        ),
        # Rechte Achse (Volatilität)
        yaxis2=dict(
            title="Volatilität (%)",
            showgrid=False,  # Kein Gitter für Volatilität, sonst wird es unruhig
            fixedrange=True,
            range=[0, top_limit],  # HIER passiert die Höhenbegrenzung
            side="right",
            tickformat=".1%"  # Zeigt z.B. "1.5%" statt "0.015" an der Achse
        ),
        xaxis=dict(fixedrange=True),
        margin=dict(l=50, r=50, t=80, b=30)  # Etwas Platz oben für die Legende
    )

    #fig.update_layout(height=500, template="plotly_white", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True, config={
    'scrollZoom': False,
    'doubleClick': False,
    'displayModeBar': False
})

except FileNotFoundError:
    st.error("Datei 'processed_stock_data.csv' nicht gefunden. Bitte führe erst 'processing.py' aus!")