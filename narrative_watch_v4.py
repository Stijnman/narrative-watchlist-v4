#!/usr/bin/env python3
"""
Narrative Watchlist v5.1.0
Multilingual narrative-shift tracking & intelligent stock watchlist.
Educational research tool — not financial advice.
"""

from __future__ import annotations

import argparse
import csv
import os
import smtplib
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    yf = None

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass

try:
    from rich.console import Console
    from rich.table import Table

    console = Console()
except ImportError:  # pragma: no cover
    console = None

VERSION = "5.1.0"
THEME = "Efficient AI architectures + inference boom"

# Color buckets for current narrative positioning
WATCHLIST: Dict[str, Dict[str, str]] = {
    "NVDA": {"tier": "green", "note_en": "Resilient across most inference/training scenarios", "note_nl": "Veerkrachtig in de meeste scenario's"},
    "TSM": {"tier": "green", "note_en": "Manufacturing backbone for almost every chip designer", "note_nl": "Productiebasis voor bijna alle chipontwerpers"},
    "CBRS": {"tier": "green", "note_en": "Specialized inference pure-play; size small (post-IPO vol)", "note_nl": "Gespecialiseerde inference; kleine positie (post-IPO)"},
    "CRDO": {"tier": "yellow", "note_en": "Connectivity / data-center fabric beneficiary", "note_nl": "Connectiviteit / datacenter-begunstigde"},
    "MU": {"tier": "yellow", "note_en": "Memory cycle + AI HBM demand sensitivity", "note_nl": "Geheugencyclus + AI HBM-vraag"},
    "AMKR": {"tier": "yellow", "note_en": "Advanced packaging / OSAT leverage", "note_nl": "Advanced packaging / OSAT"},
    "ALAB": {"tier": "yellow", "note_en": "Connectivity silicon; narrative-sensitive", "note_nl": "Connectiviteit-silicon; narratief-gevoelig"},
    "SMCI": {"tier": "yellow", "note_en": "AI server integrator; high narrative beta", "note_nl": "AI-server integrator; hoge narratieve beta"},
    "AVGO": {"tier": "yellow", "note_en": "Networking + custom ASIC leverage", "note_nl": "Netwerk + custom ASIC"},
    "AMD": {"tier": "yellow", "note_en": "GPU/CPU challenger; competitive narrative swings", "note_nl": "GPU/CPU-challenger; sterke narratief-schommelingen"},
    "META": {"tier": "yellow", "note_en": "Inference at scale for ads + open models", "note_nl": "Inference op schaal voor ads + open models"},
    "ARM": {"tier": "yellow", "note_en": "Architecture royalty on efficient edge/cloud cores", "note_nl": "Architectuur-royalty op efficiënte cores"},
    "MSFT": {"tier": "red", "note_en": "Hyperscaler; training capex scrutiny risk", "note_nl": "Hyperscaler; training-capex risico"},
    "GOOGL": {"tier": "red", "note_en": "Hyperscaler; capex vs ROI narrative risk", "note_nl": "Hyperscaler; capex vs ROI-risico"},
    "AMZN": {"tier": "red", "note_en": "AWS + Trainium; capex heavy", "note_nl": "AWS + Trainium; capex-zwaar"},
}

VIRAL_EXTRA = ["CRDO", "MU", "AMKR", "ALAB", "SMCI"]

HISTORY_EN = [
    "DeepSeek-class efficiency shocks can reprice GPU narratives in days — size for volatility.",
    "Mamba/SSM hype showed architecture stories move stocks before revenue does.",
    "Specialized chip IPOs often draw down 40–70% after listing; position sizing matters.",
    "NVIDIA has survived multiple narrative attacks when usage growth stayed real.",
]

HISTORY_NL = [
    "Efficiëntie-schokken (DeepSeek-stijl) kunnen GPU-narratieven in dagen herprijzen.",
    "Mamba/SSM-hype toonde: architectuurverhalen bewegen koersen vóór omzet.",
    "Gespecialiseerde chip-IPO's dalen vaak 40–70% na notering — positiesizing telt.",
    "NVIDIA overleefde meerdere narratief-aanvallen zolang usage-groei reëel bleef.",
]

SCENARIOS_EN = [
    ("Inference demand 3x", "NVDA/TSM/CBRS/SMCI/CRDO likely relative winners"),
    ("Training capex −40%", "Hyperscalers pressured; efficiency plays relative bid"),
    ("Memory shortage", "MU and packaging names can outperform"),
]

