# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from pydantic import GetJsonSchemaHandler
from pydantic import AliasChoices
from pydantic.json_schema import JsonSchemaValue
from typing import Optional
from datetime import datetime
from bson import ObjectId

# =======================
# PyObjectId para Pydantic v2
# =======================
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema


# ========== USUARIOS ==========
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    provider: str = "email"
    provider_id: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    password_hash: Optional[str] = None
    provider: str
    provider_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }


class UserResponse(BaseModel):
    id: str = Field(validation_alias=AliasChoices("_id", "id"))
    email: str
    username: str
    provider: str
    created_at: datetime

    model_config = {
        "json_encoders": {ObjectId: str},
    }


# ========== PROYECTOS ==========
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectInDB(ProjectBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }

class ProjectResponse(ProjectBase):
    id: str = Field(validation_alias=AliasChoices("_id", "id"))
    user_email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_encoders": {ObjectId: str},
    }


# ========== TOKEN ==========
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None