"""Esquema del estado compartido entre el supervisor y los especialistas."""

import operator
from typing import Annotated, Optional, TypedDict

from langgraph.graph import MessagesState


class Contribucion(TypedDict):
    """Registro de un aporte: quién lo hizo, qué se le pidió y qué devolvió."""

    agente: str        # "investigador" o "analista"
    instruccion: str   # la tarea puntual que le asignó el supervisor
    aporte: str        # el resultado del especialista
    paso: int          # en qué intervención ocurrió (1, 2, 3...)


class AgentState(MessagesState):
    """Hereda 'messages' (con su reducer add_messages) y suma campos propios.

    - next_agent: decisión del supervisor (a quién delega o FINISH).
    - instruccion: tarea concreta para el próximo especialista. Los especialistas
      reciben solo esto (más el contexto necesario), no todo el historial.
    - contribuciones: usa operator.add como reducer, así cada nodo SUMA su aporte
      a la lista en lugar de pisarla. Queda registrado quién aportó qué.
    - pasos: contador de intervenciones de especialistas (condición de parada).
    - task_completed: se marca en True cuando termina la síntesis.
    """

    next_agent: Optional[str]
    instruccion: str
    contribuciones: Annotated[list[Contribucion], operator.add]
    pasos: int
    task_completed: bool
