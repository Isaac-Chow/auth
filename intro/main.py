import datetime
import jwt

SECRET_KEY = "QeZW1y0aruvOnuATJpdnN3UgWpdpL1bN"

json_data={
    "sender":"Python JWT",
    "message":"Testing Python JWT",
    "date":str(datetime.datetime.now())
}

encoded_token=jwt.encode(payload=json_data,key=SECRET_KEY,algorithm="HS256")

print("Token:", encoded_token)

try:
    # JWT reference: https://pyjwt.readthedocs.io/en/stable/api.html
    decode_data = jwt.decode(jwt=encoded_token,key=SECRET_KEY,algorithms="HS256")
    print("Decoded data:",decode_data)
except Exception as e:
    message = f"Token invalid -->{e}"
    print({"message":message})