# Тренды AI Security (2026-Q2) — Executive Brief

**Период:** 2026-04-01 — 2026-06-30  
**Сравнение:** vs 2026-Q1  
**Дата подготовки:** 2026-06-15  
**Источников собрано:** 367

---

## Краткое резюме для руководства

- **Саморазвивающиеся агенты (self-evolving agents)** — Поведение агента меняется без релиза: новая поверхность для APT и insider-style атак. Классический change control и периметр не видят «тихую» эволюцию policy в memory. Затронуты: Владельцы agentic платформ, SOC, команды с long-term memory (coding/research agents). Уверенность: **High**.
- **Регуляторика ИИ (AI Act и смежные требования)** — Даже при отсрочке штрафных рамок организации должны проектировать agent/RAG-архитектуру под lifecycle security и post-market monitoring — иначе дорогой rework в 2027. Затронуты: Compliance, legal, product owners в EU; глобальные вендоры с EU-клиентами. Уверенность: **High**.
- **Инструменты AI-агентов (MCP, skills, tool-use)** — Агент = суперпользователь с LLM-интерфейсом. Компрометация одного MCP/skill даёт persistent access через mcp.json и cross-server tool shadowing. Затронуты: Dev platform teams, SecOps, все пользователи AI coding assistants. Уверенность: **High**.
- **Prompt injection и обход политик моделей** — Не нужен доступ к модели — достаточно untrusted content в browser/RAG/email pipeline. Затронуты: Enterprise с browser tools, email agents, публичные coding assistants. Уверенность: **High**.
- **Атаки на RAG и слой данных** — Model-level guardrails не спасают, если poisoned chunk попадает в retrieval. Затронуты: RAG owners, data governance, teams с external crawlers. Уверенность: **Medium**.
- **Supply chain моделей, артефактов и skills** — Третья сторона в agent stack так же критична, как зависимости в CI/CD. Затронуты: AppSec, platform engineering, procurement third-party AI tools. Уверенность: **High**.
- **Runtime-контроль агентов (gateways, sandbox, policy)** — Единственный масштабируемый контроль при hundreds of MCP tools per agent. Затронуты: Security architects внедряющих agentic AI. Уверенность: **Medium**.

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
- [From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails](https://arxiv.org/abs/2606.14517) — papers, 2026-06-15
- [From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails](https://arxiv.org/abs/2606.14517v1) — papers, 2026-06-12
- [The Meta-Agent Challenge: Are Current Agents Capable of Autonomous Agent Development?](https://arxiv.org/abs/2606.04455v1) — papers, 2026-06-03

### 2. Регуляторика ИИ (AI Act и смежные требования)

В Q2 2026 EU согласовала Digital Omnibus: сроки high-risk obligations сдвинуты (Annex III → 2 Dec 2027, product-embedded → 2 Aug 2028), но Article 15 (accuracy, robustness, cybersecurity) остаётся ядром — data/model poisoning, adversarial examples. Связка с Cyber Resilience Act уточняется на уровне Council.

**Изменение к прошлому кварталу:** Vs Q1 2026: политический deal 7 May 2026 заменил «дедлайн паники» на фазовое планирование; фокус CISO — mapping technical controls на Art. 15.

**Почему важно:** Даже при отсрочке штрафных рамок организации должны проектировать agent/RAG-архитектуру под lifecycle security и post-market monitoring — иначе дорогой rework в 2027.

**Кому актуально:** Compliance, legal, product owners в EU; глобальные вендоры с EU-клиентами.

**Уверенность:** High

**Ключевые источники:**

- [AI Act: Digital Omnibus agreement (European Parliament)](https://www.europarl.europa.eu/pdfs/news/expert/2026/5/press_release/20260427IPR42011/20260427IPR42011_en.pdf) — gov_cert, 2026-05-07
- [Article 15: Accuracy, Robustness and Cybersecurity (EU AI Act)](https://artificialintelligenceact.eu/article/15/) — standards, 2026-04-01
- [Brickcom Cameras](https://www.cisa.gov/news-events/ics-advisories/icsa-26-162-03) — gov_cert, 2026-06-11
- [Jinan USR IOT Technology Limited (PUSR) USR-W610 RS232/485 to Wi-Fi/Ethernet Converter](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-02) — gov_cert, 2026-05-28
- [MacGregor Voyage Data Recorder (VDR) G4e](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-01) — gov_cert, 2026-05-28
- [XCharge C6](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-08) — gov_cert, 2026-05-28

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
- [CVE-2026-30615: Windsurf Zero-Click MCP Prompt Injection RCE](https://policylayer.com/mcp-incidents/windsurf-zero-click-mcp-rce-cve-2026-30615) — incidents, 2026-04-15

### 4. Prompt injection и обход политик моделей

Indirect injection эволюционировал в agent-specific цепочки: веб-страница → IDE context → изменение mcp.json → RCE (OX/Windsurf). Tool descriptions как скрытый канал инструкций (tool poisoning) подтверждён CSA и Invariant Labs cross-server сценариями.

**Изменение к прошлому кварталу:** Zero-click IDE RCE и CVE-цепочки — качественный скачок vs Q1 advisory-only.

**Почему важно:** Не нужен доступ к модели — достаточно untrusted content в browser/RAG/email pipeline.

**Кому актуально:** Enterprise с browser tools, email agents, публичные coding assistants.

**Уверенность:** High

**Ключевые источники:**

- [MCP Security Crisis: Systemic Design (CSA)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_MCP_security_crisis_20260504-csa-styled.pdf) — standards, 2026-05-04
- [CVE-2026-30615: Windsurf Zero-Click MCP Prompt Injection RCE](https://policylayer.com/mcp-incidents/windsurf-zero-click-mcp-rce-cve-2026-30615) — incidents, 2026-04-15
- [From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails](https://arxiv.org/abs/2606.14517) — papers, 2026-06-15
- [From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails](https://arxiv.org/abs/2606.14517v1) — papers, 2026-06-12
- [Patcher: Post-Hoc Patching of Backdoored Large Language Models](https://arxiv.org/abs/2606.02995) — papers, 2026-06-15
- [Who Pays the Price? Stakeholder-Centric Prompt Injection Benchmarking for Real-world Web Agents](https://arxiv.org/abs/2606.13385v1) — papers, 2026-06-11

### 5. Атаки на RAG и слой данных

RAG и слой данных остаются отдельной attack surface: document injection и memory summarization превращают «факты» в инструкции. Unit 42 и AWS Bedrock case studies показывают приоритет memory над user prompt.

**Изменение к прошлому кварталу:** Больше PoC на long-term memory, не только single-turn RAG.

**Почему важно:** Model-level guardrails не спасают, если poisoned chunk попадает в retrieval.

**Кому актуально:** RAG owners, data governance, teams с external crawlers.

**Уверенность:** Medium

**Ключевые источники:**

- [MCP Security Crisis: Systemic Design (CSA)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_MCP_security_crisis_20260504-csa-styled.pdf) — standards, 2026-05-04
- [Article 15: Accuracy, Robustness and Cybersecurity (EU AI Act)](https://artificialintelligenceact.eu/article/15/) — standards, 2026-04-01
- [Zombie Agents: Persistent Control of Self-Evolving LLM Agents](https://arxiv.org/pdf/2602.15654) — papers, 2026-02-15
- [NeST: Neuron Selective Tuning for LLM Safety](https://arxiv.org/abs/2602.16835) — papers, 2026-06-15
- [Game-Theoretic Multi-Agent Control for Robust Contextual Reasoning in LLMs](https://arxiv.org/abs/2606.10322) — papers, 2026-06-15
- [The Insurability Frontier of AI Risk: Mapping Threats to Affirmative Coverage, Silent Exposures, and Exclusions](https://arxiv.org/abs/2605.18784) — papers, 2026-06-15

### 6. Supply chain моделей, артефактов и skills

Supply chain skills/MCP/артефактов: 30+ CVE за 60 дней 2026, тысячи exposed servers (Shodan), 24k secrets в публичных mcp-конфигах (GitGuardian). North Korean npm hijack внедрял rogue MCP server.

**Изменение к прошлому кварталу:** Первый квартал с массовой CVE-нумерацией именно для MCP ecosystem.

**Почему важно:** Третья сторона в agent stack так же критична, как зависимости в CI/CD.

**Кому актуально:** AppSec, platform engineering, procurement third-party AI tools.

**Уверенность:** High

**Ключевые источники:**

- [MCP STDIO RCE: Supply Chain Risk (CSA)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_mcp-stdio-rce-agentic-infrastructure_20260510-csa-styled.pdf) — gov_cert, 2026-05-10
- [Beyond Attack Success Rate: Examining Trigger Leakage in Vision-Language Agentic Systems](https://arxiv.org/abs/2606.12586v1) — papers, 2026-06-10
- [Supply Chain Compromises Impact Nx Console and GitHub Repositories](https://www.cisa.gov/news-events/alerts/2026/05/28/supply-chain-compromises-impact-nx-console-and-github-repositories) — gov_cert, 2026-05-28
- [Software Dark Matter: Gazing at Uncharted Files to Navigate SBOM Integrations](https://arxiv.org/abs/2606.13966) — papers, 2026-06-15
- [Defending the Core: A Centrality-Based Protection Strategy for Supply Chain Security in npm Dependency Network](https://arxiv.org/abs/2606.14036) — papers, 2026-06-15
- [Patcher: Post-Hoc Patching of Backdoored Large Language Models](https://arxiv.org/abs/2606.02995) — papers, 2026-06-15

### 7. Runtime-контроль агентов (gateways, sandbox, policy)

Ответ индустрии: enforcement на transport layer — agent gateways, default-deny tool policy, JSON-RPC filtering, allowlist STDIO binaries. Сдвиг от «надеемся на LLM safety» к out-of-process runtime control.

**Изменение к прошлому кварталу:** Vs Q1: зрелые product/category «agent gateway» и CSA red teaming guides.

**Почему важно:** Единственный масштабируемый контроль при hundreds of MCP tools per agent.

**Кому актуально:** Security architects внедряющих agentic AI.

**Уверенность:** Medium

**Ключевые источники:**

- [The Meta-Agent Challenge: Are Current Agents Capable of Autonomous Agent Development?](https://arxiv.org/abs/2606.04455v1) — papers, 2026-06-03
- [Beyond Runtime Enforcement: Shield Synthesis as Defensibility Analysis for Adversarial Networks](https://arxiv.org/abs/2606.13621v1) — papers, 2026-06-11
- [Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox) — vendor, 2026-05-13
- [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely) — vendor, 2026-05-08
- [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk) — vendor, 2026-04-15


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

- [RAILS: Verification-Native Clearing For Agentic Commerce](https://arxiv.org/abs/2606.08790v1) — papers — arXiv — 2026-06-07- [VATS: Exploiting Implicit Authority in Error-Path Injection via Systematic Mutation](https://arxiv.org/abs/2606.07992v1) — papers — arXiv — 2026-06-06- [From Privacy to Workflow Integrity: Communication-Graph Metadata in Autonomous Agent Interoperability](https://arxiv.org/abs/2606.07150v1) — papers — arXiv — 2026-06-05- [MCP STDIO RCE: Supply Chain Risk (CSA)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_mcp-stdio-rce-agentic-infrastructure_20260510-csa-styled.pdf) — gov_cert — Cloud Security Alliance — 2026-05-10- [AI Act: Digital Omnibus agreement (European Parliament)](https://www.europarl.europa.eu/pdfs/news/expert/2026/5/press_release/20260427IPR42011/20260427IPR42011_en.pdf) — gov_cert — European Parliament — 2026-05-07- [MCP Security Crisis: Systemic Design (CSA)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_MCP_security_crisis_20260504-csa-styled.pdf) — standards — Cloud Security Alliance — 2026-05-04- [Article 15: Accuracy, Robustness and Cybersecurity (EU AI Act)](https://artificialintelligenceact.eu/article/15/) — standards — EU AI Act — 2026-04-01- [CVE-2026-30615: Windsurf Zero-Click MCP Prompt Injection RCE](https://policylayer.com/mcp-incidents/windsurf-zero-click-mcp-rce-cve-2026-30615) — incidents — PolicyLayer / OX Security — 2026-04-15- [Brickcom Cameras](https://www.cisa.gov/news-events/ics-advisories/icsa-26-162-03) — gov_cert — CISA Cybersecurity Advisories — 2026-06-11- [Jinan USR IOT Technology Limited (PUSR) USR-W610 RS232/485 to Wi-Fi/Ethernet Converter](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-02) — gov_cert — CISA Cybersecurity Advisories — 2026-05-28- [MacGregor Voyage Data Recorder (VDR) G4e](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-01) — gov_cert — CISA Cybersecurity Advisories — 2026-05-28- [XCharge C6](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-08) — gov_cert — CISA Cybersecurity Advisories — 2026-05-28- [CP Plus 8 Ch. Network Video Recorder](https://www.cisa.gov/news-events/ics-advisories/icsa-26-148-05) — gov_cert — CISA Cybersecurity Advisories — 2026-05-28- [SkillMutator: Benchmarking and Defending Language-and-Code Cross-modal Attacks on LLM Agent Skills](https://arxiv.org/abs/2606.14154) — papers — arXiv cs.CR (snapshot) — 2026-06-15- [REPOSE: Quantifying the Price of Security in Weakly-Hard Real-Time Cyber-Physical Systems](https://arxiv.org/abs/2606.14395) — papers — arXiv cs.CR (snapshot) — 2026-06-15- [From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails](https://arxiv.org/abs/2606.14517) — papers — arXiv cs.CR (snapshot) — 2026-06-15- [From Shield to Target: Denial-of-Service Attacks on LLM-Based Agent Guardrails](https://arxiv.org/abs/2606.14517v1) — papers — arXiv — 2026-06-12- [SkillMutator: Benchmarking and Defending Language-and-Code Cross-modal Attacks on LLM Agent Skills](https://arxiv.org/abs/2606.14154v1) — papers — arXiv — 2026-06-12- [Beyond Attack Success Rate: Examining Trigger Leakage in Vision-Language Agentic Systems](https://arxiv.org/abs/2606.12586v1) — papers — arXiv — 2026-06-10- [A Five-Plane Reference Architecture for Runtime Governance of Production AI Agents](https://arxiv.org/abs/2606.12320v1) — papers — arXiv — 2026-06-10- [Towards Responsibly Non-Compliant Machines](https://arxiv.org/abs/2606.12147v1) — papers — arXiv — 2026-06-10- [Runtime Skill Audit: Targeted Runtime Probing for Agent Skill Security](https://arxiv.org/abs/2606.11671v1) — papers — arXiv — 2026-06-10- [Sovereign Assurance Boundary: Certificate-Bound Admission for Agentic Infrastructure](https://arxiv.org/abs/2606.11632v1) — papers — arXiv — 2026-06-10- [Trustworthy Smart Fabs via Professional Proxies: Scaling Safe and Sustainable by Design (SSbD) through Industrial Data Spaces](https://arxiv.org/abs/2606.09227v1) — papers — arXiv — 2026-06-08- [Governance Controls for AI-Generated Test Artifacts in Autonomous Software Testing](https://arxiv.org/abs/2606.08806v1) — papers — arXiv — 2026-06-07- [Semantic Quorum Assurance: Collective Certification for Non-Deterministic AI Infrastructure](https://arxiv.org/abs/2606.08021v1) — papers — arXiv — 2026-06-06- [Will the Agent Recuse Itself? Measuring LLM-Agent Compliance with In-Band Access-Deny Signals](https://arxiv.org/abs/2606.06460v1) — papers — arXiv — 2026-06-04- [The Meta-Agent Challenge: Are Current Agents Capable of Autonomous Agent Development?](https://arxiv.org/abs/2606.04455v1) — papers — arXiv — 2026-06-03- [State of MCP Security Audit — June 2026](https://policylayer.com/research/state-of-mcp) — papers — PolicyLayer — 2026-06-01- [Zombie Agents: Persistent Control of Self-Evolving LLM Agents](https://arxiv.org/pdf/2602.15654) — papers — arXiv — 2026-02-15- [Reconstructing AI activity in investigations](https://www.microsoft.com/en-us/security/blog/2026/06/09/reconstructing-ai-activity-investigations/) — vendor — Microsoft Security Blog — 2026-06-09- [Access OpenAI models and Codex through your Oracle cloud commitment](https://openai.com/index/openai-on-oracle-cloud) — vendor — OpenAI News — 2026-06-10- [A blueprint for democratic governance of frontier AI](https://openai.com/index/frontier-safety-blueprint) — vendor — OpenAI News — 2026-06-03- [OpenAI’s Frontier Governance Framework](https://openai.com/index/openai-frontier-governance-framework) — vendor — OpenAI News — 2026-05-28- [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex) — vendor — OpenAI News — 2026-05-27- [How enterprises are scaling AI](https://openai.com/business/guides-and-resources/how-enterprises-are-scaling-ai) — vendor — OpenAI News — 2026-05-11- [CISA Adds One Known Exploited Vulnerability to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/12/cisa-adds-one-known-exploited-vulnerability-catalog) — gov_cert — CISA Cybersecurity Advisories — 2026-06-12- [CISA Adds One Known Exploited Vulnerability to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/11/cisa-adds-one-known-exploited-vulnerability-catalog) — gov_cert — CISA Cybersecurity Advisories — 2026-06-11- [Schneider Electric Modicon Network Managed Switches](https://www.cisa.gov/news-events/ics-advisories/icsa-26-160-01) — gov_cert — CISA Cybersecurity Advisories — 2026-06-09- [CISA Adds Two Known Exploited Vulnerabilities to Catalog](https://www.cisa.gov/news-events/alerts/2026/06/08/cisa-adds-two-known-exploited-vulnerabilities-catalog) — gov_cert — CISA Cybersecurity Advisories — 2026-06-08