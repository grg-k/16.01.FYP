package com.mxevolux.mxevolux_backend.mapper;

import com.mxevolux.mxevolux_backend.dto.PackageDTO;
import com.mxevolux.mxevolux_backend.entity.Package;


public class PackageMapper {
    public static PackageDTO mapToPackageDTO(Package pkg){
        return new PackageDTO(
                pkg.getId(),
                pkg.getName(),
                pkg.getOwner(),
                pkg.getDescription(),
                pkg.getCreated_at(),
                pkg.getModified_at()
        );
    }

    public static Package maptoPackage (PackageDTO pkgDTO){
        return new Package(
                pkgDTO.getId(),
                pkgDTO.getName(),
                pkgDTO.getOwner(),
                pkgDTO.getDescription(),
                pkgDTO.getCreated_at(),
                pkgDTO.getModified_at()
        );
    }
}
