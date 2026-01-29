package com.mxevolux.mxevolux_backend.controller;
import com.mxevolux.mxevolux_backend.dto.ScenarioDTO;
import com.mxevolux.mxevolux_backend.service.ScenarioService;
import org.springframework.http.HttpStatus;
import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@AllArgsConstructor
@RestController
@RequestMapping("/api/scenarios")
public class ScenarioController {

    private ScenarioService scenarioService;

    // Build add scenario rest api
    @PostMapping
    public ResponseEntity<ScenarioDTO> createScenario(@RequestBody  ScenarioDTO scenarioDTO){
        ScenarioDTO savedScenario = scenarioService.createScenario(scenarioDTO);
        return new ResponseEntity<>(savedScenario, HttpStatus.CREATED);
    }

    // get (1) scenario by id
    @GetMapping("{id}")
    public ResponseEntity<ScenarioDTO> getScenarioById(@PathVariable("id") Long scenarioId){
        ScenarioDTO scenarioDTO = scenarioService.getScenarioById(scenarioId);
        return ResponseEntity.ok(scenarioDTO);
    }

    // get all scenarios
    @GetMapping
    public ResponseEntity<List<ScenarioDTO>> getAllScenarios(){
    List<ScenarioDTO> scenarios = scenarioService.getAllScenarios();
        return ResponseEntity.ok(scenarios);
    }

    //update scenario
    @PatchMapping("{scenarioID}")
    public ResponseEntity<ScenarioDTO> patchScenario(@PathVariable Long scenarioID, @RequestBody ScenarioDTO partialUpdate) {
        ScenarioDTO scenarioDTO = scenarioService.updateScenario(scenarioID, partialUpdate);
        return ResponseEntity.ok(scenarioDTO);
    }

    //delete scenario
    @DeleteMapping("{id}")
    public ResponseEntity<String> deleteScenario(Long scenarioID){
        scenarioService.deleteScenario(scenarioID);
        return ResponseEntity.ok("Scenario deleted");
    }

 }


 //global exception (for springboot)