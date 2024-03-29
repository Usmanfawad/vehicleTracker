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