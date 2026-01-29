package com.mxevolux.mxevolux_backend.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.Instant;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "scenarios")

public class Scenario {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "scenario_name", nullable = false, unique = true)
    private String name;

    @Column(name = "scenario_description")
    private String description;

    @Column(name = "owner_name", nullable = false)
    private String owner;

    @Column(name = "created_time", columnDefinition = "timestamptz")
    private Instant created_at;

    @Column(name = "modified_time", columnDefinition = "timestamptz")
    private Instant modified_at;

}
