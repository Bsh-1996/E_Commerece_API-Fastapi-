from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import *
from authentication import get_hashed_password

app = FastAPI()

@app.post("/registration")
async def user_registrtion(user: user_pydanticIn):
    user_info = user.dict(exclude_unset = True)
    user_info["passowrd"] =  get_hashed_password(user_info["password"])
    user_obj = await User.create(**user_info)
    new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return{
        "status" : "ok",
        "data" : f"""Hello{new_user.username}, thanks for choosing our services. please
        check your email inbox and click on the link to confirm your registration."""
    }



@app.get("/")
def index():
    return {"message": "hello world"}


register_tortoise(
    app,
    db_url= "sqlite://database.sqlite",
    modules = {"models" : ["models"]},
    generate_schemas= True,
    add_exception_handlers=True
)
