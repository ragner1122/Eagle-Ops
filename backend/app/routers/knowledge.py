from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import KnowledgeArticle
from ..schemas import KnowledgeArticleCreate, KnowledgeArticleOut
from ..auth import get_current_user

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


def normalize_tags(tags: list[str]) -> str:
    return ",".join(tag.strip().lower() for tag in tags if tag.strip())


def split_tags(tags: str) -> list[str]:
    return [tag for tag in tags.split(",") if tag]


def serialize_article(article: KnowledgeArticle) -> KnowledgeArticleOut:
    return KnowledgeArticleOut(
        id=article.id,
        title=article.title,
        content=article.content,
        tags=split_tags(article.tags),
        created_by=article.created_by,
        created_at=article.created_at,
        updated_at=article.updated_at,
    )


@router.get("/", response_model=list[KnowledgeArticleOut])
def list_articles(
    keyword: str | None = None,
    tags: list[str] | None = Query(default=None),
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    query = db.query(KnowledgeArticle)
    if keyword:
        search_term = f"%{keyword}%"
        query = query.filter(
            or_(
                KnowledgeArticle.title.ilike(search_term),
                KnowledgeArticle.content.ilike(search_term),
            )
        )
    if tags:
        for tag in tags:
            normalized = tag.strip().lower()
            if normalized:
                query = query.filter(KnowledgeArticle.tags.ilike(f"%{normalized}%"))
    articles = query.order_by(KnowledgeArticle.updated_at.desc()).all()
    return [serialize_article(article) for article in articles]


@router.post("/", response_model=KnowledgeArticleOut, status_code=status.HTTP_201_CREATED)
def create_article(
    payload: KnowledgeArticleCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    article = KnowledgeArticle(
        title=payload.title,
        content=payload.content,
        tags=normalize_tags(payload.tags),
        created_by=user.email,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return serialize_article(article)
