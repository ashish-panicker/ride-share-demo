package com.example.pasenger_service.service;

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
