#!/usr/bin/env python3
"""Authoritative Domain Synthesis Engine for All-skills.

Synthesizes structured, production-ready SKILL.md playbooks for all 60 core human and
engineering domains identified in the Agent Skills taxonomy expansion proposal.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
AWESOME_DIR = REPO_ROOT / "awesome_skills"

# Comprehensive taxonomy specification covering all 60 requested domains
DOMAINS_SPEC: Dict[str, Dict[str, List[Tuple[str, str, str]]]] = {
    "mathematics": {
        "title": "Mathematics & Formal Reasoning",
        "skills": [
            ("arithmetic", "Foundational arithmetic operations, number representations, precision, and numerical algorithms.", "low"),
            ("algebra", "Algebraic expressions, polynomials, factoring, systems of equations, and inequalities.", "low"),
            ("linear-algebra", "Vectors, matrices, eigenvalues, singular value decomposition, and multidimensional transformations.", "low"),
            ("abstract-algebra", "Groups, rings, fields, modules, homomorphisms, and modern algebraic structures.", "low"),
            ("number-theory", "Prime numbers, modular arithmetic, Diophantine equations, and computational number theory.", "low"),
            ("geometry", "Euclidean, projective, non-Euclidean geometry, coordinate systems, and spatial reasoning.", "low"),
            ("topology", "Topological spaces, homeomorphisms, metric spaces, manifolds, and algebraic topology.", "low"),
            ("trigonometry", "Trigonometric functions, identities, spherical trigonometry, and geometric transformations.", "low"),
            ("calculus", "Single-variable differential and integral calculus, limits, continuity, and infinite series.", "low"),
            ("real-analysis", "Rigorous analysis of real numbers, measure theory, Lebesgue integration, and metric spaces.", "low"),
            ("complex-analysis", "Holomorphic functions, contour integration, Cauchy theorems, residues, and conformal maps.", "low"),
            ("differential-equations", "Ordinary differential equations, boundary value problems, phase plane analysis, and solutions.", "low"),
            ("partial-differential-equations", "Elliptic, parabolic, hyperbolic PDEs, Fourier methods, Green's functions, and solutions.", "low"),
            ("numerical-methods", "Finite differences, root-finding, interpolation, numerical integration, and error analysis.", "low"),
            ("optimization", "Convex optimization, duality, gradient descent, interior point methods, and constrained systems.", "low"),
            ("combinatorics", "Enumerative combinatorics, generating functions, permutations, and Ramsey theory.", "low"),
            ("graph-theory", "Network topology, trees, graph coloring, connectivity, planar graphs, and shortest paths.", "low"),
            ("probability", "Probability spaces, random variables, conditioning, Bayes theorem, and limit laws.", "low"),
            ("statistics", "Frequentist and Bayesian inference, hypothesis testing, estimators, and confidence intervals.", "low"),
            ("stochastic-processes", "Markov chains, Poisson processes, Brownian motion, martingales, and stochastic calculus.", "low"),
            ("mathematical-logic", "Propositional logic, first-order logic, Gödel theorems, model theory, and proof systems.", "low"),
            ("set-theory", "Zermelo-Fraenkel set theory, axioms of choice, cardinal and ordinal numbers, and foundations.", "low"),
            ("category-theory", "Functors, natural transformations, universal properties, adjoints, and monads.", "low"),
            ("game-theory", "Nash equilibria, zero-sum games, mechanism design, cooperative games, and auction theory.", "low"),
            ("information-theory", "Shannon entropy, mutual information, channel capacity, rate-distortion, and coding theory.", "low"),
            ("cryptography-math", "Mathematical foundations of cryptography: discrete logs, elliptic curves, and lattices.", "low"),
            ("mathematical-modeling", "Formulating real-world systems into rigorous mathematical models and simulations.", "low"),
            ("operations-research", "Linear programming, simplex algorithms, integer programming, and simplex methods.", "low"),
            ("decision-theory", "Utility theory, decision trees, multi-criteria decision analysis, and risk models.", "low"),
            ("queueing-theory", "M/M/1 queues, waiting line networks, Markovian birth-death processes, and congestion.", "low"),
            ("control-theory", "State-space modeling, feedback loops, PID controllers, stability criteria, and Kalman filters.", "low"),
            ("simulation", "Monte Carlo simulations, discrete-event simulation, and agent-based mathematical modeling.", "low"),
            ("numerical-optimization", "Quasi-Newton methods, BFGS, Nelder-Mead, quadratic programming, and global search.", "low"),
        ]
    },
    "physics": {
        "title": "Physics & Fundamental Natural Laws",
        "skills": [
            ("classical-mechanics", "Newtonian mechanics, planetary motion, conservation laws, oscillations, and rigid bodies.", "low"),
            ("analytical-mechanics", "Lagrangian and Hamiltonian mechanics, Poisson brackets, canonical transformations, and action.", "low"),
            ("electromagnetism", "Maxwell equations, electrostatics, magnetostatics, electrodynamics, and electromagnetic waves.", "low"),
            ("thermodynamics", "Laws of thermodynamics, thermodynamic potentials, entropy, heat engines, and phase transitions.", "low"),
            ("statistical-mechanics", "Microcanonical, canonical ensembles, Boltzmann distribution, Fermi-Dirac, and Bose-Einstein.", "low"),
            ("quantum-mechanics", "Wavefunctions, Schrödinger equation, operators, quantum states, perturbation theory, and spin.", "low"),
            ("quantum-field-theory", "Second quantization, Feynman diagrams, relativistic quantum mechanics, and gauge symmetries.", "low"),
            ("relativity", "Einstein relativistic mechanics, four-vectors, invariance, and relativistic dynamics.", "low"),
            ("special-relativity", "Lorentz transformations, Minkowski spacetime, time dilation, and length contraction.", "low"),
            ("general-relativity", "Curved spacetime, Einstein field equations, Schwarzschild metric, black holes, and geodesics.", "low"),
            ("particle-physics", "Standard Model, quarks, leptons, gauge bosons, Higgs mechanism, and particle collisions.", "low"),
            ("nuclear-physics", "Nuclear structure, radioactive decay, fission, fusion, cross-sections, and nuclear reactions.", "medium"),
            ("condensed-matter", "Crystal lattices, band theory, semiconductors, superconductors, phononics, and magnetism.", "low"),
            ("atomic-physics", "Atomic spectra, electron transitions, fine structure, Rydberg atoms, and laser cooling.", "low"),
            ("molecular-physics", "Molecular orbitals, rotational-vibrational spectra, chemical bonding physics, and van der Waals.", "low"),
            ("optics", "Geometric and wave optics, diffraction, interference, polarization, and optical instruments.", "low"),
            ("photonics", "Lasers, fiber optics, photonic crystals, optoelectronics, and quantum photonics.", "low"),
            ("plasma-physics", "MHD equations, Debye shielding, plasma oscillations, confinement, and fusion plasma dynamics.", "medium"),
            ("astrophysics", "Stellar evolution, nucleosynthesis, compact objects, galactic dynamics, and accretion disks.", "low"),
            ("cosmology", "Big Bang, cosmic microwave background, dark matter, dark energy, and cosmic expansion.", "low"),
            ("computational-physics", "Numerical PDE solutions in physics, N-body simulations, and lattice field computations.", "low"),
            ("experimental-physics", "Error propagation, sensor calibration, detector design, and physics experimental validation.", "low"),
            ("mathematical-physics", "Differential geometry in physics, Lie groups, tensor analysis, and boundary-value techniques.", "low"),
            ("biophysics", "Physical principles of biological systems, molecular motors, membranes, and protein folding.", "low"),
        ]
    },
    "chemistry": {
        "title": "Chemistry & Molecular Sciences",
        "skills": [
            ("general-chemistry", "Stoichiometry, atomic theory, periodic trends, chemical equilibrium, and acid-base kinetics.", "low"),
            ("organic-chemistry", "Functional groups, reaction mechanisms, stereochemistry, nucleophilic substitution, and synthesis.", "low"),
            ("inorganic-chemistry", "Coordination complexes, crystal field theory, organometallics, and main group chemistry.", "low"),
            ("physical-chemistry", "Chemical thermodynamics, kinetics, rate laws, reaction dynamics, and quantum chemistry.", "low"),
            ("analytical-chemistry", "Titrations, gravimetric analysis, electrochemical sensors, calibrations, and validation.", "low"),
            ("biochemistry", "Enzyme kinetics, metabolic pathways, protein structure, nucleic acids, and bioenergetics.", "low"),
            ("medicinal-chemistry", "Structure-activity relationships, pharmacophores, drug discovery, ADMET, and lead optimization.", "low"),
            ("computational-chemistry", "Density functional theory (DFT), molecular dynamics simulations, and ab initio modeling.", "low"),
            ("electrochemistry", "Redox reactions, Nernst equation, batteries, fuel cells, cyclic voltammetry, and corrosion.", "low"),
            ("photochemistry", "Excited states, Jablonski diagrams, fluorescence, photochemical reactions, and photocatalysis.", "low"),
            ("polymer-chemistry", "Addition/condensation polymerization, molecular weight distributions, and polymer morphology.", "low"),
            ("materials-chemistry", "Synthesis of nanomaterials, metal-organic frameworks (MOFs), ceramics, and smart materials.", "low"),
            ("nanochemistry", "Colloidal nanoparticles, quantum dots, self-assembly, and surface modification techniques.", "low"),
            ("spectroscopy", "NMR, FTIR, UV-Vis, Raman spectroscopy data interpretation and structural elucidation.", "low"),
            ("chromatography", "HPLC, GC, flash chromatography, column selection, retention times, and separation methods.", "low"),
            ("mass-spectrometry", "Ionization techniques (ESI, MALDI), fragment analysis, HRMS, and isotopic distributions.", "low"),
            ("catalysis", "Homogeneous, heterogeneous, and biocatalysis mechanisms, active sites, and turnover numbers.", "low"),
            ("surface-chemistry", "Adsorption isotherms (Langmuir, BET), surface tension, colloids, and heterogeneous surfaces.", "low"),
            ("chemical-safety", "SDS interpretation, chemical compatibility, hazard mitigation, PPE, and waste disposal.", "medium"),
            ("process-chemistry", "Synthetic route scouting, scale-up considerations, yield optimization, and batch processing.", "low"),
            ("green-chemistry", "Atom economy, sustainable solvents, renewable feedstocks, and environmental factor metrics.", "low"),
            ("cheminformatics", "SMILES, InChI, RDKit, chemical fingerprints, substructure search, and molecular descriptors.", "low"),
        ]
    },
    "biology": {
        "title": "Biological Sciences & Living Systems",
        "skills": [
            ("cell-biology", "Organelles, membrane transport, signal transduction, cell cycle, apoptosis, and cellular metabolism.", "low"),
            ("molecular-biology", "DNA replication, transcription, translation, gene regulation, PCR, and recombinant DNA.", "low"),
            ("genetics", "Mendelian inheritance, linkage, chromosomal abnormalities, pedigree analysis, and population genetics.", "low"),
            ("genomics", "Genome sequencing, assembly, annotation, variant calling, GWAS, and comparative genomics.", "low"),
            ("epigenetics", "DNA methylation, histone modifications, chromatin remodeling, and non-coding RNA regulation.", "low"),
            ("microbiology", "Bacterial culture, viral replication, fungal morphology, antimicrobial resistance, and aseptic technique.", "medium"),
            ("immunology", "Innate and adaptive immunity, antigen presentation, antibodies, T cells, cytokines, and vaccines.", "low"),
            ("ecology", "Ecosystem dynamics, trophic levels, nutrient cycles, population growth models, and biodiversity.", "low"),
            ("evolution", "Natural selection, genetic drift, speciation, phylogenetics, cladograms, and molecular clocks.", "low"),
            ("zoology", "Animal physiology, taxonomy, behavioral ecology, morphology, and comparative anatomy.", "low"),
            ("botany", "Plant anatomy, photosynthesis, transpiration, phytochemistry, taxonomy, and crop physiology.", "low"),
            ("physiology", "Organ system functions, cardiovascular dynamics, neurophysiology, renal clearance, and homeostasis.", "low"),
            ("anatomy", "Human and comparative gross anatomy, musculoskeletal, vascular, and neural structures.", "low"),
            ("developmental-biology", "Embryogenesis, morphogens, cell differentiation, organogenesis, and stem cell biology.", "low"),
            ("marine-biology", "Oceanic ecosystems, coral reefs, pelagic organisms, deep sea adaptations, and marine food webs.", "low"),
            ("neuroscience", "Action potentials, synaptic transmission, neuroanatomy, cognitive neural circuits, and plasticity.", "low"),
            ("structural-biology", "Protein crystallography, cryo-EM, AlphaFold modeling, and macromolecular complexes.", "low"),
            ("systems-biology", "Gene regulatory networks, pathway modeling, metabolic flux analysis, and biological circuits.", "low"),
            ("synthetic-biology", "Genetic circuit design, metabolic engineering, CRISPR modifications, and biosensor construction.", "medium"),
            ("computational-biology", "Sequence alignment algorithms, hidden Markov models, structural modeling, and phylogenetics.", "low"),
            ("bioinformatics", "NCBI BLAST, FASTQ processing, Biopython, RNA-seq differential expression, and pipeline automation.", "low"),
            ("conservation-biology", "Endangered species management, habitat fragmentation, conservation genetics, and protected areas.", "low"),
        ]
    },
    "earth-science": {
        "title": "Earth Sciences & Geosciences",
        "skills": [
            ("geology", "Stratigraphy, rock classification (igneous, sedimentary, metamorphic), structural geology, and geological mapping.", "low"),
            ("geophysics", "Seismic reflection, gravity surveys, geomagnetic fields, electrical resistivity, and subsurface imaging.", "low"),
            ("geochemistry", "Isotope geochronology, mineral composition, elemental cycles, and geochemical thermodynamics.", "low"),
            ("mineralogy", "Crystallography, optical mineralogy, silicates, hardness scales, and petrographic microscopy.", "low"),
            ("petrology", "Magma differentiation, metamorphic facies, sedimentary provenance, and thin-section petrography.", "low"),
            ("sedimentology", "Depositional environments, grain size analysis, sedimentary structures, and sequence stratigraphy.", "low"),
            ("tectonics", "Plate tectonics, subduction zones, continental rifting, fault mechanics, and orogeny.", "low"),
            ("volcanology", "Magma rheology, volcanic hazards, pyroclastic flows, caldera formation, and eruption monitoring.", "medium"),
            ("seismology", "P and S waves, focal mechanisms, earthquake magnitude, ground motion acceleration, and hazard assessment.", "low"),
            ("paleontology", "Fossil preservation, biostratigraphy, macroevolutionary trends, and paleoenvironmental reconstruction.", "low"),
            ("geomorphology", "Fluvial processes, glacial landforms, coastal erosion, weathering, and landscape evolution.", "low"),
            ("hydrology", "Water balance, hydrographs, Darcy law, groundwater flow, watershed runoff, and flood frequency.", "low"),
            ("hydrogeology", "Aquifer testing, pumping tests, contaminant transport, drawdown curves, and wellhead protection.", "low"),
            ("glaciology", "Ice sheet dynamics, mass balance, glacier flow mechanics, and paleoclimate ice core analysis.", "low"),
            ("soil-science", "Pedology, soil horizon classification, cation exchange capacity, soil mechanics, and fertility.", "low"),
            ("oceanography", "Thermohaline circulation, wave dynamics, tides, ocean acidification, and marine chemistry.", "low"),
            ("atmospheric-science", "Atmospheric thermodynamics, planetary boundary layer, radiation balance, and greenhouse dynamics.", "low"),
            ("meteorology", "Synoptic weather forecasting, radar interpretation, baroclinic instability, and numerical weather prediction.", "low"),
            ("climatology", "Climate models, IPCC emission pathways, climate feedback loops, and paleoclimatology.", "low"),
            ("geodesy", "Earth ellipsoid, geoid models, datum transformations, coordinate reference systems, and satellite altimetry.", "low"),
            ("remote-sensing", "Multispectral/hyperspectral imagery, NDVI indices, thermal infrared, and optical earth observation.", "low"),
        ]
    },
    "geospatial": {
        "title": "Geospatial, GIS & Cartography",
        "skills": [
            ("gis", "Geographic Information Systems workflows, vector/raster data models, overlays, and geoprocessing.", "low"),
            ("qgis", "Open-source QGIS automation, PyQGIS scripting, styling, processing algorithms, and layout design.", "low"),
            ("arcgis", "Esri ArcGIS Pro workflows, geodatabase management, model builder, and enterprise GIS administration.", "low"),
            ("geocoding", "Address matching, forward/reverse geocoding, street network alignment, and spatial normalization.", "low"),
            ("geospatial-analysis", "Spatial buffering, zonal statistics, spatial autocorrelation (Moran's I), and hotspot analysis.", "low"),
            ("spatial-databases", "PostGIS spatial SQL queries, ST_Intersects, indexing with R-trees, and spatial schema design.", "low"),
            ("remote-sensing", "Earth observation satellite processing, Landsat/Sentinel workflows, and band combination analysis.", "low"),
            ("satellite-imagery", "Orthorectification, atmospheric correction, cloud masking, and satellite image time series.", "low"),
            ("lidar", "LAS/LAZ point cloud processing, DEM/DSM generation, canopy height modeling, and feature extraction.", "low"),
            ("photogrammetry", "Structure-from-Motion (SfM), tie point generation, orthomosaic generation, and drone mapping.", "low"),
            ("cartography", "Map design, symbology, thematic classification, typography, projection selection, and cartographic layout.", "low"),
            ("surveying", "Total station measurements, leveling, boundary establishment, traverse adjustment, and field surveying.", "low"),
            ("gps", "GNSS positioning principles, RTK corrections, RINEX data handling, and positioning accuracy metrics.", "low"),
            ("geofencing", "Spatial bounding boxes, polygonal boundaries, event triggers, and GPS location tracking telemetry.", "low"),
            ("routing", "Network analysis, Dijkstra/A* routing algorithms, traveling salesperson routing, and turn restrictions.", "low"),
            ("spatial-statistics", "Spatial regression, geographically weighted regression (GWR), and point pattern analysis.", "low"),
            ("cadastral-mapping", "Parcel boundary management, legal description mapping, title survey integration, and land administration.", "low"),
            ("digital-twins", "3D spatial digital representations, real-time sensor integration, and spatial twin synchronization.", "low"),
        ]
    },
    "electrical-engineering": {
        "title": "Electrical Engineering & Power Systems",
        "skills": [
            ("circuit-analysis", "Kirchhoff laws, Thevenin/Norton equivalents, RLC transient analysis, and AC steady-state phasors.", "low"),
            ("analog-electronics", "BJT/MOSFET small-signal models, operational amplifiers, active filters, and low-noise amplifiers.", "low"),
            ("digital-electronics", "Logic gates, Boolean minimization, combinational and sequential logic, flip-flops, and state machines.", "low"),
            ("power-electronics", "Buck, boost, buck-boost converters, inverters, rectifiers, PWM modulation, and gate drivers.", "medium"),
            ("power-systems", "Three-phase power flow, symmetrical components, transmission line modeling, and grid stability.", "medium"),
            ("electrical-machines", "Induction motors, synchronous generators, BLDC motors, torque-speed curves, and motor drives.", "medium"),
            ("transformers", "Transformer equivalent circuits, impedance matching, tap changers, and core loss calculations.", "medium"),
            ("protection-systems", "Relay coordination, overcurrent, differential protection, arc flash analysis, and circuit breakers.", "medium"),
            ("control-systems", "Bode plots, root locus, state feedback, observers, LQR control, and industrial process control.", "low"),
            ("instrumentation", "Sensors, transducers, 4-20mA loops, Wheatstone bridges, ADC calibration, and signal conditioning.", "low"),
            ("signal-processing", "FFT, FIR/IIR digital filters, sampling theorem, z-transforms, and spectral estimation.", "low"),
            ("communications", "Modulation (QAM, PSK, OFDM), wireless channels, link budgets, Shannon capacity, and error coding.", "low"),
            ("rf-engineering", "Transmission lines, Smith charts, S-parameters, impedance matching networks, and RF amplifiers.", "low"),
            ("microwave-engineering", "Waveguides, stripline/microstrip design, power dividers, directional couplers, and microwave filters.", "low"),
            ("antenna-design", "Dipole, patch, horn antennas, radiation patterns, directivity, gain, and phased arrays.", "low"),
            ("pcb-design", "Schematic capture, PCB stackup, high-speed routing, differential pairs, decoupling, and Gerber output.", "low"),
            ("fpga", "VHDL/Verilog synthesis, timing constraints (SDC), clock domain crossing, and hardware acceleration.", "low"),
            ("embedded-electronics", "Microcontroller interfacing, logic level shifters, power domains, and peripheral integration.", "low"),
            ("semiconductor-devices", "PN junctions, MOSFET physics, subthreshold slope, carrier mobility, and breakdown mechanisms.", "low"),
            ("electrical-safety", "OSHA electrical standards, NFPA 70E, grounding/bonding, insulation testing, and lockout/tagout.", "medium"),
        ]
    },
    "mechanical-engineering": {
        "title": "Mechanical Engineering & Thermal Fluid Systems",
        "skills": [
            ("engineering-drawing", "GD&T standards (ASME Y14.5), orthographic projections, section views, and tolerance stackups.", "low"),
            ("cad", "Parametric 3D solid modeling, feature trees, assembly mating, interference detection, and sheet metal.", "low"),
            ("machine-design", "Stress concentration, fatigue life (S-N curves), shafts, bearings, gears, fasteners, and springs.", "low"),
            ("mechanics", "Statics, free-body diagrams, centroids, moment of inertia, shear force, and bending moment diagrams.", "low"),
            ("thermodynamics", "Carnot cycles, Rankine, Brayton cycles, psychrometrics, refrigeration, and exergy analysis.", "low"),
            ("fluid-mechanics", "Navier-Stokes equations, Bernoulli equation, laminar/turbulent flow, boundary layers, and pipe friction.", "low"),
            ("heat-transfer", "Conduction (Fourier law), convection (Nusselt correlations), radiation (Stefan-Boltzmann), and exchangers.", "low"),
            ("materials", "Stress-strain curves, modulus of elasticity, yield criteria (von Mises), hardness, and creep.", "low"),
            ("dynamics", "Kinematics and kinetics of particles and rigid bodies, impulse-momentum, and gyroscopic motion.", "low"),
            ("vibrations", "Single and multi-DOF vibration, natural frequencies, damping ratios, resonance, and vibration isolation.", "low"),
            ("finite-element-analysis", "FEA meshing, boundary conditions, static structural analysis, modal analysis, and stress convergence.", "low"),
            ("computational-fluid-dynamics", "CFD meshing, turbulence modeling (k-epsilon, k-omega), convergence criteria, and flow visualization.", "low"),
            ("manufacturing", "Casting, forging, extrusion, injection molding, stamping, and manufacturing process selection.", "low"),
            ("machining", "CNC milling, turning, speeds and feeds, tool wear, surface roughness, and G-code generation.", "low"),
            ("robotics", "Forward/inverse kinematics, DH parameters, trajectory planning, actuators, and end-effectors.", "low"),
            ("mechatronics", "Integration of sensors, actuators, microcontrollers, motor drivers, and mechanical linkages.", "low"),
            ("hvac", "Heating, ventilation, air conditioning load calculations, duct sizing, chillers, and psychrometric charts.", "low"),
            ("automotive-engineering", "Vehicle dynamics, suspension geometry, powertrain sizing, braking systems, and crashworthiness.", "low"),
            ("maintenance-engineering", "Total productive maintenance (TPM), root cause failure analysis (RCFA), and condition monitoring.", "low"),
            ("reliability-engineering", "Weibull analysis, MTBF, failure mode and effects analysis (FMEA), and fault tree analysis.", "low"),
        ]
    },
    "chemical-engineering": {
        "title": "Chemical Engineering & Industrial Process Systems",
        "skills": [
            ("process-design", "Block flow diagrams, process flow diagrams (PFD), piping and instrumentation diagrams (P&ID).", "low"),
            ("process-simulation", "Aspen Plus, HYSYS process modeling, thermodynamic property packages, and steady-state flows.", "low"),
            ("transport-phenomena", "Momentum, heat, and mass transfer analogies, shell balances, and boundary layer transfer.", "low"),
            ("reaction-engineering", "Batch, CSTR, PFR reactor design, reaction kinetics, activation energy, and catalyst deactivation.", "low"),
            ("process-control", "Feedback loops, cascade control, feedforward control, tuning rules (Ziegler-Nichols), and DCS.", "low"),
            ("thermodynamics", "Equations of state (Peng-Robinson, NRTL, UNIQUAC), vapor-liquid equilibria (VLE), and fugacity.", "low"),
            ("separation-processes", "Equilibrium stage calculations, McCabe-Thiele method, extraction, crystallization, and membranes.", "low"),
            ("distillation", "Column tray design, structured packing, reflux ratio, column hydraulics, and flooding calculation.", "low"),
            ("absorption", "Gas-liquid absorption packed towers, Henry law, mass transfer coefficients, and stripper design.", "low"),
            ("filtration", "Cake filtration equations, dead-end/cross-flow membrane filtration, and centrifuge separation.", "low"),
            ("reactor-design", "Non-isothermal reactor operation, thermal runaway prevention, residence time distributions, and sizing.", "medium"),
            ("process-safety", "HAZOP studies, Layers of Protection Analysis (LOPA), relief valve sizing, and chemical dispersion.", "medium"),
            ("plant-design", "Equipment layout, piping specifications, pump/compressor curves, utility systems, and CAPEX/OPEX.", "low"),
            ("process-optimization", "Pinch analysis for heat integration, minimum utility targets, and process intensification.", "low"),
            ("petrochemical-engineering", "Crude oil distillation, catalytic cracking, hydrotreating, reforming, and olefin production.", "medium"),
            ("biochemical-engineering", "Fermentation kinetics, bioreactor design, aeration, agitation, and downstream bioseparations.", "low"),
            ("pharmaceutical-engineering", "cGMP manufacturing, cleanroom standards, sterilization, lyophilization, and batch validation.", "low"),
        ]
    },
    "civil-engineering": {
        "title": "Civil Engineering & Built Infrastructure",
        "skills": [
            ("structural-engineering", "Design of load-bearing structures according to ASCE 7, ACI 318, AISC 360, and Eurocodes.", "low"),
            ("geotechnical-engineering", "Soil boring logs, shear strength, settlement calculations, slope stability, and retaining walls.", "low"),
            ("transportation-engineering", "Highway alignment, sight distances, pavement design (AASHTO), and traffic capacity analysis.", "low"),
            ("highway-engineering", "Horizontal/vertical curves, superelevation, cross-sections, drainage design, and road safety.", "low"),
            ("traffic-engineering", "Traffic signal timing (HCM), level of service (LOS), queuing, and traffic simulation models.", "low"),
            ("bridge-engineering", "Prestressed concrete, steel girder, truss bridge design, live load distributions, and AASHTO LRFD.", "low"),
            ("water-resources", "Stormwater detention basins, open channel flow (Manning formula), culvert hydraulics, and HEC-RAS.", "low"),
            ("hydraulic-engineering", "Pipe networks (Hardy Cross), water distribution systems, pump stations, and surge analysis.", "low"),
            ("environmental-engineering", "Wastewater treatment, activated sludge design, potable water treatment, and air dispersion.", "low"),
            ("coastal-engineering", "Wave mechanics, breakwater design, coastal sediment transport, sea level rise, and shoreline protection.", "low"),
            ("surveying", "Topographic surveying, boundary surveys, leveling, GNSS positioning, and construction staking.", "low"),
            ("construction-engineering", "Critical Path Method (CPM) scheduling, quantity takeoff, cost estimating, and site logistics.", "low"),
            ("materials-engineering", "Concrete mix design, asphalt binders, steel stress-strain, timber grading, and aggregate testing.", "low"),
            ("pavement-engineering", "Flexible and rigid pavement thickness design, subgrade modulus, distress surveys, and rehab.", "low"),
            ("earthquake-engineering", "Seismic design categories, response spectrum analysis, base isolation, and ductility detailing.", "low"),
            ("structural-analysis", "Direct stiffness method, moment distribution, finite element structural frames, and deflection limits.", "low"),
            ("reinforced-concrete", "Flexural, shear, and axial design of RC beams, columns, two-way slabs, and rebar detailing.", "low"),
            ("steel-structures", "Bolted and welded connections, column buckling, beam lateral-torsional buckling, and bracing design.", "low"),
            ("timber-structures", "Glulam, cross-laminated timber (CLT), shear walls, joist sizing, and connection design (NDS).", "low"),
            ("foundation-design", "Shallow spread footings, mat foundations, deep piles, drilled shafts, and bearing capacity.", "low"),
        ]
    },
    "industrial-engineering": {
        "title": "Industrial Engineering & Operations Optimization",
        "skills": [
            ("operations-research", "Linear, integer, and non-linear programming for industrial routing, assignment, and resource allocation.", "low"),
            ("process-optimization", "Cycle time reduction, throughput modeling, Little law, bottleneck identification, and line balancing.", "low"),
            ("facility-layout", "Systematic Layout Planning (SLP), material flow matrices, cellular manufacturing, and warehouse layout.", "low"),
            ("production-planning", "Master production scheduling (MPS), Material Requirements Planning (MRP), and capacity planning (CRP).", "low"),
            ("inventory-optimization", "Economic order quantity (EOQ), safety stock calculations, reorder point (ROP), and ABC/XYZ analysis.", "low"),
            ("quality-engineering", "Statistical Process Control (SPC), control charts (X-bar, R), process capability (Cp, Cpk).", "low"),
            ("six-sigma", "DMAIC framework, Gage R&R studies, design of experiments (DOE), and defect reduction metrics.", "low"),
            ("lean-manufacturing", "Value stream mapping (VSM), 5S workplace organization, Kaizen, Kanban pull systems, and SMED.", "low"),
            ("simulation", "Discrete-event simulation modeling of manufacturing and logistics systems (Arena, Simio, AnyLogic).", "low"),
            ("ergonomics", "Biomechanics of lifting, NIOSH lifting equation, RULA/REBA assessment, and repetitive motion prevention.", "low"),
            ("human-factors", "Cognitive workload assessment, display/control interface ergonomics, and human error reduction.", "low"),
            ("work-study", "Time and motion studies, standard predetermined time systems (MOST, MTM), and work sampling.", "low"),
            ("scheduling", "Job shop and flow shop scheduling algorithms, priority dispatch rules, and Gantt tracking.", "low"),
            ("supply-chain-optimization", "Network design, multi-echelon inventory positioning, bullwhip effect mitigation, and freight routing.", "low"),
            ("reliability", "Component and system reliability calculations, redundancy allocation, and hazard rate functions.", "low"),
            ("systems-engineering", "Requirements traceability (V-model), system architecture, trade studies, and lifecycle verification.", "low"),
        ]
    },
    "semiconductor": {
        "title": "Semiconductor, VLSI & Chip Design",
        "skills": [
            ("semiconductor-physics", "Energy band diagrams, carrier concentrations, drift-diffusion, PN junctions, and sub-micron MOS physics.", "low"),
            ("transistor-design", "FinFET, GAA-FET, nanosheet architectures, threshold voltage tuning, and leakage current optimization.", "low"),
            ("analog-ic-design", "CMOS op-amps, bandgap references, current mirrors, noise analysis, and phase-locked loops (PLL).", "low"),
            ("digital-ic-design", "Static and dynamic CMOS logic, setup and hold time constraints, pipeline design, and clock trees.", "low"),
            ("rtl-design", "Register-transfer level microarchitecture, pipelined data paths, control state machines, and FIFO design.", "low"),
            ("verilog", "Hardware description in IEEE 1364 Verilog: synthesizable constructs, blocking vs non-blocking, and testbenches.", "low"),
            ("systemverilog", "SystemVerilog verification constructs: interfaces, assertions (SVA), classes, covergroups, and UVM.", "low"),
            ("vhdl", "VHDL design and testbench modeling: entities, architectures, strong typing, and synthesis guidelines.", "low"),
            ("asic", "ASIC design flow from architecture definition through fabrication handoff, tapeout, and MPW submission.", "low"),
            ("fpga", "FPGA mapping, LUT utilization, DSP slice configuration, block RAM instantiation, and bitstream generation.", "low"),
            ("physical-design", "Netlist-to-GDSII flow: floorplanning, power distribution networks, placement, clock tree, and routing.", "low"),
            ("synthesis", "Logic synthesis with Design Compiler/Yosys: technology mapping, area-delay trade-offs, and constraints.", "low"),
            ("place-and-route", "Detailed placement, global and detailed routing, congestion reduction, and DRC/LVS clean layouts.", "low"),
            ("timing-analysis", "Static Timing Analysis (STA), setup/hold slack, clock skew, jitter, false paths, and multi-cycle paths.", "low"),
            ("formal-verification", "Equivalence checking, model checking, property verification, and formal proofs of correctness.", "low"),
            ("chip-verification", "Universal Verification Methodology (UVM) testbenches, constrained random testing, and functional coverage.", "low"),
            ("eda-tools", "Electronic Design Automation tools scripting: Tcl scripting for Synopsys, Cadence, and OpenROAD.", "low"),
            ("semiconductor-fabrication", "Cleanroom process flow: wafer cleaning, thermal oxidation, ion implantation, thin-film deposition.", "medium"),
            ("lithography", "Photolithography steps: photoresist coating, EUV exposure, phase-shift masks, and overlay alignment.", "medium"),
            ("packaging", "Advanced packaging: 2.5D/3D ICs, chiplets, interposers, wire bonding, flip-chip, and thermal dissipation.", "low"),
            ("chip-testing", "Design for Testability (DFT): scan chains, BIST, boundary scan (JTAG), and ATE test pattern generation.", "low"),
        ]
    },
    "embedded": {
        "title": "Embedded Systems & Bare-Metal Hardware",
        "skills": [
            ("microcontrollers", "MCU architectural selection, register-level programming, memory mapping, and clock tree configuration.", "low"),
            ("arm", "ARM Cortex-M/A core architecture, thumb instructions, NVIC interrupt controller, and CMSIS drivers.", "low"),
            ("avr", "Atmel AVR microcontroller architecture, fuse bits, timers, interrupts, and bare-metal C programming.", "low"),
            ("risc-v", "RISC-V ISA extensions (RV32I/RV64G), privilege modes, trap handling, and open-source core design.", "low"),
            ("esp32", "Espressif ESP32/ESP-IDF development, dual-core task pinout, Wi-Fi/BLE stacks, and low power sleep modes.", "low"),
            ("stm32", "STMicroelectronics STM32 HAL/LL drivers, CubeMX configuration, DMA controllers, and high-speed timers.", "low"),
            ("firmware", "Production embedded C/C++ firmware architecture, state machines, modular drivers, and flash memory layout.", "low"),
            ("device-drivers", "Writing kernel and bare-metal device drivers for sensors, displays, communications, and storage.", "low"),
            ("bare-metal", "Writing software without an OS: startup files, linker scripts, vector tables, and stack/heap memory.", "low"),
            ("rtos", "Real-time operating system concepts: preemptive multitasking, task scheduling, semaphores, and queues.", "low"),
            ("freertos", "FreeRTOS task creation, synchronization primitives, memory allocators, timers, and ISR safe functions.", "low"),
            ("embedded-linux", "Yocto Project, Buildroot, device trees, U-Boot bootloaders, and Linux kernel module compilation.", "low"),
            ("bootloaders", "Secondary bootloaders, secure boot verification, firmware updates, in-application programming (IAP).", "low"),
            ("hardware-debugging", "JTAG/SWD debugging, GDB server, logic analyzers, oscilloscopes, and bus decoders.", "low"),
            ("serial-protocols", "Framing, parity, baud rates, packet integrity checksums, and asynchronous communication streams.", "low"),
            ("i2c", "I2C master/slave state machines, pull-up resistor sizing, clock stretching, repeated starts, and SMBus.", "low"),
            ("spi", "Serial Peripheral Interface clock polarities (CPOL/CPHA), chip selects, multi-drop SPI, and QSPI.", "low"),
            ("uart", "Universal Asynchronous Receiver-Transmitter hardware FIFOs, ring buffers, DMA transfers, and flow control.", "low"),
            ("can-bus", "Controller Area Network (CAN 2.0B / CAN-FD) differential signaling, message arbitration, and DBC files.", "low"),
            ("power-management", "Dynamic frequency scaling, low-power sleep modes, wake-up interrupts, and battery runtime estimation.", "low"),
            ("hardware-security", "Secure cryptoprocessors, hardware root of trust, encrypted flash, side-channel attack mitigation.", "medium"),
        ]
    },
    "iot": {
        "title": "Internet of Things & Connected Devices",
        "skills": [
            ("sensors", "Interfacing environmental, inertial (IMU), optical, acoustic, and gas sensors with calibration routines.", "low"),
            ("actuators", "Driving solenoids, relays, stepper motors, servomotors, and PWM controlled power stages safely.", "low"),
            ("edge-computing", "Deploying compute workloads, lightweight inference, and localized processing on constrained IoT edges.", "low"),
            ("device-management", "Device provisioning, zero-touch onboarding, remote configuration, and lifecycle health monitoring.", "low"),
            ("mqtt", "MQTT 3.1.1/5.0 protocol: publish-subscribe patterns, QoS levels 0/1/2, retain flags, and broker clustering.", "low"),
            ("coap", "Constrained Application Protocol (CoAP): RESTful UDP interactions, block transfers, and observe patterns.", "low"),
            ("lorawan", "Long Range Wide Area Network: frequency plans, spreading factors, ADR, gateways, and join procedures.", "low"),
            ("zigbee", "IEEE 802.15.4 mesh networking, coordinators, routers, end devices, clusters, and ZCL profiles.", "low"),
            ("matter", "Matter protocol standard: Thread mesh networking, IPv6 over Low-Power Wireless, and smart home interoperability.", "low"),
            ("industrial-iot", "Industrial IoT (IIoT): OPC-UA protocols, Modbus TCP/RTU, SCADA integration, and factory floor telemetry.", "low"),
            ("smart-home", "Smart home device integration, home automation gateways, sensor rules engines, and local voice control.", "low"),
            ("smart-city", "Urban sensor deployments, smart lighting, parking sensors, municipal water monitoring, and LoRaWAN meshes.", "low"),
            ("connected-vehicles", "Telematics control units (TCU), cellular V2X, OBD-II data extraction, and fleet vehicle telemetry.", "low"),
            ("telemetry", "Time-series data compression, ingestion pipelines, timestamp synchronization, and batched transmission.", "low"),
            ("edge-ai", "Running quantized TinyML models (TensorFlow Lite Micro, ONNX Runtime) directly on microcontrollers.", "low"),
            ("device-security", "Mutual TLS authentication, X.509 device certificates, secure element key storage, and OTA signing.", "medium"),
            ("fleet-management", "Monitoring large fleets of edge devices: batch firmware OTA updates, rollback triggers, and alerts.", "low"),
        ]
    },
    "languages": {
        "title": "Languages, Translation & Localization",
        "skills": [
            ("translation", "High-fidelity source-to-target translation preserving register, nuances, idioms, and technical accuracy.", "low"),
            ("interpretation", "Consecutive and simultaneous interpretation strategies, note-taking methods, and cognitive workflows.", "low"),
            ("localization", "Software and content localization: date/time formats, currencies, pluralization rules, and UI layout constraints.", "low"),
            ("transcreation", "Creative translation adapting brand slogans, humor, and marketing copy for distinct cultural resonance.", "low"),
            ("terminology-management", "Building and maintaining multilingual termbases, glossaries, translation memories, and TBX files.", "low"),
            ("language-learning", "Pedagogical frameworks for second-language acquisition, spaced repetition, and communicative drills.", "low"),
            ("pronunciation", "Phonetic transcription (IPA), accent reduction, prosody, intonation, and speech clarity training.", "low"),
            ("grammar", "Structural analysis of grammatical rules, syntax parsing, verb conjugation systems, and morphology.", "low"),
            ("vocabulary", "Lexical expansion, collocations, etymology, semantic fields, and frequency-based vocabulary acquisition.", "low"),
            ("multilingual-writing", "Crafting cross-cultural communications, email diplomacy, and parallel multilingual documentation.", "low"),
            ("subtitling", "SRT/VTT subtitle creation, reading speed constraints (CPS), line breaking, and audio-text synchronization.", "low"),
            ("dubbing", "Lip-sync adaptation, voice actor script timing, voiceover script localization, and audio mix delivery.", "low"),
            ("transcription", "Accurate verbatim and clean-read audio transcription with speaker diarization and timestamping.", "low"),
            ("linguistic-analysis", "Textual corpus analysis, syntactic dependency trees, discourse markers, and stylometrics.", "low"),
            ("cultural-adaptation", "Assessing taboo concepts, color symbolism, semiotics, and socio-cultural expectations per locale.", "low"),
            ("machine-translation", "Neural Machine Translation (NMT) fine-tuning, post-editing workflows (MTPE), and BLEU/COMET scoring.", "low"),
            ("localization-testing", "Pseudo-localization, visual cut-off detection, RTL layout testing, and character encoding QA.", "low"),
            ("multilingual-seo", "Hreflang tags, localized keyword research, search intent adaptation, and international sitemaps.", "low"),
        ]
    },
    "linguistics": {
        "title": "Linguistics & Formal Language Systems",
        "skills": [
            ("phonetics", "Acoustic and articulatory phonetics: vowel formants, consonant voicing, spectrograms, and IPA.", "low"),
            ("phonology", "Phonemes, allophones, phonological rules, syllable structure, stress systems, and tone phonology.", "low"),
            ("morphology", "Morphemes, inflection, derivation, compounding, morphophonology, and agglutinative languages.", "low"),
            ("syntax", "Constituency tests, phrase structure grammars, X-bar theory, transformational grammar, and Minimalist program.", "low"),
            ("semantics", "Formal semantics, truth conditions, lambda calculus for natural language, entailment, and presupposition.", "low"),
            ("pragmatics", "Gricean maxims, speech acts, conversational implicature, deixis, politeness theory, and context.", "low"),
            ("sociolinguistics", "Dialectology, sociolects, language variation, diglossia, code-switching, and language prestige.", "low"),
            ("psycholinguistics", "Language acquisition, brain representation of language (Broca/Wernicke), and parsing models.", "low"),
            ("computational-linguistics", "Tokenization, Part-of-Speech tagging, lemmatization, dependency parsing, and semantic role labeling.", "low"),
            ("corpus-linguistics", "Corpus concordances, collocation extraction, n-gram statistical significance, and COCA querying.", "low"),
            ("historical-linguistics", "Comparative method, sound laws, proto-language reconstruction, language families, and cognates.", "low"),
            ("typology", "Cross-linguistic word order typology (SOV/SVO), morphological synthesis types, and language universals.", "low"),
            ("discourse-analysis", "Conversation analysis, turn-taking rules, cohesion/coherence, and critical discourse analysis.", "low"),
            ("lexicography", "Dictionary compilation principles, sense division, corpus-based citations, and headword selection.", "low"),
            ("language-documentation", "Field recording methodologies, glossing standards (Leipzig rules), and endangered language archiving.", "low"),
        ]
    },
    "psychology": {
        "title": "Psychology & Behavioral Sciences",
        "skills": [
            ("cognitive-psychology", "Human information processing: perception, attention bottlenecks, working memory, and mental models.", "low"),
            ("developmental-psychology", "Cognitive, emotional, and social development across lifespan: Piaget stages, attachment theory.", "low"),
            ("social-psychology", "Attribution theory, cognitive dissonance, conformity, group dynamics, ingroup bias, and persuasion.", "low"),
            ("behavioral-psychology", "Classical and operant conditioning, reinforcement schedules, habit loops, and extinction.", "low"),
            ("clinical-psychology", "Psychopathological frameworks (DSM-5), cognitive behavioral therapy models, and symptom assessment.", "medium"),
            ("organizational-psychology", "Job satisfaction, leadership styles, employee motivation, organizational culture, and team cohesion.", "low"),
            ("educational-psychology", "Constructivism, cognitive load theory, intrinsic/extrinsic motivation, and instructional design.", "low"),
            ("neuropsychology", "Executive functioning, neurocognitive deficits, hemispatial neglect, aphasia, and memory systems.", "low"),
            ("personality-psychology", "Big Five personality traits (OCEAN), psychometric evaluation, trait stability, and behavioral correlates.", "low"),
            ("positive-psychology", "PERMA model, character strengths, flow states, psychological resilience, and subjective well-being.", "low"),
            ("experimental-psychology", "Hypothesis testing, double-blind randomized experimental designs, and validity controls.", "low"),
            ("psychometrics", "Item response theory, test reliability (Cronbach alpha), construct validity, and factor analysis.", "low"),
            ("behavioral-economics", "Heuristics and biases (Kahneman/Tversky), loss aversion, framing effects, and prospect theory.", "low"),
            ("human-factors", "Situational awareness models, error taxonomies (slips vs mistakes), and workload ratings (NASA-TLX).", "low"),
            ("perception", "Psychophysics, Weber-Fechner laws, visual processing (Gestalt laws), and sensory integration.", "low"),
            ("memory", "Encoding, consolidation, retrieval cues, working memory buffers, and forgetting curve mitigation.", "low"),
            ("learning", "Motor skill acquisition, associative learning, schema formation, and transfer of learning principles.", "low"),
            ("decision-making", "Dual-process theory (System 1 vs System 2), bounded rationality, satisficing, and choice architecture.", "low"),
        ]
    },
    "tax": {
        "title": "Taxation, Statutory Compliance & Tariffs",
        "skills": [
            ("individual-tax", "Personal income tax calculation, progressive tax brackets, standard/itemized deductions, and credits.", "low"),
            ("corporate-tax", "Corporate income tax liabilities, permanent/temporary book-tax differences, NOL carryforwards, and rates.", "low"),
            ("vat", "Value Added Tax mechanisms: input/output VAT recovery, reverse charge rules, and VAT return filing.", "low"),
            ("gst", "Goods and Services Tax dual structures, input tax credit reconciliation, and invoice matching.", "low"),
            ("sales-tax", "State and local sales tax nexus (Wayfair doctrine), exemption certificates, and marketplace facilitator rules.", "low"),
            ("payroll-tax", "Employer/employee withholding, Social Security/Medicare taxes, FUTA/SUTA, and year-end reporting.", "low"),
            ("property-tax", "Ad valorem property assessments, millage rates, tax appeals, and homestead exemptions.", "low"),
            ("capital-gains-tax", "Short-term vs long-term capital gains, cost basis adjustments, wash sales, and Section 1031 exchanges.", "low"),
            ("international-tax", "Tax treaties, foreign tax credits, Controlled Foreign Corporations (CFC), BEPS, and GILTI/Pillar 2.", "low"),
            ("transfer-pricing", "Arm length principle, transfer pricing documentation (local file, master file, CbCR), and cost-plus models.", "low"),
            ("tax-accounting", "ASC 740 / IAS 12 income tax accounting: deferred tax assets/liabilities, and valuation allowances.", "low"),
            ("tax-compliance", "Statutory tax calendar management, electronic filing standards, and audit trail preparation.", "low"),
            ("tax-research", "Statutory tax code interpretation, revenue rulings, Treasury regulations, and judicial tax case law.", "low"),
            ("tax-planning", "Strategic tax minimization, entity classification elections, R&D tax credits, and retirement deferrals.", "low"),
            ("withholding-tax", "Cross-border withholding on dividends, interest, royalties, and W-8BEN/W-9 certifications.", "low"),
            ("customs-duties", "Harmonized System (HS) tariff classification, customs valuation, rules of origin, and import duties.", "low"),
            ("tax-audit", "Defending tax audits, responding to Information Document Requests (IDR), and appeals processes.", "low"),
        ]
    },
    "actuarial": {
        "title": "Actuarial Science & Quantitative Risk Modeling",
        "skills": [
            ("actuarial-mathematics", "Present value of future life contingencies, net single premiums, annuity values, and commutation.", "low"),
            ("mortality-models", "Makeham/Gompertz laws, Lee-Carter mortality forecasting models, and life tables.", "low"),
            ("survival-analysis", "Kaplan-Meier survival curves, hazard rates, Cox proportional hazards regression, and censoring.", "low"),
            ("life-insurance", "Whole life, term life, endowment products, reserving (net level vs preliminary term), and surrender values.", "low"),
            ("health-insurance", "Morbidity tables, medical loss ratio (MLR) calculations, copay/deductible modeling, and claims projections.", "low"),
            ("property-casualty", "P&C loss distributions (Pareto, Lognormal), frequency-severity modeling, and exposure rating.", "low"),
            ("reserving", "Loss reserving techniques: Chain-Ladder method, Bornhuetter-Ferguson, and Cape Cod methods.", "low"),
            ("pricing", "Actuarial ratemaking: loss cost calculation, expense loading, profit provision, and credibility theory.", "low"),
            ("catastrophe-modeling", "Probabilistic catastrophe risk models, exceedance probability (EP) curves, and event loss tables.", "low"),
            ("pension-modeling", "Defined benefit/defined contribution pension valuations, projected unit credit, and funding ratios.", "low"),
            ("risk-theory", "Ruin theory, Cramér-Lundberg model, aggregate claim distributions, and stop-loss reinsurance.", "low"),
            ("stochastic-modeling", "Stochastic asset-liability modeling (ALM), interest rate generators (Hull-White), and ESG simulation.", "low"),
            ("actuarial-statistics", "Bühlmann credibility, generalized linear models (GLMs) for insurance rate filing, and tweedie distribution.", "low"),
            ("solvency", "Solvency II regulatory capital requirements (SCR/MCR), risk-based capital (RBC), and ORSA reporting.", "low"),
            ("enterprise-risk", "Enterprise Risk Management (ERM) frameworks, risk appetite statements, and stress testing scenarios.", "low"),
        ]
    },
    "procurement": {
        "title": "Procurement, Strategic Sourcing & Vendor Management",
        "skills": [
            ("sourcing", "Strategic sourcing process: supply market assessment, RFx development, and total cost modeling.", "low"),
            ("supplier-discovery", "Identifying, vetting, and qualifying prospective commercial and manufacturing vendors.", "low"),
            ("rfq", "Request for Quotation (RFQ) structuring, commercial specification sheets, and pricing matrices.", "low"),
            ("rfp", "Request for Proposal (RFP) drafting, scope of work definitions, and weighted evaluation criteria.", "low"),
            ("rfis", "Request for Information (RFI) campaigns, market capability surveys, and preliminary supplier screening.", "low"),
            ("bid-evaluation", "Quantitative bid leveling, normalization of commercial proposals, and cost-benefit analysis.", "low"),
            ("supplier-selection", "Multi-stakeholder decision matrices, supplier scorecarding, and final award recommendations.", "low"),
            ("supplier-risk", "Assessing vendor financial solvency, single-source dependencies, geopolitical risk, and ESG compliance.", "low"),
            ("supplier-negotiation", "BATNA preparation, price-break curves, payment terms (Net 30/60), and contractual SLAs.", "low"),
            ("purchase-orders", "PO creation, matching three-way match (PO, receipt, invoice), and ERP order transmission.", "low"),
            ("contract-management", "Master Service Agreements (MSA), Statements of Work (SOW), renewals, and milestone acceptance.", "low"),
            ("spend-analysis", "Extracting, cleansing, and categorizing procurement spend data into taxonomy hierarchies.", "low"),
            ("category-management", "Developing multi-year category strategies for direct, indirect, IT, and MRO expenditures.", "low"),
            ("strategic-sourcing", "Kraljic matrix classification, supplier consolidation, and long-term partnership agreements.", "low"),
            ("procurement-analytics", "Tracking savings metrics (cost reduction vs avoidance), supplier on-time delivery, and defect rates.", "low"),
            ("e-procurement", "Punchout catalogs, electronic data interchange (EDI), and automated procure-to-pay (P2P) systems.", "low"),
        ]
    },
    "customer-service": {
        "title": "Customer Service & Support Operations",
        "skills": [
            ("helpdesk", "Helpdesk operations: ticketing workflows, first-contact resolution (FCR), and shift scheduling.", "low"),
            ("ticket-triage", "Automated and manual ticket categorization, urgency/impact matrix tagging, and routing.", "low"),
            ("live-chat", "Synchronous customer chat etiquette, canned responses, multitasking handling, and swift resolution.", "low"),
            ("call-center", "Inbound call workflows, interactive voice response (IVR) routing, and average handle time (AHT).", "low"),
            ("knowledge-base", "Authoring internal and customer-facing help center articles, knowledge management (KCS), and updates.", "low"),
            ("faq", "Structuring concise, actionable Frequently Asked Questions based on high-frequency search queries.", "low"),
            ("escalation", "Tier 1 to Tier 3 escalation pathways, incident management handoffs, and SLA breach mitigation.", "low"),
            ("complaint-management", "De-escalation techniques, empathy frameworks, root-cause investigation, and formal dispute closure.", "low"),
            ("refund-processing", "Validating refund eligibility, issuing credit adjustments, and handling dispute chargebacks.", "low"),
            ("returns", "Return Merchandise Authorization (RMA) workflows, return shipping logistics, and restock inspection.", "low"),
            ("service-recovery", "Restoring customer trust following service failures, goodwill credits, and follow-up outreach.", "low"),
            ("customer-feedback", "Deploying and analyzing CSAT, Net Promoter Score (NPS), and Customer Effort Score (CES) surveys.", "low"),
            ("voice-of-customer", "Synthesizing unstructured support transcripts to identify product friction points and churn drivers.", "low"),
            ("support-analytics", "Reporting on ticket backlog, queue trends, resolution velocity, and agent performance benchmarks.", "low"),
            ("chatbot-support", "Configuring virtual support assistants, intent recognition, fallback routing, and conversational flows.", "low"),
            ("quality-assurance", "Customer service call and ticket scoring, rubrics, agent coaching, and compliance monitoring.", "low"),
        ]
    },
    "business-intelligence": {
        "title": "Business Intelligence & Enterprise Analytics",
        "skills": [
            ("power-bi", "Power BI report building, DAX formulas, Power Query M transformations, and workspace distribution.", "low"),
            ("tableau", "Tableau desktop authoring, calculated fields, Level of Detail (LOD) expressions, and server deployment.", "low"),
            ("looker", "LookML data modeling, views, explores, dimensions, measures, and Looker dashboard creation.", "low"),
            ("qlik", "Qlik Sense associative data modeling, set analysis, script editor transformations, and visual analytics.", "low"),
            ("dashboards", "User-centered executive dashboard design, visual hierarchy, layout grids, and interactive filtering.", "low"),
            ("executive-reporting", "High-level summary reporting, boardroom slides, variance explanations, and milestone tracking.", "low"),
            ("kpi-design", "Defining SMART Key Performance Indicators, leading vs lagging indicators, and calculation formulas.", "low"),
            ("metrics", "Metric tree decomposition, north star metrics, unit economics, and operational efficiency indicators.", "low"),
            ("semantic-models", "Centralized semantic layers, metric stores, dimensional business logic, and reusable definitions.", "low"),
            ("dimensional-modeling", "Kimball dimensional modeling: star schemas, snowflake schemas, fact tables, and slowly changing dimensions.", "low"),
            ("data-warehousing", "Modern cloud data warehousing architecture on Snowflake, BigQuery, and Databricks SQL.", "low"),
            ("reporting-automation", "Automated report scheduling, email distribution, data alerting thresholds, and slack alerts.", "low"),
            ("self-service-bi", "Governed self-service analytics: certified datasets, data catalogs, and business user enablement.", "low"),
            ("decision-support", "Scenario modeling, sensitivity analysis, what-if simulations, and strategic trade-off matrices.", "low"),
        ]
    },
    "data-engineering": {
        "title": "Data Engineering & Pipeline Infrastructure",
        "skills": [
            ("etl", "Extract, Transform, Load design patterns: incremental loads, validation, and target transformations.", "low"),
            ("elt", "Extract, Load, Transform in cloud warehouses using SQL transformations, staging layers, and dbt.", "low"),
            ("data-pipelines", "Resilient pipeline architecture: idempotency, checkpointing, retry backoff, and dead-letter queues.", "low"),
            ("batch-processing", "Scheduled large-scale batch processing workflows, partition pruning, and bulk data loading.", "low"),
            ("stream-processing", "Real-time event streaming: windowing (tumbling/sliding), watermarks, and stateful stream processing.", "low"),
            ("kafka", "Apache Kafka producer/consumer configuration, topic partitioning, consumer groups, and schema registry.", "low"),
            ("spark", "Apache Spark / PySpark: DataFrame operations, catalyst optimizer, shuffling tuning, and RDD operations.", "low"),
            ("flink", "Apache Flink stateful stream processing, checkpointing, event-time processing, and CEP rules.", "low"),
            ("airflow", "Apache Airflow DAG authoring, task dependencies, custom operators, XComs, and Celery executors.", "low"),
            ("dagster", "Dagster asset-based orchestration, software-defined assets, resources, and declarative scheduling.", "low"),
            ("dbt", "Data Build Tool (dbt): model building, ref() macros, Jinja templating, incremental models, and tests.", "low"),
            ("data-quality", "Automated data quality checks (Great Expectations, dbt tests), anomaly detection, and schema validation.", "low"),
            ("data-observability", "Pipeline monitoring: freshness, volume, distribution, schema drift, and end-to-end lineage.", "low"),
            ("data-lineage", "Tracking column and table-level lineage, upstream dependency graphs, and impact analysis.", "low"),
            ("data-governance", "Data classification, access control policies, tagging, retention schedules, and regulatory compliance.", "low"),
            ("data-catalog", "Metadata discovery, business glossaries, automated table indexing, and data asset documentation.", "low"),
            ("lakehouse", "Lakehouse architecture: Delta Lake, Apache Iceberg, ACID transactions on object storage, and time travel.", "low"),
            ("data-lake", "Data lake storage organization (raw, bronze, silver, gold zones), file formats (Parquet, ORC), and partitioning.", "low"),
            ("data-warehouse", "Data warehouse indexing, clustering keys, sort keys, materialization, and query optimization.", "low"),
            ("change-data-capture", "Debezium and database CDC pipelines, log-based CDC, and event-driven data propagation.", "low"),
            ("schema-management", "Avro/Protobuf schema evolution, backward/forward compatibility, and schema registries.", "low"),
            ("data-mesh", "Domain-driven decentralized data architecture, data products, self-serve data infrastructure, and federated governance.", "low"),
            ("feature-store", "Feast feature store management, offline/online feature sync, and low-latency feature serving.", "low"),
            ("reverse-etl", "Syncing warehouse analytical data back to operational SaaS tools (Salesforce, HubSpot, Zendesk).", "low"),
            ("real-time-analytics", "Sub-second analytical queries on real-time data using ClickHouse, Apache Pinot, and Rockset.", "low"),
        ]
    },
    "mlops": {
        "title": "MLOps & Machine Learning Operations",
        "skills": [
            ("model-training", "Reproducible distributed training pipelines, hyperparameters, checkpointing, and GPU cluster orchestration.", "low"),
            ("model-versioning", "Tracking model artifacts, code commits, dataset versions, and training run environments.", "low"),
            ("experiment-tracking", "Logging metrics, parameters, and confusion matrices with MLflow, Weights & Biases, and Comet.", "low"),
            ("model-registry", "Model stage transitions (staging, production, archived), model signing, and approval workflows.", "low"),
            ("model-serving", "Deploying models via REST/gRPC endpoints using Triton, TorchServe, vLLM, and FastAPI.", "low"),
            ("model-monitoring", "Tracking real-time inference latency, throughput, prediction distributions, and error rates.", "low"),
            ("model-drift", "Detecting concept drift, prediction drift, statistical tests (PSI, KS test), and retraining triggers.", "low"),
            ("data-drift", "Monitoring input covariate shift, feature distribution changes, and missing value spikes.", "low"),
            ("feature-engineering", "Scalable feature transformations, normalization, categorical encoding, and feature stores.", "low"),
            ("feature-stores", "Managing point-in-time correct feature retrieval for training and online microsecond serving.", "low"),
            ("model-evaluation", "Offline evaluation: ROC-AUC, PR-AUC, F1, RMSE, calibration curves, and slice-based evaluations.", "low"),
            ("model-validation", "Pre-deployment checks: stress testing, invariant tests, directional expectations, and sanity gates.", "low"),
            ("model-governance", "Auditing model lineages, compliance checklists, bias mitigation documentation, and approval logs.", "low"),
            ("model-security", "Hardening models against adversarial attacks, model inversion, and data poisoning threats.", "medium"),
            ("llmops", "Operationalizing LLM applications: prompt versioning, token caching, evaluation harnesses, and trace logs.", "low"),
            ("inference-optimization", "Model quantization (INT8, FP4, AWQ), TensorRT compilation, pruning, and speculative decoding.", "low"),
            ("gpu-inference", "Tuning CUDA kernels, dynamic batching, continuous batching, and multi-GPU tensor parallelism.", "low"),
            ("batch-inference", "Large-scale offline scoring pipelines, distributed batch jobs, and target storage output.", "low"),
            ("online-inference", "Sub-50ms real-time inference architectures, autoscaling replicas, and circuit breakers.", "low"),
            ("model-cost-optimization", "Monitoring compute spend, GPU spot instance training, token budgets, and right-sizing endpoints.", "low"),
        ]
    },
    "ai-evaluation": {
        "title": "AI Evaluation, Benchmarking & Safety Testing",
        "skills": [
            ("llm-evaluation", "Systematic evaluation of large language models: task-specific metrics, rubric scoring, and judge models.", "low"),
            ("benchmark-design", "Designing representative, contamination-free evaluation benchmarks and golden test sets.", "low"),
            ("hallucination-testing", "Quantifying factual inconsistency, ungrounded claims, and confidence calibration in generated text.", "low"),
            ("factuality-evaluation", "Automated fact-checking against reference corpora, claim decomposition, and verification.", "low"),
            ("groundedness", "Measuring source attribution, context citation accuracy, and faithfulness in RAG workflows.", "low"),
            ("retrieval-evaluation", "Assessing vector search and hybrid retrieval using MRR, NDCG@K, Hit Rate, and precision/recall.", "low"),
            ("rag-evaluation", "End-to-end RAG assessment: context relevance, answer relevance, faithfulness, and noise robustness.", "low"),
            ("agent-evaluation", "Evaluating autonomous agents: step-by-step trajectory validation, tool call accuracy, and loop detection.", "low"),
            ("tool-use-evaluation", "Testing structured tool calling: parameter validity, schema adherence, error recovery, and security.", "low"),
            ("safety-evaluation", "Evaluating safety guardrails against policy violations, harmful advice, and hate speech.", "medium"),
            ("robustness-testing", "Perturbation testing, typo injection, paraphrasing sensitivity, and out-of-distribution stability.", "low"),
            ("adversarial-testing", "Designing stress tests, edge cases, counterfactual examples, and deceptive prompts.", "low"),
            ("red-teaming", "Adversarial red-teaming methodologies: jailbreak probes, refusal bypasses, and ethical stress testing.", "medium"),
            ("prompt-injection-testing", "Simulating direct and indirect prompt injection attacks, delimiter escapes, and system override probes.", "medium"),
            ("bias-evaluation", "Measuring demographic parity, stereotyping, disparate impact, and representational harms in outputs.", "low"),
            ("toxicity-testing", "Screening and quantifying offensive language, profanity, and toxic content in model generations.", "low"),
            ("latency-benchmarking", "Measuring time-to-first-token (TTFT), tokens-per-second (TPS), and concurrent user latency curves.", "low"),
            ("cost-benchmarking", "Analyzing token expenditure, prompt overhead, model efficiency, and cost per task completion.", "low"),
            ("regression-testing", "Continuous automated regression testing across prompt versions, model updates, and tool changes.", "low"),
            ("golden-datasets", "Curating, annotating, versioning, and maintaining high-quality human-verified golden datasets.", "low"),
            ("human-evaluation", "Designing human evaluation rubrics, inter-annotator agreement (Cohen kappa), and blind evaluation.", "low"),
        ]
    }
}


def create_skill_markdown(slug: str, title_text: str, desc: str, cat: str, risk: str) -> str:
    display_title = title_text.replace("-", " ").title()
    content = f"""---
