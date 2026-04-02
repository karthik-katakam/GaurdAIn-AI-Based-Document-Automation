# NJ-Courts





## Things to install  

### **All Required Packages** 

To download all reqiured packages, just CD into the directory with the `package.json` file and type `npm install`


### **PostGres Database Instance**  


The PostGres database contains the case-listing information that is dynamically displayed on the case-listing page. It is hosted on a container on dockerhub so that anyone can pull the database instance and data. To get the data:  
1. Have Docker Desktop installed & configured in your machine
2. Have a Docker account configured to your Docker Desktop
3. In the terminal(Assuming Linux/Unix Terminal): Docker PULL the PostGres Database Instance from [this repository](https://hub.docker.com/repository/docker/alveejalal/guardain-postgres)
4. Docker PULL the PGAdmin Console (for GUI access to the database) from [this repository](https://hub.docker.com/repository/docker/alveejalal/guardain-pgadmin/general)
5. CD into the correct directory with the Docker-compose file
6. Type the command in the Terminal: `docker-compose up --build -d`




