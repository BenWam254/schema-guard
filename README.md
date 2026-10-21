# schema-guard

[![CI Pipeline](https://github.com/BenWam254/schema-guard/actions/workflows/ci.yml/badge.svg)](https://github.com/BenWam254/schema-guard/actions)
[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Package Manager](https://img.shields.io/badge/managed%20by-uv-purple.svg)](https://github.com/astral-sh/uv)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An automated data contract enforcement engine and schema drift detection CLI built to validate streaming data models, detect structural breaking changes, and enforce type safety before downstream storage.

Built with **Polars** for zero-copy lazy frame schema evaluation, **Pydantic** for declarative contract defintions, and **Typer** for terminal-first developer ergonomics, `schema-guard` validates incoming parquet or JSON data payloads against defined contracts and outputs interactive executice reports.

---

## Features

- **Zero-Copy Schema Inspection:** Evaluates schema types and nullability rules directly on Polars lazy frames without loading full datasets into memory.
- **Drift Detection:** Automatically flags missing columms, unintended type conversions, extra unexpected fields, and strict nullability violations.
- **Terminal Reports:** Generates clean, color-coded CLI summary tables powered by `rich`.
- **Declarative Contracts:** JSON and YAML schema contract files powered by Pydantic schema validation.
- **CI/CD Integration:** Non-zero exit codes on contract breaches, ready for Github Actions and pipeline gating.

--- 

## Tech Stack 

- **CLI Framework:** [Typer](https://typer.tiangolo.com/)
- **Data Engine:** [Polars](https://pola.rs/)
- **Validation Engine:** [Pydantic V2](https://docs.pydantic.dev/)
- **Terminal UI:** [Rich](https://rich.readtehdocs.io/)
- **Package Manager:** [`uv`](https://guthub.com/astral-sh/uv)
- **Language:** Python 3.12+

---

## Project Structure

```text
schema-guard/
├── schema_guard/
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # Typer CLI commands & argument parser
│   ├── validator.py       # Polars schema evaluation engine
│   ├── contracts.py       # Pydantic data contract models
│   └── reporter.py        # Rich terminal formatting & summaries
├── contracts/             # Sample schema contract definitions
├── tests/                 # Pytest test suite for drift rules
├── pyproject.toml         # Dependency configurations (uv)
├── .env.example           # Environment template
├── .gitignore             # Git ignore configurations
├── CHANGELOG.md           # Version release history
└── README.md              # Documentation
```

## Getting Started

1. #### Prerequisites
Ensure you have `Python 3.12+` and uv installed on your machine.

If you don't have `uv` installed, run:

```bash
# macOS/linux
curl -LsSf [htpps://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh

# Windows (Powershell)
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

2. #### Clone the Repository

```bash
git clone [https://github.com/BenWam254/schema-guard.git](https://github.com/BenWam254/schema-guard.git)
```

3. #### Environment Setup
Create an `.env` file in the root directory:

```bash
cp. .env.example .env
```

4. #### Install Dependencies
Install dependencies into an isolated virtual environment using `uv`:

```bash
uv sync
```

5. #### Usage

#### Validate a Dataset Against a Contract
Run the CLI validator against a target Parquet to JSON file using a defined schema contract:

```bash
uv run schema-guard validate --contract contracts/events_v1.json --data data/sample_stream.parquet
```

#### Run Contract Tests
Execute unit tests verifying schema drift rules and breach assertions:

```bash
uv run pytest
```

### License
Distributes under the MIT License. See `LICENSE` for more information.
