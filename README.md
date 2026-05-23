# Narrative Watchlist v5 🚀

**Multilingual Narrative Shift Tracking & Intelligent Stock Watchlist Tool**  
**Meertalige Narratief-Shift Tracking & Intelligente Aandelen Watchlist Tool**

> **Current Version: 5.1.0** — "Viral Discovery & Narrative Intelligence Edition"  
> Built from deep research into efficient AI architectures (HRM-Text, Samsung TRM, Cerebras, etc.), historical market narrative shifts, and practical needs for disciplined investors/researchers.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Autonomous](https://img.shields.io/badge/Autonomous%20Mode-Active-brightgreen)]()

---

## 🇬🇧 English | 🇳🇱 Nederlands

---

## What is this tool?

**Narrative Watchlist** is a powerful, extensible command-line tool designed to help you track stocks **during major narrative shifts** in technology and markets.

It goes far beyond simple price tracking. It combines:

- Real-time stock data + advanced technical filters
- **Thematic narrative analysis** (how the current story affects each company)
- Automatic discovery of relevant tickers from viral discussions and news
- Historical lessons from past shifts (DeepSeek, Mamba hype, post-IPO behavior)
- Risk management and intelligent position sizing
- Optional viral news impact analysis
- Email alerts, automatic refresh, CSV export, and full bilingual support

**Current primary theme**: Efficient AI architectures + the inference boom (HRM-Text, TRM, Cerebras wafer-scale inference, specialized chips, etc.)

The tool is built to be **generalizable** — it can be adapted to future narrative shifts (energy, biotech, robotics, data center infrastructure, etc.).

---

## 🚀 Everything This Tool Can Do (Complete Feature List)

This is a **complete overview** of all capabilities as of v5.1.0:

### Core Analysis Features
- **Thematic Color Coding** (`🟢` / `🟡` / `🔴`) based on how well each stock is positioned for the current narrative
- **Multi-condition Buy Signals** — Combines thematic color + price above MA50 + MA200 + RSI filter for higher quality signals
- **Risk-Adjusted Position Sizing** — Automatically suggests smaller positions for high-drawdown or volatile names (especially new IPOs like CBRS)
- **52-Week Drawdown Tracking** — Shows how far each stock is from its peak (critical during narrative volatility)
- **RSI (14) Filter** — Prevents buying into extreme euphoria
- **Narrative Phase Detection** — Detects whether we are in "Hype", "Dip/Fear", "Recovery", or "Consolidation" phase
- **Per-Ticker Narrative Impact** — Clear explanation of why each stock profits or suffers from the current narrative

### Viral & News Intelligence
- **Viral Ticker Discovery** — Automatically surfaces relevant tickers frequently mentioned in current viral discussions and news (e.g. CRDO, MU, AMKR, ALAB, SMCI)
- **News Impact Module** (`--news`) — Maps latest viral X/posts and news to "Who wins" vs "Who loses" per ticker
- **Sentiment-aware context** for the current theme

### Historical Context & Education
- **Historical Lessons Module** — Built-in knowledge from DeepSeek R1 release, Mamba hype cycle, post-IPO drawdowns of specialized chip companies, and NVIDIA’s resilience through multiple narrative attacks
- **Scenario Table** — What-if analysis (e.g. “What if training capex drops 40%?” or “What if inference demand explodes 3x?”)

### Automation & Alerts
- **Email Alerts** (`--email`) — Send professional summaries via SMTP (supports Gmail app passwords)
- **Automatic Refresh / Daemon Mode** (`--refresh X`) — Run continuously and refresh every X seconds
- **CSV Export** (`--export`) — Full snapshot with timestamp for historical tracking

### Usability & Professional Features
- **Fully Bilingual** (`--lang en` or `--lang nl`) — Professional output in English and Dutch
- **Clean, color-coded terminal output**
- **Extensible ticker list** — Easy to add new themes or stocks
- **Professional GitHub-ready structure** with proper versioning

### Future-Proof Design
- Designed from the ground up to handle **multiple narrative themes** in future versions
- Clean codebase ready for YAML config, web dashboard, Telegram/Discord alerts, backtesting, etc.

---

## 📦 Installation

```bash
git clone https://github.com/Stijnman/narrative-watchlist-v4.git
cd narrative-watchlist-v4

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

For email alerts, copy and configure the environment file:

```bash
cp .env.example .env
# Edit .env with your SMTP settings (Gmail App Password recommended)
```

---

## ▶️ Usage Examples

### Basic run (English)
```bash
python narrative_watch_v4.py
```

### Dutch output
```bash
python narrative_watch_v4.py --lang nl
```

### Full power run (recommended daily)
```bash
python narrative_watch_v4.py --lang nl --export --email
```

### With viral news impact analysis
```bash
python narrative_watch_v4.py --news
```

### Automatic refresh every 5 minutes (daemon mode)
```bash
python narrative_watch_v4.py --refresh 300
```

### See all available options
```bash
python narrative_watch_v4.py --help
```

---

## 📊 Current Watchlist & Signals (v5.1.0)

The tool currently tracks the following tickers relevant to the **efficient architectures + inference boom** narrative:

**🟢 Strong / Core Positions**
- **NVDA** (NVIDIA) — Most resilient across almost every scenario
- **TSM** (TSMC) — Quiet but powerful winner (manufactures chips for almost everyone)
- **CBRS** (Cerebras) — Purest public specialized inference play (use smaller size due to typical post-IPO volatility)

**🟡 Monitor / Viral Watchlist**
- CRDO, MU, AMKR, ALAB, SMCI, AVGO, AMD, META, ARM

**🔴 Lower Priority (higher capex risk)**
- MSFT, GOOGL, AMZN

Run the script to see live prices, signals, drawdowns, and narrative impact.

---

## 🔮 Predictions & Long-Term View (2026-2027)

Based on the full conversation and historical patterns:

1. Inference infrastructure and specialized hardware will be major winners.
2. NVDA remains dominant but will face repeated narrative attacks — usage growth usually wins in the end.
3. New efficient model players (Sapient, Samsung TRM derivatives, etc.) will likely be acquired or IPO within 18-24 months.
4. Hyperscaler training capex will come under increasing scrutiny.
5. Post-IPO drawdowns of 40-70% are normal for specialized chip companies — position sizing matters.
6. The shift from “train one giant model” to “run thousands of efficient ones” is real and accelerating.

This tool helps you stay disciplined and emotionally detached during these shifts.

---

## 📁 Project Structure

```
narrative-watchlist-v4/
├── narrative_watch_v4.py      # Main script (v5.1.0)
├── README.md                  # This comprehensive documentation
├── requirements.txt
├── .env.example               # Template for email configuration
├── .gitignore
├── LICENSE
└── exports/                   # CSV snapshots (gitignored)
```

---

## 🛠️ Version History

- **v5.1.0** — Viral Discovery & Narrative Intelligence Edition (added CRDO, MU, AMKR, ALAB, SMCI + per-ticker narrative impact)
- **v5.0.0** — Batch Implementation Edition (started systematic rollout of 23+ improvements)
- **v4.0.0** — Full professional version with email, auto-refresh, multilingual, historical lessons, risk management

---

## ⚠️ Important Disclaimer

This tool provides **thematic analysis and educational tooling only**.  
It is **not financial advice**.  

Markets are volatile. Narrative shifts create both opportunity and risk. Always do your own research and consider your personal risk tolerance.

Past performance and historical analogues (DeepSeek, Mamba, etc.) do not guarantee future results.

---

## 🤝 Contributing

Pull requests and ideas are welcome, especially for:
- Additional language support
- New narrative themes
- Better technical indicators
- Web dashboard / visualization improvements

---

**Built with care for researchers and disciplined market participants.**

*This project evolved from an in-depth conversation about the financial implications of efficient AI architectures (HRM-Text), under-the-radar inference plays, and the need for practical, historically-informed tooling.*

**Version 5.1.0 — May 2026**