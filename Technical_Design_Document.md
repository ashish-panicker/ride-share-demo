# Ride Share Application - Technical Design Document

## 1. Overview
This document outlines the architecture and design of a microservices-based Ride Share demo application using Spring Boot. The goal is to build two interacting microservices and demonstrate the use of key Spring Cloud components: Eureka Server, API Gateway, RestClient, and Circuit Breaker.

## 2. Proposed Microservices
We will build the following two microservices:

### A. Passenger Service
Manages passenger information and profiles.
- **Database:** In-memory H2 database with `schema.sql` and `data.sql`.
- **Endpoints:**
  - `POST /passengers` - Register a new passenger (includes validation).
  - `GET /passengers/{id}` - Retrieve passenger details.
  - `PUT /passengers/{id}` - Update passenger details.

### B. Ride Service
Manages ride requests and trip lifecycle. It will communicate with the Passenger Service to verify passenger details before initiating a ride.
- **Database:** In-memory H2 database with `schema.sql` and `data.sql`.
- **Endpoints:**
  - `POST /rides` - Request a new ride (includes payload validation).
  - `GET /rides/{id}` - Get ride status.
  - `PUT /rides/{id}/status` - Update the ride status (e.g., STARTED, COMPLETED).
- **Integration:** Uses `RestClient` to fetch data from the Passenger Service.

## 3. Architecture & Components

The application will leverage the following Spring Cloud features:

- **Service Registry (Eureka Server):** Both `Passenger Service` and `Ride Service` will register themselves with the Eureka Server. This allows for dynamic service discovery.
- **API Gateway:** A single entry point for all client requests. It will route traffic to the respective microservices based on the URL path (e.g., `/api/passengers/**` to Passenger Service, `/api/rides/**` to Ride Service).
- **Synchronous Communication (RestClient):** The `Ride Service` will use Spring's modern `RestClient` to make HTTP calls to the `Passenger Service`.
- **Fault Tolerance (Circuit Breaker):** We will implement a Circuit Breaker (via Resilience4j) on the `RestClient` calls within the `Ride Service`. If the `Passenger Service` is down or unresponsive, the Circuit Breaker will prevent cascading failures and return a fallback response.

## 4. Technology Stack
- **Framework:** Spring Boot
- **Language:** Java
- **Database:** H2 In-Memory Database (Spring Data JPA)
- **Validation:** Spring Boot Starter Validation
- **Cloud Components:** Spring Cloud Netflix Eureka, Spring Cloud Gateway, Resilience4j

## 5. Next Steps
Once this design is reviewed and approved, we will proceed with:
1. Generating the Spring Boot projects (Eureka Server, API Gateway, Passenger Service, Ride Service).
2. Implementing the core entities, repositories, and controllers with validation.
3. Setting up H2 database schemas.
4. Integrating inter-service communication and resilience.
