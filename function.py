import winreg as wr

def get_all_net_card_info():
    IF_REG = r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}'
    reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
    reg_key = wr.OpenKey(reg, IF_REG)
    CardInfo = {}

    for i in range(wr.QueryInfoKey(reg_key)[0]):
        subkey_name = wr.EnumKey(reg_key, i)
        try:
            reg_subkey = wr.OpenKey(reg_key, subkey_name + r'\Connection')
            Name = wr.QueryValueEx(reg_subkey, 'Name')[0]
            wr.CloseKey(reg_subkey)
            CardInfo[Name] = subkey_name
        except FileNotFoundError as e:
            pass

    return CardInfo


def get_net_card_num_by_name(name):
    CardInfo = get_all_net_card_info()
    if name in CardInfo:
        return CardInfo[name]

def main():
    print(get_all_net_card_info())
    cardnum = get_net_card_num_by_name("本地连接* 8")
    print(cardnum)

if __name__ == "__main__":
    main()
