package com.mxevolux.mxevolux_backend.service.impl;

import com.mxevolux.mxevolux_backend.dto.ScenarioDTO;
import com.mxevolux.mxevolux_backend.entity.Scenario;
import com.mxevolux.mxevolux_backend.exception.ResourceNotFoundException;
import com.mxevolux.mxevolux_backend.mapper.ScenarioMapper;
import com.mxevolux.mxevolux_backend.service.ScenarioService;
import com.mxevolux.mxevolux_backend.repository.ScenarioRepository;
import jakarta.transaction.Transactional;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.List;
import java.util.stream.Collectors;

@Service
@AllArgsConstructor
public class ScenarioServiceImpl implements ScenarioService {

    private ScenarioRepository scenarioRepository;

    @Override
    public ScenarioDTO createScenario(ScenarioDTO scenarioDTO) {

        Scenario scenario = ScenarioMapper.maptoScenario(scenarioDTO);
        Scenario savedScenario = scenarioRepository.save(scenario);
        return ScenarioMapper.mapToScenarioDTO(savedScenario);
    }

    @Override
    public ScenarioDTO getScenarioById(Long scenarioId) {
        Scenario scenario = scenarioRepository.findById(scenarioId)
                .orElseThrow(() -> new ResourceNotFoundException("No scenario with id :" + scenarioId));
        return ScenarioMapper.mapToScenarioDTO(scenario);
    }

    @Override
    public List<ScenarioDTO> getAllScenarios() {
        List<Scenario> scenarios = scenarioRepository.findAll();
        return scenarios.stream().map((scenario) -> ScenarioMapper.mapToScenarioDTO(scenario)).collect(Collectors.toList());
    }

    @Override
    @Transactional
    public ScenarioDTO updateScenario(Long scenarioID, ScenarioDTO patch) {
        Scenario scenario = scenarioRepository.findById(scenarioID)
                .orElseThrow(() -> new ResourceNotFoundException("No scenario with id:" + scenarioID));

        if (patch.getName() != null)       scenario.setName(patch.getName());
        if (patch.getOwner() != null)      scenario.setOwner(patch.getOwner());
        if (patch.getDescription() != null)scenario.setDescription(patch.getDescription());

        scenario.setModified_at(Instant.now());

        Scenario saved = scenarioRepository.save(scenario);
        return ScenarioMapper.mapToScenarioDTO(saved);
    }

    @Override
    public void deleteScenario(Long scenarioID) {
        Scenario scenario = scenarioRepository.findById(scenarioID)
                .orElseThrow(() -> new ResourceNotFoundException("No scenario with id :" + scenarioID));
        scenarioRepository.deleteById(scenarioID);
    }
}

