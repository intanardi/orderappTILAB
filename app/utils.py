import jwt
secret_key = "8217ndwv2183"

def generate_token(id):
    encoded_jwt = jwt.encode({"user_id": id}, secret_key, algorithm="HS256")
    return encoded_jwt
def verify_token(token):
    try :
        verify = jwt.decode(token, secret_key, algorithms=['HS256'])
    except:
        return
    print(verify)
    return verify