package com.mxevolux.mxevolux_backend.service.impl;
import com.mxevolux.mxevolux_backend.dto.PackageDTO;
import com.mxevolux.mxevolux_backend.entity.Package;
import com.mxevolux.mxevolux_backend.exception.ResourceNotFoundException;
import com.mxevolux.mxevolux_backend.mapper.PackageMapper;
import com.mxevolux.mxevolux_backend.repository.PackageRepository;
import com.mxevolux.mxevolux_backend.service.PackageService;
import jakarta.transaction.Transactional;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;
import java.util.stream.Collectors;

@Service
@AllArgsConstructor
public class PackageServiceImpl implements PackageService {

    private PackageRepository pkgRepository;

    @Override
    public PackageDTO createPackage(PackageDTO pkgDTO) {

        Package pkg = PackageMapper.maptoPackage(pkgDTO);
        Package savedPackage = pkgRepository.save(pkg);
        return PackageMapper.mapToPackageDTO(savedPackage);
    }

    @Override
    public PackageDTO getPackageById(Long pkgId) {
        Package pkg = pkgRepository.findById(pkgId)
                .orElseThrow(() -> new ResourceNotFoundException("No pkg with id :" + pkgId));
        return PackageMapper.mapToPackageDTO(pkg);
    }

    @Override
    public List<PackageDTO> getAllPackages() {
        List<Package> pkgs = pkgRepository.findAll();
        return pkgs.stream().map((pkg) -> PackageMapper.mapToPackageDTO(pkg)).collect(Collectors.toList());
    }

    @Override
    @Transactional
    public PackageDTO updatePackage(Long pkgID, PackageDTO patch) {
        Package pkg = pkgRepository.findById(pkgID)
                .orElseThrow(() -> new ResourceNotFoundException("No pkg with id:" + pkgID));

        if (patch.getName() != null)       pkg.setName(patch.getName());
        if (patch.getOwner() != null)      pkg.setOwner(patch.getOwner());
        if (patch.getDescription() != null)pkg.setDescription(patch.getDescription());

        pkg.setModified_at(Instant.now());

        Package saved = pkgRepository.save(pkg);
        return PackageMapper.mapToPackageDTO(saved);
    }

    @Override
    public void deletePackage(Long pkgID) {
        Package pkg = pkgRepository.findById(pkgID)
                .orElseThrow(() -> new ResourceNotFoundException("No pkg with id :" + pkgID));
        pkgRepository.deleteById(pkgID);
    }
}
