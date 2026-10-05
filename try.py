try:
    import requests
    import json
    from datetime import datetime,timezone

    response = requests.get("https://postman-echo.com/get", params={"role":"data-engineer","location":"London","company":"Google"}, timeout=30,        
    )
    response.raise_for_status()
    val = response.status_code
except requests.exceptions.JSONDecodeError:
    print("The response was not valid JSON. No file was saved.")
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)
except requests.exceptions.HTTPError as e:
    print("The API returned an HTTP error:", e)    
else:
    if val ==200:
        data = response.json()
        string_input = data["args"]
        print(string_input.get("role", "Role not found"))
        filename = f"postmanfile_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M')}.json" 
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data,file,indent=2)
    else:
        print('http is invalid',val)            
    

