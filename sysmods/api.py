from typing import Union, Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel


class rest_Server:
    def __init__(self):
        self.app_api = FastAPI()
        self.users = {}
    def configure_oauth(self):
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def register_endpoints(self):

        @self.app_api.put("/api/{item_id}")
        def a(item_id: int, item: Item):
            return {"item_name": item.name, "item_id": item_id}
        
        @self.app_api.put("/api/{node}/{property}")
        def a(item_id: int, item: Item):
            return {"item_name": item.name, "item_id": item_id}