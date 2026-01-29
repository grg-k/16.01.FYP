package com.mxevolux.mxevolux_backend.mapper;

import com.mxevolux.mxevolux_backend.dto.ScenarioDTO;
import com.mxevolux.mxevolux_backend.entity.Scenario;


public class ScenarioMapper {
    public static ScenarioDTO mapToScenarioDTO(Scenario scenario){
        return new ScenarioDTO(
                scenario.getId(),
                scenario.getName(),
                scenario.getOwner(),
                scenario.getDescription(),
                scenario.getCreated_at(),
                scenario.getModified_at()
        );
    }

    public static Scenario maptoScenario (ScenarioDTO scenarioDTO){
        return new Scenario(
                scenarioDTO.getId(),
                scenarioDTO.getName(),
                scenarioDTO.getOwner(),
                scenarioDTO.getDescription(),
                scenarioDTO.getCreated_at(),
                scenarioDTO.getModified_at()
        );
    }
}
