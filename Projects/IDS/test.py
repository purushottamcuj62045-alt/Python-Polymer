from scapy.all import IP, TCP, UDP
from ids import IntrusionDetectionSystem, TrafficAnalyzer, DetectionEngine

def test_ids():
    ids = IntrusionDetectionSystem()

    test_cases = [
        {
            "name": "Normal HTTP Traffic",
            "packet": IP(src="192.168.1.1", dst="192.168.1.2") / TCP(sport=1234, dport=80, flags="A"),
            "expect_threat": False
        },
        {
            "name": "Normal HTTPS Traffic",
            "packet": IP(src="192.168.1.3", dst="192.168.1.4") / TCP(sport=1235, dport=443, flags="P"),
            "expect_threat": False
        },
        {
            "name": "SYN Flood Simulation",
            "packet": IP(src="10.0.0.1", dst="192.168.1.2") / TCP(sport=5678, dport=80, flags="S"),
            "expect_threat": True,
            "repeat": 150  # send 150 SYN packets to trigger syn_flood rule
        },
        {
            "name": "Port Scan Simulation",
            "packet": IP(src="192.168.1.100", dst="192.168.1.2") / TCP(sport=4321, dport=22, flags="S"),
            "expect_threat": True,
            "repeat": 100  # small packets at high rate
        },
    ]

    print("=" * 60)
    print("         IDS TEST SUITE")
    print("=" * 60)

    passed = 0
    failed = 0

    for test in test_cases:
        packet = test["packet"]
        repeat = test.get("repeat", 1)
        detected_threats = []

        # Send multiple packets to build up flow stats
        base_time = 1000.0
        for i in range(repeat):
            p = packet.copy()
            p.time = base_time + (i * 0.005)  # 5ms apart = high packet rate

            features = ids.traffic_analyzer.analyze_packet(p)
            if features:
                threats = ids.detection_engine.detect_threats(features)
                detected_threats.extend(threats)

        threat_found = len(detected_threats) > 0
        expected = test["expect_threat"]
        result = "PASS" if threat_found == expected else "FAIL"

        if result == "PASS":
            passed += 1
        else:
            failed += 1

        print(f"\n[{result}] {test['name']}")
        print(f"       Expected threat: {expected} | Detected: {threat_found}")
        if detected_threats:
            seen = set()
            for t in detected_threats:
                key = t.get('rule', t.get('type'))
                if key not in seen:
                    seen.add(key)
                    print(f"       -> {t['type'].upper()}: {t.get('rule', 'anomaly')} (confidence: {t.get('confidence', 0):.2f})")

    print("\n" + "=" * 60)
    print(f"  Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 60)

if __name__ == "__main__":
    test_ids()
