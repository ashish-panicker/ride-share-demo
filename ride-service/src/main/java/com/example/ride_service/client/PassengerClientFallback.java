package com.example.ride_service.client;

import org.springframework.stereotype.Component;

@Component
public class PassengerClientFallback implements PassengerClient {
    @Override
    public Object getPassenger(Long id) {
        return "Passenger service unavailable";
    }
}
