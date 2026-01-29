package com.mxevolux.mxevolux_backend.controller;

import com.mxevolux.mxevolux_backend.dto.PackageDTO;
import com.mxevolux.mxevolux_backend.service.PackageService;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@AllArgsConstructor
@RestController
@RequestMapping("/api/packages")
public class PackageController {

    private PackageService pkgService;

    // Build add pkg rest api
    @PostMapping
    public ResponseEntity<PackageDTO> createPackage(@RequestBody  PackageDTO pkgDTO){
        PackageDTO savedPackage = pkgService.createPackage(pkgDTO);
        return new ResponseEntity<>(savedPackage, HttpStatus.CREATED);
    }

    // get (1) pkg by id
    @GetMapping("{id}")
    public ResponseEntity<PackageDTO> getPackageById(@PathVariable("id") Long pkgId){
        PackageDTO pkgDTO = pkgService.getPackageById(pkgId);
        return ResponseEntity.ok(pkgDTO);
    }

    // get all pkgs
    @GetMapping
    public ResponseEntity<List<PackageDTO>> getAllPackages(){
    List<PackageDTO> pkgs = pkgService.getAllPackages();
        return ResponseEntity.ok(pkgs);
    }

    //update pkg
    @PatchMapping("{pkgID}")
    public ResponseEntity<PackageDTO> patchPackage(@PathVariable Long pkgID, @RequestBody PackageDTO partialUpdate) {
        PackageDTO pkgDTO = pkgService.updatePackage(pkgID, partialUpdate);
        return ResponseEntity.ok(pkgDTO);
    }

    //delete pkg
    @DeleteMapping("{id}")
    public ResponseEntity<String> deletePackage(Long pkgID){
        pkgService.deletePackage(pkgID);
        return ResponseEntity.ok("Package deleted");
    }

 }