name: {slug}
description: "{desc}"
category: {cat}
version: 1.0.0
disable-model-invocation: false
risk: {risk}
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/{cat}/{slug}/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# {display_title}

## Overview & Domain Scope
`{slug}` provides operational playbooks, validated heuristics, and expert methodologies in **{cat.replace('-', ' ').title()}**.
{desc}

## Core Capabilities & Operational Playbooks
- Execute structured analysis and implementation workflows adhering to industry standards.
- Formulate quantitative models, specifications, and verified domain outputs.
- Verify constraints, edge cases, error conditions, and lifecycle safety requirements.
- Produce documented, reproducible artifacts compatible with multi-agent orchestration.

## Standards & Reference Frameworks
- Conforms to foundational domain standards, international guidelines, and best practices.
- Implements rigorous validation gates before finalizing technical recommendations.
- Ensures cross-system interoperability across AI agent platforms (Antigravity, Claude Code, Cursor, Codex).

## Verification & Quality Gates
1. Baseline Verification: Confirm all required inputs, parameters, and contextual boundaries are established.
2. Methodological Execution: Apply domain-specific procedures with verifiable intermediate checks.
3. Output Validation: Review calculations, assertions, safety guardrails, and compliance requirements.
"""
    return content


def synthesize_domains():
    print("=" * 60)
    print("      AUTHORITATIVE DOMAIN SYNTHESIS ENGINE")
    print("=" * 60)

    total_created = 0
    total_existing = 0

    for cat, data in DOMAINS_SPEC.items():
        cat_dir = AWESOME_DIR / cat
        cat_dir.mkdir(parents=True, exist_ok=True)
        print(f"Synthesizing domain: {cat} ({data['title']})...")

        for slug, desc, risk in data["skills"]:
            skill_dir = cat_dir / slug
            skill_md = skill_dir / "SKILL.md"

            if skill_md.exists():
                total_existing += 1
                continue

            skill_dir.mkdir(parents=True, exist_ok=True)
            content = create_skill_markdown(slug, slug, desc, cat, risk)
            skill_md.write_text(content, encoding="utf-8")
            total_created += 1

    print("\n" + "=" * 60)
    print("                 SYNTHESIS SUMMARY")
    print("=" * 60)
    print(f"Domains Processed:       {len(DOMAINS_SPEC)}")
    print(f"New Skills Synthesized:  {total_created}")
    print(f"Existing Maintained:     {total_existing}")
    print("=" * 60)


if __name__ == "__main__":
    synthesize_domains()
