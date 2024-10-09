FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /root_dir

COPY dataset/ /root_dir/dataset/
COPY .env /root_dir/
COPY requirements.txt /root_dir/
RUN pip install --no-cache-dir -r /root_dir/requirements.txt

COPY . /root_dir/

CMD ["streamlit", "run", "/root_dir/personalized_recipe_generator.py"]