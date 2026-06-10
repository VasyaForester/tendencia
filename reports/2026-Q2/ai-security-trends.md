# Тренды AI Security (2026-Q2) — Executive Brief

**Период:** 2026-04-01 — 2026-06-30  
**Сравнение:** vs 2026-Q1  
**Дата подготовки:** 2026-06-10  
**Источников собрано:** 330

---

## Краткое резюме для руководства

- **Саморазвивающиеся агенты (self-evolving agents)** — Поведение агента меняется без релиза: новая поверхность для APT и insider-style атак. Классический change control и периметр не видят «тихую» эволюцию policy в memory. Затронуты: Владельцы agentic платформ, SOC, команды с long-term memory (coding/research agents). Уверенность: **High**.
- **Регуляторика ИИ (AI Act и смежные требования)** — Даже при отсрочке штрафных рамок организации должны проектировать agent/RAG-архитектуру под lifecycle security и post-market monitoring — иначе дорогой rework в 2027. Затронуты: Compliance, legal, product owners в EU; глобальные вендоры с EU-клиентами. Уверенность: **High**.
- **Инструменты AI-агентов (MCP, skills, tool-use)** — Агент = суперпользователь с LLM-интерфейсом. Компрометация одного MCP/skill даёт persistent access через mcp.json и cross-server tool shadowing. Затронуты: Dev platform teams, SecOps, все пользователи AI coding assistants. Уверенность: **High**.
- **Prompt injection и обход политик моделей** — Не нужен доступ к модели — достаточно untrusted content в browser/RAG/email pipeline. Затронуты: Enterprise с browser tools, email agents, публичные coding assistants. Уверенность: **High**.
- **Инциденты и злоупотребления в продакшене** — Реальные CVE переводят agent risk из теории в patch Tuesday. Затронуты: Endpoint security, IT, разработчики на AI IDEs. Уверенность: **High**.
- **Новые сигналы в ландшафте AI Security** — Ранние индикаторы трендов H2 2026. Затронуты: Threat intel, R&D security. Уверенность: **Low**.
- **Риски supply chain моделей и артефактов** — Повторяющийся сигнал в собранных источниках квартала. Затронуты: Команды безопасности и владельцы AI-продуктов. Уверенность: **High**.
- **Атаки на RAG и слой данных** — Model-level guardrails не спасают, если poisoned chunk попадает в retrieval. Затронуты: RAG owners, data governance, teams с external crawlers. Уверенность: **Medium**.
- **MCP как новый software supply chain** — Третья сторона в agent stack так же критична, как зависимости в CI/CD. Затронуты: AppSec, platform engineering, procurement third-party AI tools. Уверенность: **High**.
- **Agent gateways и enforcement на transport layer** — Единственный масштабируемый контроль при hundreds of MCP tools per agent. Затронуты: Security architects внедряющих agentic AI. Уверенность: **Medium**.

---

## Что материально изменилось в квартале (vs 2026-Q1)

### 1. Саморазвивающиеся агенты (self-evolving agents)

Self-evolving agents вышли из research в зону production-рисков. Исследования Q2 2026 формализуют «Zombie Agents» (persistent memory injection) и «misevolution» — непреднамеренную деградацию alignment при эволюции memory/tools/workflow. Unit 42 показал poisoning долговременной памяти: вредоносные инструкции переживают сессии и приоритизируются над user input.

**Изменение к прошлому кварталу:** Vs Q1 2026: от концептуальных surveys к эмпирическим работам (ICLR 2026 misevolution, Zombie Agents) и vendor PoC по memory poisoning.

**Почему важно:** Поведение агента меняется без релиза: новая поверхность для APT и insider-style атак. Классический change control и периметр не видят «тихую» эволюцию policy в memory.

**Кому актуально:** Владельцы agentic платформ, SOC, команды с long-term memory (coding/research agents).

**Уверенность:** High

**Ключевые источники:**

