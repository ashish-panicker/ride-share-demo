package com.example.pasenger_service.repository;

import com.example.pasenger_service.entity.Passenger;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PassengerRepository extends JpaRepository<Passenger, Long> {
}
