import requests

class APIClient:
    BASE_URL = "http://localhost:8080/api/v1"

    def get_request(self, path, card_number, month, year, holder, cvv):
        payload = {
            "number": card_number,
            "year": year,
            "month": month,
            "holder": holder,
            "cvc": cvv
        }
        response = requests.post(f"{self.BASE_URL}/{path}", json=payload)
        return response
