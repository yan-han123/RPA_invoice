import requests
import json

# TODO:用你自己的api对应的AK和SK代替client_id和client_secret
def main():

    url = "https://aip.baidubce.com/oauth/2.0/token?client_id=AmVvtvDQhSd78KkuhD8VBOvj&client_secret=mjtspW3Dmfu8U49tgQKtCTpNMGNUAcjX&grant_type=client_credentials"

    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == '__main__':
    main()
