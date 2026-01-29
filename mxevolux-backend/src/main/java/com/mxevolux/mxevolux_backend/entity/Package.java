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
@Table(name = "packages")

public class Package {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "packages_name", nullable = false, unique = true)
    private String name;

    @Column(name = "package_description")
    private String description;

    @Column(name = "owner_name", nullable = false)
    private String owner;

    @Column(name = "created_time")
    private Instant created_at;

    @Column(name = "modified_time")
    private Instant modified_at;

}
