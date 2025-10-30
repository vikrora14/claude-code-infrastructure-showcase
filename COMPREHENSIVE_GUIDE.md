# Claude Code Infrastructure Showcase - Comprehensive Guide

> **A complete understanding of what this is, why it matters, and how to use it**

---

## Table of Contents

1. [What Is This Service?](#what-is-this-service)
2. [The Problem It Solves](#the-problem-it-solves)
3. [Features & Functionality](#features--functionality)
4. [Architecture Overview](#architecture-overview)
5. [Impact & Benefits](#impact--benefits)
6. [Step-by-Step Consumption Guide](#step-by-step-consumption-guide)
7. [Real-World Use Cases](#real-world-use-cases)
8. [Advanced Topics](#advanced-topics)

---

## What Is This Service?

### **It's NOT a Service - It's a Reference Library**

This repository is **a curated collection of production-tested infrastructure patterns** for Claude Code (Anthropic's AI coding assistant). Think of it as a toolkit or template library that you copy components from into your own projects.

### What It Actually Is

**Claude Code Infrastructure Showcase** is:
- ✅ A **reference library** of reusable components
- ✅ A **pattern catalog** extracted from real production use
- ✅ A **best practices guide** for Claude Code configuration
- ✅ An **educational resource** showing how to maximize Claude Code effectiveness

**It is NOT:**
- ❌ A working application you run
- ❌ A SaaS service you subscribe to
- ❌ A framework you install via npm/pip
- ❌ A standalone tool

### The Origin Story

This infrastructure was built over **6 months** of daily Claude Code use on a complex production project:
- 6 microservices in production
- 50,000+ lines of TypeScript
- React frontend with complex data grids
- Sophisticated workflow engine

The creator documented their learnings in a [viral Reddit post](https://www.reddit.com/r/ClaudeAI/comments/1gc4xme/claude_code_is_a_beast_part_2_the_secret_to/) titled "Claude Code is a Beast - Part 2". After hundreds of requests for the infrastructure, this showcase repository was created.

---

## The Problem It Solves

### The #1 Problem with Claude Code: Skills Don't Activate Automatically

When you use Claude Code, you can create "skills" (specialized knowledge bases), but they just sit there. **You have to remember to manually tell Claude which skill to use.**

**Imagine this scenario:**
```
You: "Add a new API endpoint for user registration"
Claude: *Creates code without following your patterns*
You: "Wait, use the backend-dev-guidelines skill!"
Claude: "Oh! Let me redo that following the patterns..."
```

**This is frustrating because:**
- ❌ You must remember which skill applies
- ❌ Claude won't suggest skills proactively  
- ❌ Skills are only as useful as your memory
- ❌ Inconsistent code gets written

### Additional Problems

**Problem #2: Large Skills Hit Context Limits**
- Skills with 2000+ lines don't fit in context
- Claude can't process them effectively
- You lose the benefit of comprehensive guidance

**Problem #3: Context Resets Lose Project Knowledge**
- When you start a new conversation, Claude forgets everything
- Project-specific patterns must be re-explained
- Wastes time rebuilding context

**Problem #4: No Consistency Across Development**
- Different developers (or Claude sessions) make different choices
- Architectural patterns aren't enforced
- Technical debt accumulates

---

## Features & Functionality

This showcase provides **4 main categories of components** that work together:

### 1. **Auto-Activating Skills System** ⭐ (The Breakthrough Feature)

**What it does:**
- Automatically suggests relevant skills based on what you're doing
- Analyzes your prompts and detects which skill is needed
- Checks which files you're editing and activates matching skills
- Makes skills activate when needed, not when remembered

**How it works:**
```
You edit: src/api/routes/users.ts
Hook detects: "This is a backend TypeScript file"
Hook checks: skill-rules.json
Hook injects: "Consider using backend-dev-guidelines skill"
Claude: "I'll use the backend patterns for this route..."
```

**Components:**
- `skill-activation-prompt` hook (UserPromptSubmit)
- `post-tool-use-tracker` hook (PostToolUse)
- `skill-rules.json` configuration

### 2. **Modular Skills** (5 Production-Ready Skills)

**The 500-Line Rule:**
Each skill follows a modular structure to avoid context limits:
```
skill-name/
  SKILL.md                  # Main file <500 lines (overview)
  resources/
    architecture.md         # <500 lines (deep dive)
    best-practices.md       # <500 lines (deep dive)
    examples.md             # <500 lines (deep dive)
```

**Available Skills:**

| Skill | Purpose | Lines | Tech Stack |
|-------|---------|-------|------------|
| **skill-developer** | Meta-skill for creating skills | 426 | Framework-agnostic |
| **backend-dev-guidelines** | Node.js/Express API patterns | 304 + 12 resources | Express, Prisma, TypeScript |
| **frontend-dev-guidelines** | React development patterns | 398 + 11 resources | React, MUI v7, TypeScript |
| **route-tester** | Testing authenticated endpoints | 389 | JWT cookie auth |
| **error-tracking** | Sentry integration patterns | ~250 | Sentry v8 |

### 3. **Specialized Agents** (10 Autonomous Agents)

Agents are autonomous Claude instances that handle complex, multi-step tasks:

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| code-architecture-reviewer | Review code for architectural issues | Before merging big changes |
| code-refactor-master | Execute comprehensive refactoring | Reorganizing code structure |
| documentation-architect | Generate comprehensive docs | Documenting new features |
| frontend-error-fixer | Debug frontend errors | React/TypeScript errors |
| plan-reviewer | Review development plans | Before starting complex work |
| refactor-planner | Create refactoring strategies | Planning code modernization |
| web-research-specialist | Research technical issues | Finding solutions online |
| auth-route-tester | Test authenticated endpoints | Testing JWT auth routes |
| auth-route-debugger | Debug auth issues | Authentication failures |
| auto-error-resolver | Auto-fix TypeScript errors | Build failures |

**Key Advantage:** Agents are standalone - just copy the `.md` file and use immediately!

### 4. **Hooks System** (6 Automation Hooks)

Hooks run at specific points in Claude's workflow to enable automation:

**Essential Hooks (Copy These):**
- **skill-activation-prompt**: Auto-suggests skills (UserPromptSubmit)
- **post-tool-use-tracker**: Tracks file changes (PostToolUse)

**Optional Hooks (For Advanced Setups):**
- **tsc-check**: TypeScript compilation check (Stop)
- **trigger-build-resolver**: Auto-launches error resolver (Stop)
- **error-handling-reminder**: Reminds about error handling (Stop)
- **stop-build-check-enhanced**: Enhanced build checks (Stop)

### 5. **Dev Docs Pattern**

A system for preserving knowledge across context resets:

**Three-file structure:**
```
dev/active/your-feature/
  ├── feature-plan.md      # Strategic plan
  ├── feature-context.md   # Key decisions and files
  └── feature-tasks.md     # Checklist format
```

**Slash Commands:**
- `/dev-docs` - Create structured dev documentation
- `/dev-docs-update` - Update docs before context reset
- `/route-research-for-testing` - Research route patterns

---

## Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR PROJECT                             │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  .claude/                                                 │ │
│  │                                                           │ │
│  │  ├── skills/                                             │ │
│  │  │   ├── backend-dev-guidelines/    ← Domain knowledge  │ │
│  │  │   ├── frontend-dev-guidelines/                       │ │
│  │  │   └── skill-rules.json          ← Activation config  │ │
│  │  │                                                       │ │
│  │  ├── hooks/                                              │ │
│  │  │   ├── skill-activation-prompt.*  ← Auto-activation   │ │
│  │  │   └── post-tool-use-tracker.sh   ← Context tracking  │ │
│  │  │                                                       │ │
│  │  ├── agents/                                             │ │
│  │  │   ├── code-architecture-reviewer.md ← Specialists    │ │
│  │  │   └── ... 9 more agents                              │ │
│  │  │                                                       │ │
│  │  └── settings.json                   ← Hook config      │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  Your actual code:                                              │
│  ├── src/api/           ← Triggers backend-dev-guidelines      │
│  ├── src/frontend/      ← Triggers frontend-dev-guidelines     │
│  └── ...                                                        │
└─────────────────────────────────────────────────────────────────┘
```

### How Auto-Activation Works

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. User Action                                                   │
│    - Edits file: src/api/routes/users.ts                         │
│    - Or asks: "How do I create a new controller?"                │
└────────────────┬─────────────────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────────────────────────┐
│ 2. Hook Triggers (skill-activation-prompt)                       │
│    - UserPromptSubmit hook intercepts                            │
│    - Reads skill-rules.json                                      │
│    - Analyzes: prompt keywords + file paths                      │
└────────────────┬─────────────────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────────────────────────┐
│ 3. Skill Matching                                                │
│    skill-rules.json:                                             │
│    {                                                             │
│      "backend-dev-guidelines": {                                 │
│        "promptTriggers": {                                       │
│          "keywords": ["controller", "API", "route"]              │
│        },                                                        │
│        "fileTriggers": {                                         │
│          "pathPatterns": ["src/api/**/*.ts"]                     │
│        }                                                         │
│      }                                                           │
│    }                                                             │
│    ✅ MATCH FOUND!                                              │
└────────────────┬─────────────────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────────────────────────┐
│ 4. Skill Injection                                               │
│    Hook modifies prompt:                                         │
│    "Consider using the backend-dev-guidelines skill which        │
│     provides patterns for Express controllers, services, and     │
│     Prisma repositories."                                        │
└────────────────┬─────────────────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────────────────────────────────┐
│ 5. Claude Responds                                               │
│    "I'll use the backend-dev-guidelines skill. Based on the      │
│     patterns, I'll create a controller extending BaseController  │
│     with proper error handling..."                               │
└──────────────────────────────────────────────────────────────────┘
```

### Modular Skill Loading

```
┌────────────────────────────────────────────────────────────┐
│ Claude's Context Window (Limited)                          │
│                                                            │
│ ┌────────────────────────────────────────────┐            │
│ │ Initial Load:                              │            │
│ │   backend-dev-guidelines/SKILL.md          │            │
│ │   (304 lines - high-level overview)        │            │
│ │                                            │            │
│ │   "For routing details, see resources/     │            │
│ │    routing-patterns.md"                    │            │
│ └────────────────────────────────────────────┘            │
│                                                            │
│ User asks: "How do I implement route validation?"          │
│                                                            │
│ ┌────────────────────────────────────────────┐            │
│ │ Progressive Load:                          │            │
│ │   resources/routing-patterns.md            │            │
│ │   (Deep dive on routing - loaded on demand)│            │
│ └────────────────────────────────────────────┘            │
└────────────────────────────────────────────────────────────┘
```

---

## Impact & Benefits

### Quantifiable Impact

**Time Savings:**
- ⏱️ **15-30 minutes** to integrate into your project
- ⏱️ **6 months** of iteration time saved (you're getting proven patterns)
- ⏱️ **50-70% reduction** in context-rebuilding time
- ⏱️ **Instant skill activation** vs manual skill invocation every time

**Code Quality:**
- 📈 **Consistent patterns** across entire codebase
- 📈 **Fewer bugs** from following tested patterns
- 📈 **Better architecture** from enforced best practices
- 📈 **Faster onboarding** for new team members (or new Claude sessions)

**Developer Experience:**
- ✨ **Skills activate automatically** - no more "I forgot to use the skill"
- ✨ **Context persists** across resets via dev docs
- ✨ **Specialized agents** handle complex tasks autonomously
- ✨ **Progressive disclosure** prevents context overflow

### Before vs After Comparison

| Aspect | Before This Infrastructure | After This Infrastructure |
|--------|---------------------------|---------------------------|
| **Skill Usage** | "Claude, use the backend skill" (every time) | Automatic activation when editing backend files |
| **Context Management** | Manually rebuild context after reset | Dev docs preserve key information |
| **Code Consistency** | Varies by Claude session/developer | Enforced by guardrail skills |
| **Large Codebases** | Skills hit context limits | Modular skills load progressively |
| **Complex Tasks** | Manually step through complex refactors | Agents handle autonomously |
| **Time to Productivity** | 10-15 minutes rebuilding context | Immediate with preserved dev docs |

### Real Impact Example

**Scenario: Adding a new authenticated API endpoint**

**Without this infrastructure (15 minutes):**
```
1. Ask Claude to create endpoint [3 min]
2. Claude creates it without patterns
3. You: "Wait, use the backend guidelines" [1 min]
4. Claude recreates with some patterns [3 min]
5. You: "Don't forget error handling" [1 min]
6. Claude adds Sentry integration [2 min]
7. You: "Use BaseController pattern" [1 min]
8. Claude refactors again [3 min]
9. You review and fix inconsistencies [1 min]
```

**With this infrastructure (3 minutes):**
```
1. Edit: src/api/routes/users.ts
2. Hook detects: backend-dev-guidelines activates automatically
3. You: "Add user registration endpoint with validation"
4. Claude: Creates endpoint with:
   ✅ BaseController pattern
   ✅ Sentry error handling
   ✅ Zod validation
   ✅ Prisma repository pattern
   ✅ Proper async/await
   [Done in one shot]
```

**Time saved: 12 minutes per endpoint × dozens of endpoints = hours saved**

---

## Step-by-Step Consumption Guide

### Prerequisites

**You need:**
- ✅ Claude Code installed (Anthropic's AI coding assistant)
- ✅ An existing project (or starting a new one)
- ✅ 15-30 minutes for setup

**You don't need:**
- ❌ Any specific tech stack (skills can be adapted)
- ❌ To use all components (pick what's relevant)
- ❌ To install this as a dependency

### Phase 1: Understand What You Have (5 minutes)

**Step 1.1: Clone or download this repository**
```bash
git clone https://github.com/vikrora14/claude-code-infrastructure-showcase.git
cd claude-code-infrastructure-showcase
```

**Step 1.2: Browse the structure**
```bash
# Explore the directory structure
tree -L 3 .claude/

# Read the main README
cat README.md

# Check out the skills
ls -la .claude/skills/

# Check out the agents
ls -la .claude/agents/
```

**Step 1.3: Identify what's relevant to your project**

Ask yourself:
- Do I use Node.js/Express? → `backend-dev-guidelines` skill
- Do I use React/MUI? → `frontend-dev-guidelines` skill
- Do I want skills to auto-activate? → Essential hooks
- Do I need specialized help? → Agents

### Phase 2: Set Up Auto-Activation (15 minutes)

This is the **most impactful** part - makes skills activate automatically.

**Step 2.1: Create the .claude directory in your project**
```bash
cd /path/to/your/project

# Create directory structure
mkdir -p .claude/hooks
mkdir -p .claude/skills
mkdir -p .claude/agents
```

**Step 2.2: Copy the essential hooks**
```bash
# Copy skill-activation-prompt hook (both files)
cp /path/to/showcase/.claude/hooks/skill-activation-prompt.sh \
   .claude/hooks/

cp /path/to/showcase/.claude/hooks/skill-activation-prompt.ts \
   .claude/hooks/

# Copy post-tool-use-tracker hook
cp /path/to/showcase/.claude/hooks/post-tool-use-tracker.sh \
   .claude/hooks/

# Make them executable
chmod +x .claude/hooks/*.sh
```

**Step 2.3: Install hook dependencies**
```bash
cd .claude/hooks

# If package.json exists in showcase hooks, copy it
cp /path/to/showcase/.claude/hooks/package.json .

# Install dependencies
npm install

cd ../..
```

**Step 2.4: Configure settings.json**

Create or update `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/skill-activation-prompt.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use-tracker.sh"
          }
        ]
      }
    ]
  }
}
```

**Step 2.5: Verify hooks are working**
```bash
# Check hooks are executable
ls -la .claude/hooks/*.sh

# Should show: -rwxr-xr-x (executable)

# Test hook manually
./.claude/hooks/skill-activation-prompt.sh

# Should run without errors
```

✅ **Checkpoint:** You now have the auto-activation system ready!

### Phase 3: Add Your First Skill (10 minutes)

**Step 3.1: Choose a relevant skill**

Based on your tech stack:
- **Node.js/Express backend?** → `backend-dev-guidelines`
- **React frontend?** → `frontend-dev-guidelines`
- **Need to create skills?** → `skill-developer`
- **JWT auth testing?** → `route-tester`
- **Sentry error tracking?** → `error-tracking`

**Step 3.2: Copy the skill**

Example: Adding backend-dev-guidelines
```bash
cp -r /path/to/showcase/.claude/skills/backend-dev-guidelines \
      .claude/skills/
```

**Step 3.3: Create/update skill-rules.json**

This file tells the hook when to activate skills.

**If you DON'T have skill-rules.json yet:**
```bash
cp /path/to/showcase/.claude/skills/skill-rules.json \
   .claude/skills/
```

Then edit `.claude/skills/skill-rules.json` to match YOUR project structure:

```json
{
  "backend-dev-guidelines": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "promptTriggers": {
      "keywords": [
        "backend", "API", "route", "controller", "service",
        "repository", "database", "Prisma", "Express"
      ],
      "intentPatterns": [
        "creat(e|ing) .* (route|endpoint|controller|service)",
        "implement .* API",
        "add .* (authentication|validation)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "src/api/**/*.ts",        // ← UPDATE THIS!
        "backend/**/*.ts",        // ← TO MATCH YOUR PROJECT!
        "server/**/*.ts"          // ← STRUCTURE!
      ],
      "contentPatterns": [
        "import.*prisma",
        "extends BaseController",
        "Sentry\\.captureException"
      ]
    }
  }
}
```

**CRITICAL:** Update the `pathPatterns` array to match where YOUR backend code lives!

**Common patterns:**
- Single app: `["src/**/*.ts"]`
- Monorepo: `["packages/*/src/**/*.ts", "apps/*/src/**/*.ts"]`
- Backend folder: `["backend/src/**/*.ts"]`

**Step 3.4: Validate configuration**
```bash
# Check JSON is valid
cat .claude/skills/skill-rules.json | jq .

# Should parse without errors
```

**Step 3.5: Test the skill activation**

1. Edit a file in your backend directory (e.g., `src/api/routes/users.ts`)
2. Ask Claude: "How should I structure a new controller?"
3. You should see: Claude mentions using the backend-dev-guidelines skill

✅ **Checkpoint:** Your first skill is auto-activating!

### Phase 4: Add Specialized Agents (5 minutes)

Agents are the easiest to add - just copy the `.md` file!

**Step 4.1: Choose relevant agents**
```bash
cd .claude/agents

# List available agents
ls /path/to/showcase/.claude/agents/

# Common useful ones:
# - code-architecture-reviewer.md
# - documentation-architect.md
# - frontend-error-fixer.md (if you have frontend)
# - web-research-specialist.md
```

**Step 4.2: Copy agents**
```bash
# Copy individual agents
cp /path/to/showcase/.claude/agents/code-architecture-reviewer.md .
cp /path/to/showcase/.claude/agents/documentation-architect.md .

# Or copy all agents
cp /path/to/showcase/.claude/agents/*.md .
```

**Step 4.3: Check for hardcoded paths** (optional but recommended)
```bash
# Check if any agent has hardcoded paths
grep -n "~/git/\|/root/\|/Users/" *.md

# If found, update to use $CLAUDE_PROJECT_DIR or relative paths
```

**Step 4.4: Use an agent**

Ask Claude:
```
"Use the code-architecture-reviewer agent to review my controllers"
```

Claude will invoke the agent autonomously and return a comprehensive review.

✅ **Checkpoint:** You can now use specialized agents!

### Phase 5: Optional - Add More Skills (As Needed)

Repeat Phase 3 for additional skills:
- `frontend-dev-guidelines` (if you have React/MUI)
- `route-tester` (if you have JWT auth)
- `error-tracking` (if you use Sentry)
- `skill-developer` (if you want to create custom skills)

### Phase 6: Optional - Add Slash Commands (5 minutes)

```bash
# Create commands directory
mkdir -p .claude/commands

# Copy useful commands
cp /path/to/showcase/.claude/commands/dev-docs.md \
   .claude/commands/

cp /path/to/showcase/.claude/commands/dev-docs-update.md \
   .claude/commands/
```

Update paths in the commands to match your project structure.

Use with: `/dev-docs` in Claude Code

### Verification Checklist

After setup, verify everything works:

```bash
# ✅ Hooks are executable
ls -la .claude/hooks/*.sh | grep rwx

# ✅ skill-rules.json is valid
cat .claude/skills/skill-rules.json | jq .

# ✅ Hook dependencies installed
ls .claude/hooks/node_modules/

# ✅ Skills are present
ls -la .claude/skills/

# ✅ Agents are present
ls -la .claude/agents/

# ✅ settings.json is valid
cat .claude/settings.json | jq .
```

**Manual test:**
1. Edit a file that should trigger a skill (e.g., backend file)
2. The skill should be suggested automatically
3. Ask Claude to use an agent
4. Agent should execute successfully

---

## Real-World Use Cases

### Use Case 1: Maintaining Consistent API Patterns

**Scenario:** You're building a multi-service Node.js application and want consistent patterns across all services.

**Setup:**
```bash
# Add backend skill
cp -r showcase/.claude/skills/backend-dev-guidelines .claude/skills/

# Configure for monorepo
# In skill-rules.json:
{
  "pathPatterns": [
    "services/*/src/**/*.ts",
    "packages/shared/**/*.ts"
  ]
}
```

**Result:**
- ✅ All developers (human or Claude) follow the same layered architecture
- ✅ BaseController pattern used consistently
- ✅ Error handling with Sentry automatic
- ✅ Validation with Zod standardized

### Use Case 2: React Frontend Development

**Scenario:** Building a React app with MUI and want to prevent common mistakes.

**Setup:**
```bash
# Add frontend skill as guardrail
cp -r showcase/.claude/skills/frontend-dev-guidelines .claude/skills/

# Configure as guardrail (enforcement: "block")
# This prevents MUI v6 patterns from being used
```

**Result:**
- ✅ Automatically uses MUI v7 Grid with `size={{}}` prop
- ✅ useSuspenseQuery pattern enforced
- ✅ Proper loading states and error boundaries
- ✅ Claude is blocked from using deprecated patterns

### Use Case 3: Testing Authenticated Endpoints

**Scenario:** You have JWT cookie authentication and need to test endpoints regularly.

**Setup:**
```bash
# Add route-tester skill
cp -r showcase/.claude/skills/route-tester .claude/skills/

# Add auth-route-tester agent
cp showcase/.claude/agents/auth-route-tester.md .claude/agents/
```

**Usage:**
```
You: "Test the /api/users/profile endpoint"

Claude: [Uses route-tester skill]
1. Generates test-auth-route.js script
2. Gets JWT token from login
3. Tests endpoint with authenticated cookie
4. Reports results
```

**Result:**
- ✅ Consistent testing approach
- ✅ Auth handling automatic
- ✅ Easy debugging of auth issues

### Use Case 4: Large Refactoring

**Scenario:** Need to reorganize your codebase structure.

**Setup:**
```bash
# Add refactoring agents
cp showcase/.claude/agents/refactor-planner.md .claude/agents/
cp showcase/.claude/agents/code-refactor-master.md .claude/agents/
```

**Usage:**
```
You: "Use refactor-planner to plan moving auth logic to a separate package"

Claude: [Invokes refactor-planner agent]
[Returns comprehensive plan with file moves, import updates, etc.]

You: "Use code-refactor-master to execute this plan"

Claude: [Invokes code-refactor-master agent]
[Autonomously executes the refactoring with verification]
```

**Result:**
- ✅ Complex refactoring handled autonomously
- ✅ Import paths updated automatically
- ✅ Verification that nothing broke

### Use Case 5: Documentation Generation

**Scenario:** Need to document a new feature before context reset.

**Setup:**
```bash
# Add dev docs command
cp showcase/.claude/commands/dev-docs.md .claude/commands/

# Add documentation agent
cp showcase/.claude/agents/documentation-architect.md .claude/agents/
```

**Usage:**
```
You: "/dev-docs user-authentication"

Claude: [Creates dev docs structure]
dev/active/user-authentication/
  ├── user-authentication-plan.md
  ├── user-authentication-context.md
  └── user-authentication-tasks.md

[Fills in current progress, key decisions, remaining tasks]

Later (after context reset):
You: "Continue working on user authentication"
Claude: [Reads dev docs, understands context immediately]
```

**Result:**
- ✅ Context preserved across resets
- ✅ Easy handoff between Claude sessions
- ✅ Clear task tracking

---

## Advanced Topics

### Creating Custom Skills for Your Tech Stack

**Scenario:** You use Django/Python instead of Express/Node.js

**Approach:**
1. Use `skill-developer` skill as meta-guidance
2. Copy `backend-dev-guidelines` structure
3. Replace Express patterns with Django patterns
4. Keep architecture concepts (layered architecture transfers)

**Example:**
```bash
# Copy as template
cp -r .claude/skills/backend-dev-guidelines \
      .claude/skills/django-dev-guidelines

# Edit SKILL.md
# Replace:
# - Express routes → Django views
# - Prisma → Django ORM
# - BaseController → Django CBV/FBV patterns

# Keep:
# - Layered architecture concept
# - Error handling philosophy
# - Testing strategies
# - File organization
```

### Adapting Skills for Different Frameworks

**Frontend Example: Vue instead of React**

```bash
# Copy as template
cp -r .claude/skills/frontend-dev-guidelines \
      .claude/skills/vue-dev-guidelines

# Replace in SKILL.md and resources:
# - React.FC → Vue defineComponent
# - useSuspenseQuery → Vue composables
# - MUI components → Vuetify/PrimeVue
# - React Router → Vue Router

# Keep:
# - File organization (features/ pattern)
# - Performance optimization strategies
# - TypeScript standards
# - Loading/error state patterns
```

### Advanced Hook Customization

**Creating a custom hook to enforce commit message format:**

```bash
# Create new hook
nano .claude/hooks/commit-message-enforcer.sh
```

```bash
#!/bin/bash
# Enforces conventional commit format

PROMPT=$1

# Check if prompt contains commit-related keywords
if echo "$PROMPT" | grep -qi "commit\|push"; then
  SUGGESTION="Remember to use conventional commit format:
    feat: New feature
    fix: Bug fix
    docs: Documentation
    refactor: Code refactoring
    test: Tests
    chore: Maintenance"
  
  echo "$SUGGESTION"
fi
```

Add to settings.json:
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/commit-message-enforcer.sh"
          }
        ]
      }
    ]
  }
}
```

### Skill Priority and Conflicts

**When multiple skills match:**

skill-rules.json supports priority:
```json
{
  "backend-dev-guidelines": {
    "priority": "high"
  },
  "error-tracking": {
    "priority": "medium"
  },
  "route-tester": {
    "priority": "low"
  }
}
```

Higher priority skills are suggested first.

### Guardrail Skills (Enforcement: "block")

**Preventing breaking changes:**

```json
{
  "frontend-dev-guidelines": {
    "type": "guardrail",
    "enforcement": "block",  // ← Blocks action if skill not used
    "priority": "high",
    "promptTriggers": {
      "keywords": ["MUI", "Grid", "DataGrid"]
    }
  }
}
```

**Use cases for guardrails:**
- Preventing deprecated API usage (MUI v6 → v7)
- Enforcing security patterns (SQL injection prevention)
- Ensuring critical validation (authentication checks)

### Monorepo Configuration

**For Nx monorepo:**
```json
{
  "backend-dev-guidelines": {
    "fileTriggers": {
      "pathPatterns": [
        "apps/api/src/**/*.ts",
        "libs/backend-utils/src/**/*.ts",
        "libs/data-access/src/**/*.ts"
      ]
    }
  },
  "frontend-dev-guidelines": {
    "fileTriggers": {
      "pathPatterns": [
        "apps/web/src/**/*.tsx",
        "libs/ui-components/src/**/*.tsx",
        "libs/features/src/**/*.tsx"
      ]
    }
  }
}
```

### Performance Considerations

**Hook execution time:**
- skill-activation-prompt: ~100-200ms (TypeScript analysis)
- post-tool-use-tracker: ~50ms (bash script)

**Optimization tips:**
- Keep skill-rules.json focused (don't match too broadly)
- Use specific pathPatterns (avoid `**/*` if possible)
- Limit number of active skills to 3-5

### Integration with CI/CD

**Example: Enforce skill usage in PR reviews**

```bash
# .github/workflows/skill-check.yml
name: Skill Compliance Check

on: [pull_request]

jobs:
  check-skills:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check for skill markers
        run: |
          # Check if backend changes include skill markers
          if git diff origin/main --name-only | grep "src/api/"; then
            if ! git log origin/main..HEAD | grep "backend-dev-guidelines"; then
              echo "⚠️ Backend changes should follow backend-dev-guidelines"
              exit 1
            fi
          fi
```

---

## Summary

### What You've Learned

1. **What this is:** A reference library of Claude Code infrastructure, not a service
2. **The problem:** Skills don't activate automatically in Claude Code
3. **The solution:** Hooks + skill-rules.json + modular skills + agents
4. **The impact:** Massive time savings and code quality improvements
5. **How to use it:** Copy components into your project, customize paths

### Quick Start Recap

**Minimum viable setup (15 minutes):**
1. Copy 2 essential hooks
2. Add 1 relevant skill
3. Configure skill-rules.json with your paths
4. Update settings.json

**You get:**
- ✅ Auto-activating skills
- ✅ Consistent code patterns
- ✅ Time savings on every task

### Next Steps

1. **Try it now:** Follow Phase 1-3 of the consumption guide
2. **Start simple:** One skill, two hooks, test it works
3. **Expand gradually:** Add agents and more skills as needed
4. **Customize:** Adapt skills for your tech stack
5. **Share:** Contribute your own skills/agents back to the community

### Getting Help

**Resources:**
- [Main README](README.md) - Overview and quick start
- [Claude Integration Guide](CLAUDE_INTEGRATION_GUIDE.md) - Detailed integration instructions
- [Skills Guide](.claude/skills/README.md) - All about skills
- [Hooks Guide](.claude/hooks/README.md) - Hook setup and customization
- [Agents Guide](.claude/agents/README.md) - Using agents effectively

**Community:**
- ⭐ Star this repo if you find it useful
- 🐛 Open issues for bugs or questions
- 💬 Share your custom skills/agents
- 📝 Contribute improvements

---

**Created by:** Real-world user after 6 months of production Claude Code use
**Shared because:** Hundreds of developers asked for this infrastructure
**License:** MIT - Use freely in your projects

**Now go make your Claude Code experience 10x better! 🚀**
