# Coordination Frameworks for Multi-Agent LLM Systems: A Comparison

*Note: This document was restored and converted from an earlier binary format. It outlines the landscape of multi-agent frameworks to inform our 3-model architecture.*

## 1. Introduction
As AI systems evolve from single-prompt chatbots to autonomous agents, "coordination frameworks" have emerged to manage the complexity. This document compares the leading options and contrasts them with our bespoke "Terminal-based 3-Model" approach.

## 2. Leading Frameworks

### A. LangChain / LangGraph
*   **Philosophy**: Chained execution, DAGs (Directed Acyclic Graphs).
*   **Strengths**: Huge ecosystem, vast integration library, state management.
*   **Weaknesses**: Can be overly verbose, "abstraction hell," steep learning curve.
*   **Best For**: Complex, production-grade applications needing strict control flow.

### B. Microsoft AutoGen
*   **Philosophy**: Conversational agents. Agents "talk" to each other to solve tasks.
*   **Strengths**: Multi-agent conversation patterns are built-in, code execution support.
*   **Weaknesses**: Can get stuck in loops, harder to control precise output.
*   **Best For**: Open-ended problem solving, simulation.

### C. CrewAI
*   **Philosophy**: Role-based agents (similar to a movie crew).
*   **Strengths**: Easy to define "Roles" (Researcher, Writer), process-oriented.
*   **Weaknesses**: Newer, smaller ecosystem than LangChain.
*   **Best For**: Task delegation workflows.

## 3. Comparison with Our Approach (The "3-Model CLI" System)

| Feature | Frameworks (AutoGen, etc.) | Our CLI System |
| :--- | :--- | :--- |
| **Control** | Automated / Loop-based | Human-in-the-loop (User is the orchestrator) |
| **Tooling** | Python/JS SDKs | Native Terminal / Shell |
| **Flexibility** | High (programmatic) | High (ad-hoc) |
| **Setup** | Complex (requires coding) | Simple (requires CLI installation) |

## 4. Why We Chose the CLI Approach
For this project, we prioritize **human agency** and **simplicity**.
*   We don't need agents chatting endlessly in a background loop.
*   We need powerful tools that we can invoke precisely when needed.
*   The "User as Router" pattern eliminates the need for complex orchestration code.

## 5. Conclusion
While frameworks like LangGraph offer power for autonomous apps, a set of specialized CLIs (Gemini, Claude, OpenAI) orchestrated by a human developer offers the best balance of control and assistance for software engineering workflows.
