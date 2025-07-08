import time

CINZA = (169, 169, 169)
DELAY = 1.0  # segundos
MAX_CRITICAS = 5

_ultimo_tempo = 0

def agir_sensor(plantas):
    """
    Avalia o estado das plantas e retorna um alerta se houverem plantas com pouca água.

    :param plantas: Lista de objetos planta com atributos: maturidade, agua, coletada, morta.
    :return: Mensagem de status ou alerta.
    """
    global _ultimo_tempo
    agora = time.time()
    if agora - _ultimo_tempo < DELAY:
        return "Aguardando próxima leitura..."

    # Coleta as informações essenciais de cada planta
    info = [
        (i, round(p.maturidade, 1), round(p.agua, 1), p.coletada, p.morta)
        for i, p in enumerate(plantas)
    ]

    # Filtra plantas com pouca água, que não foram coletadas e não estão mortas
    criticas = [
        i for i, matur, agua, coletada, morta in info
        if agua < 20 and not coletada and not morta
    ]

    _ultimo_tempo = agora

    if criticas:
        return f"Plantas com pouca água (máx {MAX_CRITICAS}): {criticas[:MAX_CRITICAS]}"
    else:
        return "Todas as plantas estão com níveis de água aceitáveis."
