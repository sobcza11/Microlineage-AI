FROM python:3.11-slim
WORKDIR /app

# Dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# 🔧 Generate data at build time so the dashboard has files ready
RUN python _supporting/data/make_sku_forecast.py \
 && python _supporting/models/optimize_prices.py \
 && python _supporting/reports/sanity_check.py

EXPOSE 8501
CMD ["streamlit","run","_supporting/dashboard/forecast_dashboard.py","--server.port=8501","--server.address=0.0.0.0"]
