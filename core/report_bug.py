import requests
import os

def send_report_bug(description, user_name="Unknown", screenshot_path=None):
    url = "https://toolmuxapp.pythonanywhere.com/bot-proxy/report-bug"

    data = {
        'description': description,
        'user_name': user_name
    }

    files = {}

    if screenshot_path:
        files['screenshot'] = open(screenshot_path, 'rb')
        
    try:
        response = requests.post(url, data=data, files=files)

        if files.get('screenshot'):
            files['screenshot'].close() 

        if response.status_code == 200:
            print('Bug report enviado com sucesso!')
        else:
            print('Falha ao enviar o relatório.')
    except requests.exceptions.RequestException as e:
        print(f'Erro ao conectar ao servidor: {e}')



