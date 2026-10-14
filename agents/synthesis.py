"""Fase de síntesis: combina los aportes de los especialistas en la respuesta final."""

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage

from llm import texto
from state import AgentState


def crear_nodo_sintesis(llm: BaseChatModel):
    async def nodo_sintesis(state: AgentState) -> dict:
        pregunta_original = texto(state["messages"][0])
        aportes = "\n\n".join(f"- [{c['agente']}] {c['aporte']}" for c in state.get("contribuciones", []))

        prompt = (
            f"Pregunta original: {pregunta_original}\n\n"
            f"Aportes del equipo:\n{aportes}\n\n"
            "Redactá una respuesta final clara y breve en español combinando estos aportes. "
            "Usá solo la información de los aportes; no agregues datos nuevos. "
            "Mencioná la fuente de la documentación."
        )
        respuesta = await llm.ainvoke([HumanMessage(content=prompt)])

        return {
            "messages": [AIMessage(content=texto(respuesta), name="sintesis")],
            "task_completed": True,
        }

    return nodo_sintesis
