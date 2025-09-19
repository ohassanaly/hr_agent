# uv's official Python image (includes Python and uv)
FROM ghcr.io/astral-sh/uv:python3.11-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# Ensure the venv is on PATH for subsequent commands and at runtime
ENV PATH="/app/.venv/bin:${PATH}"

COPY about/ ./about/
COPY hr_agent/ ./hr_agent/

# Default command: run Streamlit app. Honors $PORT if set, else 8080
CMD ["uv", "run", "streamlit", "run", "hr_agent/ui.py", "--server.port=${PORT:-8080}", "--server.address=0.0.0.0", "--server.headless=true"]