# vehicleTracker
This repository uses DistanceMatrix.ai API and Logger Android application and provides REST services for tracking your vehicle.

## Quick Start

1. **Clone the Repository:**

   ```shell
   git clone https://github.com/Usmanfawad/vehicleTracker
    ```
   
2. **Create and activate a virtual environment for Linux:**

   ```shell
   python -m venv venv
   source venv/bin/activate
   ```

3. **Create and activate a virtual environment for Windows:**

   ```shell
   python -m venv venv
   venv/Scripts/activate
   ```
   
4. **Install the requirements:**

   ```shell
    pip install -r requirements.txt
    ```


5. **Run the app.**

   ```shell
   uvicorn app.main:app--reload
   ```

   

## Docker 

   ```shell
   docker build --tag matleo-image .  
   ```

   ```shell
   docker run --name matleo-container -p 8000:8000 matleo-image
   ```

## End points 

The best endpoint explanation can be looked at the Swagger API documentation under the root URL/docs


[URL to Swagger documentation](https://vehicle-tracker-f73518128155.herokuapp.com/docs "Swagger docs")

## Azure Setup

The Vehicle Tracker is deployed in the Azure Cloud using Azure Container Apps and reachable under the following URL:
https://tracker.befriends.me/app/v1/bus_stops

Note the Endpoint is mTLS protected. Follow the Initial Setup to setup mTLS.

### Initial Setup

#### mTLS Installation Keychain

To Install the mTLS certificate in Keychain open Keypass download and execute server-cert.p12 file from the BE Friends MTLS Cert.
Use the password from the entry for the installation. After the Installation the URL above is reachable.


#### mTLS using Curl

Follow the instruction above. To request the API via Curl download the server-cert.pem and server-key.pem and execute the following Code-Snipped:
```
url https://tracker.befriends.me/app/v1/bus_stops --cert server-cert.pem  --key server-key.pem
```

### Database

#### Connect via MySQL Workbench

Connect to the MySQL Database using the DB Credentials from Keypass and Set the mysql-client-ca-crt.pem as 

![img.png](images/img.png)
![img.png](img.png)

### Deployment

#### Deployment via VCS

To Deploy an new version 
