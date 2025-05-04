# Dev Branch
# Web Application with Docker, Docker Compose, and NGINX

This project involves building and deploying a web application with Docker, Docker Compose, and NGINX as a reverse proxy. The application integrates with MongoDB and Redis, with Docker used for containerization and NGINX used to serve the app securely with SSL certificates.

## Project Overview

This project is divided into multiple tasks:

- **Task 1 (Linux Machine)**: 
  - Set up an SSH key pair for access.
  - Access a machine and gather important specs, including CPU count, RAM, disk space, and the operating system details.
  - Prepare the workspace for further tasks.

- **Task 2 (Docker)**: 
  - Develop a web application that counts user access, integrates with MongoDB and Redis, and saves the user’s IP address.
  - The application is dockerized, and the images are pushed to DockerHub.

- **Task 3 (Docker-Compose)**: 
  - Set up Docker Compose to manage the web application, MongoDB, and Redis, ensuring that all services can be easily configured using environment variables.

## Setup Instructions

To run the application, MongoDB, and Redis, follow these steps:

1. **App, MongoDB, and Redis Setup**:
   - The application, MongoDB, and Redis are created and run as separate containers.
   - These containers can be run manually using Docker or managed together with Docker Compose.

2. **Running the Containers with Docker**:
   - First, build the Docker images for each container (app, MongoDB, and Redis).
   - Run the MongoDB and Redis containers first. Ensure they are up and running before connecting the app to them.
   - Use Docker's networking feature to connect the app to the MongoDB and Redis containers directly.

3. **Running with Docker Compose**:
   - Alternatively, use **Docker Compose** to manage all containers (app, MongoDB, and Redis) together.
   - Docker Compose allows you to define and run multi-container applications with a single command.
   - It simplifies the process of running the containers with the necessary configurations, including environment variables.

## Installation

Follow the steps below to set up the required dependencies and install Docker, Node.js, and Python:

