"""Descarga el ranking público de Trading Latam y regenera los archivos del repositorio."""
import csv, json, os, re, urllib.request, urllib.error, datetime, pathlib, time

SRC = "https://trading-latam.com/ranking-toptraders/data.json"
ROOT = pathlib.Path(__file__).resolve().parent.parent
FIELDS = ["position", "strategy_alias", "broker", "platform", "tl_score", "tl_rating",
          "gain_pct", "monthly_pct", "drawdown_max", "profit_factor", "sharpe",
          "win_rate", "trades_count", "copyable", "last_sync_at", "report_url"]

def validate_ranking(data):
    if not isinstance(data, dict) or data.get("status") != "ok":
        raise ValueError("La fuente no devuelve un ranking disponible")
    strategies = data.get("strategies")
    if not isinstance(strategies, list) or type(data.get("total")) is not int or data["total"] != len(strategies):
        raise ValueError("Ranking incompleto: total y filas no coinciden")
    if not all(isinstance(row, dict) and {"position", "strategy_alias", "report_url"} <= row.keys() for row in strategies):
        raise ValueError("Filas del ranking sin los campos públicos requeridos")
    date = data.get("date_modified")
    if not isinstance(date, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", date):
        raise ValueError("Fecha de la fuente inválida")
    datetime.date.fromisoformat(date)
    return data


def fetch_ranking():
    downloaded = os.environ.get('RANKING_SOURCE_FILE')
    if downloaded:
        with open(downloaded, encoding='utf-8') as source:
            return validate_ranking(json.load(source))
    req = urllib.request.Request(SRC, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    for attempt in range(3):
        delay = 5 * (attempt + 1)
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                return validate_ranking(json.load(response))
        except urllib.error.HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504):
                raise
            retry_after = error.headers.get("Retry-After", "") if error.headers else ""
            if retry_after.isdigit():
                delay = max(delay, int(retry_after))
                if delay > 60:
                    raise RuntimeError("La fuente pide esperar; se conserva la captura anterior") from error
            last_error = error
        except (ValueError, urllib.error.URLError) as error:
            last_error = error
        if attempt < 2:
            time.sleep(delay)
    raise RuntimeError("Fuente inválida tras tres intentos; no se modifican los archivos") from last_error


data = fetch_ranking()
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
