"""
Файл с функциями для VPN.
Если нет NORD VPN - функции заполнить PASS или же переписать функции под свой VPN/proxy.
"""
from time import sleep
from nordvpn_switcher import initialize_VPN, rotate_VPN


def start_vpn():
    initialize_VPN(save=1, area_input=['complete rotation'])


def switch_vpn():
    rotate_VPN()
    sleep(3)
