import io
from typing import Union, List

from fastapi import FastAPI, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from pydantic import BaseModel


from PIL import Image
from qrcode import QRCode

app = FastAPI()

REDIRECTBASEURL = "https://r-fred-qrcodeapiredirecttrial-main-gnar8l.streamlitapp.com/"

def create_qrcode(data: str, x: int, y: int) -> bytes:
    buff = io.BytesIO(initial_bytes=b"")
    qrc = QRCode()
    
    if x != y: # always keep aspect ratio. Use x as reference.
        y = x
    
    qrc.add_data(f"{REDIRECTBASEURL}?param={data}")
    qrc.make()
    img = qrc.make_image()
    
    img = img.resize((x,y), Image.ANTIALIAS)

    img.save(buff, "PNG")
    buff.seek(0)
    
    return buff.getvalue()

@app.get(path="/qrcode/{data}")
async def qrcode_generator(data: str, x: int = 100, y: int = 100):
    output = create_qrcode(data=data, x = x, y = y)
    
    return Response(content=output, media_type="image/png")   
