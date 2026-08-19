package com.rideshare.ride;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;

@Component
public class PassengerClient {
    private static final Logger log = LoggerFactory.getLogger(PassengerClient.class);
    private final RestClient restClient;

    public PassengerClient(RestClient.Builder builder) {
        // Will rewrite URL later for Eureka, using localhost for Phase 2 test
        this.restClient = builder.baseUrl("http://localhost:8081").build();
    }

    @CircuitBreaker(name = "passengerService", fallbackMethod = "fallbackGetPassenger")
    public String getPassenger(Long id) {
        log.info("Calling passenger service for id: {}", id);
        return restClient.get()
                .uri("/api/passengers/{id}", id)
                .retrieve()
                .body(String.class);
    }

    public String fallbackGetPassenger(Long id, Throwable t) {
        log.error("Passenger service is down, fallback triggered for id: {}. Error: {}", id, t.getMessage());
        return "{\"fallback\": true, \"message\": \"Passenger service unavailable\"}";
    }
}