SCENARIOS_NL = [
    ("Inference-vraag 3x", "NVDA/TSM/CBRS/SMCI/CRDO relatieve winnaars"),
    ("Training-capex −40%", "Hyperscalers onder druk; efficiëntie-plays relatief"),
    ("Geheugentekort", "MU en packaging-namen kunnen outperformen"),
]


@dataclass
class Row:
    ticker: str
    tier: str
    price: float
    ma50: float
    ma200: float
    rsi14: float
    drawdown_52w: float
    signal: str
    phase: str
    size_hint: str
    note: str


def t(lang: str, en: str, nl: str) -> str:
    return nl if lang == "nl" else en


def rsi(series: pd.Series, period: int = 14) -> float:
    if series is None or len(series) < period + 1:
        return float("nan")
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    val = 100 - (100 / (1 + rs))
    return float(val.iloc[-1])


def fetch_metrics(ticker: str) -> Optional[Tuple[float, float, float, float, float]]:
    if yf is None:
        return None
    try:
        hist = yf.Ticker(ticker).history(period="2y")
        if hist is None or hist.empty or "Close" not in hist:
            return None
        close = hist["Close"].dropna()
        if len(close) < 50:
            return None
        price = float(close.iloc[-1])
        ma50 = float(close.rolling(50).mean().iloc[-1])
        ma200 = float(close.rolling(200).mean().iloc[-1]) if len(close) >= 200 else float("nan")
        r = rsi(close)
        peak = float(close.tail(252).max()) if len(close) >= 20 else float(close.max())
        dd = (price / peak - 1.0) * 100.0 if peak else 0.0
        return price, ma50, ma200, r, dd
    except Exception:
        return None


def narrative_phase(price: float, ma50: float, ma200: float, rsi14: float) -> str:
    if np.isnan(ma50):
        return "Unknown"
    if not np.isnan(rsi14) and rsi14 >= 70 and price > ma50:
        return "Hype"
    if not np.isnan(rsi14) and rsi14 <= 35 and price < ma50:
        return "Dip/Fear"
    if not np.isnan(ma200) and price > ma50 > ma200:
        return "Recovery"
    return "Consolidation"


def buy_signal(tier: str, price: float, ma50: float, ma200: float, rsi14: float) -> str:
    if any(np.isnan(x) for x in (price, ma50, rsi14)):
        return "HOLD"
    tech_ok = price > ma50 and (np.isnan(ma200) or price > ma200) and rsi14 < 68
    if tier == "green" and tech_ok:
        return "BUY"
    if tier == "yellow" and tech_ok and rsi14 < 60:
        return "WATCH_BUY"
    if tier == "red" and tech_ok:
        return "HOLD"
    if not np.isnan(rsi14) and rsi14 > 75:
        return "CAUTION"
    return "HOLD"


def size_hint(tier: str, drawdown: float, rsi14: float) -> str:
    if tier == "green" and abs(drawdown) > 35:
        return "small→medium"
    if tier == "green":
        return "core"
    if tier == "yellow":
        return "small" if (not np.isnan(rsi14) and rsi14 > 65) else "tactical"
    return "underweight"


