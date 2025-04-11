from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Modelo de entrada para el login
class LoginData(BaseModel): 
    email: str
    password: str

@app.post("/login")
def login(data: LoginData):
    try:
        conn = mysql.connector.connect(
            host="gateway01.us-east-1.prod.aws.tidbcloud.com",
            port=4000,
            user="Tcwsmq6TvJV4Yp9.root",
            password="DY1CkEYxao5YJMdU",
            database="test",
            ssl_ca="C:/Users/SENA/Desktop/login2/ca.pem"
        )
        cursor = conn.cursor(buffered=True)  # <--- ESTA ES LA CLAVE
        cursor.execute("SELECT * FROM login WHERE email=%s AND password=%s", (data.email, data.password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return {"message": "Login exitoso", "user": {"email": user[0]}}
        else:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    except Exception as e:
        print("ERROR EN EL SERVIDOR:", e)
        raise HTTPException(status_code=500, detail=str(e))
