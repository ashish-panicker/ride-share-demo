package com.rideshare.ride;

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
