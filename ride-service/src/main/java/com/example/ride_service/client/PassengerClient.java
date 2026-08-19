package com.example.ride_service.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "passengerService", url = "${passenger.service.url}", fallback = PassengerClientFallback.class)
public interface PassengerClient {
    @GetMapping("/api/passengers/{id}")
    Object getPassenger(@PathVariable("id") Long id);
}
