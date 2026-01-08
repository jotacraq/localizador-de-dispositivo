import socket
from datetime import datetime
import pytz
import subprocess
import json
from winrt.windows.devices.geolocation import Geolocator, PositionAccuracy


def pegar_data_hora():
    """Retorna data e hora atual no fuso horário de São Paulo"""
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    data_hora_atual = datetime.now(fuso_horario)
    return data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')


def pegar_nome_host():
    try:
        nome_host = socket.gethostname()
        return nome_host
    except Exception as e:
        print(f"⚠ Aviso: Não foi possível obter o nome do host. Detalhes: {str(e)}")
        return "NULL"


def pegar_uuid_hardware():
    try:
        comando = [
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_ComputerSystemProduct).UUID"
        ]

        resultado = subprocess.check_output(
            comando,
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()

        if not resultado:
            return "UUID_NAO_ENCONTRADO"

        if resultado.upper() in (
            "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF",
            "00000000-0000-0000-0000-000000000000"
        ):
            return "UUID_INVALIDO"

        return resultado

    except Exception:
        return "UUID_ERRO"


def pegar_ssid():
    try:
        resultado = subprocess.run(['netsh', 'wlan', 'show', 'interface'], 
                                 capture_output=True, text=True, encoding='utf-8')
        linhas = resultado.stdout.split('\n')
        
        for linha in linhas:
            if 'SSID' in linha and ':' in linha:
                ssid = linha.split(':', 1)[1].strip()
                if ssid:
                    return ssid
        
        return "NULL"
    except Exception as e:
        print(f"⚠ Aviso: Não foi possível obter o SSID. Detalhes: {str(e)}")
        return "NULL"


def pegar_ip_local():
    try:
        iplocal = socket.gethostbyname(socket.gethostname())
        return iplocal
    except Exception as e:
        print(f"⚠ Aviso: Não foi possível obter o IP local. Detalhes: {str(e)}")
        return "NULL"


def pegar_ip_publico():
    try:
        import urllib.request
        ippublico = urllib.request.urlopen('https://api.ipify.org').read().decode().strip()
        return ippublico if ippublico else "NULL"
    except Exception as e:
        print(f"⚠ Aviso: Não foi possível obter o IP público. Detalhes: {str(e)}")
        return "NULL"


def verificar_internet():
    try:
        socket.gethostbyname('google.com')
        return 1
    except Exception:
        return 0


def pegar_localizacao():
    """Obtém localização geográfica do dispositivo"""
    try:
        locator = Geolocator()
        locator.desired_accuracy = PositionAccuracy.HIGH

        pos = locator.get_geoposition_async().get()

        coord = pos.coordinate
        ponto = coord.point.position

        latitude = ponto.latitude
        longitude = ponto.longitude
    
        return latitude, longitude
    except Exception as e:
        print(f"⚠ Aviso: Não foi possível obter localização. Detalhes: {str(e)}")
        latitude = "NULL"
        longitude = "NULL"
        return latitude, longitude


def montar_json_completo():
    data_hora = pegar_data_hora()
    uuid_hardware = pegar_uuid_hardware()
    iplocal = pegar_ip_local()
    ippublico = pegar_ip_publico()
    ssid = pegar_ssid()
    tem_internet = verificar_internet()
    latitude, longitude = pegar_localizacao()
    nome_host = pegar_nome_host()
    
    dados = {
        "data_hora": data_hora,
        "uuid_hardware": uuid_hardware,
        "nome_host": nome_host,
        "ip_local": iplocal,
        "ip_publico": ippublico,
        "ssid": ssid,
        "tem_internet": tem_internet,
        "latitude": latitude,
        "longitude": longitude
    }
    
    return dados


if __name__ == "__main__":
    
    if verificar_internet() == 0:
        print("⚠ Aviso: Sem conexão com a internet. Alguns dados podem estar ausentes.")
    elif verificar_internet() == 1:
        print("✔ Conexão com a internet estabelecida.")
        dados = montar_json_completo()
        print(json.dumps(dados, indent=4, ensure_ascii=False))
        
    
    