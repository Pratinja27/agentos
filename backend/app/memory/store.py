from sqlalchemy.orm import Session

from ..config import settings
from ..models import MemoryItem


def add_memory(db: Session, kind: str, title: str, content: str) -> MemoryItem:
    item = MemoryItem(kind=kind, title=title, content=content)
    db.add(item)
    db.commit()
    db.refresh(item)
    if settings.chroma_enabled:
        try:
            from .chroma import upsert_memory

            upsert_memory(item.id, kind, title, content)
        except Exception:
            pass
    return item


def search_memory(db: Session, query: str, limit: int = 4) -> list[MemoryItem]:
    if settings.chroma_enabled:
        try:
            from .chroma import query_memory

            ids = query_memory(query, limit)
            if ids:
                rows = db.query(MemoryItem).filter(MemoryItem.id.in_(ids)).all()
                if rows:
                    return rows
        except Exception:
            pass
    rows = db.query(MemoryItem).order_by(MemoryItem.id.desc()).all()
    scored = []
    tokens = set(query.lower().split())
    for row in rows:
        hay = f"{row.title} {row.content}".lower()
        score = sum(1 for token in tokens if token in hay)
        scored.append((score, row))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [row for score, row in scored[:limit] if score or True][:limit]
