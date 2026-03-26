import requests

def get_ip_info(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return {
            "country": res.get("country","Unknown"),
            "city": res.get("city","Unknown")
        }
    except:
        return {"country":"Unknown","city":"Unknown"}
