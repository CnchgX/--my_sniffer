import datetime

from UI import *
from function import *
from scapy.all import *
import datetime

mainpage = None
card = ""
filter = ""
packages = []
pack_id = 0
pause_flag = False
kkk = 0


def deal_message():
    mainpage.openaction.triggered.connect(open_file)
    mainpage.exitaction.triggered.connect(qApp.quit)
    mainpage.saveaction.triggered.connect(save_file)
    mainpage.startaction.triggered.connect(start_capture)
    mainpage.stopaction.triggered.connect(stop_capture)
    mainpage.aboutaction.triggered.connect(about_message)

    mainpage.frame1.start_button.clicked.connect(start_capture)
    mainpage.frame1.stop_button.clicked.connect(stop_capture)
    mainpage.frame1.save_button.clicked.connect(save_file)

    mainpage.frame2.table.cellPressed.connect(get_row)


def open_file():
    file_name = QFileDialog.getOpenFileName(mainpage, "test", "./", "pcap files(*.pcap);;All files(*.*)")
    file_path = file_name[0]
    packages = rdpcap(file_path)
    for i in packages:
        deal_package(i)


def save_file():
    file_path = QFileDialog.getSaveFileName(mainpage, "save file", "./", "pcap files(*.pcap);;all files(*.*)")
    file_name = file_path[0]
    if file_path[0].find(".pcap") == -1:
        file_name = file_name + ".pcap"
    wrpcap(file_name, packages)


def start_capture():
    kkk = 0
    iface = "\\device\\NPF_" + get_net_card_num_by_name(card)
    # sniff(prn=(lambda x: deal_package(x)), filter=filter, stop_filter=(lambda x: stop_sending.isset()), iface=iface)
    sniff(prn=(lambda x: deal_package(x)), timeout=10, filter=filter, stop_filter=(lambda x: kkk), iface=iface)


def stop_capture():
    global kkk
    kkk = 1


def about_message():
    # TODO
    pass


def deal_package(package):
    if not pause_flag:
        global packages
        packages.append(package)
        pack_time = datetime.datetime.fromtimestamp(int(package.time))
        src = package[Ether].src
        dst = package[Ether].dst
        type = package[Ether].type
        types = {0x0800: 'IPv4', 0x0806: 'ARP', 0x86dd: 'IPv6', 0x88cc: 'LLDP', 0x891D: 'TTE'}

        if type in types:
           proto = types[type]
        else:
             proto = 'Unknown'

        # IP
        if proto == 'IPv4':
            # 建立协议查询字典
            protos = {1: 'ICMP', 2: 'IGMP', 4: 'IP', 6: 'TCP', 8: 'EGP', 9: 'IGP', 17: 'UDP', 41: 'IPv6', 50: 'ESP', 89: 'OSPF'}
            src = package[IP].src
            dst = package[IP].dst
            proto = package[IP].proto
            if proto in protos:
                proto = protos[proto]

        # TCP
        if TCP in package:
            protos_tcp = {80: 'Http', 443: 'Https', 23: 'Telnet', 21: 'Ftp', 20: 'ftp_data', 22: 'SSH', 25: 'SMTP'}
            sport = package[TCP].sport
            dport = package[TCP].dport
            if sport in protos_tcp:
                proto = protos_tcp[sport]
            elif dport in protos_tcp:
                proto = protos_tcp[dport]

        # UDP
        elif UDP in package:
            if package[UDP].sport == 53 or package[UDP].dport == 53:
                proto = 'DNS'

        length = len(package)
        info = package.summary()
        global pack_id
        mainpage.frame2.table.insertRow(pack_id)
        item = [pack_id + 1, str(pack_time), src, dst, proto, length, info]
        for j in range(7):
            mainpage.frame2.table.setItem(pack_id, j, QTableWidgetItem(str(item[j])))
        pack_id += 1


def get_row(row):
    mainpage.frame2.label.setText(packages[row].summary())
    mainpage.frame2.label1.setText(hexdump(packages[row], dump=True))


def main():
    app = QApplication(sys.argv)

    startpage = StartPage()
    global card
    card = startpage.card
    global mainpage
    mainpage = MainPage("my_sniffer--" + card)
    deal_message()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


