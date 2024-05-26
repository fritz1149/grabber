import threading
from scapy.all import wrpcapng, sniff, wrpcap
from datetime import datetime
import os

packets_save_freq = 60000

class Sniffer:
    def __init__(self):
        self.packets = []
        self.stop_sniff = False

    def _ingest_packet(self, packet):
        self.packets.append(packet)
        # if len(self.packets) >= packets_save_freq:
        #     self.save()

    def _stop_sniff(self, packet):
        ret = self.stop_sniff
        return ret

    def run(self, tag):
        self.stop_sniff = False
        self.tag = tag
        self.thread = threading.Thread(target=
                                       lambda: sniff(iface='WLAN', 
                                                     prn=self._ingest_packet, 
                                                     stop_filter=self._stop_sniff))
        self.thread.start()

    def stop(self, if_save = True):
        self.stop_sniff = True
        self.thread.join()
        if if_save:
            self.save()
        else:
            self.packets.clear()

    def save(self):
        filename = os.path.join("save",
                                f'{self.tag}.{datetime.now().strftime("%Y%m%d%H%M%S")}.pcap')
        # wrpcapng(filename, self.packets)
        wrpcap(filename, self.packets)
        self.packets.clear()

if __name__ == '__main__':
    sniffer_ = Sniffer()
    sniffer_.run('test')
    from time import sleep
    sleep(10)
    sniffer_.stop()