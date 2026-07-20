from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import (
    CredenciaisInvalidas,
    EmpresaNaoEncontrada,
    UsuarioJaExiste,
    UsuarioNaoEncontrado,
)
from routes.auth import router as auth_router
from routes.empresas import router as empresas_router

app = FastAPI()


@app.exception_handler(EmpresaNaoEncontrada)
async def empresa_nao_encontrada_handler(request: Request, exc: EmpresaNaoEncontrada):

    return JSONResponse(
        status_code=404,
        content={"success": False, "message": exc.mensagem, "data": None},
    )


@app.exception_handler(UsuarioNaoEncontrado)
async def usuario_nao_encontrado_handler(request: Request, exc: UsuarioNaoEncontrado):

    return JSONResponse(
        status_code=404,
        content={"success": False, "message": exc.mensagem, "data": None},
    )


@app.exception_handler(CredenciaisInvalidas)
async def credenciais_handler(request: Request, exc: CredenciaisInvalidas):

    return JSONResponse(
        status_code=401,
        content={"success": False, "message": exc.mensagem, "data": None},
    )


app.include_router(auth_router)
app.include_router(empresas_router)


@app.get("/")
def home():
    return {"mensagem": "API rodando"}


@app.exception_handler(UsuarioJaExiste)
async def usuario_ja_existe_handler(request: Request, exc: UsuarioJaExiste):

    return JSONResponse(
        status_code=409,
        content={"success": False, "message": exc.mensagem, "data": None},
    )
