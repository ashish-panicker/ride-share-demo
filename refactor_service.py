import os

# Create PassengerService Interface with JavaDocs
interface_content = """package com.example.pasenger_service.service;

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
"""
with open("pasenger-service/src/main/java/com/example/pasenger_service/service/PassengerService.java", "w") as f:
    f.write(interface_content)

# Create PassengerServiceImpl class
impl_content = """package com.example.pasenger_service.service;

import com.example.pasenger_service.dto.PassengerDto;
import com.example.pasenger_service.entity.Passenger;
import com.example.pasenger_service.repository.PassengerRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class PassengerServiceImpl implements PassengerService {
    private final PassengerRepository repository;

    public PassengerServiceImpl(PassengerRepository repository) {
        this.repository = repository;
    }

    private PassengerDto mapToDto(Passenger p) {
        return new PassengerDto(p.getId(), p.getName(), p.getEmail());
    }

    @Override
    public List<PassengerDto> getAllPassengers() {
        return repository.findAll().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    @Override
    public PassengerDto getPassengerById(Long id) {
        return repository.findById(id)
                .map(this::mapToDto)
                .orElseThrow(() -> new RuntimeException("Passenger not found with id: " + id));
    }

    @Override
    public PassengerDto createPassenger(PassengerDto dto) {
        Passenger passenger = new Passenger();
        passenger.setName(dto.name());
        passenger.setEmail(dto.email());
        Passenger saved = repository.save(passenger);
        return mapToDto(saved);
    }
    
    @Override
    public PassengerDto updatePassenger(Long id, PassengerDto dto) {
        Passenger passenger = repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Passenger not found with id: " + id));
        passenger.setName(dto.name());
        passenger.setEmail(dto.email());
        Passenger updated = repository.save(passenger);
        return mapToDto(updated);
    }
}
"""
with open("pasenger-service/src/main/java/com/example/pasenger_service/service/PassengerServiceImpl.java", "w") as f:
    f.write(impl_content)

