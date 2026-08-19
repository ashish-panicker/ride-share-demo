package com.example.ride_service.service;

import com.example.ride_service.client.PassengerClient;
import com.example.ride_service.dto.RideDto;
import com.example.ride_service.entity.Ride;
import com.example.ride_service.repository.RideRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class RideServiceImpl implements RideService {
    private final RideRepository repository;
    private final PassengerClient passengerClient;

    public RideServiceImpl(RideRepository repository, PassengerClient passengerClient) {
        this.repository = repository;
        this.passengerClient = passengerClient;
    }

    private RideDto mapToDto(Ride r) {
        return new RideDto(r.getId(), r.getPassengerId(), r.getDriverId(), r.getStatus(), null);
    }

    private RideDto mapToDtoWithDetails(Ride r, Object details) {
        return new RideDto(r.getId(), r.getPassengerId(), r.getDriverId(), r.getStatus(), details);
    }

    @Override
    public List<RideDto> getAllRides() {
        return repository.findAll().stream().map(this::mapToDto).collect(Collectors.toList());
    }

    @Override
    public RideDto getRideById(Long id) {
        return repository.findById(id).map(this::mapToDto).orElseThrow(() -> new RuntimeException("Ride not found"));
    }

    @Override
    public RideDto requestRide(RideDto dto) {
        Object passengerInfo = passengerClient.getPassenger(dto.passengerId());
        
        Ride ride = new Ride();
        ride.setPassengerId(dto.passengerId());
        ride.setDriverId(dto.driverId());
        ride.setStatus("REQUESTED");
        
        Ride saved = repository.save(ride);
        return mapToDtoWithDetails(saved, passengerInfo);
    }
}
