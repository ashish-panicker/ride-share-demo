package com.example.pasenger_service.controller;

import com.example.pasenger_service.dto.PassengerDto;
import com.example.pasenger_service.service.PassengerService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;

import java.util.List;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api/passengers")
public class PassengerController {
    private final PassengerService passengerService;

    public PassengerController(PassengerService passengerService) {
        this.passengerService = passengerService;
    }

    @GetMapping
    public List<PassengerDto> getAllPassengers() {
        return passengerService.getAllPassengers();
    }

    @GetMapping("/{id}")
    public PassengerDto getPassengerById(@PathVariable Long id) {
        return passengerService.getPassengerById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public PassengerDto createPassenger(@Valid @RequestBody PassengerDto dto) {
        return passengerService.createPassenger(dto);
    }
    
    @PutMapping("/{id}")
    public PassengerDto updatePassenger(@PathVariable Long id, @Valid @RequestBody PassengerDto dto) {
        return passengerService.updatePassenger(id, dto);
    }
}
