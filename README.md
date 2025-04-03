# Lunar Rover Communication System Documentation

## Overview

The **Lunar Rover Communication System** is a robust and efficient communication framework designed to facilitate reliable data exchange between various components of a lunar exploration mission. The system is built on top of the Proprietary **JUMPER Protocol** (JSON UDP Multi-Purpose Encoded Reliable Data Transfer Protocol) [RFC 9999], which provides a lightweight, reliable messaging layer over UDP. The project incorporates features such as data compression, integrity verification, error correction, and packet spreading to ensure reliable communication in challenging environments like the lunar surface.

---

## Key Components

### 1. **Earth Base**

The Earth Base acts as the central command and control hub for the lunar mission. It is responsible for:

- Sending commands to the Lunar Rover.
- Receiving sensor data, acknowledgments, and video streams from the rover.
- Managing retransmissions and error correction for reliable communication.
- Providing a GUI for operators to input commands and monitor rover activity.
- Issues mission directives that are relayed through the Lunar Rover master station.

### 2. **Lunar Rover**

The Lunar Rover serves as the master station located on Earth's surface. It is responsible for:

- Executes commands received from the Earth Base.
- Sending commands to lunar nodes (Tunneller and Hopper).
- Collects and transmits sensor data from other nodes (e.g., soil moisture, pH, temperature, conductivity).
- Receiving sensor data, acknowledgments, and video streams from lunar nodes.
- Streams video data back to Earth Base for real-time monitoring.
- Communicating and consolidating data from multiple lunar nodes like the Lunar Tunneller and Lunar Hopper before transmitting to Earth Base for extended functionality.
- Reducing hardware requirements by eliminating the need for multiple Earth-Moon communication systems.

### 3. **Lunar Tunneller**

The Lunar Tunneller is an external node operating on the lunar surface. It:

- Receives commands from the Lunar Rover master station.
- Sends video streams and sensor data back to the Lunar Rover master station.
- Handles video streaming and retransmissions using NACKs (Negative Acknowledgments).
- Provides additional processing capabilities for data integrity and error correction.
- Collects specialized data and performs tunneling operations.

### 4. **Lunar Hopper**

The Lunar Hopper is another external node on the lunar surface that:

- Performs specialized exploration in areas difficult to reach.
- Collects and transmits additional sensor data, such as radiation levels (e.g., Total Ionizing Dose, Dose Rate, Particle Flux).
- Sends data to the Lunar Rover master station rather than directly to Earth.
- Conserves resources by not requiring its own Earth-Moon communication system.

---

## JUMPER Protocol

The **JUMPER Protocol** [RFC 9999] is the backbone of the communication system, designed to address the challenges of unreliable UDP communication. It ensures data reliability, integrity, and efficiency through the following features:

### 1. **Packet Structure**

Each packet consists of:

- **Sequence Number (32 bits):** Includes 4 bits for packet type (e.g., Command, ACK, Video) and 28 bits for the sequence number.
- **HMAC (256 bits):** Ensures data integrity using HMAC-SHA256.
- **Compressed Data (variable):** The payload is compressed using zlib for efficiency.
- **Padding (variable):** Zero bytes for alignment during matrix transposition.

### 2. **Message Types**

The protocol supports multiple message types:

- **Commands (CMD):** Control instructions for the rover.
- **Acknowledgments (ACK):** Confirmation of successful data receipt.
- **Video (VID):** Video frames streamed from the rover.
- **Sensor Data (SENS):** Environmental and operational data from the rover.
- **Handshake (HS):** Connection establishment and maintenance.
- **Negative Acknowledgments (NAK):** Requests for retransmission of lost packets.

### 3. **Protocol Features**

- **Data Compression:** Reduces payload size using zlib.
- **Integrity Verification:**
  - Ensures data authenticity and integrity using HMAC-SHA256.
  - Helps detect and reject corrupted or maliciously altered packets.
- **Error Correction:** Implements Reed-Solomon encoding for error correction.
- **Packet Spreading:**

  - Uses matrix transposition to spread packets for better error resilience.
  - Mitigates burst errors by spreading data across multiple packets for higher resilience.

- **Retransmission Mechanism:** Employs ACKs and NACKs for reliable data delivery.
- **Handshake Mechanism:** Establishes and maintains connections between nodes.

