import uvicorn as uvicorn
from fastapi import FastAPI

from backend.auth.endpoints import user_router
from backend.note.endpoints import note_router

app = FastAPI(title='Fast web project')
app.include_router(user_router, prefix='/user', tags=['user'])
app.include_router(note_router, prefix='', tags=['note'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
