from fastapi import FastAPI
from routes import auth_routes, agent_routes

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(agent_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
