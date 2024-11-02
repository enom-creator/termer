import subprocess
import threading
import time

class WifiNetwork:
    def __init__(self, ssid, channel):
        self.ssid = ssid
        self.channel = channel
        self.process = None

    def start(self):
        self.process = subprocess.Popen([
            'hostapd', '-B',
            '-i', 'wlan0',
            '-c', f'/tmp/{self.ssid}.conf'
        ])

        with open(f'/tmp/{self.ssid}.conf', 'w') as f:
            f.write(f'interface=wlan0\n')
            f.write(f'ssid={self.ssid}\n')
            f.write(f'channel={self.channel}\n')

    def stop(self):
        if self.process:
            self.process.kill()
            self.process.wait()

def create_networks(num_networks):
    networks = []
    for i in range(num_networks):
        ssid = input(f"Enter the name for network {i+1}: ")
        channel = 6  # use a fixed channel for simplicity
        network = WifiNetwork(ssid, channel)
        networks.append(network)
        network.start()

    input("Press Enter to destroy all networks...")
    for network in networks:
        network.stop()

if __name__ == "__main__":
    num_networks = int(input("Enter the number of networks to create: "))
    create_networks(num_networks)
    print("All networks destroyed.")