- [RAILS: Verification-Native Clearing For Agentic Commerce](https://arxiv.org/abs/2606.08790v1) — papers, 2026-06-07
- [VATS: Exploiting Implicit Authority in Error-Path Injection via Systematic Mutation](https://arxiv.org/abs/2606.07992v1) — papers, 2026-06-06
- [From Privacy to Workflow Integrity: Communication-Graph Metadata in Autonomous Agent Interoperability](https://arxiv.org/abs/2606.07150v1) — papers, 2026-06-05
- [The Meta-Agent Challenge: Are Current Agents Capable of Autonomous Agent Development?](https://arxiv.org/abs/2606.04455v1) — papers, 2026-06-03
- [SeClaw: Spec-Driven Security Task Synthesis for Evaluating Autonomous Agents](https://arxiv.org/abs/2606.02302v1) — papers, 2026-06-01

### 2. Регуляторика ИИ (AI Act и смежные требования)

В Q2 2026 EU согласовала Digital Omnibus: сроки high-risk obligations сдвинуты (Annex III → 2 Dec 2027, product-embedded → 2 Aug 2028), но Article 15 (accuracy, robustness, cybersecurity) остаётся ядром — data/model poisoning, adversarial examples. Связка с Cyber Resilience Act уточняется на уровне Council.

**Изменение к прошлому кварталу:** Vs Q1 2026: политический deal 7 May 2026 заменил «дедлайн паники» на фазовое планирование; фокус CISO — mapping technical controls на Art. 15.

**Почему важно:** Даже при отсрочке штрафных рамок организации должны проектировать agent/RAG-архитектуру под lifecycle security и post-market monitoring — иначе дорогой rework в 2027.

**Кому актуально:** Compliance, legal, product owners в EU; глобальные вендоры с EU-клиентами.

**Уверенность:** High

**Ключевые источники:**

- [AI Act: Digital Omnibus agreement (European Parliament)](https://www.europarl.europa.eu/pdfs/news/expert/2026/5/press_release/20260427IPR42011/20260427IPR42011_en.pdf) — gov_cert, 2026-05-07
- [Article 15: Accuracy, Robustness and Cybersecurity (EU AI Act)](https://artificialintelligenceact.eu/article/15/) — standards, 2026-04-01
- [CP Plus 8 Ch. Network Video Recorder](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-05) — gov_cert, 2026-05-28
- [XCharge C6](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-08) — gov_cert, 2026-05-28
- [Jinan USR IOT Technology Limited (PUSR) USR-W610 RS232/485 to Wi-Fi/Ethernet Converter](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-02) — gov_cert, 2026-05-28

### 3. Инструменты AI-агентов (MCP, skills, tool-use)

MCP стал de-facto стандартом tool-use (Cursor, Windsurf, VS Code). Q2 2026 — волна CVE (вкл. CVE-2026-30615 zero-click RCE в Windsurf), CSA notes по STDIO RCE, npm supply-chain (WAVESHAPER). Аудит 2031 публичных MCP servers: ~40% с destructive/exec tools, 96% без предупреждений агенту. Skills/marketplace = новый software supply chain.

**Изменение к прошлому кварталу:** Vs Q1 2026: от «best practices» к documented exploit chains, CVE numeration и industry calls for transport-layer enforcement (agent gateways).

**Почему важно:** Агент = суперпользователь с LLM-интерфейсом. Компрометация одного MCP/skill даёт persistent access через mcp.json и cross-server tool shadowing.

**Кому актуально:** Dev platform teams, SecOps, все пользователи AI coding assistants.

**Уверенность:** High

**Ключевые источники:**

- [RAILS: Verification-Native Clearing For Agentic Commerce](https://arxiv.org/abs/2606.08790v1) — papers, 2026-06-07
- [VATS: Exploiting Implicit Authority in Error-Path Injection via Systematic Mutation](https://arxiv.org/abs/2606.07992v1) — papers, 2026-06-06
- [From Privacy to Workflow Integrity: Communication-Graph Metadata in Autonomous Agent Interoperability](https://arxiv.org/abs/2606.07150v1) — papers, 2026-06-05
- [MCP STDIO RCE: Supply Chain Risk (CSA)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_mcp-stdio-rce-agentic-infrastructure_20260510-csa-styled.pdf) — gov_cert, 2026-05-10
- [MCP Security Crisis: Systemic Design (CSA)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_MCP_security_crisis_20260504-csa-styled.pdf) — standards, 2026-05-04

### 4. Prompt injection и обход политик моделей

Indirect injection эволюционировал в agent-specific цепочки: веб-страница → IDE context → изменение mcp.json → RCE (OX/Windsurf). Tool descriptions как скрытый канал инструкций (tool poisoning) подтверждён CSA и Invariant Labs cross-server сценариями.

**Изменение к прошлому кварталу:** Zero-click IDE RCE и CVE-цепочки — качественный скачок vs Q1 advisory-only.

**Почему важно:** Не нужен доступ к модели — достаточно untrusted content в browser/RAG/email pipeline.

**Кому актуально:** Enterprise с browser tools, email agents, публичные coding assistants.

**Уверенность:** High

**Ключевые источники:**

- [CVE-2026-30615: Windsurf Zero-Click MCP Prompt Injection RCE](https://policylayer.com/mcp-incidents/windsurf-zero-click-mcp-rce-cve-2026-30615) — incidents, 2026-04-15
- [GitInject: Real-World Prompt Injection Attacks in AI-Powered CI/CD Pipelines](https://arxiv.org/abs/2606.09935) — papers, 2026-06-10
- [Assessing Automated Prompt Injection Attacks in Agentic Environments](https://arxiv.org/abs/2606.10525) — papers, 2026-06-10
- [Assessing Automated Prompt Injection Attacks in Agentic Environments](https://arxiv.org/abs/2606.10525v1) — papers, 2026-06-09
- [Brain-Prompt Injection: A Route-Safety Audit for BCI-LLM Agents](https://arxiv.org/abs/2606.09315v1) — papers, 2026-06-08

### 5. Инциденты и злоупотребления в продакшене

Инцидентный слой Q2: Windsurf CVE-2026-30615, LiteLLM CVE-2026-30623, массовые registry poisoning cases. Паттерн: AI assistant как канал exfil и persistence.

**Изменение к прошлому кварталу:** Количество critical CVE по agent tooling выросло кратно vs Q1.

**Почему важно:** Реальные CVE переводят agent risk из теории в patch Tuesday.

**Кому актуально:** Endpoint security, IT, разработчики на AI IDEs.

**Уверенность:** High

**Ключевые источники:**

- [MacGregor Voyage Data Recorder (VDR) G4e](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-01) — gov_cert, 2026-05-28
- [CISA Adds Two Known Exploited Vulnerabilities to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/08/cisa-adds-two-known-exploited-vulnerabilities-catalog) — gov_cert, 2026-06-08
- [CISA Adds One Known Exploited Vulnerability to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/05/cisa-adds-one-known-exploited-vulnerability-catalog) — gov_cert, 2026-06-05
- [Hitachi Energy ITT600 Explorer](https://www.cisa.gov/news-events/ics-advisories/icsa-26-155-02) — gov_cert, 2026-06-04
- [CISA Adds One Known Exploited Vulnerability to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/03/cisa-adds-one-known-exploited-vulnerability-catalog) — gov_cert, 2026-06-03

### 6. Новые сигналы в ландшафте AI Security

Смежные сигналы: autonomous coding worms, multi-agent trust boundaries, continuous runtime monitoring для policy drift.

**Изменение к прошлому кварталу:** Пока слабее подтверждены количественно.

**Почему важно:** Ранние индикаторы трендов H2 2026.

**Кому актуально:** Threat intel, R&D security.

**Уверенность:** Low

**Ключевые источники:**

- [Proof of Source of Funds: Efficient On-chain Provenance of Cryptoassets](https://arxiv.org/abs/2606.10172) — papers, 2026-06-10
- [Layer Order Semantics for Automata-Based Cybersecurity](https://arxiv.org/abs/2606.10649) — papers, 2026-06-10
- [Who Gets Flagged? The Pluralistic Evaluation Gap in AI Content Watermarking](https://arxiv.org/abs/2604.13776) — papers, 2026-06-10
- [Trustworthy Smart Fabs via Professional Proxies: Scaling Safe and Sustainable by Design (SSbD) through Industrial Data Spaces](https://arxiv.org/abs/2606.09227v1) — papers, 2026-06-08
- [Governance Controls for AI-Generated Test Artifacts in Autonomous Software Testing](https://arxiv.org/abs/2606.08806v1) — papers, 2026-06-07

### 7. Риски supply chain моделей и артефактов

Ключевые сигналы:
• Anchors that Don't Lift: Understanding Supply Chain Driven Kernel Lock-In and Governance-Mediated Mitigation Strategies in SOHO Devices
• MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills
• Supply Chain Compromises Impact Nx Console and GitHub Repositories

**Изменение к прошлому кварталу:** См. сравнение с предыдущим кварталом в полном отчёте.

**Почему важно:** Повторяющийся сигнал в собранных источниках квартала.

**Кому актуально:** Команды безопасности и владельцы AI-продуктов.

**Уверенность:** High

**Ключевые источники:**

- [Anchors that Don't Lift: Understanding Supply Chain Driven Kernel Lock-In and Governance-Mediated Mitigation Strategies in SOHO Devices](https://arxiv.org/abs/2606.11175) — papers, 2026-06-10
- [MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills](https://arxiv.org/abs/2606.07131) — papers, 2026-06-10
- [Supply Chain Compromises Impact Nx Console and GitHub Repositories](https://www.cisa.gov/news-events/alerts/2026/05/28/supply-chain-compromises-impact-nx-console-and-github-repositories) — gov_cert, 2026-05-28
- [GRAFT: Graphlet-Triggered Backdoor Attack on GNN-Based Hardware Security Systems](https://arxiv.org/abs/2606.10163) — papers, 2026-06-10
- [RedAct: Redacting Agent Capability Traces for Procedural Skill Protection](https://arxiv.org/abs/2606.10813) — papers, 2026-06-10

### 8. Атаки на RAG и слой данных

RAG остаётся data-layer attack surface: document injection и memory summarization превращают «факты» в инструкции. Unit 42 и AWS Bedrock case studies показывают приоритет memory над user prompt.

**Изменение к прошлому кварталу:** Больше PoC на long-term memory, не только single-turn RAG.

**Почему важно:** Model-level guardrails не спасают, если poisoned chunk попадает в retrieval.

**Кому актуально:** RAG owners, data governance, teams с external crawlers.

**Уверенность:** Medium

**Ключевые источники:**

- [Game-Theoretic Multi-Agent Control for Robust Contextual Reasoning in LLMs](https://arxiv.org/abs/2606.10322v1) — papers, 2026-06-09
- [Relevance as a Vulnerability: How Web Retrieval Degrades Safety Alignment in LLM Agents](https://arxiv.org/abs/2605.29224v1) — papers, 2026-05-28
- [ABB AC500 V2](https://www.cisa.gov/news-events/ics-advisories/icsa-26-146-02) — gov_cert, 2026-05-26
- [Game-Theoretic Multi-Agent Control for Robust Contextual Reasoning in LLMs](https://arxiv.org/abs/2606.10322) — papers, 2026-06-10
- [AgentCanary: A Security Evaluation Framework for Autonomous AI Agents in Real Executable Environments](https://arxiv.org/abs/2606.10484) — papers, 2026-06-10

### 9. MCP как новый software supply chain

MCP supply chain: 30+ CVE за 60 дней 2026, тысячи exposed servers (Shodan), 24k secrets в публичных mcp-конфигах (GitGuardian). North Korean npm hijack внедрял rogue MCP server в конфиги Claude/Cursor/Windsurf.

**Изменение к прошлому кварталу:** Первый квартал с массовой CVE-нумерацией именно для MCP ecosystem.

**Почему важно:** Третья сторона в agent stack так же критична, как зависимости в CI/CD.

**Кому актуально:** AppSec, platform engineering, procurement third-party AI tools.

**Уверенность:** High

**Ключевые источники:**

- [MCP STDIO RCE: Supply Chain Risk (CSA)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_mcp-stdio-rce-agentic-infrastructure_20260510-csa-styled.pdf) — gov_cert, 2026-05-10
- [CVE-2026-30615: Windsurf Zero-Click MCP Prompt Injection RCE](https://policylayer.com/mcp-incidents/windsurf-zero-click-mcp-rce-cve-2026-30615) — incidents, 2026-04-15
- [Anchors that Don't Lift: Understanding Supply Chain Driven Kernel Lock-In and Governance-Mediated Mitigation Strategies in SOHO Devices](https://arxiv.org/abs/2606.11175) — papers, 2026-06-10
- [MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills](https://arxiv.org/abs/2606.07131) — papers, 2026-06-10
- [CISA Adds Two Known Exploited Vulnerabilities to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/08/cisa-adds-two-known-exploited-vulnerabilities-catalog) — gov_cert, 2026-06-08

### 10. Agent gateways и enforcement на transport layer

Ответ индустрии: enforcement на transport layer — agent gateways, default-deny tool policy, JSON-RPC filtering, allowlist STDIO binaries. Сдвиг от «надеемся на LLM safety» к out-of-process runtime control.

**Изменение к прошлому кварталу:** Vs Q1: зрелые product/category «agent gateway» и CSA red teaming guides.

**Почему важно:** Единственный масштабируемый контроль при hundreds of MCP tools per agent.

**Кому актуально:** Security architects внедряющих agentic AI.

**Уверенность:** Medium

**Ключевые источники:**

- [CISA Adds Two Known Exploited Vulnerabilities to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/08/cisa-adds-two-known-exploited-vulnerabilities-catalog) — gov_cert, 2026-06-08
- [Our views on AI policy and political advocacy](https://openai.com/index/our-views-on-ai-policy-and-political-advocacy) — vendor, 2026-06-01
- [Schneider Electric EcoStruxure Panel Server](https://www.cisa.gov/news-events/ics-advisories/icsa-26-160-03) — gov_cert, 2026-06-09
- [EcoDefender: Energy-Efficient Hybrid Anomaly Detection for IoT Edge Gateways](https://arxiv.org/abs/2511.18235) — papers, 2026-06-10
- [Industrial policy for the Intelligence Age](https://openai.com/index/industrial-policy-for-the-intelligence-age) — vendor, 2026-06-09


---

## Ландшафт угроз (сжато)

| Поверхность | Сигнал квартала |
|-------------|-----------------|
| Модель и промпт | Prompt/indirect injection, jailbreaks |
| Агенты и инструменты | MCP, skills, delegated auth, tool abuse |
| RAG и данные | Poisoning, утечки через retrieval |
| Supply chain | Целостность моделей, зависимости, артефакты |
| Эксплуатация | Логирование агентов, IR, rate limits |
| Governance | AI Act, NIST/OWASP mapping, evals |

---

## Приоритетные рекомендации

1. **Инвентаризация agent tools** — каталог MCP/skills, owner, scope permissions (быстрый выигрыш).
2. **Разделение trusted/untrusted контекста** — для RAG и browser/email tools (стратегически).
3. **Запрет неконтролируемого self-modification** — human approval на новые skills и policy drift.
4. **Маппинг на AI Act / NIST AI RMF** — для high-risk use cases до масштабирования.
5. **Red-teaming агентных сценариев** — indirect injection + tool chain, не только chat jailbreaks.

---

## Метрики для мониторинга

- Количество активных MCP/skills и % с security review
- Инциденты tool invocation вне policy
- Доля ответов с retrieval из untrusted corpora
- Время реакции на новые vendor advisories по LLM

---

## Открытые вопросы

- Насколько self-evolving agents станут production-default в 2026 H2?
- Будут ли industry-стандарты для MCP trust и signing в Q3–Q4?
- Какие метрики post-market monitoring примет регулятор для agentic systems?

---

## Приложение: источники

- [RAILS: Verification-Native Clearing For Agentic Commerce](https://arxiv.org/abs/2606.08790v1) — papers — arXiv — 2026-06-07- [VATS: Exploiting Implicit Authority in Error-Path Injection via Systematic Mutation](https://arxiv.org/abs/2606.07992v1) — papers — arXiv — 2026-06-06- [From Privacy to Workflow Integrity: Communication-Graph Metadata in Autonomous Agent Interoperability](https://arxiv.org/abs/2606.07150v1) — papers — arXiv — 2026-06-05- [MCP STDIO RCE: Supply Chain Risk (CSA)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_mcp-stdio-rce-agentic-infrastructure_20260510-csa-styled.pdf) — gov_cert — Cloud Security Alliance — 2026-05-10- [AI Act: Digital Omnibus agreement (European Parliament)](https://www.europarl.europa.eu/pdfs/news/expert/2026/5/press_release/20260427IPR42011/20260427IPR42011_en.pdf) — gov_cert — European Parliament — 2026-05-07- [MCP Security Crisis: Systemic Design (CSA)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_MCP_security_crisis_20260504-csa-styled.pdf) — standards — Cloud Security Alliance — 2026-05-04- [Article 15: Accuracy, Robustness and Cybersecurity (EU AI Act)](https://artificialintelligenceact.eu/article/15/) — standards — EU AI Act — 2026-04-01- [CVE-2026-30615: Windsurf Zero-Click MCP Prompt Injection RCE](https://policylayer.com/mcp-incidents/windsurf-zero-click-mcp-rce-cve-2026-30615) — incidents — PolicyLayer / OX Security — 2026-04-15- [CP Plus 8 Ch. Network Video Recorder](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-05) — gov_cert — CISA Cybersecurity Advisories — 2026-05-28- [XCharge C6](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-08) — gov_cert — CISA Cybersecurity Advisories — 2026-05-28- [Jinan USR IOT Technology Limited (PUSR) USR-W610 RS232/485 to Wi-Fi/Ethernet Converter](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-02) — gov_cert — CISA Cybersecurity Advisories — 2026-05-28- [MacGregor Voyage Data Recorder (VDR) G4e](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-01) — gov_cert — CISA Cybersecurity Advisories — 2026-05-28- [Proof of Source of Funds: Efficient On-chain Provenance of Cryptoassets](https://arxiv.org/abs/2606.10172) — papers — arXiv cs.CR (snapshot) — 2026-06-10- [Layer Order Semantics for Automata-Based Cybersecurity](https://arxiv.org/abs/2606.10649) — papers — arXiv cs.CR (snapshot) — 2026-06-10- [Anchors that Don't Lift: Understanding Supply Chain Driven Kernel Lock-In and Governance-Mediated Mitigation Strategies in SOHO Devices](https://arxiv.org/abs/2606.11175) — papers — arXiv cs.CR (snapshot) — 2026-06-10- [MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills](https://arxiv.org/abs/2606.07131) — papers — arXiv cs.CR (snapshot) — 2026-06-10- [Who Gets Flagged? The Pluralistic Evaluation Gap in AI Content Watermarking](https://arxiv.org/abs/2604.13776) — papers — arXiv cs.CR (snapshot) — 2026-06-10- [Game-Theoretic Multi-Agent Control for Robust Contextual Reasoning in LLMs](https://arxiv.org/abs/2606.10322v1) — papers — arXiv — 2026-06-09- [Trustworthy Smart Fabs via Professional Proxies: Scaling Safe and Sustainable by Design (SSbD) through Industrial Data Spaces](https://arxiv.org/abs/2606.09227v1) — papers — arXiv — 2026-06-08- [Governance Controls for AI-Generated Test Artifacts in Autonomous Software Testing](https://arxiv.org/abs/2606.08806v1) — papers — arXiv — 2026-06-07- [Semantic Quorum Assurance: Collective Certification for Non-Deterministic AI Infrastructure](https://arxiv.org/abs/2606.08021v1) — papers — arXiv — 2026-06-06- [Will the Agent Recuse Itself? Measuring LLM-Agent Compliance with In-Band Access-Deny Signals](https://arxiv.org/abs/2606.06460v1) — papers — arXiv — 2026-06-04- [The Meta-Agent Challenge: Are Current Agents Capable of Autonomous Agent Development?](https://arxiv.org/abs/2606.04455v1) — papers — arXiv — 2026-06-03- [The Impact of Configuring Agentic AI Coding Tools on Build-vs-Buy Decisions: A Study Protocol](https://arxiv.org/abs/2606.03907v1) — papers — arXiv — 2026-06-02- [Overlaying Governance: A Compositional Authorization Framework for Delegation and Scope in Agentic AI](https://arxiv.org/abs/2606.03518v1) — papers — arXiv — 2026-06-02- [SeClaw: Spec-Driven Security Task Synthesis for Evaluating Autonomous Agents](https://arxiv.org/abs/2606.02302v1) — papers — arXiv — 2026-06-01- [Relevance as a Vulnerability: How Web Retrieval Degrades Safety Alignment in LLM Agents](https://arxiv.org/abs/2605.29224v1) — papers — arXiv — 2026-05-28- [State of MCP Security Audit — June 2026](https://policylayer.com/research/state-of-mcp) — papers — PolicyLayer — 2026-06-01- [Zombie Agents: Persistent Control of Self-Evolving LLM Agents](https://arxiv.org/pdf/2602.15654) — papers — arXiv — 2026-02-15- [Reconstructing AI activity in investigations](https://www.microsoft.com/en-us/security/blog/2026/06/09/reconstructing-ai-activity-investigations/) — vendor — Microsoft Security Blog — 2026-06-09- [A blueprint for democratic governance of frontier AI](https://openai.com/index/frontier-safety-blueprint) — vendor — OpenAI News — 2026-06-03- [OpenAI’s Frontier Governance Framework](https://openai.com/index/openai-frontier-governance-framework) — vendor — OpenAI News — 2026-05-28- [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex) — vendor — OpenAI News — 2026-05-27- [How enterprises are scaling AI](https://openai.com/business/guides-and-resources/how-enterprises-are-scaling-ai) — vendor — OpenAI News — 2026-05-11- [Schneider Electric Modicon Network Managed Switches](https://www.cisa.gov/news-events/ics-advisories/icsa-26-160-01) — gov_cert — CISA Cybersecurity Advisories — 2026-06-09- [CISA Adds Two Known Exploited Vulnerabilities to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/08/cisa-adds-two-known-exploited-vulnerabilities-catalog) — gov_cert — CISA Cybersecurity Advisories — 2026-06-08- [CISA Adds One Known Exploited Vulnerability to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/05/cisa-adds-one-known-exploited-vulnerability-catalog) — gov_cert — CISA Cybersecurity Advisories — 2026-06-05- [Hitachi Energy ITT600 Explorer](https://www.cisa.gov/news-events/ics-advisories/icsa-26-155-02) — gov_cert — CISA Cybersecurity Advisories — 2026-06-04- [CISA Adds One Known Exploited Vulnerability to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/03/cisa-adds-one-known-exploited-vulnerability-catalog) — gov_cert — CISA Cybersecurity Advisories — 2026-06-03- [CISA and Partners Urge Hardening Automatic Tank Gauge Systems](https://www.cisa.gov/resources-tools/resources/cisa-and-partners-urge-hardening-automatic-tank-gauge-systems) — gov_cert — CISA Cybersecurity Advisories — 2026-06-02