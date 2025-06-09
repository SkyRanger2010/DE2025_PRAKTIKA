from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, crud, schemas
from app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        raise Exception("DB Error", e)
    finally:
        db.close()


@app.get("/keyword_search", response_model=schemas.UserInSearchResults)
def get_info_by_keyword(
    keywords: str,
    start_idx: int = 0,
    end_idx: int = None,
    db: Session = Depends(get_db)
):
    # Разделяем по запятой и убираем лишние пробелы
    keywords_to_search = set()
    for kw in keywords.split(','):
        keywords_to_search.add(kw.strip())

    # Если end_idx не указан, выводим все записи до конца
    if end_idx is None:
        # Получаем общее количество подходящих записей
        total = db.query(models.UserIn).count()
        end_idx = total

    if end_idx <= start_idx:
        raise HTTPException(status_code=400, detail="end_idx должен быть больше start_idx")

    try:
        ans = crud.get_users_by_keywords(db, keywords_to_search, start_idx, end_idx)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "count": len(ans),
        "res": ans
    }

