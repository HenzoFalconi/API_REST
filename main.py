from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional

app = FastAPI(title="API REST CRUD - Persistência em Memória")

class MovieData(BaseModel):
    searchTerm: str = Field(..., max_length=1024)
    count: int = Field(default=1, ge=1)
    poster_url: str = Field(..., max_length=1024)
    movie_id: int

    @validator("searchTerm", "poster_url")
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("Campo não pode ser vazio.")
        return v

db: List[MovieData] = []

@app.post("/movies", response_model=MovieData)
def create_movie(movie: MovieData):
    # Verifica se o movie_id já existe
    if any(m.movie_id == movie.movie_id for m in db):
        raise HTTPException(status_code=400, detail="movie_id já existe.")
    db.append(movie)
    return movie


@app.get("/movies", response_model=List[MovieData])
def list_movies():
    return db

@app.get("/movies/{movie_id}", response_model=MovieData)
def get_movie(movie_id: int):
    for movie in db:
        if movie.movie_id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Filme não encontrado.")

@app.put("/movies/{movie_id}", response_model=MovieData)
def update_movie(movie_id: int, updated: MovieData):
    for i, movie in enumerate(db):
        if movie.movie_id == movie_id:
            db[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Filme não encontrado para atualização.")

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    for i, movie in enumerate(db):
        if movie.movie_id == movie_id:
            del db[i]
            return {"message": "Filme removido com sucesso."}
    raise HTTPException(status_code=404, detail="Filme não encontrado para exclusão.")
