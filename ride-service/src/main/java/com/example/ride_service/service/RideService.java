package com.example.ride_service.service;

import com.example.ride_service.dto.RideDto;
import java.util.List;

/**
 * Service interface for managing ride-related operations.
 */
public interface RideService {
    /**
     * Retrieves all requested rides.
     * @return a list of RideDto representing all rides.
     */
    List<RideDto> getAllRides();

    /**
     * Retrieves a specific ride by its ID.
     * @param id the unique identifier of the ride.
     * @return the RideDto containing the ride's details.
     */
    RideDto getRideById(Long id);

    /**
     * Requests a new ride. Verifies passenger via PassengerService.
     * @param dto the data transfer object containing the ride information.
     * @return the saved RideDto.
     */
    RideDto requestRide(RideDto dto);
}
