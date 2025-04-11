# VPN Project
VPN implementation in Python for Linux (and potentially other Unix-like operating systems).

Tested with **Python 3.12.6**

Create a tunnel interface (requires superuser permissions):

Run
```shell
docker-compose build
docker-compose up
docker ps

# Validate no connectivity between client and internal host
docker exec -it <client-container-id> ping 192.168.60.7

# Start VPN client and server
docker exec -it <client-container-id> /volumes/client/client.py &
docker exec -it <server-container-id> /volumes/server/server.py &

# Validate the connectivity between client and internal host
docker exec -it <client-conatiner-id> ping 192.168.60.7
```

## Project Milestones
- [x] Virtual interface created and data encapsulated inside the VPN's UDP packets  
- [x] UDP packet sent by VPN from one device to another  
- [x] Basic UDP client–server communication established; packets can be sent both ways  
- [ ] Basic encryption/decryption method implemented for securing network traffic  
- [ ] Authentication configured  
- [ ] Performance testing conducted with iperf  
- [ ] Functional prototype deployed  
- [ ] User guides developed  
- [ ] Technical documentation developed  

## Functional Requirements
- [ ] Working prototype developed to align with the client–server model (Jing et al., 1999, p. 30)
- [ ] Encryption implemented using asymmetric algorithms like ECDSA, ML–DSA, ML–DLM, and AES–256 (Australian Cyber Security Centre, 2025, p. 178) or the newly developed quantum–resistant FIPS–203 standard (NIST, 2024) 
- [ ] User authentication  
- [ ] UDP tunnelling 
- [ ] Verbose logging and debugging features
- [ ] Virtual interface implemented to facilitate network communication

## Non–Functional Requirements
- [ ] Resource usage kept at a minimum
- [ ] Low–latency
- [ ] Adhering to industry–standard encryption protocols
<br>

---

##### References  
  
###### Australian Cyber Security Centre. (2025). *Information security manual (ISM) (March 2025 ed.).* Australian Signals Directorate. https://www.cyber.gov.au/resources-business-and-government/essential-cybersecurity/ism

###### Jing, J., Helal, A. S., & Elmagarmid, A. (1999). *Client-server computing in mobile environments.* ACM Computing Surveys (CSUR), *31(2)*, 117-157. [https://doi.org/10.1145/319806.31981](https://doi.org/10.1145/319806.31981)  

###### National Institute of Standards and Technology (NIST). (2024). *Module-Lattice-Based Key-Encapsulation Mechanism Standard.* [https://doi.org/10.6028/NIST.FIPS.203](https://doi.org/10.6028/NIST.FIPS.203)
