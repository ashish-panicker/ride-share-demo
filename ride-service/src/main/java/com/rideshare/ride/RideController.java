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
