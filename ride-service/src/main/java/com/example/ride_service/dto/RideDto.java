package com.example.ride_service.dto;

import jakarta.validation.constraints.NotNull;
import com.fasterxml.jackson.annotation.JsonInclude;

@JsonInclude(JsonInclude.Include.NON_NULL)
public record RideDto(
    Long id,
    @NotNull Long passengerId,
    Long driverId,
    String status,
    String passengerDetails
) {}
