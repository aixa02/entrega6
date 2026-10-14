"""Grafo principal: topología jerárquica con Supervisor."""

from typing import Literal

from langchain_core.language_models import BaseChatModel
from langchain_google_genai.chat_models import GoogleAPIError
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import RetryPolicy

from agents import crear_nodo_analista, crear_nodo_investigador, crear_nodo_sintesis, crear_nodo_supervisor
from state import AgentState

# Reintenta un nodo solo ante errores del servidor de Gemini (500/503, "high demand"),
# esperando 5s, 10s, 20s... No reintenta el 429 de cuota diaria: eso no se arregla esperando.
REINTENTOS = RetryPolicy(max_attempts=4, initial_interval=5.0, retry_on=GoogleAPIError)


def enrutar(state: AgentState) -> Literal["investigador", "analista", "sintesis"]:
    """Traduce la decisión del supervisor al nombre del nodo siguiente.

    El Literal del retorno le dice a LangGraph cuáles son los destinos posibles.
    """
    if state["next_agent"] == "FINISH":
        return "sintesis"
    return state["next_agent"]


def construir_grafo(llm: BaseChatModel) -> CompiledStateGraph:
    grafo = StateGraph(AgentState)

    grafo.add_node("supervisor", crear_nodo_supervisor(llm), retry_policy=REINTENTOS)
    grafo.add_node("investigador", crear_nodo_investigador(llm), retry_policy=REINTENTOS)
    grafo.add_node("analista", crear_nodo_analista(llm), retry_policy=REINTENTOS)
    grafo.add_node("sintesis", crear_nodo_sintesis(llm), retry_policy=REINTENTOS)

    grafo.add_edge(START, "supervisor")
    grafo.add_conditional_edges("supervisor", enrutar)
    # Los especialistas siempre vuelven al supervisor: él valida y decide el próximo paso.
    grafo.add_edge("investigador", "supervisor")
    grafo.add_edge("analista", "supervisor")
    grafo.add_edge("sintesis", END)

    return grafo.compile()
