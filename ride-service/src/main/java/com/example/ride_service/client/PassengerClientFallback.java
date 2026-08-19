package com.example.ride_service.client;

import org.springframework.stereotype.Component;

@Component
public class PassengerClientFallback implements PassengerClient {
    @Override
    public String getPassenger(Long id) {
        return "{\"fallback\": true, \"message\": \"Passenger service unavailable\"}";
    }
}
