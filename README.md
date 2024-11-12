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

### **Flow of the Program**

The program operates in a multi-step process, where the voter interacts with the system, their identity is verified, and their vote is securely cast and counted.

1. **Voter Login**:
   - The voter navigates to the **E-Voting Portal** and is presented with a form asking for their **Voter ID** and the **candidate** they wish to vote for.
   - Before the voter can submit their vote, the environment is checked to ensure the conditions are safe for voting.

2. **Environment Check**:
   - **Face Detection**: The system uses **Haar Cascade face detection** to ensure that exactly one face is detected in the environment. If more than one face is detected or if no face is detected, the voter will be denied access to vote.
   - **Sound Level Detection**: The system uses **PyAudio** to measure the ambient sound level. If the sound level exceeds a pre-defined threshold, the voter is not allowed to vote, as excessive background noise could indicate fraudulent activity.

3. **Vote Submission**:
   - If the environment check passes (exactly one face is detected, and sound level is below the threshold), the voter can proceed to submit their vote.
   - The voter signs their vote using their **private key** to ensure it is authentic and tamper-proof.
   - A **digital signature** is created by hashing the **Voter ID** (using SHA-256) and then signing it with the **private key** of the voter. This signed hash ensures that the vote comes from a verified voter and prevents anyone from altering the vote after submission.
   - The **public key** of the voter (corresponding to the private key used for signing) is also sent to the verification server to enable the server to verify the authenticity of the signature.

4. **Vote Verification**:
   - The signed vote and the public key of the voter are sent to the **Verification Server**.
   - The Verification Server uses the public key to verify the signature of the vote. This confirms that the vote has been signed by the rightful voter and that it has not been tampered with.
   - If the verification is successful, the voter is marked as **voted** on the server, and they can proceed to cast their vote.

5. **Vote Encryption**:
   - Once the vote is verified, it is then **encrypted** before being sent to the **Tally Server**.
   - The **Tally Server** has a **public key** that is used to encrypt the vote. The voter’s vote is encrypted using this public key, ensuring that only the **Tally Server** (which possesses the corresponding private key) can decrypt and read the vote.
   - The encrypted vote is then securely transmitted to the **Tally Server**.

6. **Vote Tallying**:
   - Upon receiving the encrypted vote, the **Tally Server** decrypts it using its **private key**.
   - The Tally Server increments the vote count for the chosen candidate and returns a success message to the voter.

7. **Vote Confirmation**:
   - If the vote submission is successful, the voter is notified with a confirmation message, and they are redirected to a success page.
   - In case of any failure during the process (e.g., if the voter has already voted, or if there is a problem with verification), the voter will be shown an error message explaining the reason for failure.

---

## **Generating Keys Using OpenSSL (NOT REQUIRED, ALREADY PRESENT)**

### **1. Install OpenSSL**

OpenSSL is required to generate the public/private key pairs. To install it on a Linux machine, use the following commands:

```bash
sudo apt update
sudo apt install openssl
```

### **2. Generate RSA Keys**

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

### **3. Generate ECDSA Keys (If Using Elliptic Curve Cryptography)**

#### **Generate ECDSA Private Key:**

To generate an ECDSA private key using the `prime256v1` curve (standard for many systems):

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
## Assumptions
- The system assumes that both the client and the server have their own **public** and **private** key pairs, which are used for secure voting and identity verification.
- The keys can be generated using OpenSSL, and are saved in PEM format for compatibility with the system.
- The environment of the voter (face detection and sound level) must meet specific thresholds before allowing the vote to be submitted.
- The **addresses** of the **Verification Server** and **Tally Server** are assumed to be configured as:
    - **Verification Server**: `http://127.0.0.1:5001`
    - **Tally Server**: `http://127.0.0.1:5002`

## **Future Enhancements**  

1. Multi-language support for user interfaces.  
2. Integration with blockchain for immutable voting records.  
3. Biometric-based authentication for enhanced voter validation.  
4. Scalability improvements for nationwide voting.  

---

## **Contributors**  
- **Mukund Khandelwal**: [GitHub Profile](https://github.com/mukvnd)  
- **Spoorthi C Bhoji**: [GitHub Profile](https://github.com/spoorthibhoji)  

Feel free to contribute and submit issues via the repository!  

--- 




Here’s the additional assumption you can add to the **Assumptions** section in the README:

---

### **Assumptions**

- The system assumes that both the client and the server have their own **public** and **private** key pairs, which are used for secure voting and identity verification.
- The keys can be generated using OpenSSL, and are saved in PEM format for compatibility with the system.
- The environment of the voter (face detection and sound level) must meet specific thresholds before allowing the vote to be submitted.
- The **addresses** of the **Verification Server** and **Tally Server** are assumed to be configured as:
    - **Verification Server**: `http://127.0.0.1:5001`
    - **Tally Server**: `http://127.0.0.1:5002`

---

This adds the assumption regarding the server addresses to the README.