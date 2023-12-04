import requests

ip="162.31.128.3"
port=20001

s = requests.Session()
r = s.post(f"http://{ip}:20001/login",json={"username":"test","password":"test"})

r1 = s.get(f"http://{ip}:20001/me")
print(r1.text)
