"""
Full Skill Catalog - Defines comprehensive skills with metadata across all domains
"""

from typing import List
from .registry import SkillModule, SkillDomain, SkillLevel


def get_full_catalog() -> List[SkillModule]:
    """Returns the complete skill catalog across all 28 domains"""
    skills = []
    
    # 1. PROGRAMMING & SOFTWARE DEVELOPMENT
    skills.extend([
        SkillModule(
            name="prog.fundamentals",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.FUNDAMENTAL,
            priority=0,
            description="Programming fundamentals - variables, control flow, functions, data types",
            tags=["programming", "basics", "fundamentals"],
        ),
        SkillModule(
            name="prog.oop",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.fundamentals"],
            description="Object-Oriented Programming - classes, inheritance, polymorphism",
            tags=["programming", "oop", "paradigm"],
        ),
        SkillModule(
            name="prog.functional",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.fundamentals"],
            description="Functional Programming - pure functions, immutability, composition",
            tags=["programming", "functional", "paradigm"],
        ),
        SkillModule(
            name="prog.data_structures",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.CORE,
            priority=5,
            dependencies=["prog.fundamentals"],
            description="Data Structures - arrays, linked lists, trees, graphs, hash tables",
            tags=["programming", "data-structures", "cs-fundamentals"],
            repos=[
                "https://github.com/TheAlgorithms/Python",
                "https://github.com/trekhleb/javascript-algorithms",
            ],
        ),
        SkillModule(
            name="prog.algorithms",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.CORE,
            priority=5,
            dependencies=["prog.data_structures"],
            description="Algorithms - sorting, searching, graph algorithms, dynamic programming",
            tags=["programming", "algorithms", "cs-fundamentals"],
            repos=[
                "https://github.com/TheAlgorithms/Python",
                "https://github.com/williamfiset/Algorithms",
            ],
        ),
        SkillModule(
            name="prog.design_patterns",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            dependencies=["prog.oop"],
            description="Software Design Patterns - GoF patterns, architectural patterns",
            tags=["programming", "design-patterns", "architecture"],
            repos=[
                "https://github.com/iluwatar/java-design-patterns",
                "https://github.com/faif/python-patterns",
            ],
        ),
        SkillModule(
            name="prog.python",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.CORE,
            priority=5,
            dependencies=["prog.fundamentals"],
            description="Python programming language mastery",
            tags=["programming", "python", "language"],
            repos=["https://github.com/vinta/awesome-python"],
        ),
        SkillModule(
            name="prog.javascript",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.CORE,
            priority=5,
            dependencies=["prog.fundamentals"],
            description="JavaScript/TypeScript programming language mastery",
            tags=["programming", "javascript", "typescript", "language"],
            repos=["https://github.com/sorrycc/awesome-javascript"],
        ),
        SkillModule(
            name="prog.rust",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.INTERMEDIATE,
            priority=15,
            dependencies=["prog.fundamentals", "prog.data_structures"],
            description="Rust programming - ownership, borrowing, lifetimes",
            tags=["programming", "rust", "systems", "language"],
            repos=["https://github.com/rust-unofficial/awesome-rust"],
        ),
        SkillModule(
            name="prog.go",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.INTERMEDIATE,
            priority=15,
            dependencies=["prog.fundamentals"],
            description="Go programming - goroutines, channels, simplicity",
            tags=["programming", "go", "language"],
            repos=["https://github.com/avelino/awesome-go"],
        ),
        SkillModule(
            name="prog.cpp",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.INTERMEDIATE,
            priority=15,
            dependencies=["prog.fundamentals", "prog.data_structures"],
            description="C/C++ programming - memory management, templates, STL",
            tags=["programming", "c", "cpp", "systems", "language"],
            repos=["https://github.com/fffaraz/awesome-cpp"],
        ),
        SkillModule(
            name="prog.java",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.fundamentals", "prog.oop"],
            description="Java/Kotlin programming",
            tags=["programming", "java", "kotlin", "language"],
            repos=["https://github.com/akullpp/awesome-java"],
        ),
        SkillModule(
            name="prog.git",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.FUNDAMENTAL,
            priority=2,
            description="Git version control - branching, merging, rebasing, internals",
            tags=["programming", "git", "version-control", "tools"],
        ),
        SkillModule(
            name="prog.testing",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.CORE,
            priority=15,
            dependencies=["prog.fundamentals"],
            description="Software testing - unit, integration, e2e, property-based",
            tags=["programming", "testing", "quality"],
        ),
        SkillModule(
            name="prog.concurrency",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.ADVANCED,
            priority=25,
            dependencies=["prog.fundamentals", "prog.data_structures"],
            description="Concurrent/Parallel programming - threads, async, locks, atomics",
            tags=["programming", "concurrency", "parallel", "advanced"],
        ),
        SkillModule(
            name="prog.clean_code",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.INTERMEDIATE,
            priority=15,
            dependencies=["prog.fundamentals"],
            description="Clean code principles, refactoring, SOLID, DRY, KISS",
            tags=["programming", "clean-code", "best-practices"],
            repos=["https://github.com/ryanmcdermott/clean-code-javascript"],
        ),
    ])

    # 2. AI & MACHINE LEARNING
    skills.extend([
        SkillModule(
            name="ai.math_foundations",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.FUNDAMENTAL,
            priority=0,
            description="Math foundations for AI - linear algebra, calculus, probability",
            tags=["ai", "math", "foundations"],
        ),
        SkillModule(
            name="ai.classical_ml",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["ai.math_foundations", "prog.python"],
            description="Classical ML - regression, classification, clustering, dimensionality reduction",
            tags=["ai", "ml", "classical"],
            repos=["https://github.com/scikit-learn/scikit-learn"],
        ),
        SkillModule(
            name="ai.deep_learning",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            dependencies=["ai.classical_ml"],
            description="Deep Learning - neural networks, backpropagation, architectures",
            tags=["ai", "deep-learning", "neural-networks"],
            repos=[
                "https://github.com/pytorch/pytorch",
                "https://github.com/tensorflow/tensorflow",
            ],
        ),
        SkillModule(
            name="ai.nlp",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.INTERMEDIATE,
            priority=25,
            dependencies=["ai.deep_learning"],
            description="NLP - tokenization, embeddings, transformers, language models",
            tags=["ai", "nlp", "language"],
            repos=[
                "https://github.com/huggingface/transformers",
                "https://github.com/explosion/spaCy",
            ],
        ),
        SkillModule(
            name="ai.computer_vision",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.INTERMEDIATE,
            priority=25,
            dependencies=["ai.deep_learning"],
            description="Computer Vision - classification, detection, segmentation, generation",
            tags=["ai", "computer-vision", "image"],
            repos=[
                "https://github.com/ultralytics/ultralytics",
                "https://github.com/opencv/opencv",
            ],
        ),
        SkillModule(
            name="ai.llm",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.ADVANCED,
            priority=30,
            dependencies=["ai.nlp", "ai.deep_learning"],
            description="Large Language Models - GPT, LLaMA, fine-tuning, RLHF, prompting",
            tags=["ai", "llm", "gpt", "language-models"],
            repos=[
                "https://github.com/facebookresearch/llama",
                "https://github.com/ggerganov/llama.cpp",
                "https://github.com/ollama/ollama",
            ],
        ),
        SkillModule(
            name="ai.generative",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.ADVANCED,
            priority=30,
            dependencies=["ai.deep_learning"],
            description="Generative AI - GANs, VAEs, Diffusion Models, image/video generation",
            tags=["ai", "generative", "diffusion", "gan"],
            repos=[
                "https://github.com/CompVis/stable-diffusion",
                "https://github.com/AUTOMATIC1111/stable-diffusion-webui",
            ],
        ),
        SkillModule(
            name="ai.rl",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.ADVANCED,
            priority=30,
            dependencies=["ai.deep_learning"],
            description="Reinforcement Learning - Q-learning, policy gradient, PPO, multi-agent",
            tags=["ai", "reinforcement-learning", "rl"],
            repos=["https://github.com/Farama-Foundation/Gymnasium"],
        ),
        SkillModule(
            name="ai.mlops",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.INTERMEDIATE,
            priority=25,
            dependencies=["ai.classical_ml"],
            description="MLOps - experiment tracking, model serving, pipelines, monitoring",
            tags=["ai", "mlops", "deployment"],
            repos=[
                "https://github.com/mlflow/mlflow",
                "https://github.com/iterative/dvc",
            ],
        ),
        SkillModule(
            name="ai.agents",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.ADVANCED,
            priority=35,
            dependencies=["ai.llm"],
            description="AI Agents - tool use, planning, multi-agent systems, RAG",
            tags=["ai", "agents", "rag", "tools"],
            repos=[
                "https://github.com/langchain-ai/langchain",
                "https://github.com/run-llama/llama_index",
                "https://github.com/microsoft/autogen",
                "https://github.com/Significant-Gravitas/AutoGPT",
            ],
        ),
        SkillModule(
            name="ai.safety",
            domain=SkillDomain.AI_ML,
            level=SkillLevel.EXPERT,
            priority=40,
            dependencies=["ai.deep_learning", "ai.llm"],
            description="AI Safety - alignment, interpretability, adversarial robustness, fairness",
            tags=["ai", "safety", "alignment", "ethics"],
        ),
    ])

    # 3. CYBERSECURITY
    skills.extend([
        SkillModule(
            name="sec.fundamentals",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.FUNDAMENTAL,
            priority=0,
            description="Security fundamentals - CIA triad, threat modeling, risk assessment",
            tags=["security", "fundamentals"],
        ),
        SkillModule(
            name="sec.networking",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.CORE,
            priority=5,
            dependencies=["sec.fundamentals"],
            description="Network security - protocols, firewalls, IDS/IPS",
            tags=["security", "networking"],
        ),
        SkillModule(
            name="sec.web_hacking",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.INTERMEDIATE,
            priority=15,
            dependencies=["sec.fundamentals"],
            description="Web application security - OWASP Top 10, injection, XSS, CSRF",
            tags=["security", "web", "hacking", "pentesting"],
            repos=[
                "https://github.com/OWASP/wstg",
                "https://github.com/swisskyrepo/PayloadsAllTheThings",
                "https://github.com/juice-shop/juice-shop",
            ],
        ),
        SkillModule(
            name="sec.pentesting",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            dependencies=["sec.networking", "sec.fundamentals"],
            description="Penetration testing - methodology, tools, reporting",
            tags=["security", "pentesting", "offensive"],
            repos=[
                "https://github.com/rapid7/metasploit-framework",
                "https://github.com/nmap/nmap",
                "https://github.com/enaqx/awesome-pentest",
            ],
        ),
        SkillModule(
            name="sec.binary_exploitation",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.ADVANCED,
            priority=30,
            dependencies=["sec.fundamentals", "prog.cpp"],
            description="Binary exploitation - buffer overflow, ROP, heap exploitation, shellcode",
            tags=["security", "binary", "exploitation", "pwn"],
        ),
        SkillModule(
            name="sec.reverse_engineering",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.ADVANCED,
            priority=30,
            dependencies=["sec.fundamentals", "prog.cpp"],
            description="Reverse engineering - disassembly, decompilation, malware analysis",
            tags=["security", "reverse-engineering", "malware"],
            repos=[
                "https://github.com/NationalSecurityAgency/ghidra",
                "https://github.com/radareorg/radare2",
                "https://github.com/frida/frida",
            ],
        ),
        SkillModule(
            name="sec.cryptography",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            dependencies=["sec.fundamentals", "ai.math_foundations"],
            description="Cryptography - symmetric, asymmetric, hashing, PKI, ZKP",
            tags=["security", "cryptography", "encryption"],
        ),
        SkillModule(
            name="sec.forensics",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.INTERMEDIATE,
            priority=25,
            dependencies=["sec.fundamentals"],
            description="Digital forensics - disk, memory, network forensics, incident response",
            tags=["security", "forensics", "dfir"],
            repos=["https://github.com/volatilityfoundation/volatility3"],
        ),
        SkillModule(
            name="sec.osint",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.INTERMEDIATE,
            priority=15,
            dependencies=["sec.fundamentals"],
            description="OSINT - people search, domain intel, social media intelligence",
            tags=["security", "osint", "intelligence"],
            repos=[
                "https://github.com/sherlock-project/sherlock",
                "https://github.com/smicallef/spiderfoot",
            ],
        ),
        SkillModule(
            name="sec.cloud_security",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.ADVANCED,
            priority=30,
            dependencies=["sec.fundamentals"],
            description="Cloud security - AWS/GCP/Azure security, misconfigurations",
            tags=["security", "cloud", "aws", "gcp", "azure"],
        ),
        SkillModule(
            name="sec.active_directory",
            domain=SkillDomain.CYBERSECURITY,
            level=SkillLevel.ADVANCED,
            priority=30,
            dependencies=["sec.pentesting"],
            description="Active Directory attacks - Kerberoasting, DCSync, BloodHound",
            tags=["security", "active-directory", "windows"],
            repos=["https://github.com/BloodHoundAD/BloodHound"],
        ),
    ])

    # 4. WEB DEVELOPMENT
    skills.extend([
        SkillModule(
            name="web.html_css",
            domain=SkillDomain.WEB_DEV,
            level=SkillLevel.FUNDAMENTAL,
            priority=0,
            description="HTML5 & CSS3 - semantic HTML, accessibility, layouts, animations",
            tags=["web", "html", "css", "frontend"],
        ),
        SkillModule(
            name="web.javascript",
            domain=SkillDomain.WEB_DEV,
            level=SkillLevel.FUNDAMENTAL,
            priority=2,
            dependencies=["prog.javascript"],
            description="JavaScript for web - DOM, events, async, browser APIs",
            tags=["web", "javascript", "frontend"],
        ),
        SkillModule(
            name="web.react",
            domain=SkillDomain.WEB_DEV,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["web.javascript"],
            description="React ecosystem - hooks, context, Next.js, server components",
            tags=["web", "react", "frontend", "framework"],
            repos=[
                "https://github.com/facebook/react",
                "https://github.com/vercel/next.js",
            ],
        ),
        SkillModule(
            name="web.backend",
            domain=SkillDomain.WEB_DEV,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.fundamentals"],
            description="Backend development - APIs, authentication, server architecture",
            tags=["web", "backend", "api"],
            repos=[
                "https://github.com/tiangolo/fastapi",
                "https://github.com/expressjs/express",
            ],
        ),
        SkillModule(
            name="web.databases",
            domain=SkillDomain.WEB_DEV,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["web.backend"],
            description="Databases - SQL, NoSQL, ORMs, query optimization, design",
            tags=["web", "database", "sql", "nosql"],
            repos=[
                "https://github.com/prisma/prisma",
                "https://github.com/drizzle-team/drizzle-orm",
            ],
        ),
        SkillModule(
            name="web.fullstack",
            domain=SkillDomain.WEB_DEV,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            dependencies=["web.react", "web.backend", "web.databases"],
            description="Full-stack patterns - SSR, SSG, BFF, real-time, deployment",
            tags=["web", "fullstack"],
            repos=["https://github.com/gothinkster/realworld"],
        ),
        SkillModule(
            name="web.performance",
            domain=SkillDomain.WEB_DEV,
            level=SkillLevel.ADVANCED,
            priority=25,
            dependencies=["web.fullstack"],
            description="Web performance - Core Web Vitals, caching, CDN, optimization",
            tags=["web", "performance", "optimization"],
        ),
    ])

    # 5. DEVOPS & INFRASTRUCTURE
    skills.extend([
        SkillModule(
            name="devops.linux",
            domain=SkillDomain.DEVOPS,
            level=SkillLevel.FUNDAMENTAL,
            priority=0,
            description="Linux administration - filesystem, processes, networking, systemd",
            tags=["devops", "linux", "sysadmin"],
            repos=["https://github.com/trimstray/the-book-of-secret-knowledge"],
        ),
        SkillModule(
            name="devops.docker",
            domain=SkillDomain.DEVOPS,
            level=SkillLevel.CORE,
            priority=5,
            dependencies=["devops.linux"],
            description="Docker - images, containers, compose, multi-stage builds",
            tags=["devops", "docker", "containers"],
            repos=["https://github.com/veggiemonk/awesome-docker"],
        ),
        SkillModule(
            name="devops.kubernetes",
            domain=SkillDomain.DEVOPS,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            dependencies=["devops.docker"],
            description="Kubernetes - pods, services, deployments, helm, operators",
            tags=["devops", "kubernetes", "orchestration"],
            repos=[
                "https://github.com/kubernetes/kubernetes",
                "https://github.com/ramitsurana/awesome-kubernetes",
            ],
        ),
        SkillModule(
            name="devops.cicd",
            domain=SkillDomain.DEVOPS,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.git"],
            description="CI/CD - GitHub Actions, GitLab CI, ArgoCD, pipeline design",
            tags=["devops", "cicd", "automation"],
            repos=["https://github.com/argoproj/argo-cd"],
        ),
        SkillModule(
            name="devops.iac",
            domain=SkillDomain.DEVOPS,
            level=SkillLevel.INTERMEDIATE,
            priority=15,
            dependencies=["devops.linux"],
            description="Infrastructure as Code - Terraform, Ansible, Pulumi",
            tags=["devops", "iac", "terraform", "ansible"],
            repos=[
                "https://github.com/hashicorp/terraform",
                "https://github.com/ansible/ansible",
            ],
        ),
        SkillModule(
            name="devops.cloud",
            domain=SkillDomain.DEVOPS,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["devops.linux"],
            description="Cloud platforms - AWS, GCP, Azure services and architecture",
            tags=["devops", "cloud", "aws", "gcp", "azure"],
        ),
        SkillModule(
            name="devops.monitoring",
            domain=SkillDomain.DEVOPS,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            dependencies=["devops.linux"],
            description="Monitoring & Observability - Prometheus, Grafana, OpenTelemetry",
            tags=["devops", "monitoring", "observability"],
            repos=[
                "https://github.com/prometheus/prometheus",
                "https://github.com/grafana/grafana",
            ],
        ),
        SkillModule(
            name="devops.sre",
            domain=SkillDomain.DEVOPS,
            level=SkillLevel.ADVANCED,
            priority=30,
            dependencies=["devops.monitoring", "devops.kubernetes"],
            description="Site Reliability Engineering - SLIs/SLOs, error budgets, incident management",
            tags=["devops", "sre", "reliability"],
        ),
    ])

    # 6. DATA ENGINEERING
    skills.extend([
        SkillModule(
            name="data.pipelines",
            domain=SkillDomain.DATA,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.python"],
            description="ETL / ELT Pipelines with Airflow, dbt, Spark",
            tags=["data", "etl", "spark", "airflow"],
            repos=["https://github.com/apache/airflow", "https://github.com/dbt-labs/dbt-core"],
        ),
        SkillModule(
            name="data.streaming",
            domain=SkillDomain.DATA,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            dependencies=["data.pipelines"],
            description="Real-time stream processing with Kafka and Flink",
            tags=["data", "streaming", "kafka", "flink"],
            repos=["https://github.com/apache/kafka", "https://github.com/apache/flink"],
        ),
        SkillModule(
            name="data.analytics",
            domain=SkillDomain.DATA,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.python"],
            description="High-performance data analysis with Pandas, Polars, and DuckDB",
            tags=["data", "pandas", "polars", "duckdb"],
            repos=["https://github.com/pola-rs/polars", "https://github.com/duckdb/duckdb"],
        ),
    ])

    # 7. BLOCKCHAIN & WEB3
    skills.extend([
        SkillModule(
            name="blockchain.fundamentals",
            domain=SkillDomain.BLOCKCHAIN,
            level=SkillLevel.CORE,
            priority=5,
            dependencies=["sec.cryptography"],
            description="Blockchain fundamentals - consensus, P2P, merkle trees",
            tags=["blockchain", "web3", "crypto"],
        ),
        SkillModule(
            name="blockchain.smart_contracts",
            domain=SkillDomain.BLOCKCHAIN,
            level=SkillLevel.INTERMEDIATE,
            priority=15,
            dependencies=["blockchain.fundamentals", "prog.fundamentals"],
            description="Smart contract development - Solidity, security, gas optimization",
            tags=["blockchain", "smart-contracts", "solidity"],
            repos=[
                "https://github.com/OpenZeppelin/openzeppelin-contracts",
                "https://github.com/foundry-rs/foundry",
            ],
        ),
        SkillModule(
            name="blockchain.defi",
            domain=SkillDomain.BLOCKCHAIN,
            level=SkillLevel.ADVANCED,
            priority=25,
            dependencies=["blockchain.smart_contracts"],
            description="DeFi - AMMs, lending, yield farming, MEV",
            tags=["blockchain", "defi", "finance"],
            repos=["https://github.com/Uniswap/v3-core"],
        ),
        SkillModule(
            name="blockchain.zk",
            domain=SkillDomain.BLOCKCHAIN,
            level=SkillLevel.EXPERT,
            priority=40,
            dependencies=["blockchain.fundamentals", "sec.cryptography"],
            description="Zero-knowledge proofs - ZK-SNARKs, ZK-STARKs, circom, ZK-EVMs",
            tags=["blockchain", "zk", "zero-knowledge", "cryptography"],
            repos=["https://github.com/iden3/circom"],
        ),
    ])

    # 8. MOBILE DEVELOPMENT
    skills.extend([
        SkillModule(
            name="mobile.flutter",
            domain=SkillDomain.MOBILE,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.fundamentals"],
            description="Cross-platform mobile apps with Flutter & Dart",
            tags=["mobile", "flutter", "dart"],
            repos=["https://github.com/flutter/flutter"],
        ),
        SkillModule(
            name="mobile.react_native",
            domain=SkillDomain.MOBILE,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["web.react"],
            description="React Native cross-platform mobile development",
            tags=["mobile", "react-native"],
            repos=["https://github.com/facebook/react-native"],
        ),
    ])

    # 9. GAME DEVELOPMENT
    skills.extend([
        SkillModule(
            name="game.engines",
            domain=SkillDomain.GAME_DEV,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.fundamentals"],
            description="Game engine architecture - Godot, Bevy, Raylib",
            tags=["game-dev", "godot", "engine"],
            repos=["https://github.com/godotengine/godot", "https://github.com/bevyengine/bevy"],
        ),
        SkillModule(
            name="game.shaders",
            domain=SkillDomain.GAME_DEV,
            level=SkillLevel.ADVANCED,
            priority=25,
            dependencies=["game.engines"],
            description="GLSL/HLSL graphics shaders and particle effects",
            tags=["game-dev", "shaders", "graphics"],
        ),
    ])

    # 10. EMBEDDED SYSTEMS & IOT
    skills.extend([
        SkillModule(
            name="embedded.microcontrollers",
            domain=SkillDomain.EMBEDDED,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.cpp"],
            description="Microcontroller firmware - ESP32, STM32, Arduino, FreeRTOS",
            tags=["embedded", "firmware", "iot"],
            repos=["https://github.com/espressif/esp-idf", "https://github.com/FreeRTOS/FreeRTOS"],
        ),
    ])

    # 11. OS & LOW-LEVEL
    skills.extend([
        SkillModule(
            name="systems.os_concepts",
            domain=SkillDomain.OS_LOWLEVEL,
            level=SkillLevel.CORE,
            priority=5,
            dependencies=["prog.cpp"],
            description="OS concepts - processes, memory management, file systems, scheduling",
            tags=["systems", "os", "kernel"],
            repos=["https://github.com/mit-pdos/xv6-riscv"],
        ),
        SkillModule(
            name="systems.compiler_design",
            domain=SkillDomain.OS_LOWLEVEL,
            level=SkillLevel.ADVANCED,
            priority=30,
            dependencies=["prog.data_structures", "prog.algorithms"],
            description="Compiler design - lexing, parsing, AST, codegen, optimization",
            tags=["systems", "compiler", "language-design"],
            repos=["https://github.com/munificent/craftinginterpreters"],
        ),
    ])

    # 12. MATHEMATICS & CS THEORY
    skills.extend([
        SkillModule(
            name="math.cs_theory",
            domain=SkillDomain.MATH_CS,
            level=SkillLevel.CORE,
            priority=5,
            description="Complexity theory, automata, Turing machines, lambda calculus",
            tags=["math", "theory", "cs"],
        ),
    ])

    # 13. GRAPHICS & 3D
    skills.extend([
        SkillModule(
            name="graphics.webgpu_threejs",
            domain=SkillDomain.GRAPHICS_3D,
            level=SkillLevel.INTERMEDIATE,
            priority=15,
            dependencies=["web.javascript"],
            description="3D rendering on the web with WebGL, WebGPU, and Three.js",
            tags=["graphics", "threejs", "webgl"],
            repos=["https://github.com/mrdoob/three.js"],
        ),
    ])

    # 14. NETWORKING & DISTRIBUTED SYSTEMS
    skills.extend([
        SkillModule(
            name="systems.distributed",
            domain=SkillDomain.NETWORKING,
            level=SkillLevel.ADVANCED,
            priority=30,
            dependencies=["prog.algorithms"],
            description="Distributed systems - consensus, replication, consistency, CAP theorem",
            tags=["systems", "distributed", "consensus"],
            repos=["https://github.com/donnemartin/system-design-primer"],
        ),
    ])

    # 15. DESIGN (UI/UX)
    skills.extend([
        SkillModule(
            name="design.ui_ux",
            domain=SkillDomain.DESIGN,
            level=SkillLevel.CORE,
            priority=10,
            description="Design systems, layout hierarchy, typography, WCAG accessibility",
            tags=["design", "ui", "ux", "accessibility"],
        ),
    ])

    # 16. AUDIO & MUSIC
    skills.extend([
        SkillModule(
            name="audio.dsp_synthesis",
            domain=SkillDomain.AUDIO,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            description="Digital signal processing, audio synthesis, plugin development",
            tags=["audio", "dsp", "music"],
            repos=["https://github.com/JUCE-framework/JUCE"],
        ),
    ])

    # 17. ROBOTICS
    skills.extend([
        SkillModule(
            name="robotics.ros2",
            domain=SkillDomain.ROBOTICS,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            dependencies=["prog.python", "prog.cpp"],
            description="Robot Operating System 2, motion planning, SLAM navigation",
            tags=["robotics", "ros2", "slam"],
            repos=["https://github.com/ros2/ros2", "https://github.com/AtsushiSakai/PythonRobotics"],
        ),
    ])

    # 18. QUANTUM COMPUTING
    skills.extend([
        SkillModule(
            name="quantum.qiskit",
            domain=SkillDomain.QUANTUM,
            level=SkillLevel.ADVANCED,
            priority=25,
            dependencies=["ai.math_foundations"],
            description="Quantum circuits, qubits, quantum gates, Qiskit and PennyLane",
            tags=["quantum", "qiskit", "physics"],
            repos=["https://github.com/qiskit/qiskit"],
        ),
    ])

    # 19. BUSINESS & PROFESSIONAL
    skills.extend([
        SkillModule(
            name="biz.product_engineering",
            domain=SkillDomain.BUSINESS,
            level=SkillLevel.CORE,
            priority=10,
            description="Agile/Scrum roadmapping, RFCs, technical product requirements",
            tags=["business", "product", "agile"],
        ),
    ])

    # 20. SCIENCE & ENGINEERING
    skills.extend([
        SkillModule(
            name="science.computational",
            domain=SkillDomain.SCIENCE,
            level=SkillLevel.INTERMEDIATE,
            priority=20,
            dependencies=["prog.python"],
            description="Bioinformatics, computational physics, geospatial analysis",
            tags=["science", "bioinformatics", "physics"],
            repos=["https://github.com/biopython/biopython", "https://github.com/qgis/QGIS"],
        ),
    ])

    # 21. CREATIVE ARTS & WRITING
    skills.extend([
        SkillModule(
            name="creative.technical_writing",
            domain=SkillDomain.CREATIVE,
            level=SkillLevel.CORE,
            priority=5,
            description="Technical documentation, RFCs, architecture decision records, guides",
            tags=["creative", "writing", "documentation"],
        ),
    ])

    # 22. LANGUAGES & COMMUNICATION
    skills.extend([
        SkillModule(
            name="lang.cross_cultural",
            domain=SkillDomain.LANGUAGES,
            level=SkillLevel.CORE,
            priority=10,
            description="Technical persuasion, rhetoric, multi-lingual localization",
            tags=["languages", "communication", "localization"],
        ),
    ])

    # 23. HEALTH & FITNESS
    skills.extend([
        SkillModule(
            name="health.ergonomics",
            domain=SkillDomain.HEALTH,
            level=SkillLevel.CORE,
            priority=10,
            description="Developer ergonomics, cognitive endurance, stress management",
            tags=["health", "ergonomics", "wellness"],
        ),
    ])

    # 24. SURVIVAL & PRACTICAL SKILLS
    skills.extend([
        SkillModule(
            name="survival.preparedness",
            domain=SkillDomain.SURVIVAL,
            level=SkillLevel.CORE,
            priority=15,
            description="Disaster preparedness, trades craftsmanship, electrical basics",
            tags=["survival", "practical", "trades"],
        ),
    ])

    # 25. PSYCHOLOGY & COGNITIVE SKILLS
    skills.extend([
        SkillModule(
            name="psych.mental_models",
            domain=SkillDomain.PSYCHOLOGY,
            level=SkillLevel.CORE,
            priority=5,
            description="Mental models, cognitive bias mitigation, speed reading, learning strategies",
            tags=["psychology", "cognitive", "learning"],
        ),
    ])

    # 26. LEGAL & REGULATORY
    skills.extend([
        SkillModule(
            name="legal.compliance_oss",
            domain=SkillDomain.LEGAL,
            level=SkillLevel.CORE,
            priority=10,
            description="Open source licenses, GDPR/CCPA privacy, patent basics, compliance",
            tags=["legal", "compliance", "licensing"],
        ),
    ])

    # 27. AUTOMATION
    skills.extend([
        SkillModule(
            name="auto.browser_rpa",
            domain=SkillDomain.AUTOMATION,
            level=SkillLevel.CORE,
            priority=10,
            dependencies=["prog.python"],
            description="Browser automation with Playwright, Selenium, and workflow RPA",
            tags=["automation", "playwright", "scraping"],
            repos=["https://github.com/microsoft/playwright"],
        ),
    ])

    # 28. PRIVACY & ANONYMITY
    skills.extend([
        SkillModule(
            name="privacy.opsec",
            domain=SkillDomain.PRIVACY,
            level=SkillLevel.CORE,
            priority=10,
            description="Operational security, encrypted communications, Tor onion routing",
            tags=["privacy", "opsec", "security"],
        ),
    ])

    return skills
