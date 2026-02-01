import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mini Valorisation d'Action", layout="wide")
st.markdown("""
<style>
.stApp {
    background-color: #fffdf4;  /* un jaune très pâle */
}
.stMarkdown { color: black !important; }
.stWrite { color: black !important; }
.stText { color: black !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #d9534f;'>Mini Valorisation</h1>", unsafe_allow_html=True)



#st.title("Mini Valorisation d'Action")#

ticker = st.text_input("Entre le ticker", "AAPL")

if ticker:
    try:
        action = yf.Ticker(ticker)
        infos = action.info
        devise = infos.get("currencySymbol") or infos.get("currency") or "?"
        prix = infos.get("currentPrice", "Non dispo")
        eps = infos.get("trailingEps", "Non dispo")
        per = infos.get("trailingPE", "Non dispo")
        fper = infos.get("forwardPE", "Non dispo")

        st.write(f"**Prix actuel** : {prix} {devise}")
        st.write(f"**PER (trailing)** : {per}")
        st.write(f"**PER (forward)** : {fper}")
        st.write(f"**EPS (trailing)** : {eps}")


        st.markdown("<h2 style='color: #d9534f;'>Méthode 1 - Estimation simple</h2>", unsafe_allow_html=True)

        cagr_eps = st.number_input("Mon CAGR estimé pour les EPS (en %)", 
                                   min_value=-100.0, value=12.0)

        eps_actuel = infos.get("trailingEps", 0.01)
        eps_futur = eps_actuel * ((1 + cagr_eps / 100) ** 5)

        per_estime = st.number_input("PER que j'estime dans 5 ans", min_value=5.0, value=20.0)
        prix_cible = eps_futur * per_estime
        st.write(f"**Prix cible dans 5 ans** : {prix_cible:.2f} {devise}")

        # CAGR nécessaire pour aller du prix actuel au cible
        if prix and prix_cible > 0:
           cagr_prix = ((prix_cible / prix) ** (1/5) - 1) * 100
           if cagr_prix >= 10:
              st.success(f"**CAGR au prix actuel (5 ans)** : {cagr_prix:.1f} %")
           else:
              st.error(f"**CAGR au prix actuel (5 ans)** : {cagr_prix:.1f} %")
         

        st.markdown("<h2 style='color: #d9534f;'>Méthode 2 - Prix d'entrée juste</h2>", unsafe_allow_html=True)

        rendement_attendu = st.number_input("Rendement annuel attendu (%)", value=10.0)
        horizon = st.number_input("Nombre d'années", value=5, step=1)

        # Prix futur = EPS actuel × (1 + CAGR)^horizon × PER futur
        prix_futur = eps_actuel * ((1 + cagr_eps / 100) ** horizon) * per_estime

        # Prix d'entrée = prix futur / (1 + rendement)^horizon
        prix_entree = prix_futur / ((1 + rendement_attendu / 100) ** horizon)

        if  prix_entree>= prix:
              st.success(f"**CAGR au prix actuel (5 ans)** : {cagr_prix:.1f} %")
        else:
              st.error(f"**CAGR au prix actuel (5 ans)** : {cagr_prix:.1f} %")
           
        st.write(f"**Prix d'entrée juste aujourd'hui** : {prix_entree:.2f} $")


    except Exception as e:
        st.error(f"Erreur avec {ticker} : {e}")









