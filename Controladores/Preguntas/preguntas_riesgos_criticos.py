# Diccionarios de preguntas
PREGUNTAS_RC_SUP = {
    "RC01": [
        {"codigo": "RC01-01", "pregunta": "Eléctrico: ¿La identificación y señalización de los puntos para el corte de energía está de acuerdo a lo definido en el procedimiento?"},
        {"codigo": "RC01-02", "pregunta": "Eléctrico: ¿El equipo de trabajo cuenta con las tarjetas y candados personales para realizar el bloqueo?"},
        {"codigo": "RC01-03", "pregunta": "Eléctrico: ¿Los equipos utilizados para la verificación de energía cero están certificados por el proveedor y tienen su revisión al día?"},
        {"codigo": "RC01-04", "pregunta": "¿Los tableros eléctricos portátiles y herramientas eléctricas se encuentran con sus mantenciones de acuerdo al programa?"},
        {"codigo": "RC01-05", "pregunta": "Eléctrico: ¿Las protecciones de los equipos a intervenir se encuentran con sus mantenciones al día?"}
    ],
    "RC02": [
        {"codigo": "RC02-01", "pregunta": "¿Verifiqué que la plataforma fija temporal se encuentra autorizada por personal competente?"},
        {"codigo": "RC02-02", "pregunta": "¿Verifiqué que se cumple con el programa de mantenimiento e inspección de las plataformas móviles?"}
    ],
    # Agrega aquí todas las preguntas para los 28 Riesgos Críticos
}

PREGUNTAS_TR = {
    "RC01": [
        {"codigo": "RC01-01", "pregunta": "¿Identifiqué el equipo y los puntos para el corte de energía (Aislación y bloqueo)?"},
        {"codigo": "RC01-02", "pregunta": "¿Instalé bloqueo con tarjeta(s) y candado(s) personal en el o los puntos y equipos correspondientes?"},
        {"codigo": "RC01-03", "pregunta": "¿Realicé y/o participé en las pruebas de verificación de ausencia de tensión y verifiqué la puesta a tierra antes de iniciar el trabajo?"},
        {"codigo": "RC01-04", "pregunta": "¿Verifiqué según check list que no existe fuga a tierra en las herramientas eléctricas antes de iniciar el trabajo?"},
        {"codigo": "RC01-05", "pregunta": "¿Identifiqué las protecciones a equipos de inversión y están operativas?"}
            ],
    "RC02": [
        {"codigo": "RC02-01", "pregunta": "¿Verifiqué que la plataforma fija temporal se encuentra autorizada por personal competente?"},
        {"codigo": "RC02-02", "pregunta": "¿Verifiqué que se cumple con el programa de mantenimiento e inspección de las plataformas móviles?"}
    ],
    # Agrega aquí todas las preguntas para los 28 Riesgos Críticos
}

def obtener_preguntas_sup_por_codigo(rc_codigo):
    # Obtener los primeros 4 caracteres del código RC
    rc_codigo_base = rc_codigo[:4]
    return PREGUNTAS_RC_SUP.get(rc_codigo_base, [])

def obtener_preguntas_tr_por_codigo(rc_codigo):
    # Obtener los primeros 4 caracteres del código RC
    rc_codigo_base = rc_codigo[:4]
    return PREGUNTAS_TR.get(rc_codigo_base, [])