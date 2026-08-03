import re

FORMATO_CNPJ = re.compile(r"[A-Z0-9]{12}[0-9]{2}")
PESOS_PRIMEIRO_DV = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
PESOS_SEGUNDO_DV = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
CARACTERES_FORMATACAO = str.maketrans("", "", "./-")


def normalizar_cnpj(valor: str) -> str:
    return valor.strip().upper().translate(CARACTERES_FORMATACAO)


def _valor_para_calculo(caractere: str) -> int:
    return ord(caractere) - ord("0")


def _calcular_digito(base: str, pesos: tuple[int, ...]) -> str:
    soma = sum(
        _valor_para_calculo(caractere) * peso
        for caractere, peso in zip(base, pesos, strict=True)
    )
    resto = soma % 11
    return "0" if resto < 2 else str(11 - resto)


def calcular_digitos_verificadores(base: str) -> str:
    primeiro_digito = _calcular_digito(base, PESOS_PRIMEIRO_DV)
    segundo_digito = _calcular_digito(
        base + primeiro_digito,
        PESOS_SEGUNDO_DV,
    )
    return primeiro_digito + segundo_digito


def validar_cnpj(valor: object) -> str:
    if not isinstance(valor, str):
        raise ValueError("CNPJ deve ser informado como texto")

    cnpj = normalizar_cnpj(valor)

    if not FORMATO_CNPJ.fullmatch(cnpj):
        raise ValueError(
            "CNPJ deve conter 12 caracteres alfanuméricos e 2 dígitos verificadores"
        )

    if cnpj.isdigit() and len(set(cnpj)) == 1:
        raise ValueError("CNPJ inválido")

    if cnpj[-2:] != calcular_digitos_verificadores(cnpj[:12]):
        raise ValueError("CNPJ inválido")

    return cnpj
