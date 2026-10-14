"""Configuración compartida.

Las constantes del RAG son las mismas de la Pre-entrega 4, para conectarse
al índice que ya existe en Pinecone sin volver a crearlo.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# --- LLM (Gemini, como en el notebook de ejemplo) ---
LLM_MODEL = os.getenv("LLM_MODEL") or "gemini-3.5-flash"  # `or` cubre LLM_MODEL= vacío en el .env

# --- RAG de la Pre-entrega 4 ---
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
INDEX_NAME = os.getenv("INDEX_NAME", "fastapi-docs-rag")
NAMESPACE = "fastapi-docs"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNKS_PATH = "chunks.json"  # copiado de la Pre-entrega 4 (BM25 corre en memoria)
TOP_K = 5

# --- Orquestador ---
MAX_PASOS = 6          # máximo de intervenciones de especialistas (evita el "Supervisor Infinito")
RECURSION_LIMIT = 25   # techo de pasos del grafo completo