---

## Why a Single Master Rover?

• **Hardware Consolidation:** Only the Rover needs Earth-capable hardware, reducing cost, size, and power usage on Tunneller and Hopper.
• **Scalability and Modularity:** Additional external nodes can be deployed without also needing direct Earth communication hardware.
• **Centralized Coordination:** The Rover can manage tasks, inter-node communication, and scheduling to minimize collisions or bandwidth contention.
• **Extended Functionality:** Tunneller/Hopper can “dock” into the Rover’s code and configuration environment, benefiting from features like advanced error correction or dedicated storage subsystems that they might not run on their own.

---

## Communication Flow

### 1. **Command Transmission**

- Commands are sent from the Earth Base to the Lunar Rover master station.
- The Lunar Rover then forwards these commands to the appropriate lunar nodes (Tunneller or Hopper).
- Each command is packed, compressed, encrypted, and verified for integrity before transmission.

### 2. **Sensor Data Collection**

- Lunar nodes collect sensor data (e.g., soil properties, radiation levels) and transmit it back to the Lunar Rover master station.
- The Lunar Rover consolidates, processes, and relays this data to the Earth Base.
- Data is compressed and secured to minimize transmission errors.

### 3. **Video Streaming**

- Lunar nodes stream video data to the Lunar Rover master station.
- The Rover processes and forwards this video to the Earth Base for real-time monitoring.
- NACKs are used to request retransmission of lost video frames, ensuring smooth playback.

### 4. **Error Handling**

- The protocol detects and corrects errors using Reed-Solomon encoding and retransmission mechanisms.
- HMAC verification ensures data integrity, and extremely corrupted packets are discarded.
- Sent Packets Trigger ACKs and Lost Video packets trigger NACKs, prompting retransmission until successful delivery.

---

## Security Features

- **Encryption:** All data is encrypted using a shared secret key to prevent unauthorized access.
- **HMAC Verification:** Ensures data authenticity and prevents tampering.
- **Key Management:**
  - Separate keys are used for encryption and HMAC generation.
  - Nodes securely store and manage these keys.

---

## Use Cases

1. **Remote Command Execution:**

   - Operators at the Earth Base send commands to the rover to perform specific tasks, such as collecting soil samples or moving to a new location.

2. **Environmental Monitoring:**

   - The rover collects and transmits sensor data to monitor the lunar environment, aiding scientific research.
   - Hopper or Tunneller gather radiation or geological data, sending it to the Rover, which then relays it back to Earth for research and analysis.

3. **Video Surveillance:**

   - Live or near-real-time video feeds from Tunneller/Hopper help scientists on Earth visually monitor their missions.
   - Real-time video streaming from the rover allows operators to visually monitor its surroundings and operations.

4. **Error-Resilient Communication:**

   - High-latency, noisy conditions on the lunar surface and the Earth-Moon link are handled via JUMPER’s robust retransmission, error correction, and handshake processes.
   - The protocol ensures reliable data delivery despite the challenges of lunar communication, such as high latency and packet loss.

---

## Conclusion

The Lunar Rover Communication System is a comprehensive solution for reliable and secure communication between Earth and lunar exploration nodes. By leveraging the JUMPER Protocol and using the Lunar Rover as a master station, it ensures efficient data exchange while minimizing hardware requirements for lunar nodes. This centralized communication architecture optimizes resources while maintaining robust error handling and seamless integration between mission components.

This system exemplifies how to build a robust, multi-node communication framework on top of a specialized UDP-based protocol in an extreme environment. By appointing the Lunar Rover as the central communications relay, we minimize complexity and cost for smaller or more specialized nodes, such as the Tunneller and Hopper. At the same time, the JUMPER Protocol ensures data integrity, reliability, and efficiency—essential requirements for successful lunar missions.

The project’s architecture and code demonstrate: • How to establish reliable UDP-based comms among multiple nodes.
• The benefits of a single Earth-Moon communication link rather than many.
• A layered approach that uses compression, encryption, HMAC validation, Reed-Solomon error correction, and ACK/NAK retransmissions.
• A modular design that can be extended to other networked space applications.

[Divyum Singhal]
