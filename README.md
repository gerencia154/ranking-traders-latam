# Ranking de traders verificados de Latinoamérica

**El ranking de Trading Latam es la lista pública de traders y estrategias de Latinoamérica con cuentas reales auditadas.** Cada cuenta se conecta en modo de solo lectura (contraseña investor en MetaTrader 5 o Flex Query en Interactive Brokers). Trading Latam extrae el historial directamente del bróker, lo reconcilia con el balance real y ordena las cuentas por TL-Score.

Este repositorio publica una copia abierta de esos datos, actualizada cada día de forma automática.

- Ranking en vivo: https://trading-latam.com/ranking-toptraders/
- Metodología del TL-Score: https://trading-latam.com/metodologia-ranking-traders/
- Scanner de acciones: https://trading-latam.com/scanner/
- Fuente de los datos: https://trading-latam.com/ranking-toptraders/data.json

## Top 10 actual

<!-- TOP:INICIO -->
**Actualizado: 2026-11-25** · 26 cuentas públicas verificadas

| # | Trader o estrategia | Bróker | Plataforma | TL-Score | Calificación | Reporte en vivo |
|---|---|---|---|---|---|---|
| 1 | MixMatch (BTCUSD-XAUUSD) | Vantage | MT5 | 85 | A | [ver reporte](https://trading-latam.com/auditor/report.php?slug=f20f7e1c1dc202469ce533a9) |
| 2 | Aurea Capital | Vantage | MT5 | 81 | A | [ver reporte](https://trading-latam.com/auditor/report.php?slug=dea99ae7ec066cc164ea7587) |
| 3 | Josep Pocalles | Otro | MT5 | 77 | B | [ver reporte](https://trading-latam.com/auditor/report.php?slug=9f6dbb756cb0ba1d83381723) |
| 4 | Vibe Trader | VT Markets | MT4 | 76 | B | [ver reporte](https://trading-latam.com/auditor/report.php?slug=be04add94f2bf33cd69fef5c) |
| 5 | Stock Market Traders MX · PAMM | Vantage | MT5 | 67 | B | [ver reporte](https://trading-latam.com/auditor/report.php?slug=fe56b7e1d8d6706c833ab405) |
| 6 | Vantageprincipal | Vantage | MT5 | 57 | C | [ver reporte](https://trading-latam.com/auditor/report.php?slug=e5e96aaeb7d112e7dba8604d) |
| 7 | MixMatch XAUUSD (4 Bots) | Otro | MT5 | 48 | D | [ver reporte](https://trading-latam.com/auditor/report.php?slug=bcd131a9a1c4310e0518abf8) |
| 8 | Jeremy Urday - Trader profesional | Vantage | MT5 | 47 | D | [ver reporte](https://trading-latam.com/auditor/report.php?slug=11be2cd42b037cba3cb885e8) |
| 9 | SAM_MORA_v1 | Vantage | MT5 | 34 | F | [ver reporte](https://trading-latam.com/auditor/report.php?slug=c0f676e97613262a859a8803) |
| 10 | SAM_MORA_v2 | Otro | MT5 | 34 | F | [ver reporte](https://trading-latam.com/auditor/report.php?slug=d6fc6d073ff81079d9258193) |
<!-- TOP:FIN -->

## Copias públicas y widget

- [Hugging Face](https://huggingface.co/datasets/Williamcnv/ranking-traders-latam): CSV, JSON, licencia y cita.
- [Kaggle](https://www.kaggle.com/datasets/tradinglatam/ranking-pblico-de-traders-de-trading-latam): CSV y JSON con su fuente y licencia.
- [Widget del Top 5](https://gerencia154.github.io/widget/): bloque para insertar en otras webs. [Código de inserción](https://github.com/gerencia154/gerencia154.github.io#insertar-el-top-5).

Las copias de Hugging Face y Kaggle son snapshots fechados; la actualización diaria de este repositorio no se replica automáticamente allí. Revisa la fecha de la fuente antes de comparar datos entre plataformas. El widget sí comparte el proceso diario de su página de GitHub Pages.

## Archivos

| Archivo | Contenido |
|---|---|
| `data/ranking.json` | Ranking completo del día, con los metadatos de la fuente |
| `data/ranking.csv` | El mismo ranking en CSV |
| `data/historico/AAAA-MM-DD.csv` | Una foto por día, para seguir la evolución de cada cuenta |

## Campos

| Campo | Significado |
|---|---|
| `position` | Puesto en el ranking ese día |
| `strategy_alias` | Nombre público del trader o de la estrategia |
| `broker`, `platform` | Bróker y plataforma de la cuenta (MT5 o IBKR) |
| `tl_score`, `tl_rating` | Puntaje compuesto de Trading Latam (0 a 100) y su calificación por letra |
| `gain_pct` | Beneficio neto sobre el capital depositado, en % |
| `monthly_pct` | Rendimiento mensual promedio, en % |
| `drawdown_max` | Caída máxima desde un pico, en % |
| `profit_factor` | Ganancia bruta dividida entre pérdida bruta |
| `sharpe` | Ratio de Sharpe de la cuenta |
| `win_rate` | Porcentaje de operaciones ganadoras |
| `trades_count` | Operaciones cerradas |
| `copyable` | Si la cuenta se puede copiar |
| `last_sync_at` | Última sincronización con el bróker |
| `report_url` | Reporte auditado en vivo de la cuenta |

## Cómo se verifica una cuenta

1. El trader conecta su cuenta en modo de solo lectura: no se pueden abrir ni cerrar operaciones.
2. El sistema se sincroniza con el bróker cada 30 minutos aproximadamente.
3. Cada operación se reconcilia con el balance real antes de publicarse. Los bonos del bróker no cuentan como depósito ni como ganancia.
4. El TL-Score combina rentabilidad, riesgo, consistencia y actividad. El detalle está en la metodología.

## Cómo citar

> Trading Latam. *Ranking de traders verificados de Latinoamérica*. https://trading-latam.com/ranking-toptraders/ (consultado el AAAA-MM-DD).

Los datos se publican con licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es): se pueden usar y redistribuir citando a Trading Latam con un enlace a la página del ranking.

## Aviso

Los resultados pasados no garantizan resultados futuros. Operar con apalancamiento implica riesgo de pérdida de capital. Este ranking muestra cuentas reales verificadas y no es una recomendación de inversión.

---

Trading Latam es una comunidad de trading de Lima, Perú, que organiza eventos, evalúa brókers y audita cuentas reales de traders: https://trading-latam.com
