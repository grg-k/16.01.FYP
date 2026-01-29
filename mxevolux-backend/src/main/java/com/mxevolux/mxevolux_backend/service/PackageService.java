package com.mxevolux.mxevolux_backend.service;
import com.mxevolux.mxevolux_backend.dto.PackageDTO;

import java.util.List;


public interface PackageService {
    PackageDTO createPackage(PackageDTO packageDTO);

    PackageDTO getPackageById(Long packageId);

    List<PackageDTO> getAllPackages();

    PackageDTO updatePackage(Long packageID, PackageDTO updatedPackage);

    void deletePackage(Long packageID);
}
