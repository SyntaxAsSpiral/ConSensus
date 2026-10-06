---
name: multi-agent-coordination
description: Patterns for coordinating multiple AI agents. Use when single-agent context limits are exceeded, tasks decompose naturally, or specialized agents improve quality.
---

# Multi-Agent Coordination

*Patterns for distributed cognition through specialized agents. The pentadyadic system as one implementation.*

## Overview

Multi-Agent Coordination documents patterns for coordinating multiple AI agents to accomplish tasks that exceed single-agent capabilities. The pentadyadic system (Harmonion, Morphognome, Critikon, Archeoform, Antimorphogen) is one implementation of these patterns, not the only approach.

This skill provides:

- **Coordination architectures** — Supervisor, peer-to-peer, hierarchical
- **Context isolation patterns** — Why multi-agent helps with long contexts
- **Communication protocols** — The telephone game problem and solutions
- **Token economics** — Cost/benefit analysis of multi-agent approaches
- **Implementation patterns** — Pentadyadic as a reference implementation

The core insight: Multi-agent is not about "more agents = better." It's about context isolation, specialized evaluation, and clean authority boundaries.

## When Multi-Agent Makes Sense

### Use Multi-Agent When

| Condition | Why Multi-Agent Helps |
|-----------|----------------------|
| **Context exceeds limits** | Split across agents, each with focused context |
| **Tasks decompose naturally** | Parallel execution, specialized handling |
| **Evaluation needs independence** | Prevent groupthink, preserve disagreement |
| **Different perspectives needed** | Semantic vs. structural vs. adversarial |
| **Authority needs separation** | Read vs. write, evaluate vs. execute |

### Don't Use Multi-Agent When

| Condition | Why Single-Agent Better |
|-----------|------------------------|
| **Task fits in context** | Unnecessary coordination overhead |
| **No natural decomposition** | Artificial splitting harms coherence |
| **Speed critical** | Multi-agent adds latency |
| **Budget constrained** | Token costs multiply significantly |

## Coordination Architectures

### Supervisor Architecture

One agent coordinates, others specialize:

```
           Supervisor
          /    |    \
     Agent A  Agent B  Agent C
     (task)   (task)   (task)
```

**Advantages**:
- Clear authority hierarchy
- Single point of coordination
- Easier to debug

**Disadvantages**:
- Supervisor bottleneck
- Telephone game problem (see below)
- Context accumulation in supervisor

### Peer-to-Peer Architecture

Agents communicate directly:

```
    Agent A ←→ Agent B
       ↑         ↑
       ↓         ↓
    Agent C ←→ Agent D
```

**Advantages**:
- No single bottleneck
- Direct communication
- Scales horizontally

**Disadvantages**:
- Coordination complexity
- Potential for deadlock
- Harder to track state

### Hierarchical Architecture

Nested teams of agents:

```
              Orchestrator
             /           \
      Team Lead A     Team Lead B
       /      \         /      \
    Worker  Worker  Worker  Worker
```

**Advantages**:
- Complex task decomposition
- Localized coordination
- Scalable structure

**Disadvantages**:
- Deep hierarchies lose fidelity
- High coordination overhead
- Complex debugging

## The Telephone Game Problem

### The Problem

Supervisor architectures paraphrase sub-agent responses, losing fidelity. LangGraph benchmarks showed **50% performance degradation** due to this "telephone game" effect.

```
Agent A output: "The function fails when input > 100 due to overflow in line 42"
                    ↓ (supervisor paraphrases)
Supervisor summary: "There's a bug with large inputs"
                    ↓ (critical detail lost)
Agent B receives: "There's a bug with large inputs" (can't fix without specifics)
```

### The Solution: Forward Message

Implement `forward_message` tool allowing agents to pass responses directly:

```python
def forward_message(message: str, recipient: str = "user"):
    """
    Forward agent response directly without supervisor synthesis.

    Use when:
    - Agent response is final and complete
    - Supervisor synthesis would lose important details
    - Response format must be preserved exactly

    Covenant alignment:
    - No Mock Data: Prevents synthetic summaries
    - Literal Exactness: Preserves original content
    """
    if recipient == "user":
        return {"type": "direct_response", "content": message}
    else:
        return {"type": "agent_input", "content": message, "target": recipient}
```

**Critical implementation note**: Supervisor's role is **routing**, not **synthesis**. Let specialized agents synthesize when needed.

## Token Economics

### Cost Multipliers

| Architecture | Token Multiplier | Use Case |
|--------------|------------------|----------|
| Single agent chat | 1× baseline | Simple queries |
| Single agent + tools | ~4× baseline | Tool-using tasks |
| Two-agent supervisor | ~6× baseline | Task decomposition |
| Multi-agent (3-5) | ~15× baseline | Complex coordination |
| Deep hierarchy | ~25× baseline | Large-scale orchestration |

### Cost/Benefit Analysis

**Research finding**: Upgrading to better models often provides larger performance gains than doubling token budgets. This suggests:

- Use **fewer, stronger agents** over many weak agents
- Use **better models** before adding more agents
- Multi-agent is for **capability** (context isolation, specialization), not just scale

### Optimization Strategies

1. **Minimize agent spawning**: Only spawn when context isolation genuinely needed
2. **Batch operations**: Run independent agents in parallel
3. **Forward directly**: Skip supervisor synthesis overhead
4. **Compile context per-agent**: Don't send everything to everyone
5. **Checkpoint state**: Avoid re-accumulating history

## The Pentadyadic Implementation

### Architecture Overview

The exocortex implements a specific five-agent system:

