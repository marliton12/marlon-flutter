from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# Configuración de la base de datos (con claves correctas)
db_config = {
    "host": "gateway01.us-east-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "user": "Tcwsmq6TvJV4Yp9.root",
    "password": "DY1CkEYxao5YJMdU",
    "database": "test"
}

# Modelo de datos para login
class LoginRequest(BaseModel):
    email: str
    password: str

# Función para conexión a la base de datos
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Ruta para login
@app.post("/login")
def login(login_request: LoginRequest):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM login WHERE email = %s AND password = %s"
        cursor.execute(query, (login_request.email, login_request.password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            return {"message": "Login exitoso", "user": user}
        else:
            return JSONResponse(status_code=401, content={"detail": "Credenciales incorrectas"})

    except mysql.connector.Error as err:
        return JSONResponse(status_code=500, content={"detail": str(err)})

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "Servidor FastAPI activo"}
