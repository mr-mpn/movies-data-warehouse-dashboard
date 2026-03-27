# Data Warehouse Project

## Step 1: Launch the DB

```bash
cd ./db
docker-compose up -d
cd ..
```

## Step 2: Download dependencies and install them

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Step 3: Launch the DMS to read the dataset and write it to the DB

```bash
python Source-DMS/main.py
```