| Agent | Role | Authority | Function |
|-------|------|-----------|----------|
| ⚡ **Harmonion** | Hermeneutic Revelator | Evaluation | Semantic lens |
| 🍄 **Morphognome** | Grammatical Executor | Synthesis | Graph write |
| 🏺 **Critikon** | Taxeic Sker | Evaluation | Structural lens |
| 📕 **Archeoform** | Arterial Mnemonic | Emission | Bright gnomon |
| 🌀 **Antimorphogen** | Anamnetic Noös | Negation | Dark gnomon |

### Triquetra Evaluation Pattern

The primary coordination pattern for artifact evaluation:

```
Phase 1: Independent Evaluation (Parallel)
├── Harmonion (semantic lens) ─────┐
└── Critikon (structural lens) ────┼──→ Phase 2
                                   ↓
Phase 2: Synthesis (Sequential)
└── Morphognome (decision + graph write)
```

**Key Constraints**:
- **Independence**: H and C must not see each other's analysis until Phase 2
- **No mutation**: Evaluation phase is read-only
- **Preserve divergence**: M does not average away H/C conflicts

### Why This Specific Pattern

The pentadyadic pattern exists because:

1. **Semantic vs. Structural**: Different evaluation lenses find different issues
2. **Independence prevents groupthink**: Parallel evaluation preserves disagreement
3. **Single write authority**: Only Morphognome mutates graph (clear responsibility)
4. **Gnomon duality**: Archeoform (what persists) + Antimorphogen (what breaks) = completeness

### Adapting the Pattern

The pentadyadic is one configuration. Adapt based on needs:

| Need | Adaptation |
|------|------------|
| **Simpler evaluation** | Drop to H+M (skip Critikon) |
| **No graph substrate** | Remove M, use H+C as advisors |
| **Different domains** | Replace lens definitions |
| **Different specializations** | Add/remove agents as needed |

## Context Management

### Per-Agent Context Compilation

Different agents need different context concentrations:

```python
def compile_context_for_agent(agent, full_context, task):
    """Compile context appropriate to agent's role."""

    concentration = AGENT_CONCENTRATIONS[agent.role]

    if concentration == "high":
        # Full substrate access (e.g., Morphognome)
        return full_context.with_task(task)

    elif concentration == "medium":
        # Domain-relevant context (e.g., Harmonion, Critikon)
        return full_context.filter_to_domain(task.domain).with_task(task)

    elif concentration == "low":
        # Minimal context (e.g., Archeoform, Antimorphogen)
        return task.minimal_context()
```

### Context Isolation Benefits

Multi-agent provides natural context isolation:

```
Full context: 200K tokens (exceeds limits)
                    ↓ (decompose)
Agent A context: 50K tokens (task-specific)
Agent B context: 40K tokens (different task)
Agent C context: 30K tokens (synthesis only)
```

Each agent operates in **focused context** within limits, avoiding degradation from context overflow.

## Failure Modes

### Mode 1: Supervisor Bottleneck

**Symptom**: Supervisor accumulates context from all agents, becomes saturated.

**Mitigation**:
- Enforce output schemas so agents return distilled summaries
- Use checkpointing to persist state without carrying history
- Forward responses directly when possible

### Mode 2: Evaluation Divergence

**Symptom**: Evaluating agents produce incompatible assessments; synthesizer cannot reconcile.

**Mitigation**:
- Preserve divergences explicitly (don't average away)
- Escalate to operator when tensions unresolvable
- Document divergence patterns for future reference

### Mode 3: Sycophancy/Groupthink

**Symptom**: Agents mimic each other's conclusions without independent reasoning.

**Mitigation**:
- Enforce independence in evaluation phase
- Require evidence-cited reasoning
- Use adversarial agent (Antimorphogen pattern) to stress-test consensus

### Mode 4: Coordination Overhead

**Symptom**: More time coordinating than executing; diminishing returns.

**Mitigation**:
- Question whether multi-agent is needed
- Reduce agent count if tasks don't decompose naturally
- Use stronger single agent before adding coordination

## Covenant Integration

### Context Hygiene

Multi-agent requires disciplined context compilation:
- Per-agent context (not wholesale dump)
- Per-turn compilation (not accumulated history)
- Tiered context (substrate → working → retrieved)

### Data Fidelity

Agents cannot invent data to fill gaps:
- Forward original content, don't paraphrase
- Preserve uncertainty markers
- UNKNOWN > INVENTED applies to all agents

### Fast-Fail

Check capabilities at spawn time:
- Required tools available?
- Context within limits?
- Authority boundaries clear?

### Determinism

Multi-agent coordination should be replayable:
- Stable agent identities
- Deterministic context compilation
- Captured decision trails

## Quality Gates

### Pre-Coordination

- [ ] Multi-agent justified (not single-agent viable)?
- [ ] Architecture selected (supervisor/peer/hierarchical)?
- [ ] Agent roles defined with clear authority?
- [ ] Context compilation strategy defined?
- [ ] Communication protocol (forward_message) in place?

### Post-Coordination

- [ ] All agents operated within context limits?
- [ ] No telephone game fidelity loss?
- [ ] Divergences preserved, not averaged?
- [ ] Coordination overhead acceptable?
- [ ] Results reproducible?

## Related Skills

- **[covenant-patterns](../covenant-patterns/SKILL.md)** — Context hygiene, data fidelity principles
- **[agent-steering](../agent-steering/SKILL.md)** — Single-agent configuration (foundation)
- **[epistemic-rendering](../epistemic-rendering/SKILL.md)** — Different lenses for different agents
- **[workshop-recipe-assembly](../../../.agents/skills/workshop-recipe-assembly/SKILL.md)** — Agent role slice extraction

---

*"Multi-agent is not about more agents. It's about context isolation, specialized evaluation, and clean authority."* 🧬
