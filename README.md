# **Cryptographically secured E-Voting system**  

This project is a secure electronic voting system that ensures voter authenticity and environmental validation before allowing a user to cast a vote. The system uses a **client-server architecture** involving:  
1. **Voter Interface**.  
2. **Verification Server** to verify voter identity and status.  
3. **Tallying Server** to record and store encrypted votes.

It additionally performs **environment checks**, including **face detection** using a Haar cascade classifier and **sound level monitoring**, to ensure the voting environment meets defined criteria.

---

## **Features**  

1. **Secure Voter Verification**:  
   - Uses digital certificates signed with the voter's private key.  
   - Public key verification on the server ensures authenticity.

2. **Environment Validation**:  
   - Face detection ensures exactly one person is in the frame.  
   - Sound level threshold prevents voting in noisy environments.  
   - Live video feed displayed during validation.  

3. **Encrypted Voting**:  
   - Votes are encrypted using Paillier encryption for confidentiality.  

4. **Distributed Architecture**:  
   - **Verification Server** verifies voter identity and updates voting status.  
   - **Tallying Server** maintains the vote count.  

5. **JSON-based Storage**:  
   - Voter details (status) and tallies are stored in JSON files for simplicity.  


---
## **Project Structure**  

```
evoting-cryptography-cybersec/
├── voter/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   ├── vote.html
│   │   ├── index.html
│   │   ├── failure.html
│   │   └── success.html
│   ├── client_private_key.pem
│   ├── public_key_server.json
│   └── app.py
├── tallying server/
│   ├── public_key_server.json
│   ├── server.py
│   ├── tally.json
├── verification server/
│   ├── client_public_key.pem
│   ├── server.py
│   ├── voter_data.json
├── requirements.txt
├── README.md
└──
```

---

## **Setup Instructions**  

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/mukvnd/evoting-cryptography-cybersec.git
   cd evoting-cryptography-cybersec
   ```

2. **Install Dependencies**:  
   Ensure Python 3.8 or above is installed. Run:  
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Servers**:  
   Open two terminal windows:  
   - Start the **Verification Server**:  
     ```bash
     cd verification server
     python verification_server.py
     ```  
   - Start the **Tallying Server**:  
     ```bash
     cd tallying server
     python tallying_server.py
     ```  

4. **Run Voter Application**:  
   Start the Flask app:  
   ```bash
   cd voter
   python app.py
   ```  

5. **Access the Application**:  
   Open your browser and navigate to:  
   ```
   http://127.0.0.1:5000
   ```  

---

## **Error Codes and Messages**  

| **Error Code** | **Error Message**                 | **Suggested Fix**                                          |  
|----------------|-----------------------------------|----------------------------------------------------------|  
| 400            | Voter not found                  | Ensure voter ID is registered in `voter_data.json`.     | 
| 401            | Invalid signature                | Verify the private key and digital certificate.          |  
| 402            | Invalid vote                     | Ensure proper voting for the tallying server            |  
| 403            | Voter already voted              | Avoid multiple votes from the same voter ID.            |  
| 500            | Internal server error            | Check server logs for more details on the issue.        |   

---

## **Generating Keys Using OpenSSL (NOT REQUIRED, ALREADY PRESENT)**

### **1. Install OpenSSL**

OpenSSL is required to generate the public/private key pairs. To install it on a Linux machine, use the following commands:

```bash
sudo apt update
sudo apt install openssl
```
### **3. Generate RSA Keys**
#### **Generate RSA Private Key:**

To generate a 2048-bit RSA private key and save it in a file named `private_key.pem`:

```bash
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```

#### **Extract the Corresponding Public Key:**

To generate the public key from the private key and save it to a file named `public_key.pem`:

```bash
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

### **3. Generate ECDSA Keys**

#### **Generate ECDSA Private Key:**

To generate an ECDSA private key using the `prime256v1` curve:

```bash
openssl ecparam -genkey -name prime256v1 -out private_key.pem
```

#### **Extract the Corresponding ECDSA Public Key:**

To generate the public key from the private key:

```bash
openssl ec -in private_key.pem -pubout -out public_key.pem
```

### **4. Encrypt Private Key (Password Protected)**

To generate an encrypted private key (password protected), you can use:

```bash
openssl genpkey -algorithm RSA -aes256 -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```

You will be prompted to enter a password, and the private key will be encrypted.

---

## **Assumptions**
- The system assumes that both the client and the server have their own **public** and **private** key pairs, which are used for secure voting and identity verification.
- The keys can be generated using OpenSSL, and are saved in PEM format for compatibility with the system.
- The environment of the voter (face detection and sound level) must meet specific thresholds before allowing the vote to be submitted.
- The **addresses** of the **Verification Server** and **Tally Server** are assumed to be configured as:
    - **Verification Server**: `http://127.0.0.1:5001`
    - **Tally Server**: `http://127.0.0.1:5002`

---

## **Future Enhancements**  

1. Integration with blockchain for immutable voting records.  
2. Biometric-based authentication for enhanced voter validation.  
3. Scalability improvements for nationwide voting.
4. Better cryptographic methods for enhanced security.

---

## **Contributors**  
- **Mukund Khandelwal**: [GitHub Profile](https://github.com/mukvnd)  
- **Spoorthi C Bhoji**: [GitHub Profile](https://github.com/spoorthibhoji)  

Feel free to contribute and submit issues via the repository!  

--- 



