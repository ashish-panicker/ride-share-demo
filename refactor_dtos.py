import os

passenger_dto = """package com.rideshare.passenger;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public record PassengerDto(
    Long id,
    @NotBlank String name,
    @NotBlank @Email String email
) {}
"""

passenger_controller = """package com.rideshare.passenger;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/passengers")
public class PassengerController {
    private static final Logger log = LoggerFactory.getLogger(PassengerController.class);
    private final PassengerRepository repository;

    public PassengerController(PassengerRepository repository) {
        this.repository = repository;
    }

    private PassengerDto mapToDto(Passenger p) {
        return new PassengerDto(p.getId(), p.getName(), p.getEmail());
    }

    @GetMapping
    public List<PassengerDto> getAll() {
        log.info("Fetching all passengers");
        return repository.findAll().stream().map(this::mapToDto).collect(Collectors.toList());
    }

    @GetMapping("/{id}")
    public PassengerDto getById(@PathVariable Long id) {
        log.info("Fetching passenger {}", id);
        return repository.findById(id).map(this::mapToDto).orElseThrow(() -> new RuntimeException("Not found"));
    }

    @PostMapping
    public PassengerDto create(@Valid @RequestBody PassengerDto dto) {
        log.info("Creating passenger {}", dto.name());
        Passenger passenger = new Passenger();
        passenger.setName(dto.name());
        passenger.setEmail(dto.email());
        Passenger saved = repository.save(passenger);
        return mapToDto(saved);
    }
}
"""

ride_dto = """package com.rideshare.ride;

import jakarta.validation.constraints.NotNull;

public record RideDto(
    Long id,
    @NotNull Long passengerId,
    Long driverId,
    String status
) {}
"""

ride_controller = """package com.rideshare.ride;

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

    private RideDto mapToDto(Ride r) {
        return new RideDto(r.getId(), r.getPassengerId(), r.getDriverId(), r.getStatus());
    }

    @PostMapping
    public RideDto createRide(@Valid @RequestBody RideDto dto) {
        log.info("Requesting ride for passenger {}", dto.passengerId());
        String passengerInfo = passengerClient.getPassenger(dto.passengerId());
        log.info("Passenger info: {}", passengerInfo);
        
        Ride ride = new Ride();
        ride.setPassengerId(dto.passengerId());
        ride.setDriverId(dto.driverId());
        ride.setStatus("REQUESTED");
        
        Ride saved = repository.save(ride);
        return mapToDto(saved);
    }
    
    @GetMapping("/{id}")
    public RideDto getRide(@PathVariable Long id) {
        return repository.findById(id).map(this::mapToDto).orElseThrow(() -> new RuntimeException("Not found"));
    }
}
"""

with open("passenger-service/src/main/java/com/rideshare/passenger/PassengerDto.java", "w") as f:
    f.write(passenger_dto)
with open("passenger-service/src/main/java/com/rideshare/passenger/PassengerController.java", "w") as f:
    f.write(passenger_controller)

with open("ride-service/src/main/java/com/rideshare/ride/RideDto.java", "w") as f:
    f.write(ride_dto)
with open("ride-service/src/main/java/com/rideshare/ride/RideController.java", "w") as f:
    f.write(ride_controller)

