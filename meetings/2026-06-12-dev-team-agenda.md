# Dev Team Meeting Agenda — June 12, 2026
**Duration:** 60 min | **Attendees:** Mujtaba, Manish, Rakshit, Nishant, Tilak, Krish

---

## 1. Build Cycle Reset (5 min — Mujtaba leads)
- We are in pre-lab certification sprint, ends June 28. Every decision in this meeting is oriented toward that gate.
- GCP is unlocked. Monthly cost estimate due from Nishant by EOD.

## 2. Architecture State + Gaps (20 min — Manish leads)
- Walk Zone A component status: Classifier, Rescheduler, AE, Eval Framework, DVFS, Cooling optimization
- Walk Zone B status: Historian Connector (already built), OPC-UA (built), MQTT/BACnet/Modbus (confirm status)
- **Krish's DVFS + Cooling work** — confirmed in scope for Zone A. Assign owner + date today.
- Low-fidelity DT: status from Rakshit. Due July 2 for AE validator loop — on track?
- Architecture gaps to name explicitly before leaving this block

## 3. Assign Pre-Lab Sprint Deliverables (20 min — decision moment)

| Component | Proposed Owner | Date |
|---|---|---|
| Classifier (flex-tier, priority scoring) | Rakshit | June 20 |
| Rescheduler (dispatch + trigger gates) | Manish | June 25 |
| Accountability Engine (11 rules, 4 clusters) | Manish | June 25 |
| DVFS optimization | Krish | TBD — assign today |
| Cooling optimization | Krish | TBD — assign today |
| Historian Connector | Nishant | DONE — confirm deploy-ready |
| OPC-UA | Nishant | DONE — confirm |
| MQTT plugin | Nishant | TBD — assess vs. workload |
| BACnet plugin | Nishant | TBD — assess vs. workload |
| Modbus plugin | Nishant | TBD — assess vs. workload |
| Interfaces (Decision Engine + Operator UI + Tenant surface) | Manish | July 4 |
| Eval Framework gates (all 6) | Tilak | June 23 |
| Zone A↔B integration test | Tilak | June 28 |

## 4. Lab Scope: In vs. Out (10 min)
- **Humber lab:** minimal PLC document. Build with Humber team. Don't over-engineer pre-visit.
- **In scope for pre-lab cert:** Classifier, Rescheduler, AE, Historian plugins, Interfaces, Eval Framework, DVFS, Cooling
- **Out of scope (post sprint):** hi-fi DT (UCalgary/Mostafa), full 50MW simulation (due July 25)
- **Sarnia / Ottawa (Spur):** confirm what needs to be working before we send Nishant on-site

## 5. Ops (5 min)
- Eval Framework assignment confirmed today (Tilak owns)
- GitHub: branch strategy and commit hygiene — Nishant to define by June 14
- GCP monthly budget: Nishant to pull estimate today and send to Mujtaba by EOD

## 6. Governance (5 min)
- 1:1 cadence: Mujtaba ↔ Manish weekly; Manish ↔ each dev weekly
- Quarterly review: first one end of Q2 (June 30)
- Jira: Mujtaba + Manish set up this weekend. All tasks migrated from sprint YAML into Jira by June 14.
