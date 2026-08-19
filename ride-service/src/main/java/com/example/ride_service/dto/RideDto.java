package com.example.ride_service.dto;

import jakarta.validation.constraints.NotNull;

public record RideDto(
    Long id,
    @NotNull Long passengerId,
    Long driverId,
    String status
) {}
