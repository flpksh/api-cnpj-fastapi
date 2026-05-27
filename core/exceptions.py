class EmpresaNaoEncontrada(Exception):

    def __init__(
        self,
        mensagem: str = "Empresa não encontrada"
    ):
        self.mensagem = mensagem


class UsuarioNaoEncontrado(Exception):

    def __init__(
        self,
        mensagem: str = "Usuário não encontrado"
    ):
        self.mensagem = mensagem


class CredenciaisInvalidas(Exception):

    def __init__(
        self,
        mensagem: str = "Usuário ou senha inválidos"
    ):
        self.mensagem = mensagem

class UsuarioJaExiste(Exception):

    def __init__(
        self,
        mensagem: str = "Usuário já existe"
    ):
        self.mensagem = mensagem
