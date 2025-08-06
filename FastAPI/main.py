from typing import List
from fastapi import FastAPI
from sqlalchemy import update, desc
from sqlalchemy.future import select
import models
import schemas
from database import engine, session


app = FastAPI()


# @app.on_event("startup")
# async def shutdown():
#     async with engine.begin() as conn:
#         await conn.run_sync(models.Base.metadata.create_all)
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await session.close()
#     await engine.dispose()


@app.get('/recipes/', response_model=List[schemas.BaseRecipe])
async def recipes() -> List[models.Recipe]:
    async with session.begin():
        res = await session.execute(select(models.Recipe).order_by(desc(models.Recipe.count_view),
                                                               models.Recipe.cooking_time))
    return res.scalars().all()

@app.get('/recipes/{recipe_id:int}/', response_model=List[schemas.AllInfoRecipe])
async def recipes_info(recipe_id: int) -> List[models.Recipe]:
    async with session.begin():
        query = select(models.Recipe).where(models.Recipe.id == recipe_id)
        res = await session.execute(query)
        records = res.scalars().all()
        count_view_get: int = (records[0].count_view)
        query_update_count_view = (update(models.Recipe).
                                where(models.Recipe.id == recipe_id).
                                values(count_view=count_view_get + 1))
        await session.execute(query_update_count_view)
    return records

@app.post('/recipes/', response_model=schemas.AllInfoRecipe)
async def add_recipe(recipe: schemas.AllInfoRecipe) -> models.Recipe:
    new_recipe = models.Recipe(**recipe.dict())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe
