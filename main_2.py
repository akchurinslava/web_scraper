import requests

bn = 2
a = 100
aj = ""
ae = 8
af = 50
otsi = "%D0%BF%D0%BE%D0%B8%D1%81%D0%BA"

url = f"https://rus.auto24.ee/kasutatud/nimekiri.php?bn={bn}&a={a}&aj={aj}&ae={8}&af={50}&otsi={otsi}"

payload = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
    'Connection': 'keep-alive',
}

response = requests.request("GET", url, headers=headers)

print(response.text)
