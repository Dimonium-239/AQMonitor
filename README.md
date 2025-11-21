## Air Quality Monitor API

API for making CRUD operations on Air Quality data. 
API saves, returns list of measurements, updates and delete.
For each of these operations chosen correct and specific HTTP methods.

### Installation
!!! Before installation Docker should be installed and running
```bash
git clone https://github.com/Dimonium-239/AQMonitor.git
cd AQMonitor/
docker compose up --build
```

### Swagger
[LOCAL] http://localhost:8080/docs

[DEV] https://chosen-noami-dimonium-239-f939ab63.koyeb.app/docs

### Database
Database is deployed on Render service and is available for LOCAL and for DEV environment.

This helps to have data be persisted for long time and display it