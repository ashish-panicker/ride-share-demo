package com.rideshare.passenger;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public record PassengerDto(
    Long id,
    @NotBlank String name,
    @NotBlank @Email String email
) {}
