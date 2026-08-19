package com.example.ride_service.controller;

import com.example.ride_service.dto.RideDto;
import com.example.ride_service.service.RideService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;

import java.util.List;

@CrossOrigin(origins = "*")
@RestController
@RequestMapping("/api/rides")
public class RideController {
    private final RideService rideService;

    public RideController(RideService rideService) {
        this.rideService = rideService;
    }

    @GetMapping
    public List<RideDto> getAllRides() {
        return rideService.getAllRides();
    }

    @GetMapping("/{id}")
    public RideDto getRideById(@PathVariable Long id) {
        return rideService.getRideById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public RideDto requestRide(@Valid @RequestBody RideDto dto) {
        return rideService.requestRide(dto);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public String handleIllegalArgumentException(IllegalArgumentException ex) {
        return ex.getMessage();
    }
}
