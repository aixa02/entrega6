"""Demo en consola del flujo de delegación.

Uso:
    python main.py                      # consulta de ejemplo
    python main.py "tu propia consulta"
"""

import asyncio
import sys

from langchain_core.messages import HumanMessage

from config import RECURSION_LIMIT
from graph import construir_grafo
from llm import crear_llm, texto

CONSULTA_EJEMPLO = (
    "Según la documentación de FastAPI, ¿qué campos tiene el modelo Item del tutorial de "
    "Request Body y cuáles son obligatorios? Con ese esquema, validá si estos JSON serían "
    'aceptados: {"name": "Teclado", "price": 45.2} y {"description": "Sin nombre", "price": "barato"}.'
)

ICONOS = {"supervisor": "🧭", "investigador": "🔎", "analista": "🧪", "sintesis": "✅"}


def estado_inicial(consulta: str) -> dict:
    return {
        "messages": [HumanMessage(content=consulta)],
        "next_agent": None,
        "instruccion": "",
        "contribuciones": [],
        "pasos": 0,
        "task_completed": False,
    }


async def ejecutar(consulta: str) -> list[dict]:
    app = construir_grafo(crear_llm())
    print(f"🧑 Consulta: {consulta}\n")
    print("🎬 Flujo de delegación:\n")

    contribuciones: list[dict] = []
    # stream_mode="updates": después de cada nodo devuelve solo lo que ese nodo cambió.
    async for evento in app.astream(
        estado_inicial(consulta), {"recursion_limit": RECURSION_LIMIT}, stream_mode="updates"
    ):
        for nodo, cambios in evento.items():
            for m in cambios.get("messages", []):
                print(f"{ICONOS[nodo]} [{nodo}]\n{texto(m)}\n")
            contribuciones += cambios.get("contribuciones", [])

    print("📋 Contribuciones registradas en el estado:")
    for c in contribuciones:
        print(f"   paso {c['paso']}: {c['agente']}")
    return contribuciones


if __name__ == "__main__":
    asyncio.run(ejecutar(sys.argv[1] if len(sys.argv) > 1 else CONSULTA_EJEMPLO))
