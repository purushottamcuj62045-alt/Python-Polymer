# Building the packet capture Engine
from scapy.all import sniff, IP, TCP, UDP
from collections import defaultdict
import threading
import queue

class PacketCapture:
    def __init__(self):
        self.packet_queue = queue.Queue()
        self.stop_capture = threading.Event()

    def packet_callback(self, packet):
        if IP in packet and (TCP in packet or UDP in packet):
            self.packet_queue.put(packet)

    def start_capture(self, interface="eth0"):
        def capture_thread():
            sniff(iface=interface,
                prn=self.packet_callback,
                store=0,
                stop_filter=lambda x: self.stop_capture.is_set())
        self.capture_thread = threading.Thread(target=capture_thread)
        self.capture_thread.start()

    def stop(self):
        self.stop_capture.set()
        self.capture_thread.join()


# Building the traffic analysis module
class TrafficAnalyzer:
    def __init__(self):
        self.connections = defaultdict(list)
        self.flow_stats = defaultdict(lambda: {
            'packet_count': 0,
            'byte_count': 0,
            'start_time': None,
            'last_time': None
        })

    def analyze_packet(self, packet):
        if IP in packet and TCP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            port_src = packet[TCP].sport
            port_dst = packet[TCP].dport

            flow_key = (ip_src, ip_dst, port_src, port_dst)

            # Update flow statistics
            stats = self.flow_stats[flow_key]
            stats['packet_count'] += 1
            stats['byte_count'] += len(packet)
            current_time = packet.time

            if not stats['start_time']:
                stats['start_time'] = current_time
            stats['last_time'] = current_time

            # Avoid division by zero on first packet
            duration = stats['last_time'] - stats['start_time']
            if duration == 0:
                return None

            return self.extract_features(packet, stats)

    def extract_features(self, packet, stats):
        duration = stats['last_time'] - stats['start_time']
        return {
            'packet_size': len(packet),
            'flow_duration': duration,
            'packet_rate': stats['packet_count'] / duration,
            'byte_rate': stats['byte_count'] / duration,
            'tcp_flags': packet[TCP].flags,
            'window_size': packet[TCP].window
        }


# Building the detection engine
from sklearn.ensemble import IsolationForest
import numpy as np

class DetectionEngine:
    def __init__(self):
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.signature_rules = self.load_signature_rules()
        self.training_data = []
        self.is_trained = False
        self._train_with_dummy_data()

    def _train_with_dummy_data(self):
        # Train with basic normal traffic patterns [packet_size, packet_rate, byte_rate]
        dummy_data = np.array([
            [64,   10.0,  640.0],
            [128,  20.0,  2560.0],
            [256,  15.0,  3840.0],
            [512,  5.0,   2560.0],
            [1024, 8.0,   8192.0],
            [100,  12.0,  1200.0],
            [200,  18.0,  3600.0],
            [300,  9.0,   2700.0],
            [150,  11.0,  1650.0],
            [400,  7.0,   2800.0],
        ])
        self.anomaly_detector.fit(dummy_data)
        self.is_trained = True

    def load_signature_rules(self):
        return {
            'syn_flood': {
                'condition': lambda features: (
                    features['tcp_flags'] == 2 and  # SYN flag
                    features['packet_rate'] > 100
                )
            },
            'port_scan': {
                'condition': lambda features: (
                    features['packet_size'] < 100 and
                    features['packet_rate'] > 50
                )
            }
        }

    def train_anomaly_detector(self, normal_traffic_data):
        self.anomaly_detector.fit(normal_traffic_data)
        self.is_trained = True

    def detect_threats(self, features):
        threats = []

        # Signature-based detection
        for rule_name, rule in self.signature_rules.items():
            if rule['condition'](features):
                threats.append({
                    'type': 'signature',
                    'rule': rule_name,
                    'confidence': 1.0
                })

        # Anomaly-based detection (only if trained)
        if self.is_trained:
            feature_vector = np.array([[
                features['packet_size'],
                features['packet_rate'],
                features['byte_rate']
            ]])
            anomaly_score = self.anomaly_detector.score_samples(feature_vector)[0]
            if anomaly_score < -0.5:
                threats.append({
                    'type': 'anomaly',
                    'score': anomaly_score,
                    'confidence': min(1.0, abs(anomaly_score))
                })

        return threats


# Building the alert system
import logging
import json
from datetime import datetime

class AlertSystem:
    def __init__(self, log_file="ids_alerts.log"):
        self.logger = logging.getLogger("IDS_Alerts")
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def generate_alert(self, threat, packet_info):
        alert = {
            'timestamp': datetime.now().isoformat(),
            'threat_type': threat['type'],
            'source_ip': packet_info.get('source_ip'),
            'destination_ip': packet_info.get('destination_ip'),
            'confidence': threat.get('confidence', 0.0),
            'details': threat
        }

        self.logger.warning(json.dumps(alert))
        print(f"[ALERT] {json.dumps(alert, indent=2)}")

        if threat['confidence'] > 0.8:
            self.logger.critical(
                f"High confidence threat detected: {json.dumps(alert)}"
            )


# Putting it all together
class IntrusionDetectionSystem:
    def __init__(self, interface="eth0"):
        self.packet_capture = PacketCapture()
        self.traffic_analyzer = TrafficAnalyzer()
        self.detection_engine = DetectionEngine()
        self.alert_system = AlertSystem()
        self.interface = interface

    def start(self):
        print(f"Starting IDS on interface {self.interface}")
        self.packet_capture.start_capture(self.interface)
        while True:
            try:
                packet = self.packet_capture.packet_queue.get(timeout=1)

                # Only process TCP and UDP packets
                if not (IP in packet and (TCP in packet or UDP in packet)):
                    continue

                features = self.traffic_analyzer.analyze_packet(packet)
                if features:
                    threats = self.detection_engine.detect_threats(features)
                    for threat in threats:
                        if TCP in packet:
                            packet_info = {
                                'protocol': 'TCP',
                                'source_ip': packet[IP].src,
                                'destination_ip': packet[IP].dst,
                                'source_port': packet[TCP].sport,
                                'destination_port': packet[TCP].dport
                            }
                        else:
                            packet_info = {
                                'protocol': 'UDP',
                                'source_ip': packet[IP].src,
                                'destination_ip': packet[IP].dst,
                                'source_port': packet[UDP].sport,
                                'destination_port': packet[UDP].dport
                            }
                        self.alert_system.generate_alert(threat, packet_info)

            except queue.Empty:
                continue
            except KeyboardInterrupt:
                print("\nStopping IDS...")
                self.packet_capture.stop()
                break


if __name__ == "__main__":
    ids = IntrusionDetectionSystem()
    ids.start()
