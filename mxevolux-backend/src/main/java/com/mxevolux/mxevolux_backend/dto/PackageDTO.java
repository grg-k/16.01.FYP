package com.mxevolux.mxevolux_backend.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.Instant;


@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor

public class PackageDTO {
    private Long id;
    private String name;
    private String description;
    private String owner;
    private Instant created_at;
    private Instant modified_at;

}
