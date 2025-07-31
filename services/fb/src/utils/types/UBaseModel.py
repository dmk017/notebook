from pydantic import BaseModel, ConfigDict

class UBaseModel(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=()
    )
