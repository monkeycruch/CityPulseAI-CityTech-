from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import pandas as pd
import os

DATA_PATH = os.environ.get('DATA_PATH', 'citypulse_real_311_scored.csv')
if not os.path.exists(DATA_PATH):
    print(f"Warning: {DATA_PATH} not found. Attempting to start with empty data.")
    df = pd.DataFrame(columns=['unique_key','complaint_type','borough','latitude','longitude',
        'priority_score','priority_tier','severity','weather','impact',
        'complaints','accessibility'])
else:
    df = pd.read_csv(DATA_PATH)

cols = ['unique_key','complaint_type','borough','latitude','longitude',
        'priority_score','priority_tier','severity','weather','impact',
        'complaints','accessibility']
df = df[cols].copy()
df = df.rename(columns={
    'unique_key':'id','complaint_type':'complaint',
    'latitude':'lat','longitude':'lon',
    'priority_score':'score','priority_tier':'tier'
})
for col in ['lat','lon','score','severity','weather','impact','complaints','accessibility']:
    df[col] = df[col].round(2)
INCIDENTS = df.to_dict(orient='records')
print(f'Loaded {len(INCIDENTS)} incidents')

app = FastAPI(title='CityPulse AI')
app.add_middleware(CORSMiddleware, allow_origins=['*'],
    allow_credentials=False, allow_methods=['*'], allow_headers=['*'])

@app.get('/api/health')
async def health():
    return {'status': 'ok', 'total': len(INCIDENTS)}

@app.get('/api/stats')
async def stats(borough: Optional[str] = None):
    data = [i for i in INCIDENTS if not borough or i['borough']==borough]
    return {'critical': sum(1 for i in data if i['tier']=='Critical'),
            'high': sum(1 for i in data if i['tier']=='High'),
            'medium': sum(1 for i in data if i['tier']=='Medium'),
            'low': sum(1 for i in data if i['tier']=='Low'),
            'total': len(data)}

@app.get('/api/incidents')
async def get_incidents(tier: Optional[str]=None, borough: Optional[str]=None, limit: int=10000):
    data = INCIDENTS
    if tier: data = [i for i in data if i['tier']==tier]
    if borough: data = [i for i in data if i['borough']==borough]
    return sorted(data, key=lambda x: x['score'], reverse=True)[:limit]

@app.get('/api/top')
async def top(n: int=20, borough: Optional[str]=None):
    data = [i for i in INCIDENTS if not borough or i['borough']==borough]
    return sorted(data, key=lambda x: x['score'], reverse=True)[:n]
