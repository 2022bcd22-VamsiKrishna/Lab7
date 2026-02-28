FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
# IMPORTANT: The pipeline puts model.pkl in output/model, we copy it to root
COPY output/model/model.pkl . 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]