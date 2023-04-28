from scapy.all import *

def scan_wifi():
    ssid_list = []
    mac_list = []

    os.system("sudo ifconfig <interface> down")
    os.system("sudo iwconfig <interface> mode monitor")
    os.system("sudo ifconfig <interface> up")

    os.system("airodump-ng --output-format csv -w output_file <interface> & sleep 5")

    with open("output_file-01.csv", "r") as file:
        lines = file.readlines()

        for line in lines[2:]:
            line = line.strip()
            values = line.split(",")

            if len(values) >= 14:
                mac = values[0].strip()
                ssid = values[13].strip()

                if ssid and mac not in mac_list:
                    ssid_list.append(ssid)
                    mac_list.append(mac)

    os.system("sudo pkill airodump-ng")

    os.system("sudo ifconfig <interface> down")
    os.system("sudo iwconfig <interface> mode managed")
    os.system("sudo ifconfig <interface> up")

    return ssid_list, mac_list

ssids, macs = scan_wifi()

for ssid, mac in zip(ssids, macs):
    print(f"SSID: {ssid}, MAC Address: {mac}")
