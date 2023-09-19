import sys # for local
sys.path.append('.') #for local

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from api.routers import router, router2 # Import routers


app = FastAPI(title="LEDGER° API") # Initialize the Flask application
app.include_router(router) # Include the routers in the app
app.include_router(router2) # Include the routers in the app
# and enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/') # Index Route
def root():

    data = {
        "Message": "Connected to LEDGER API",
        "Framework": "FastApi"
    }

    return data


# Start the server when the script is run directly
if __name__ == '__main__':
    uvicorn.run(app)
    
