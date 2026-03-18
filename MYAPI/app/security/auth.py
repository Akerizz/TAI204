from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


security = HTTPBasic() 
def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):

    usuarioAuth = secrets.compare_digest(credentials.username, "Marron")
    contraAuth = secrets.compare_digest(credentials.password, "123456")

    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no Autorizadas",
        )
    
    return credentials.username