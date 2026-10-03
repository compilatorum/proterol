// ============================================================
// PROTEROL: ORACLE — AGROFLORESTA COMPUTACIONAL
// ============================================================

gene BiomeSensor : Agent {
    sign: "🌱" ;
    meaning: "Sensor de umidade do solo, biomassa e biodiversidade" ;
    operators: [measure, test] ;
    constraints: ["sample_rate_hz >= 1"] ;
    license: "MIT" ;
}

gene CanopyDynamics : Process {
    sign: "🌳" ;
    meaning: "Simulação de estrato arbóreo e interceptação luminosa" ;
    operators: [simulate, change] ;
    constraints: ["photosynthesis_model == Farquhar"] ;
    license: "MIT" ;
}

gene RegenerativeYield : Concept {
    sign: "🪙" ;
    meaning: "Retorno econômico acoplado ao acúmulo de carbono e água" ;
    operators: [calculate, tokenize] ;
    constraints: ["positive_carbon_delta == true"] ;
    license: "CC-BY-SA-4.0" ;
}

// Nexos transformacionais
BiomeSensor =[measure]=> CanopyDynamics ;
CanopyDynamics =[simulate]=> RegenerativeYield ;
RegenerativeYield =[tokenize]=> BioregionalCredit ;

construct AgroflorestaDigital = BiomeSensor (+) CanopyDynamics (+) RegenerativeYield ;
