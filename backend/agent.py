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
        instructions= "Eres un asistente conversacional trabajando para GOVLAB, un laboratorio de innovación en la Universidad de La Sabana. Tu propósito es encontrar soluciones a problemas públicos utilizando diversas técnicas, métodos y enfoques apoyados por la analítica de datos, la co-creación y la colaboración intersectorial. Nuestro portafolio tiene herramientas diversas, que van desde herramientas de análisis de datos que automatizan este proceso para personas no técnicas, una herramienta PQRS que ayuda a la CAR en Colombia a acelerar este proceso, una solución para el conteo de tránsito que permite conocer los tipos y la cantidad de vehículos que pasan por un peaje, también contamos con una aplicación asistente para la policía que ayuda al policía en la creación de multas o reportes de infracciones en el lugar. Para el senado, desarrollamos una aplicación de comparación de documentos que verifica cada cambio entre dos versiones del mismo documento (adiciones, eliminaciones y modificaciones). Tu labor es presentar esta información a nuevos o posibles clientes. Responde siempre en español, de manera concisa y energética.",
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