1. **Update the System**:
   ```bash
   sudo apt update
   sudo apt upgrade -y
2.Install Node.js and npm:
sudo apt install nodejs npm
3. Install Python 3 and pip:
sudo apt update
sudo apt install python3 python3-pip

4. Install Docker:
   Step 1: Update system packages and install required dependencies:
   sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
Step 2: Add Docker’s Official GPG Key:
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
Step 3: Add Docker Repository:
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
Step 4: Install Docker Engine:
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
Step 5: Start Docker and enable it to start on boot:
sudo systemctl start docker
sudo systemctl enable docker
Step 6: Verify the installation:
sudo docker --version
Step 7: (Optional) Run Docker without sudo:
sudo usermod -aG docker \$USER
docker run hello-world


Running the Application
Once the code has been completed and the Docker images are built, follow the instructions below to run the containers:

Using Docker:
Build the Docker Image:
docker build -t your-app-name .
Run the Containers (MongoDB, Redis, and the Application):

First, start the MongoDB container:
docker run -d --name mongo-container -p 27017:27017 mongo

Next, run the Redis container:
docker run -d --name redis-container -p 6379:6379 redis

Then, run the application container (connect it to the MongoDB and Redis containers using a Docker network):
docker run -d --name app-container --network your-network-name -p 8080:8080 your-app-name

Create a Docker Network:
docker network create your-network-name

Using Docker Compose:
Create the docker-compose.yml File:
version: '3'
services:
  app:
    image: your-app-name
    ports:
      - "8080:8080"
    environment:
      - MONGO_URI=mongodb://mongo:27017
      - REDIS_HOST=redis
  mongo:
    image: mongo
    ports:
      - "27017:27017"
  redis:
    image: redis
    ports:
      - "6379:6379"


2.Run All Services:
docker-compose up -d


Configuration
The application uses the following configuration files for MongoDB and Redis:

MongoDB Configuration (mongod.conf):
net:
  port: 27017
  bindIp: 0.0.0.0

security:
  authorization: disabled

Redis Configuration (redis.conf):
bind 0.0.0.0
protected-mode yes
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300
daemonize no
supervised no
pidfile /var/run/redis_6379.pid
loglevel notice
logfile ""
databases 16
save 900 1
save 60 10000
stop-writes-on-bgsave-error yes
requirepass yousef123
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data

Testing
Testing was carried out throughout the project in sections to ensure each component was functioning correctly. The following steps were involved in the testing process:

Individual Testing:

Each component (MongoDB, Redis, and the application) was tested independently.

MongoDB and Redis were tested by checking connectivity and functionality via their respective ports.

The application was tested by ensuring it could properly connect to both MongoDB and Redis, count user accesses, and save the user data.

Integration Testing:

After ensuring each component worked independently, integration tests were conducted to verify that the application could communicate correctly with MongoDB and Redis through Docker networks or Docker Compose.

The health check for the application was tested on a specific route (e.g., /health) to confirm it returned an HTTP status 200 with the "OK" message.

Troubleshooting:

Issues encountered during testing were primarily related to container communication. This was resolved by ensuring the correct Docker network was created, allowing containers to communicate with each other.

Another challenge involved ensuring proper environment variable configuration for MongoDB and Redis connections, which was resolved by using Docker Compose's environment variable passing feature.

Build and Push to Docker Hub:

After every modification made to the application, it was necessary to rebuild the Docker image to ensure that the changes were reflected properly.

Rebuild the Docker Image:


docker build -t your-app-name .
Push to Docker Hub:


docker push your-app-name
Deployment
To deploy the application, we can follow these steps:

Using Docker:

Build the Docker images for the application, MongoDB, and Redis as needed.

Run the containers either individually using Docker or by using Docker Compose to handle all containers together.

Ensure the correct environment variables are configured, especially for MongoDB and Redis connections.

Using Docker Compose:

For ease of deployment, use Docker Compose to start all services together with a single command.

Docker Compose ensures that the containers are networked correctly and simplifies environment variable management.

To deploy the application with Docker Compose:


docker-compose up -d
NGINX Reverse Proxy Setup:

NGINX acts as a reverse proxy to the web application, ensuring secure communication through SSL certificates.

Configure NGINX with SSL certificates generated by Let's Encrypt for secure HTTPS connections.

To deploy NGINX and ensure it starts automatically with the server, configure it as a systemd service:

Start NGINX manually:

sudo systemctl start nginx
Enable NGINX to start on boot:


sudo systemctl enable nginx
SSL Certificate:

Use Let’s Encrypt to generate and configure SSL certificates for secure communication.

To generate SSL certificates for your domain, you can use the certbot tool:


sudo certbot --nginx
Ensure that the NGINX configuration points to the correct SSL certificate and key files.

Extra Features
Health Check Endpoint:

A health check route has been implemented at /health. This endpoint is designed to provide the status of the application.

When the endpoint is accessed, it returns an HTTP status code of 200 along with an "OK" message, indicating that the application is running properly.

Example:

Accessing http://your-domain/health will return:

json
Copy
{
  "status": "OK"
}
NGINX Auto-Start on Reboot:

EXTRA 1: Ensure that the NGINX service will start automatically when the machine reboots.

After setting up NGINX as a reverse proxy, configure it as a systemd service to ensure it starts on boot:

To enable NGINX to start on reboot, run the following command:


sudo systemctl enable nginx
Contributing
We welcome contributions to this project! If you'd like to contribute, please follow these guidelines:

Fork the Repository:

Fork the repository to your own GitHub account to make changes.

Clone the Repository:

Clone your fork to your local machine:


git clone https://github.com/your-username/repository-name.git
Create a New Branch:

Create a new branch for the changes you want to make:


git checkout -b feature-name
Make Changes:

Make the necessary changes in the code or documentation.

Be sure to follow the coding standards and conventions used in the project.

Commit Changes:

Commit your changes with clear and concise commit messages:


git commit -m "Add a brief description of the changes"
Push Changes:

Push the changes to your fork on GitHub:


git push origin feature-name
Create a Pull Request:

Open a pull request (PR) on the original repository, describing your changes and why they should be merged.

Code Reviews:

After submitting the PR, your changes will be reviewed by the project maintainers.

Be open to feedback and willing to make any necessary changes before the PR is merged.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Copy
Save the File:
After pasting the content into the README.md, save the file.

