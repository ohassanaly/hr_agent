FROM ghcr.io/astral-sh/uv:python3.13-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:${PATH}"

COPY . .

CMD ["bash", "-lc", "uv run streamlit run hr_agent/ui.py --server.port=${PORT:-8080}  --server.address=0.0.0.0 --server.headless=true"]