package com.rideshare.passenger;

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
