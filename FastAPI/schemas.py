from pydantic import BaseModel


class BaseRecipe(BaseModel):
    name: str
    cooking_time: int
    count_view: int


    class Config:
        orm_mode = True

class AllInfoRecipe(BaseRecipe):
    ingredients_list: str
    description: str

    class Config:
        orm_mode = True
