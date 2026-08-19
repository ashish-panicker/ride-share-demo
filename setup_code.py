import os

passenger_dir = "passenger-service/src/main/java/com/rideshare/passenger"
ride_dir = "ride-service/src/main/java/com/rideshare/ride"

passenger_files = {
    "Passenger.java": """package com.rideshare.passenger;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

@Entity
public class Passenger {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    private String name;

    @Email
    @NotBlank
    private String email;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
""",
    "PassengerRepository.java": """package com.rideshare.passenger;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PassengerRepository extends JpaRepository<Passenger, Long> {
}
""",
    "PassengerController.java": """package com.rideshare.passenger;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/passengers")
public class PassengerController {
    private static final Logger log = LoggerFactory.getLogger(PassengerController.class);
    private final PassengerRepository repository;

    public PassengerController(PassengerRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<Passenger> getAll() {
        log.info("Fetching all passengers");
        return repository.findAll();
    }

    @GetMapping("/{id}")
    public Passenger getById(@PathVariable Long id) {
        log.info("Fetching passenger {}", id);
        return repository.findById(id).orElseThrow(() -> new RuntimeException("Not found"));
    }

    @PostMapping
    public Passenger create(@Valid @RequestBody Passenger passenger) {
        log.info("Creating passenger {}", passenger.getName());
        return repository.save(passenger);
    }
}
"""
}

ride_files = {
    "Ride.java": """package com.rideshare.ride;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.validation.constraints.NotNull;

@Entity
public class Ride {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotNull
    private Long passengerId;

    private Long driverId;
    private String status;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getPassengerId() { return passengerId; }
    public void setPassengerId(Long passengerId) { this.passengerId = passengerId; }
    public Long getDriverId() { return driverId; }
    public void setDriverId(Long driverId) { this.driverId = driverId; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}
""",
    "RideRepository.java": """package com.rideshare.ride;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RideRepository extends JpaRepository<Ride, Long> {
}
""",
    "PassengerClient.java": """package com.rideshare.ride;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;

@Component
public class PassengerClient {
    private static final Logger log = LoggerFactory.getLogger(PassengerClient.class);
    private final RestClient restClient;

    public PassengerClient(RestClient.Builder builder) {
        // Will rewrite URL later for Eureka, using localhost for Phase 2 test
        this.restClient = builder.baseUrl("http://localhost:8081").build();
    }

    @CircuitBreaker(name = "passengerService", fallbackMethod = "fallbackGetPassenger")
    public String getPassenger(Long id) {
        log.info("Calling passenger service for id: {}", id);
        return restClient.get()
                .uri("/api/passengers/{id}", id)
                .retrieve()
                .body(String.class);
    }

    public String fallbackGetPassenger(Long id, Throwable t) {
        log.error("Passenger service is down, fallback triggered for id: {}. Error: {}", id, t.getMessage());
        return "{\\"fallback\\": true, \\"message\\": \\"Passenger service unavailable\\"}";
    }
}
""",
    "RideController.java": """package com.rideshare.ride;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/rides")
public class RideController {
    private static final Logger log = LoggerFactory.getLogger(RideController.class);
    private final RideRepository repository;
    private final PassengerClient passengerClient;

    public RideController(RideRepository repository, PassengerClient passengerClient) {
        this.repository = repository;
        this.passengerClient = passengerClient;
    }

    @PostMapping
    public Ride createRide(@Valid @RequestBody Ride ride) {
        log.info("Requesting ride for passenger {}", ride.getPassengerId());
        String passengerInfo = passengerClient.getPassenger(ride.getPassengerId());
        log.info("Passenger info: {}", passengerInfo);
        
        ride.setStatus("REQUESTED");
        return repository.save(ride);
    }
    
    @GetMapping("/{id}")
    public Ride getRide(@PathVariable Long id) {
        return repository.findById(id).orElseThrow(() -> new RuntimeException("Not found"));
    }
}
"""
}

for name, content in passenger_files.items():
    with open(os.path.join(passenger_dir, name), "w") as f:
        f.write(content)

for name, content in ride_files.items():
    with open(os.path.join(ride_dir, name), "w") as f:
        f.write(content)

