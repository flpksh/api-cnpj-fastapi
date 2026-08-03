import pytest

from core.cnpj import calcular_digitos_verificadores, validar_cnpj


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        ("12345678000195", "12345678000195"),
        ("12.345.678/0001-95", "12345678000195"),
        ("12ABC34501DE35", "12ABC34501DE35"),
        ("12.abc.345/01de-35", "12ABC34501DE35"),
    ],
)
def test_validar_cnpj_aceita_formatos_validos(valor: str, esperado: str) -> None:
    assert validar_cnpj(valor) == esperado


@pytest.mark.parametrize(
    "valor",
    [
        "123",
        "12ABC34501DE34",
        "12ABC34501DE3A",
        "12ABC345@1DE35",
        "12 ABC34501DE35",
        "00000000000000",
        12345678000195,
    ],
)
def test_validar_cnpj_rejeita_valores_invalidos(valor: object) -> None:
    with pytest.raises(ValueError, match="CNPJ"):
        validar_cnpj(valor)


def test_calcular_digitos_verificadores_exemplo_oficial() -> None:
    assert calcular_digitos_verificadores("12ABC34501DE") == "35"
