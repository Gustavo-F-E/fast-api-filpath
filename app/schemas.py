# app/schemas.py
from pydantic import BaseModel, EmailStr, Field, model_validator
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
    password: Optional[str] = None
    provider: str = "email"
    provider_id: Optional[str] = None

'''
class UserLogin(BaseModel):
    # Cambiamos para aceptar email O username
    email: Optional[str] = None
    username: Optional[str] = None
    password: str

    # Validación para asegurar que se proporcione email O username
    @model_validator(mode='after')
    def check_email_or_username(self):
        if not self.email and not self.username:
            raise ValueError('Debe proporcionar email o username')
        return self'''

class UserLogin(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: str

    @model_validator(mode='after')
    def check_email_or_username(self):
        email = getattr(self, 'email', None)
        username = getattr(self, 'username', None)
        
        if not email and not username:
            raise ValueError('Debe proporcionar email o username')
        return self
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
    liner_name: Optional[str] = None
    machine_name: Optional[str] = None
    layers: list = []
    completion_percentage: int = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    liner_name: Optional[str] = None
    machine_name: Optional[str] = None
    layers: Optional[list] = None
    completion_percentage: Optional[int] = None


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

# ========== LINERS ==========
class LinerSection(BaseModel):
    tipo: str # Ninguno, Semiesferico, Isotensoide, Conico, Cilindro
    diametro_menor: float = 0
    diametro_mayor: float = 0
    longitud: float = 0
    diametro: float = 0 # Solo para cilindro

class LinerBase(BaseModel):
    name: str
    tipo_liner: str = "simple" # simple, compuesto, no-axisimetrico
    extremo_inicial: LinerSection
    medio: LinerSection
    extremo_final: LinerSection
    user_email: Optional[EmailStr] = None

class LinerCreate(LinerBase):
    pass

class LinerInDB(LinerBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime
    updated_at: datetime
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }

class LinerResponse(LinerBase):
    id: str = Field(validation_alias=AliasChoices("_id", "id"))
    created_at: datetime
    updated_at: datetime

# ========== MAQUINAS ==========
class MachineAxis(BaseModel):
    eje: str # X, Y, Z, A
    unidad: Optional[str] = None # Radianes, Grados (solo para giros)

class MachineBase(BaseModel):
    name: str
    tipo: str = "CNC" # CNC, Robot
    posicion_inicial: str = "giro horario" # giro horario, giro antihorario
    coordenadas: dict = {"x_p": 0, "y_p": 0, "x_pp": 0, "y_pp": 0}
    giro_mandril: MachineAxis
    longitudinal: MachineAxis
    giro_devanador: MachineAxis
    acercamiento_devanador: MachineAxis
    velocidad_maquina: float = 0 # mm/min
    user_email: Optional[EmailStr] = None

class MachineCreate(MachineBase):
    pass

class MachineInDB(MachineBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime
    updated_at: datetime
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }

class MachineResponse(MachineBase):
    id: str = Field(validation_alias=AliasChoices("_id", "id"))
    created_at: datetime
    updated_at: datetime


# ========== TOKEN ==========
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None

class OAuthLogin(BaseModel):
    email: EmailStr
    username: str
    provider: str
    provider_id: str