def tier_emoji(tier: str) -> str:
    return {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(tier, "⚪")


def analyze(lang: str = "en", news: bool = False) -> List[Row]:
    rows: List[Row] = []
    for ticker, meta in WATCHLIST.items():
        metrics = fetch_metrics(ticker)
        note = meta["note_nl"] if lang == "nl" else meta["note_en"]
        if not metrics:
            rows.append(
                Row(
                    ticker=ticker,
                    tier=meta["tier"],
                    price=float("nan"),
                    ma50=float("nan"),
                    ma200=float("nan"),
                    rsi14=float("nan"),
                    drawdown_52w=float("nan"),
                    signal="N/A",
                    phase="N/A",
                    size_hint="n/a",
                    note=note + t(lang, " (data unavailable)", " (data niet beschikbaar)"),
                )
            )
            continue
        price, ma50, ma200, r, dd = metrics
        rows.append(
            Row(
                ticker=ticker,
                tier=meta["tier"],
                price=price,
                ma50=ma50,
                ma200=ma200,
                rsi14=r,
                drawdown_52w=dd,
                signal=buy_signal(meta["tier"], price, ma50, ma200, r),
                phase=narrative_phase(price, ma50, ma200, r),
                size_hint=size_hint(meta["tier"], dd, r),
                note=note,
            )
        )
    if news:
        for r in rows:
            if r.ticker in VIRAL_EXTRA:
                r.note += t(
                    lang,
                    " | Viral watchlist name in current theme discussions",
                    " | Virale watchlist-naam in huidig thema",
                )
    return rows


def print_report(rows: List[Row], lang: str, news: bool) -> str:
    lines: List[str] = []
    title = t(lang, "Narrative Watchlist", "Narratief Watchlist")
    lines.append(f"{title} v{VERSION} — {THEME}")
    lines.append(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
    lines.append(t(lang, "Not financial advice.", "Geen financieel advies."))
    lines.append("")

    for r in rows:
        px = f"{r.price:.2f}" if not np.isnan(r.price) else "—"
        rsi_s = f"{r.rsi14:.1f}" if not np.isnan(r.rsi14) else "—"
        dd = f"{r.drawdown_52w:.1f}%" if not np.isnan(r.drawdown_52w) else "—"
        lines.append(
            f"{tier_emoji(r.tier)} {r.ticker:6} px={px:>8} rsi={rsi_s:>5} "
            f"dd={dd:>7} sig={r.signal:10} phase={r.phase:14} size={r.size_hint}"
        )
        lines.append(f"         {r.note}")

    lines.append("")
    lines.append(t(lang, "Historical lessons", "Historische lessen") + ":")
    for h in HISTORY_NL if lang == "nl" else HISTORY_EN:
        lines.append(f"  • {h}")
    lines.append("")
    lines.append(t(lang, "Scenarios", "Scenario's") + ":")
    for a, b in SCENARIOS_NL if lang == "nl" else SCENARIOS_EN:
        lines.append(f"  • {a}: {b}")
    if news:
        lines.append("")
        lines.append(
            t(
                lang,
                "News mode: highlighted viral theme names (static seed list; extend with live feeds later).",
                "News-modus: virale thema-namen gemarkeerd (statische seed; later live feeds).",
            )
        )

    text = "\n".join(lines)
    if console:
        table = Table(title=title)
        table.add_column("T")
        table.add_column("Ticker")
        table.add_column("Price", justify="right")
        table.add_column("RSI", justify="right")
        table.add_column("DD52w", justify="right")
        table.add_column("Signal")
        table.add_column("Phase")
        table.add_column("Size")
        for r in rows:
            table.add_row(
                tier_emoji(r.tier),
                r.ticker,
                f"{r.price:.2f}" if not np.isnan(r.price) else "—",
                f"{r.rsi14:.1f}" if not np.isnan(r.rsi14) else "—",
                f"{r.drawdown_52w:.1f}%" if not np.isnan(r.drawdown_52w) else "—",
                r.signal,
                r.phase,
                r.size_hint,
            )
        console.print(table)
        console.print(text)
    else:
        print(text)
    return text


def export_csv(rows: List[Row], path: Optional[Path] = None) -> Path:
    out_dir = Path("exports")
    out_dir.mkdir(exist_ok=True)
    path = path or out_dir / f"narrative_watch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()) if rows else ["ticker"])
        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))
    return path


def send_email(body: str, subject: str) -> bool:
    host = os.getenv("SMTP_HOST")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    to_addr = os.getenv("SMTP_TO") or user
    from_addr = os.getenv("SMTP_FROM") or user
    port = int(os.getenv("SMTP_PORT") or "587")
    if not all([host, user, password, to_addr]):
        print("Email skipped: configure SMTP_* in .env", file=sys.stderr)
        return False
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(user, password)
        smtp.send_message(msg)
    return True


def run_once(args: argparse.Namespace) -> str:
    rows = analyze(lang=args.lang, news=args.news)
    text = print_report(rows, args.lang, args.news)
    if args.export:
        path = export_csv(rows)
        print(f"Exported: {path}")
    if args.email:
        ok = send_email(text, f"Narrative Watchlist v{VERSION}")
        print("Email sent" if ok else "Email not sent")
    return text


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Narrative Watchlist v5 — thematic stock tracker")
    parser.add_argument("--lang", choices=["en", "nl"], default="en")
    parser.add_argument("--export", action="store_true", help="Write CSV snapshot to exports/")
    parser.add_argument("--email", action="store_true", help="Send SMTP summary using .env")
    parser.add_argument("--news", action="store_true", help="Annotate viral theme names")
    parser.add_argument("--refresh", type=int, default=0, metavar="SEC", help="Daemon refresh interval")
    args = parser.parse_args(argv)

    if yf is None:
        print("Install dependencies: pip install -r requirements.txt", file=sys.stderr)
        return 1

    if args.refresh and args.refresh > 0:
        while True:
            run_once(args)
            print(f"Sleeping {args.refresh}s …")
            time.sleep(args.refresh)
    else:
        run_once(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
