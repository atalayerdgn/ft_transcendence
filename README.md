# **Ft_transcendence**
---

**ft_transcendence** is a modern project that reimagines the classic Pong game with a focus on scalability, security, and advanced gameplay features. By leveraging microservices architecture and modern web technologies, we have created a robust and dynamic platform that goes beyond the traditional Pong experience.


## **Project Overview**

This project focuses on creating a modern and secure platform using advanced technologies and design principles. We built a REST API with the **Django framework**, following **Clean** and **Onion Architecture** to ensure a maintainable and scalable structure.

We explored **microservices** to divide the system into smaller, independent components and used **Docker** for easy deployment. An **API Gateway** was implemented to route requests to the correct services, while **middleware** ensures security by validating **JWT tokens**.

The frontend is designed as a **Single Page Application (SPA)** for dynamic updates without reloading. We also used **Three.js** to create a visually engaging 3D game experience.

To enhance user security, we added **Two-Factor Authentication (2FA)** and **SMTP** for email services.

This project combines **scalability**, **security**, and **dynamic features** to deliver a robust and innovative platform.


## **Modules Overview**

The project is organized into several **major** and **minor** modules, each contributing to a specific aspect of functionality, architecture, or usability. Below is a detailed summary:


### **1. Web Modules**

- **Major Module: Use a Framework to Build the Backend**  
  The backend is developed using the **Django framework**. Clean and Onion Architecture are implemented to ensure clear separation of concerns, maintainability, and scalability.

- **Minor Module: Use a Framework or Toolkit to Build the Frontend**  
  The frontend is built with **vanilla JavaScript** and **Bootstrap**, offering a dynamic and responsive user interface that enhances usability and design consistency.

- **Minor Module: Use a Database for the Backend**  
  **PostgreSQL** is utilized as the backend database to ensure data consistency, high performance, and seamless integration with the system's components.


### **2. User Management Modules**

- **Major Module: Standard User Management and Authentication**  
  Features secure user registration, login, and profile management. Users can:  
  - Set unique display names.  
  - Upload avatars.  
  - View match history.  
  - Add friends and track their online status.  

- **Major Module: Implement Two-Factor Authentication (2FA) and JWT**  
  Implements **2FA** for added security, allowing users to verify their identity using a secondary method like email or an authenticator app.  
  **JSON Web Tokens (JWT)** are used to manage secure authentication and session validation.


### **3. DevOps Modules**

- **Major Module: Designing the Backend as Microservices**  
  The backend is designed using a **microservices architecture**. Each service handles a specific functionality, promoting:  
  - Modularity  
  - Scalability  
  - Independent deployment  
  Services communicate seamlessly via **RESTful APIs**.


### **4. Graphics Modules**

- **Major Module: Implementing Advanced 3D Techniques**  
  The game leverages **Three.js/WebGL** to implement advanced 3D graphics.  
  This creates a **visually immersive** and engaging gaming experience, elevating the classic Pong gameplay.


### **5. Accessibility Modules**

- **Minor Module: Support on All Devices**  
  The platform is fully responsive, ensuring compatibility across desktops, tablets, and smartphones. It provides:  
  - Consistent user experiences.  
  - Adaptation to various screen sizes and orientations.  
  - Support for touch, mouse, and keyboard inputs.


####
These modules collectively deliver a **secure**, **scalable**, **visually stunning**, and **user-friendly** enhancement of the classic Pong game. The project sets a strong foundation for future enhancements and innovations while showcasing modern development techniques and architectures.

---

# **Ft_transcendence - Setup Instructions**

### Follow the steps below to set up and run the project locally.

## **Requirements:**

Before you begin, ensure that you have the following tools installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## **Steps:**

### 1. Clone the Repository

Clone the repository to your local machine:

    git clone https://github.com/Uchimann/ft_transcendence.git

### 2. Navigate to the Project Directory

Change to the project directory:

    cd ft_transcendence

### 3. Set Up Environment Variables

Configure the necessary environment variables

### 4. Build the Docker Containers

Use Docker Compose to build and start the project:

    docker-compose up --build

### 5. Access the Application

Once the build is complete, open your browser and go to the following address:

    https://localhost:8008

