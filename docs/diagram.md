# 3-Model Concurrent Workflow Diagram

## System Architecture

```mermaid
flowchart TB
    subgraph Project["Project Folder"]
        SC[shared-context.md]

        subgraph Context["Context Files"]
            CM[CLAUDE.md]
            GM[GEMINI.md]
            OM[OPENAI.md]
        end

        subgraph Output["Shared Output"]
            R[research/]
            D[drafts/]
            O[output/]
        end
    end

    subgraph Tools["3 Concurrent AI Tools"]
        C["Claude Code<br/>Deep Work & Agents"]
        G["Gemini CLI<br/>Research & Web Search"]
        OA["OpenAI CLI<br/>Analysis & Review"]
    end

    C <--> CM
    G <--> GM
    OA <--> OM

    C <--> SC
    G <--> SC
    OA <--> SC

    C --> R
    C --> D
    C --> O
    G --> R
    OA --> D
```

## Workflow Pattern

```mermaid
sequenceDiagram
    participant U as User
    participant C as Claude Code
    participant G as Gemini CLI
    participant O as OpenAI CLI
    participant F as Project Files

    U->>U: run.bat → Enter task

    par Launch All Three
        U->>C: Start Claude
        U->>G: Start Gemini
        U->>O: Start OpenAI
    end

    Note over C,O: All read shared-context.md

    par Concurrent Work
        C->>F: Complex tasks, file edits
        G->>F: Research, web search
        O->>F: Analysis, code review
    end

    Note over C,O: Update shared-context.md when switching focus

    C->>F: git commit
```

## Tool Responsibilities

```mermaid
pie showData
    title Task Distribution
    "Claude Code (Complex)" : 40
    "Gemini CLI (Research)" : 35
    "OpenAI CLI (Analysis)" : 25
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        PROJECT FOLDER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │ CLAUDE.md│    │GEMINI.md │    │OPENAI.md │   Context Files  │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘                  │
│       │               │               │                         │
│       ▼               ▼               ▼                         │
│  ┌─────────────────────────────────────────┐                   │
│  │          shared-context.md              │   Sync Layer      │
│  │   (Cross-tool state & handoff notes)    │                   │
│  └─────────────────────────────────────────┘                   │
│                       │                                         │
│       ┌───────────────┼───────────────┐                        │
│       ▼               ▼               ▼                         │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐                   │
│  │research/│    │ drafts/  │    │ output/  │   Shared Output   │
│  └─────────┘    └──────────┘    └──────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  ┌───────────┐        ┌───────────┐        ┌───────────┐
  │  Claude   │        │  Gemini   │        │  OpenAI   │
  │   Code    │        │   CLI     │        │   CLI     │
  ├───────────┤        ├───────────┤        ├───────────┤
  │ • Agents  │        │ • Web     │        │ • Code    │
  │ • Files   │        │   Search  │        │   Review  │
  │ • Complex │        │ • Research│        │ • Analysis│
  │   Tasks   │        │ • Explore │        │ • Reason  │
  └───────────┘        └───────────┘        └───────────┘
```
