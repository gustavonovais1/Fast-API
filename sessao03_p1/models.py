from typing import Optional
from pydantic import BaseModel, validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int 
    horas: int

    @validator("titulo")
    def validar_titulo(cls, value: str):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError("O titulo deve conter no minimo 3 palavras")
        
        return value
    
cursos = [
    Curso(id=1, titulo = "DevOps de infra", aulas=150, horas = 100),
    Curso(id=2, titulo = "Programação em python", aulas=100, horas = 50)
]