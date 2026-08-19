package com.rideshare.passenger;

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
