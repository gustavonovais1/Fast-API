from fastapi import FastAPI, HTTPException, status, Response, Path, Query, Header, Depends
from typing import Optional, Any, List, Dict
from models import Curso, cursos
from time import sleep

def fake_db():
    try:
        print('Abrindo conexão com o banco de dados...')
        sleep(1)
    finally:
        print('Fechando onexão com o banco de dados...')
        sleep(1)

app = FastAPI(title='Api exemplo', version="0.0.1", description="Uma api de estudo do fasapi")



@app.get('/cursos', 
        description="Retorna todos os cursos ou uma lista vazia.",
        response_description="Cursos encontrados com sucesso.",
        summary="Retorna todos os cursos",
        response_model=List[Curso])

async def get_cursos(db: Any = Depends(fake_db)):
    return cursos

# Exemplo de Path parameters
@app.get('/cursos/{curso_id}')
async def get_curso(curso_id: int = Path(title="ID do curso", description="Deve ser entre 1 e 2", gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado.")

# Exemplo de Injeção de Dependências
@app.post('/cursos', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Curso):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso

@app.put("/cursos/{curso_id}")
async def put_cursos(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um curso com o ID {curso_id}")

@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe um curso com o ID {curso_id}")

# Exemplo de Query e Header parameters
@app.get('/calculadora')
async def calculadora(a: int = Query(default=None, gt=5), b: int = Query(default=None, gt=10), x_header:set = Header(default=None, ), c: Optional[int] = None ):
    soma: int = a+b
    if c:
        soma+= + c
    print(f"X-HEADER:{x_header}")
    
    return {"Resultado":soma}

if __name__=='__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="info", reload=True)