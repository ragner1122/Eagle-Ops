from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import KnowledgeArticle
from ..schemas import KnowledgeArticleOut
from ..auth import get_current_user

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/", response_model=list[KnowledgeArticleOut])
def list_articles(db: Session = Depends(get_db), _user=Depends(get_current_user)):
    return db.query(KnowledgeArticle).all()
