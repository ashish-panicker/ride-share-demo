package com.example.pasenger_service.service;

import com.example.pasenger_service.dto.PassengerDto;
import java.util.List;

/**
 * Service interface for managing passenger-related operations.
 */
public interface PassengerService {

    /**
     * Retrieves all registered passengers in the system.
     * 
     * @return a list of PassengerDto representing all passengers.
     */
    List<PassengerDto> getAllPassengers();

    /**
     * Retrieves a specific passenger by their unique identifier.
     * 
     * @param id the unique identifier of the passenger.
     * @return the PassengerDto containing the passenger's details.
     * @throws RuntimeException if the passenger is not found.
     */
    PassengerDto getPassengerById(Long id);

    /**
     * Registers a new passenger in the system.
     * 
     * @param dto the data transfer object containing the new passenger's information.
     * @return the saved PassengerDto with the generated ID.
     */
    PassengerDto createPassenger(PassengerDto dto);

    /**
     * Updates an existing passenger's information.
     * 
     * @param id the unique identifier of the passenger to update.
     * @param dto the data transfer object containing the updated information.
     * @return the updated PassengerDto.
     * @throws RuntimeException if the passenger is not found.
     */
    PassengerDto updatePassenger(Long id, PassengerDto dto);
}
