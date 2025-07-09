import time
CINZA = (169, 169, 169)

ultimo_tempo = 0
delay = 1.0  # segundos

def agir_sensor(plantas):
    global ultimo_tempo
    agora = time.time()
    if agora - ultimo_tempo < delay:
        return "Aguardando leitura..."

    # Coleta informações detalhadas sobre as plantas
    info = [(i, round(p.maturidade, 1), round(p.agua, 1), p.coletada, p.morta)
            for i, p in enumerate(plantas)]
    
    # Identifica plantas críticas (pouca água)
    criticas = [i for i, m, a, c, mto in info if a < 20 and not c and not mto]
    
    # Conta plantas por estado
    total_plantas = len(plantas)
    plantas_vivas = sum(1 for p in plantas if not p.morta and not p.coletada)
    plantas_coletadas = sum(1 for p in plantas if p.coletada)
    plantas_mortas = sum(1 for p in plantas if p.morta)
    
    # Calcula médias
    if plantas_vivas > 0:
        agua_media = sum(p.agua for p in plantas if not p.morta and not p.coletada) / plantas_vivas
        maturidade_media = sum(p.maturidade for p in plantas if not p.morta and not p.coletada) / plantas_vivas
    else:
        agua_media = maturidade_media = 0
    
    ultimo_tempo = agora
    
    # Retorna um dicionário com todas as informações
    return {
        'plantas_criticas': criticas,
        'total_plantas': total_plantas,
        'plantas_vivas': plantas_vivas,
        'plantas_coletadas': plantas_coletadas,
        'plantas_mortas': plantas_mortas,
        'agua_media': agua_media,
        'maturidade_media': maturidade_media,
        'timestamp': agora
    }