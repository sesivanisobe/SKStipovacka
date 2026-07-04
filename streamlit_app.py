import json
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SKS Tipovačka 2025/26 — Sešívaní sobě",
    page_icon="❤️",
    layout="centered",
)

DATA = json.loads(Path(__file__).with_name("sks_data.json").read_text(encoding="utf-8"))
LB = DATA["leaderboard"]
MATCHES = DATA["matches"]
META = DATA["meta"]

# ---------------------------------------------------------------- styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Archivo:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"], .stMarkdown, p, span, div { font-family:'Archivo',sans-serif; }
.block-container { padding-top:1.6rem; max-width:880px; }
#MainMenu, footer { visibility:hidden; }

.hero { text-align:center; margin-bottom:.4rem;
  background:radial-gradient(circle at 15% -20%,rgba(232,0,61,.22),transparent 50%); }
.crest { font-size:12px; letter-spacing:.4em; text-transform:uppercase; color:#9fb3a8; font-weight:700; }
.crest b { color:#E8003D; }
.bigtitle { font-family:'Bebas Neue',sans-serif; font-size:clamp(52px,12vw,104px); line-height:.85;
  margin:6px 0 2px; color:#F4F1E9; }
.bigtitle .yr { color:#E8003D; }
.subt { color:#9fb3a8; font-size:14px; }
.statrow { display:flex; gap:26px; justify-content:center; margin:18px 0 6px; flex-wrap:wrap; }
.stat b { display:block; font-family:'JetBrains Mono',monospace; font-size:26px; color:#F4F1E9; }
.stat span { font-size:10px; letter-spacing:.16em; text-transform:uppercase; color:#9fb3a8; }

.lbrow { display:grid; grid-template-columns:50px 1fr auto; align-items:center; gap:14px;
  background:rgba(0,0,0,.18); border:1px solid rgba(244,241,233,.12); border-radius:14px;
  padding:12px 16px; margin-bottom:6px; }
.lbrow.t1 { background:linear-gradient(100deg,rgba(232,178,61,.22),rgba(0,0,0,.18)); border-color:rgba(232,178,61,.5); }
.lbrow.t2 { border-color:rgba(244,241,233,.35); }
.lbrow.t3 { border-color:rgba(232,0,61,.4); }
.rk { font-family:'Bebas Neue',sans-serif; font-size:30px; text-align:center; color:#9fb3a8; line-height:1; }
.t1 .rk{color:#E8B23D} .t2 .rk{color:#dfe7e2} .t3 .rk{color:#E8003D}
.nm { font-weight:700; font-size:17px; color:#F4F1E9; }
.mt { font-family:'JetBrains Mono',monospace; font-size:11px; color:#9fb3a8; margin-top:2px; }
.pts { font-family:'JetBrains Mono',monospace; font-weight:700; font-size:25px; color:#F4F1E9; text-align:right; }
.pts small { font-size:11px; color:#9fb3a8; }
.flagp { font-size:10px; font-weight:700; color:#E8003D; border:1px solid #E8003D; border-radius:6px;
  padding:1px 6px; margin-left:8px; letter-spacing:.04em; }

.badge { font-size:10px; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
  background:#F4F1E9; color:#0A3D2B; padding:3px 9px; border-radius:6px; }
.badge.lm{background:#E8B23D} .badge.cup{background:#E8003D;color:#fff} .badge.nad{background:#7fd1aa}
.scorer { display:inline-flex; align-items:center; gap:7px; background:rgba(0,0,0,.2);
  border:1px solid rgba(244,241,233,.12); border-radius:10px; padding:5px 11px; margin:0 6px 6px 0; font-size:13px; }
.posb { font-size:10px; font-weight:700; padding:1px 6px; border-radius:5px; background:#F4F1E9; color:#0A3D2B; text-transform:uppercase; }
.posb.obrance{background:#7fd1aa} .posb.zaloznik{background:#E8B23D} .posb.utocnik{background:#ff9a6b} .posb.brankar{background:#E8003D;color:#fff}
.mtitle { font-family:'Bebas Neue',sans-serif; font-size:30px; line-height:1; color:#F4F1E9; }
.mres { font-family:'JetBrains Mono',monospace; font-weight:700; font-size:26px; color:#F4F1E9; }
.mres.kont { color:#E8003D; font-size:18px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- header
st.markdown(
    f"""
<div class="hero">
  <div class="crest">Sešívaní sobě &#10084; SK Slavia Praha</div>
  <div class="bigtitle">SKS Tipovačka <span class="yr">25/26</span></div>
  <div class="subt">Soutěž ve fanouškovských tipech — výsledky celé sezóny</div>
  <div class="statrow">
    <div class="stat"><b>{META['tippers']}</b><span>tipujících</span></div>
    <div class="stat"><b>{META['matches']}</b><span>zápasů</span></div>
    <div class="stat"><b>{META['tips']}</b><span>tipů</span></div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

MEDALS = {1: "🥇", 2: "🥈", 3: "🥉"}


def comp_class(c: str) -> str:
    if "mistrů" in c:
        return "lm"
    if "MOL" in c:
        return "cup"
    if "nadstavba" in c:
        return "nad"
    return ""


tab_lb, tab_m = st.tabs(["🏆  Žebříček", "⚽  Zápasy"])

# ---------------------------------------------------------------- leaderboard
with tab_lb:
    q = st.text_input("Hledat tipujícího", "", placeholder="Začni psát jméno…").strip().lower()
    rows = [p for p in LB if not q or q in p["name"].lower()]
    if not rows:
        st.info("Nikdo takový tu není.")
    html = []
    for p in rows:
        cls = f" t{p['rank']}" if p["rank"] <= 3 else ""
        rk = MEDALS.get(p["rank"], p["rank"]) if p["rank"] <= 3 else p["rank"]
        flag = '<span class="flagp">sloučit</span>' if p.get("petr") else ""
        html.append(
            f'<div class="lbrow{cls}"><div class="rk">{rk}</div>'
            f'<div><div class="nm">{p["name"]}{flag}</div>'
            f'<div class="mt">{p["res"]} za výsledky · {p["sc"]} za střelce</div></div>'
            f'<div class="pts">{p["tot"]}<small> b</small></div></div>'
        )
    st.markdown("".join(html), unsafe_allow_html=True)

# ---------------------------------------------------------------- matches
with tab_m:
    choice = st.radio(
        "Soutěž",
        ["Vše", "Liga", "Liga mistrů", "MOL Cup", "Nadstavba"],
        horizontal=True,
        label_visibility="collapsed",
    )

    def passes(m):
        if choice == "Vše":
            return True
        if choice == "Nadstavba":
            return "nadstavba" in m["comp"]
        if choice == "Liga":
            return m["comp"] == "Liga"
        return m["comp"] == choice

    shown = [m for m in MATCHES if passes(m)]
    st.caption(f"{len(shown)} zápasů")

    for m in shown:
        res = f"{m['result']} (kontumace)" if m.get("kontumace") else m["result"]
        with st.expander(f"**{m['round']}. kolo**  ·  {m['label']}  —  {res}", expanded=False):
            st.markdown(
                f'<span class="badge {comp_class(m["comp"])}">{m["comp"]}</span> '
                f'<span style="color:#9fb3a8;font-size:13px">&nbsp; {m["dow"]} {m["date"]}</span>',
                unsafe_allow_html=True,
            )

            if m["scorers"]:
                chips = "".join(
                    f'<span class="scorer"><span class="posb {s["pos"]}">{s["pos"]}</span>'
                    f'{s["name"]} <b style="font-family:JetBrains Mono">+{s["pts"]}</b></span>'
                    for s in m["scorers"]
                )
            else:
                chips = '<span style="color:#9fb3a8">Slavia v tomto zápase nedala gól.</span>'
            st.markdown(f'<div style="margin-top:10px"><b>Střelci Slavie:</b><br>{chips}</div>', unsafe_allow_html=True)

            df = pd.DataFrame(
                [
                    {
                        "Tipující": t["name"],
                        "Skóre": t["score"] or "—",
                        "Střelec": t["scorer"] or "—",
                        "Výsl.": t["rp"],
                        "Stř.": t["sp"],
                        "Body": t["tot"],
                    }
                    for t in m["tips"]
                ]
            )

            def highlight(row):
                color = "background-color: rgba(127,209,170,.14)" if row["Body"] > 0 else ""
                return [color] * len(row)

            st.markdown("<div style='margin-top:12px'></div>", unsafe_allow_html=True)
            st.dataframe(
                df.style.apply(highlight, axis=1),
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Výsl.": st.column_config.NumberColumn(width="small"),
                    "Stř.": st.column_config.NumberColumn(width="small"),
                    "Body": st.column_config.NumberColumn(width="small"),
                },
            )

st.divider()
st.caption(
    "Bodování: 5 b za přesný výsledek · střelec podle pozice (útočník 1 / záložník 2 / obránce 3 / brankář 5). "
    "Sešívaní sobě — fanouškovský podcast o SK Slavia Praha ❤️🤍"
)
