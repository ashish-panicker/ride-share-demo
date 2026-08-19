package com.example.gateway_service;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.function.RouterFunction;
import org.springframework.web.servlet.function.ServerResponse;
import java.net.URI;
import static org.springframework.cloud.gateway.server.mvc.handler.GatewayRouterFunctions.route;
import static org.springframework.cloud.gateway.server.mvc.handler.HandlerFunctions.http;
import static org.springframework.cloud.gateway.server.mvc.filter.FilterFunctions.uri;
import static org.springframework.cloud.gateway.server.mvc.filter.LoadBalancerFilterFunctions.lb;
import static org.springframework.web.servlet.function.RequestPredicates.path;

@Configuration
public class GatewayConfig {

    @Bean
    public RouterFunction<ServerResponse> passengerRoute() {
        return route("passenger-service")
                .route(path("/api/passengers/**"), http())
                .filter(lb("PASSENGER-SERVICE"))
                .build();
    }

    @Bean
    public RouterFunction<ServerResponse> rideRoute() {
        return route("ride-service")
                .route(path("/api/rides/**"), http())
                .filter(lb("RIDE-SERVICE"))
                .build();
    }
}
