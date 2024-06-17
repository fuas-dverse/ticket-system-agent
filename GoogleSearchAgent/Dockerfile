FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

ENV NAME GoogleSearchAgent

# Run your app.py script as entrypoint
CMD [ "python3", "app.py"]