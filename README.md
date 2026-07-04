# SKS Tipovačka 2025/26 — webová aplikace

Výsledky fanouškovské tipovačky podcastu **Sešívaní sobě** (SK Slavia Praha).
Žebříček celé sezóny + proklik na jednotlivé zápasy s tipy a body.

## Soubory
- `streamlit_app.py` — aplikace
- `sks_data.json` — data (žebříček + zápasy); stačí přepsat a appka se aktualizuje
- `requirements.txt` — závislosti
- `.streamlit/config.toml` — barvy (zelená/červená brand)

## Spuštění lokálně
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Nasazení zdarma (Streamlit Community Cloud)
1. Nahraj tyhle soubory do GitHub repa (klidně `sesivanisobe/slavia-dashboard` nebo nové).
2. Na https://share.streamlit.io → **New app** → vyber repo a `streamlit_app.py`.
3. Hotovo — appka pojede na veřejné URL.

## Aktualizace dat
Vše je v `sks_data.json`:
- `leaderboard`: pořadí (`rank`, `name`, `tot`, `res`, `sc`, `petr`)
- `matches`: zápasy (`round`, `date`, `comp`, `label`, `result`, `scorers`, `tips`)

## Ještě dořešit
- Sloučit řádky „Petr" (dva neuložené účty) do dvou osob.
- Ověřit střelce nadstavbových kol 42–46.
