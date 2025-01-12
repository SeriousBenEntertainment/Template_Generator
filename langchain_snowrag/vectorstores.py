### `langchain_snowrag/vectorstores.py`
### ❄️ Template Generator
### Open-Source, hosted on https://github.com/SeriousBenEntertainment/Template_Generator
### Please reach out to ben@seriousbenentertainment.org for any questions
### Loading needed Python libraries
from __future__ import annotations
import streamlit as st
import hashlib
import json
import logging
import warnings
from typing import Any, Iterable, List, Optional, Tuple, Type
from snowflake.snowpark import Session
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from snowflake.connector import DictCursor
from snowflake.connector.connection import SnowflakeConnection
from Functions import create_session

VECTOR_LENGTH = 1024
logger = logging.getLogger(__name__)

class SnowflakeVectorStore(VectorStore):
    """Wrapper around Snowflake vector data type used as vector store."""

    def __init__(
        self,
        table: str,
        connection: Optional[SnowflakeConnection],
        embedding: Embeddings,
        vector_length: int = VECTOR_LENGTH,
    ):

        if not connection:
            connection = create_session().connection

        if not isinstance(embedding, Embeddings):
            warnings.warn("embeddings input must be Embeddings object.")

        self._connection = connection
        self._table = table
        self._embedding = embedding
        self._vector_length = vector_length

        self.create_table_if_not_exists()

    def create_table_if_not_exists(self) -> None:
        self._connection.cursor().execute(
            f"""
            CREATE TEMPORARY TABLE IF NOT EXISTS {self._table}
            (
              rowid INTEGER AUTOINCREMENT,
              rowhash VARCHAR,
              text VARCHAR,
              metadata VARIANT,
              text_embedding vector(float, {self._vector_length})
            )
            ;
            """
        )

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> List[str]:
        """Add more texts to the vectorstore index.

        Args:
            texts: Iterable of strings to add to the vectorstore.
            metadatas: Optional list of metadatas associated with the texts.
            kwargs: vectorstore specific parameters
        """
        max_id = (
            self._connection.cursor(DictCursor)
            .execute(f"SELECT NVL(max(rowid), 0) as rowid FROM {self._table}")
            .fetchone()["ROWID"]
        )
        embeds = self._embedding.embed_documents(list(texts))
        if not metadatas:
            metadatas = [{} for _ in texts]

        data_input = [
            (text, json.dumps(metadata), embed)
            for text, metadata, embed in zip(texts, metadatas, embeds)
        ]
        self._connection.cursor().execute("begin")
        for row in data_input:
            _hash = hashlib.sha256(row[0].encode("UTF-8")).hexdigest()
            _text = row[0].replace("'", "\\'")
            _metadata = row[1]
            _vec = row[2]

            _q = f"""
                MERGE INTO {self._table} t USING (
                    SELECT
                        ?::VARCHAR as rowhash,
                        ?::VARCHAR as text,
                        PARSE_JSON(?) as metadata,
                        {_vec}::VECTOR(float, {self._vector_length}) as text_embedding
                    ) s
                ON s.rowhash = t.rowhash
                WHEN NOT MATCHED THEN
                    INSERT (rowhash, text, metadata, text_embedding)
                    VALUES (s.rowhash, s.text, s.metadata, s.text_embedding);
            """
            self._connection.cursor().execute(_q, [_hash, _text, _metadata])
        self._connection.cursor().execute("commit")

        # Pulling every ids we just inserted
        results = self._connection.cursor(DictCursor).execute(
            f"SELECT rowid FROM {self._table} WHERE rowid > {max_id}"
        )
        return [row["ROWID"] for row in results]

    def similarity_search_with_score_by_vector(
        self, embedding: List[float], k: int = 4, **kwargs: Any
    ) -> List[Tuple[Document, float]]:
        sql_query = f"""
            WITH search_t AS (
                SELECT {embedding}::VECTOR(float, {self._vector_length}) AS search_embedding
            )
            SELECT
                text,
                metadata,
                VECTOR_COSINE_SIMILARITY(e.text_embedding, s.search_embedding) AS similarity
            FROM {self._table} e, search_t s
            ORDER BY similarity DESC
            LIMIT {k}
        """
        cursor = self._connection.cursor(DictCursor)
        cursor.execute(sql_query)
        results = cursor.fetchall()

        documents = []
        for row in results:
            metadata = json.loads(row["METADATA"]) or {}
            doc = Document(page_content=row["TEXT"], metadata=metadata)
            documents.append((doc, row["SIMILARITY"]))

        return documents

    def similarity_search(
        self, query: str, k: int = 8, **kwargs: Any
    ) -> List[Document]:
        """Return docs most similar to query."""
        embedding = self._embedding.embed_query(query)
        documents = self.similarity_search_with_score_by_vector(
            embedding=embedding, k=k
        )
        return [doc for doc, _ in documents]

    def similarity_search_with_score(
        self, query: str, k: int = 8, **kwargs: Any
    ) -> List[Tuple[Document, float]]:
        """Return docs most similar to query."""

        embedding = self._embedding.embed_query(query)
        documents = self.similarity_search_with_score_by_vector(
            embedding=embedding, k=k
        )
        return documents

    def similarity_search_by_vector(
        self, embedding: List[float], k: int = 8, **kwargs: Any
    ) -> List[Document]:
        documents = self.similarity_search_with_score_by_vector(
            embedding=embedding, k=k
        )
        return [doc for doc, _ in documents]

    @classmethod
    def from_texts(
        cls: Type[SnowflakeVectorStore],
        texts: List[str],
        embedding: Embeddings,
        metadatas: Optional[List[dict]] = None,
        table: str = "langchain",
        connection: Optional[SnowflakeConnection] = None,
        **kwargs: Any,
    ) -> SnowflakeVectorStore:
        """Return VectorStore initialized from texts and embeddings."""

        vector_store = cls(table=table, connection=connection, embedding=embedding)
        vector_store.add_texts(texts=texts, metadatas=metadatas)
        return vector_store
