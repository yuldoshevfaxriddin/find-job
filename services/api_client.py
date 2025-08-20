import requests

session = requests.Session()

def get_data(query):
    """
    Inline query uchun ma'lumotlarni olish funksiyasi.
    """
    response = session.get(query)
    
    if response.status_code != 200:
        return []
    return response.json()  # JSON formatidagi ma'lumotlarni qaytarish