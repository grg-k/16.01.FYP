package com.mxevolux.mxevolux_backend.service;
import com.mxevolux.mxevolux_backend.dto.ScenarioDTO;

import java.util.List;


public interface ScenarioService {
    ScenarioDTO createScenario(ScenarioDTO scenarioDTO);

    ScenarioDTO getScenarioById(Long scenarioId);

    List<ScenarioDTO> getAllScenarios();

    ScenarioDTO updateScenario(Long scenarioID, ScenarioDTO updatedScenario);

    void deleteScenario(Long scenarioID);
}
