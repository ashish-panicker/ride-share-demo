package com.rideshare.ride;

import jakarta.validation.constraints.NotNull;

public record RideDto(
    Long id,
    @NotNull Long passengerId,
    Long driverId,
    String status
) {}
