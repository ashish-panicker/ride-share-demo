import os

# Remove @Repository from PassengerRepository
repo_path = "pasenger-service/src/main/java/com/example/pasenger_service/repository/PassengerRepository.java"
with open(repo_path, "r") as f:
    content = f.read()

content = content.replace("import org.springframework.stereotype.Repository;\n", "")
content = content.replace("@Repository\n", "")

with open(repo_path, "w") as f:
    f.write(content)


# Create DTO
os.makedirs("pasenger-service/src/main/java/com/example/pasenger_service/dto", exist_ok=True)
dto_content = """package com.example.pasenger_service.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

public record PassengerDto(
    Long id,
    @NotBlank String name,
    @NotBlank @Email String email
) {}
"""
with open("pasenger-service/src/main/java/com/example/pasenger_service/dto/PassengerDto.java", "w") as f:
    f.write(dto_content)

# Create Service
os.makedirs("pasenger-service/src/main/java/com/example/pasenger_service/service", exist_ok=True)
service_content = """package com.example.pasenger_service.service;

import com.example.pasenger_service.dto.PassengerDto;
import com.example.pasenger_service.entity.Passenger;
import com.example.pasenger_service.repository.PassengerRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class PassengerService {
    private final PassengerRepository repository;

    public PassengerService(PassengerRepository repository) {
        this.repository = repository;
    }

    private PassengerDto mapToDto(Passenger p) {
        return new PassengerDto(p.getId(), p.getName(), p.getEmail());
    }

    public List<PassengerDto> getAllPassengers() {
        return repository.findAll().stream()
                .map(this::mapToDto)
                .collect(Collectors.toList());
    }

    public PassengerDto getPassengerById(Long id) {
        return repository.findById(id)
                .map(this::mapToDto)
                .orElseThrow(() -> new RuntimeException("Passenger not found with id: " + id));
    }

    public PassengerDto createPassenger(PassengerDto dto) {
        Passenger passenger = new Passenger();
        passenger.setName(dto.name());
        passenger.setEmail(dto.email());
        Passenger saved = repository.save(passenger);
        return mapToDto(saved);
    }
    
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
with open("pasenger-service/src/main/java/com/example/pasenger_service/service/PassengerService.java", "w") as f:
    f.write(service_content)

