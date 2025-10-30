# Automation Examples with Mermaid Diagrams

This document shows real-world examples of how the auto-activation system works with visual Mermaid diagrams.

---

## Table of Contents

1. [Use Case 1: Creating a New API Endpoint](#use-case-1-creating-a-new-api-endpoint)
2. [Use Case 2: Building a React Component](#use-case-2-building-a-react-component)
3. [Use Case 3: Debugging an Error](#use-case-3-debugging-an-error)
4. [Use Case 4: Refactoring Code](#use-case-4-refactoring-code)
5. [System Architecture](#system-architecture)
6. [Auto-Activation Flow](#auto-activation-flow)

---

## Use Case 1: Creating a New API Endpoint

### Scenario
Developer wants to add a new authenticated endpoint for user registration.

### Flow Diagram

```mermaid
sequenceDiagram
    actor Dev as Developer
    participant File as src/api/routes/users.ts
    participant Hook as skill-activation-prompt
    participant Rules as skill-rules.json
    participant Claude as Claude Code
    participant Skill as backend-dev-guidelines

    Dev->>File: Opens file in editor
    Dev->>Claude: "Add user registration endpoint"
    
    Note over Hook: UserPromptSubmit hook triggers
    Hook->>Rules: Check trigger patterns
    Rules-->>Hook: Match found:<br/>- File: src/api/**/*.ts<br/>- Keyword: "endpoint"
    
    Hook->>Claude: Inject skill suggestion
    Note over Claude: Auto-loads skill
    Claude->>Skill: Access patterns and guidelines
    
    Skill-->>Claude: Returns:<br/>✅ BaseController pattern<br/>✅ Zod validation<br/>✅ Prisma repository<br/>✅ Sentry error handling
    
    Claude->>File: Generate code with patterns
    Note over File: Code follows all patterns!
    
    Claude->>Dev: "Created endpoint following<br/>backend-dev-guidelines"
    
    Note over Dev,File: ✨ 3 minutes instead of 15!
```

### Without Automation

```mermaid
sequenceDiagram
    actor Dev as Developer
    participant Claude as Claude Code
    participant File as src/api/routes/users.ts

    Dev->>Claude: "Add user registration endpoint"
    Claude->>File: Creates basic endpoint
    Note over File: ❌ No patterns followed
    
    Dev->>Claude: "Wait, use backend-dev-guidelines!"
    Claude->>File: Recreates with some patterns
    Note over File: ⚠️ Partial patterns
    
    Dev->>Claude: "Add error handling with Sentry"
    Claude->>File: Adds error handling
    
    Dev->>Claude: "Use BaseController pattern"
    Claude->>File: Refactors to BaseController
    
    Dev->>Claude: "Add Zod validation"
    Claude->>File: Adds validation
    
    Note over Dev,File: 😩 15 minutes, multiple iterations
```

### Time Comparison

```mermaid
pie title Time Savings Per Endpoint
    "With Auto-Activation (3 min)" : 3
    "Without Auto-Activation (15 min)" : 15
```

---

## Use Case 2: Building a React Component

### Scenario
Developer creates a data grid component with MUI v7.

### Flow Diagram

```mermaid
sequenceDiagram
    actor Dev as Developer
    participant File as src/features/users/UserList.tsx
    participant Hook as skill-activation-prompt
    participant Rules as skill-rules.json
    participant Claude as Claude Code
    participant Skill as frontend-dev-guidelines

    Dev->>File: Creates new .tsx file
    Dev->>Claude: "Create user list with MUI DataGrid"
    
    Note over Hook: UserPromptSubmit hook triggers
    Hook->>Rules: Check trigger patterns
    Rules-->>Hook: Match found:<br/>- File: src/**/*.tsx<br/>- Keyword: "MUI", "DataGrid"<br/>- Enforcement: BLOCK
    
    Hook->>Claude: Inject skill (GUARDRAIL)
    Note over Claude: Skill required before proceeding
    Claude->>Skill: Access MUI v7 patterns
    
    Skill-->>Claude: Returns:<br/>✅ Grid with size={{}}<br/>✅ useSuspenseQuery<br/>✅ Error boundaries<br/>✅ Loading states
    
    Claude->>File: Generate component
    Note over File: MUI v7 patterns enforced!
    
    Claude->>Dev: "Created DataGrid with MUI v7 patterns"
    
    Note over Dev,File: ✨ No deprecated v6 code!
```

### Guardrail Protection

```mermaid
graph TD
    A[Developer asks for MUI component] --> B{frontend-dev-guidelines<br/>activated?}
    B -->|No - Blocked| C[❌ Cannot proceed]
    B -->|Yes| D[Check MUI version]
    D --> E{Using v7 patterns?}
    E -->|No| F[🚫 Warn: Use v7 patterns]
    E -->|Yes| G[✅ Generate code]
    
    C --> H[Suggest: Activate skill]
    H --> B
    F --> I[Show v7 examples]
    I --> G
    
    style C fill:#ffcccc
    style F fill:#ffffcc
    style G fill:#ccffcc
```

---

## Use Case 3: Debugging an Error

### Scenario
Frontend build fails with TypeScript errors.

### Flow Diagram

```mermaid
sequenceDiagram
    actor Dev as Developer
    participant Build as npm run build
    participant Hook as post-tool-use-tracker
    participant Agent as auto-error-resolver
    participant Files as Source Files
    participant Claude as Claude Code

    Dev->>Build: Runs build
    Build-->>Dev: ❌ 12 TypeScript errors
    
    Note over Hook: PostToolUse hook detects errors
    Hook->>Agent: Trigger auto-error-resolver
    
    Agent->>Build: Analyze error output
    Agent->>Files: Identify affected files
    
    Note over Agent: Autonomous analysis
    Agent->>Files: Apply fixes
    
    Agent->>Build: Re-run build
    Build-->>Agent: ✅ Build successful
    
    Agent->>Dev: Report: Fixed 12 errors in 4 files
    Note over Dev: Errors resolved automatically!
```

### Error Resolution Flow

```mermaid
graph LR
    A[Build Fails] --> B[post-tool-use-tracker<br/>detects errors]
    B --> C{Trigger<br/>auto-error-resolver?}
    C -->|Yes| D[Agent analyzes errors]
    C -->|No| E[Manual debugging]
    
    D --> F[Categorize errors]
    F --> G[Import errors]
    F --> H[Type errors]
    F --> I[Syntax errors]
    
    G --> J[Fix imports]
    H --> K[Fix types]
    I --> L[Fix syntax]
    
    J --> M[Re-run build]
    K --> M
    L --> M
    
    M --> N{Build passes?}
    N -->|Yes| O[✅ Report success]
    N -->|No| P[Report remaining errors]
    
    style O fill:#ccffcc
    style E fill:#ffcccc
```

---

## Use Case 4: Refactoring Code

### Scenario
Developer needs to move authentication logic to a shared package.

### Flow Diagram

```mermaid
sequenceDiagram
    actor Dev as Developer
    participant Claude as Claude Code
    participant Planner as refactor-planner agent
    participant Master as code-refactor-master agent
    participant Files as Source Files
    participant Tests as Test Suite

    Dev->>Claude: "Move auth logic to shared package"
    
    Note over Claude: Delegates to specialized agent
    Claude->>Planner: Invoke refactor-planner
    
    Planner->>Files: Analyze dependencies
    Planner->>Files: Map file relationships
    Planner-->>Claude: Return refactoring plan:<br/>1. Create shared/auth package<br/>2. Move 8 files<br/>3. Update 24 imports<br/>4. Update tests
    
    Claude->>Dev: Show plan for approval
    Dev->>Claude: "Execute the plan"
    
    Claude->>Master: Invoke code-refactor-master
    Master->>Files: Create shared/auth directory
    Master->>Files: Move files with history
    Master->>Files: Update all imports
    Master->>Tests: Update test imports
    
    Master->>Tests: Run test suite
    Tests-->>Master: ✅ All tests pass
    
    Master-->>Claude: Refactoring complete
    Claude->>Dev: "Moved auth to shared package<br/>✅ 8 files moved<br/>✅ 24 imports updated<br/>✅ Tests passing"
```

### Agent Collaboration

```mermaid
graph TD
    A[Developer Request] --> B[Claude Code]
    B --> C{Complex task?}
    C -->|Yes| D[Delegate to Agent]
    C -->|No| E[Handle directly]
    
    D --> F{Which agent?}
    F -->|Planning| G[refactor-planner]
    F -->|Execution| H[code-refactor-master]
    F -->|Review| I[code-architecture-reviewer]
    F -->|Docs| J[documentation-architect]
    
    G --> K[Create plan]
    K --> L[Return to Claude]
    
    H --> M[Execute changes]
    M --> N[Verify results]
    N --> L
    
    I --> O[Review code]
    O --> P[Provide feedback]
    P --> L
    
    J --> Q[Generate docs]
    Q --> L
    
    L --> R[Present to Developer]
    
    style D fill:#cce5ff
    style G fill:#e5ccff
    style H fill:#ffe5cc
    style I fill:#ccffe5
    style J fill:#ffccf2
```

---

## System Architecture

### Complete Auto-Activation System

```mermaid
graph TB
    subgraph "User Actions"
        A1[Edit File]
        A2[Submit Prompt]
        A3[Ask Question]
    end
    
    subgraph "Hooks Layer"
        H1[skill-activation-prompt<br/>UserPromptSubmit]
        H2[post-tool-use-tracker<br/>PostToolUse]
        H3[tsc-check<br/>Stop Hook]
    end
    
    subgraph "Configuration"
        C1[skill-rules.json]
        C2[settings.json]
    end
    
    subgraph "Skills Library"
        S1[backend-dev-guidelines]
        S2[frontend-dev-guidelines]
        S3[route-tester]
        S4[error-tracking]
        S5[skill-developer]
    end
    
    subgraph "Agents"
        AG1[code-architecture-reviewer]
        AG2[refactor-planner]
        AG3[auto-error-resolver]
        AG4[documentation-architect]
    end
    
    subgraph "Claude Code"
        CL[Claude Processing]
    end
    
    A1 --> H2
    A2 --> H1
    A3 --> H1
    
    H1 --> C1
    H2 --> C1
    H3 --> C2
    
    C1 --> S1
    C1 --> S2
    C1 --> S3
    C1 --> S4
    C1 --> S5
    
    S1 --> CL
    S2 --> CL
    S3 --> CL
    S4 --> CL
    S5 --> CL
    
    CL --> AG1
    CL --> AG2
    CL --> AG3
    CL --> AG4
    
    AG1 --> CL
    AG2 --> CL
    AG3 --> CL
    AG4 --> CL
    
    style H1 fill:#ffe5cc
    style H2 fill:#ffe5cc
    style C1 fill:#cce5ff
    style CL fill:#ccffcc
```

---

## Auto-Activation Flow

### Detailed Trigger Mechanism

```mermaid
flowchart TD
    Start([User Action]) --> A{What happened?}
    
    A -->|Edited file| B[PostToolUse Hook]
    A -->|Submitted prompt| C[UserPromptSubmit Hook]
    
    B --> D[Extract file path]
    C --> E[Extract prompt text]
    
    D --> F[Read skill-rules.json]
    E --> F
    
    F --> G{Check all skills}
    
    G --> H{Match<br/>fileTriggers?}
    H -->|Yes| I[Add to matches]
    H -->|No| J{Match<br/>promptTriggers?}
    
    J -->|Yes| I
    J -->|No| K{More skills?}
    
    K -->|Yes| G
    K -->|No| L{Any matches?}
    
    L -->|No| M[Continue without skills]
    L -->|Yes| N[Sort by priority]
    
    N --> O{Enforcement<br/>level?}
    
    O -->|suggest| P[Suggest skill]
    O -->|block| Q[Require skill]
    
    P --> R[Inject into prompt]
    Q --> R
    
    R --> S[Load skill content]
    S --> T[Claude processes]
    T --> U([Generate response])
    
    I --> K
    
    style Q fill:#ffcccc
    style P fill:#ffffcc
    style U fill:#ccffcc
```

### Skill Matching Logic

```mermaid
flowchart LR
    A[skill-rules.json] --> B{For each skill}
    
    B --> C[Check fileTriggers]
    B --> D[Check promptTriggers]
    
    C --> C1{pathPatterns<br/>match?}
    C --> C2{contentPatterns<br/>match?}
    
    D --> D1{keywords<br/>match?}
    D --> D2{intentPatterns<br/>match?}
    
    C1 -->|Yes| E[File Match]
    C2 -->|Yes| E
    D1 -->|Yes| F[Prompt Match]
    D2 -->|Yes| F
    
    E --> G{Score}
    F --> G
    
    G --> H[Calculate priority]
    H --> I[Add to results]
    
    C1 -->|No| J[Next check]
    C2 -->|No| J
    D1 -->|No| J
    D2 -->|No| J
    
    J --> K{More skills?}
    K -->|Yes| B
    K -->|No| L[Return matches]
    
    style E fill:#ccffcc
    style F fill:#ccffcc
    style L fill:#cce5ff
```

---

## Time Savings Visualization

### Daily Developer Workflow

```mermaid
gantt
    title Developer Time Comparison (Typical Day)
    dateFormat X
    axisFormat %M min
    
    section Without Auto-Activation
    Create 3 API endpoints    :a1, 0, 45
    Build 2 React components  :a2, after a1, 60
    Debug errors manually     :a3, after a2, 40
    Context rebuilds (3x)     :a4, after a3, 30
    Manual skill invocations  :a5, after a4, 20
    
    section With Auto-Activation
    Create 3 API endpoints    :b1, 0, 9
    Build 2 React components  :b2, after b1, 20
    Auto-resolved errors      :b3, after b2, 5
    Context preserved         :b4, after b3, 0
    Automatic skill loading   :b5, after b4, 0
```

### Productivity Metrics

```mermaid
graph LR
    A[Without Automation] -->|195 min/day| B[Development Time]
    C[With Automation] -->|34 min/day| B
    
    B --> D[Time Saved:<br/>161 min/day]
    D --> E[83% reduction]
    
    F[Manual Skill Invocations] -->|20/day| G[Cognitive Load]
    H[Automatic Activation] -->|0/day| G
    
    G --> I[Mental Energy Saved]
    I --> J[100% automation]
    
    style A fill:#ffcccc
    style C fill:#ccffcc
    style E fill:#ccffcc
    style J fill:#ccffcc
```

---

## Real-World Impact

### Cumulative Time Savings

```mermaid
graph TD
    A[1 Endpoint] -->|Saves 12 min| B[12 minutes saved]
    C[10 Endpoints/week] -->|12 min each| D[120 min/week]
    D --> E[2 hours/week]
    
    F[Context Resets] -->|3 per day| G[30 min saved/day]
    G --> H[2.5 hours/week]
    
    I[Manual Skill Invocations] -->|20 per day| J[20 min saved/day]
    J --> K[1.7 hours/week]
    
    E --> L[Total Weekly Savings]
    H --> L
    K --> L
    
    L --> M[6.2 hours/week]
    M --> N[25 hours/month]
    N --> O[~3 work days/month]
    
    style O fill:#ccffcc
```

---

## Implementation in Another Repo

To implement this automation system in a repository without automations:

```mermaid
flowchart TD
    Start([Your Repo]) --> A[Step 1: Copy Essential Hooks]
    
    A --> B[skill-activation-prompt.sh<br/>skill-activation-prompt.ts<br/>post-tool-use-tracker.sh]
    
    B --> C[Step 2: Install Dependencies]
    C --> D[npm install in .claude/hooks/]
    
    D --> E[Step 3: Configure settings.json]
    E --> F[Add UserPromptSubmit hook<br/>Add PostToolUse hook]
    
    F --> G[Step 4: Copy Relevant Skill]
    G --> H{Your tech stack?}
    
    H -->|Node/Express| I[backend-dev-guidelines]
    H -->|React| J[frontend-dev-guidelines]
    H -->|Other| K[Adapt existing skill]
    
    I --> L[Step 5: Create skill-rules.json]
    J --> L
    K --> L
    
    L --> M[Update pathPatterns<br/>to match YOUR paths]
    
    M --> N[Step 6: Test]
    N --> O{Skill activates?}
    
    O -->|Yes| P[✅ Done!<br/>Add more skills as needed]
    O -->|No| Q[Debug:<br/>Check paths, hooks executable]
    
    Q --> N
    
    style P fill:#ccffcc
    style Q fill:#ffffcc
```

### Quick Setup Commands

```bash
# 1. Create structure
mkdir -p .claude/hooks
mkdir -p .claude/skills
mkdir -p .claude/agents

# 2. Copy hooks from this repo
cp path/to/showcase/.claude/hooks/skill-activation-prompt.* .claude/hooks/
cp path/to/showcase/.claude/hooks/post-tool-use-tracker.sh .claude/hooks/

# 3. Make executable
chmod +x .claude/hooks/*.sh

# 4. Install dependencies
cd .claude/hooks && npm install

# 5. Copy a skill
cp -r path/to/showcase/.claude/skills/backend-dev-guidelines .claude/skills/

# 6. Copy and customize skill-rules.json
cp path/to/showcase/.claude/skills/skill-rules.json .claude/skills/
# Edit pathPatterns to match YOUR project structure

# 7. Add to settings.json (see COMPREHENSIVE_GUIDE.md for full config)
```

---

## Summary

These diagrams show how the auto-activation system:

1. **Detects context** (files, prompts) automatically
2. **Matches skills** based on rules
3. **Injects guidance** proactively
4. **Saves time** (80%+ reduction)
5. **Ensures consistency** (enforced patterns)

The system transforms Claude Code from a helpful assistant into an expert team member who knows your patterns and applies them automatically.
