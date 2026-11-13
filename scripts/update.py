"""Descarga el ranking público de Trading Latam y regenera los archivos del repositorio."""
import csv, json, re, urllib.request, datetime, pathlib

SRC = "https://trading-latam.com/ranking-toptraders/data.json"
ROOT = pathlib.Path(__file__).resolve().parent.parent
FIELDS = ["position", "strategy_alias", "broker", "platform", "tl_score", "tl_rating",
          "gain_pct", "monthly_pct", "drawdown_max", "profit_factor", "sharpe",
          "win_rate", "trades_count", "copyable", "last_sync_at", "report_url"]

req = urllib.request.Request(SRC, headers={"User-Agent": "Mozilla/5.0"})
data = json.load(urllib.request.urlopen(req, timeout=60))
rows = [{k: s.get(k) for k in FIELDS} for s in data["strategies"]]
fecha = data.get("date_modified") or datetime.date.today().isoformat()

out = {k: v for k, v in data.items() if k != "strategies"}
out["source"] = "https://trading-latam.com/ranking-toptraders/"
out["strategies"] = rows
(ROOT / "data" / "ranking.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")

def write_csv(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

write_csv(ROOT / "data" / "ranking.csv")
write_csv(ROOT / "data" / "historico" / f"{fecha}.csv")

tabla = ["| # | Trader o estrategia | Bróker | Plataforma | TL-Score | Calificación | Reporte en vivo |",
         "|---|---|---|---|---|---|---|"]
for r in rows[:10]:
    tabla.append(f"| {r['position']} | {r['strategy_alias']} | {r['broker']} | {r['platform']} | "
                 f"{r['tl_score']} | {r['tl_rating']} | [ver reporte]({r['report_url']}) |")
bloque = (f"<!-- TOP:INICIO -->\n**Actualizado: {fecha}** · {len(rows)} cuentas públicas verificadas\n\n"
          + "\n".join(tabla) + "\n<!-- TOP:FIN -->")
readme = ROOT / "README.md"
txt = readme.read_text()
readme.write_text(re.sub(r"<!-- TOP:INICIO -->.*?<!-- TOP:FIN -->", bloque, txt, flags=re.S))
print(f"{fecha}: {len(rows)} filas")
