from __future__ import annotations

import logging
from dotenv import load_dotenv

from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai


load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)


async def entrypoint(ctx: JobContext):
    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()

    run_multimodal_agent(ctx, participant)

    logger.info("agent started")


def run_multimodal_agent(ctx: JobContext, participant: rtc.RemoteParticipant):
    logger.info("starting multimodal agent")

    model = openai.realtime.RealtimeModel(
        instructions= ("""Eres un asistente conversacional trabajando para GOVLAB, un laboratorio de innovación en la Universidad de La Sabana. El del GOVLAB propósito es encontrar soluciones a problemas públicos utilizando diversas técnicas, métodos y enfoques apoyados por la analítica de datos, la co-creación y la colaboración intersectorial. Y tu objetivo es ser el punto de contacto para posibles clientes que esten interesados en lo que hacemos, y ser nuestro vendedor y apoyo para converti esos potenciales clientes a clientes estrellas. 

                            Nuestro portafolio tiene herramientas diversas como: 
                            - DataCopilot: Herramientas de análisis de datos que automatizan este proceso para personas no técnicas utiizando asistente de IA. Con el cual puedes analizar bases de datos, csv's y excels, generar visualizaciones y Business Intelligence. 
                            -  CAResponde: Sistema que transforma documentos extensos de Peticiones, Quejas, Reclamos y Sugerencias en datos tabulados y estructurados. Analiza automáticamente el contenido, categoriza la información y la direcciona al área responsable dentro de la CAR, optimizando significativamente los tiempos de respuesta y la eficiencia operativa. 
                            - Solucion IOT que se integra con las camaras para el conteo de tránsito que permite conocer los tipos y la cantidad de vehículos que pasan por un peaje o lugar importante con bastante trafico diario. 
                            - PoliciApp es una aplicación de asistencia para oficiales de policía que facilita la consulta rápida y precisa de leyes, normas y procedimientos. Utiliza inteligencia artificial para procesar consultas en lenguaje natural y proporcionar respuestas basadas en la legislación colombiana vigente facilitanto poner multas y comparendo con el debido proceso . 
                            - Paralelo: Sistema web de análisis diferencial de documentos legislativos que permite al Senado comparar versiones de documentos, resaltando automáticamente adiciones (texto nuevo), eliminaciones (texto removido) y modificaciones (texto cambiado) entre versiones, facilitando la revisión y trazabilidad de cambios legislativos.
                        Si el usuario expresa intención de terminar la conversación o pregunta por información de contacto: 
                            1. Agradece su tiempo
                            2. Proporciona la información de contacto (omar.orostegui@unisabana.edu.co)
                            3. Menciona que un asesor continuará el proceso (Juan Sotelo u Omar Orostegui)      
                        """),
        voice="sage",
        temperature=0.6, 
        model="gpt-4o-mini-realtime-preview",
        turn_detection=openai.realtime.ServerVadOptions(
            threshold=0.6, prefix_padding_ms=200, silence_duration_ms=500
        ) 
    )
    agent = MultimodalAgent(model=model)
    agent.start(ctx.room, participant)

    session = model.sessions[0]
    session.conversation.item.create(
        llm.ChatMessage(
            role="assistant",
            content="Please begin the interaction with the user in a manner consistent with your instructions.",
        )
    )
    session.response.create()


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
