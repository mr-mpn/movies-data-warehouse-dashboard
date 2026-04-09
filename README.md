# Data Warehouse Project

## Step 1: Launch the DB

```bash
cd ./db/postgres;
docker-compose up -d;
cd ../..;
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

## Step 4: First ETL (Raw -> Bronze)

```bash
python Bronze-ETL/main.py
```

## Step 5: Second ETL (Bronze -> Silver)

```bash
python Silver-ETL/main.py
```


## Step 6: Start MongoDb which is used to authenticate users 

```bash
cd ./db/mongo;
docker-compose up -d;
cd ../..;
```

## Step 7: Launch the backend 

```bash
uvicorn Dashboard.Backend.main:app --reload
```

## Step 8: Launch the frontend

```bash
cd Dashboard/Frontend;
npm install;
npm run dev;
```
