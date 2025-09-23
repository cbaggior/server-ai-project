from fastapi import FastAPI, Depends
from app.db import Base, engine
from app.routes import users, ai, auth
from app.deps import get_current_user

# Cria as tabelas no startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Backend AI Project", version="1.1.0")

app.include_router(users.router)
app.include_router(ai.router)
app.include_router(auth.router)

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}

@app.get("/me", tags=["user"], dependencies=[Depends(get_current_user)])
def me(current=Depends(get_current_user)):
    return {"msg": "rota protegida", "user": current}
