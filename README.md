# Claude Code Infrastructure Showcase

**A curated reference library of production-tested Claude Code infrastructure.**

Born from 6 months of real-world use managing a complex TypeScript microservices project, this showcase provides the patterns and systems that solved the "skills don't activate automatically" problem and scaled Claude Code for enterprise development.

> **This is NOT a working application** - it's a reference library. Copy what you need into your own projects.

> **📖 Documentation Guides:**
> - **[Quick Start Visual Guide](QUICK_START_VISUAL.md)** - One-page visual overview with diagrams (perfect for visual learners!)
> - **[Comprehensive Guide](COMPREHENSIVE_GUIDE.md)** - Complete understanding with step-by-step instructions (1000+ lines, covers everything!)
> - **[Implementation Guide](IMPLEMENTATION_GUIDE.md)** - Step-by-step guide to implement in YOUR repository
> - **[Automation Examples](AUTOMATION_EXAMPLES.md)** - Mermaid diagrams showing how automation works
> - **[Claude Integration Guide](CLAUDE_INTEGRATION_GUIDE.md)** - For AI-assisted setup (designed for Claude to read)

---

## What's Inside

**Production-tested infrastructure for:**
- ✅ **Auto-activating skills** via hooks
- ✅ **Modular skill pattern** (500-line rule with progressive disclosure)
- ✅ **Specialized agents** for complex tasks
- ✅ **Dev docs system** that survives context resets
- ✅ **Comprehensive examples** using generic blog domain
- ✅ **Data science example** showing automation for data projects

**Time investment to build:** 6 months of iteration
**Time to integrate into your project:** 15-30 minutes

---

## Quick Start - Pick Your Path

### 🤖 Using Claude Code to Integrate?

**Claude:** Read [`CLAUDE_INTEGRATION_GUIDE.md`](CLAUDE_INTEGRATION_GUIDE.md) for step-by-step integration instructions tailored for AI-assisted setup.

### 🎯 I want skill auto-activation

**The breakthrough feature:** Skills that actually activate when you need them.

**What you need:**
1. The skill-activation hooks (2 files)
2. A skill or two relevant to your work
3. 15 minutes

**👉 [Setup Guide: .claude/hooks/README.md](.claude/hooks/README.md)**

### 📚 I want to add ONE skill

Browse the [skills catalog](.claude/skills/) and copy what you need.

**Available:**
- **backend-dev-guidelines** - Node.js/Express/TypeScript patterns
- **frontend-dev-guidelines** - React/TypeScript/MUI v7 patterns
- **skill-developer** - Meta-skill for creating skills
- **route-tester** - Test authenticated API routes
- **error-tracking** - Sentry integration patterns

**👉 [Skills Guide: .claude/skills/README.md](.claude/skills/README.md)**

### 🤖 I want specialized agents

10 production-tested agents for complex tasks:
- Code architecture review
- Refactoring assistance
- Documentation generation
- Error debugging
- And more...

**👉 [Agents Guide: .claude/agents/README.md](.claude/agents/README.md)**

### 📊 I want to see data science automation

**Example project** showing automation for data engineering and ML:
- Data science best practices skill
- Data quality checker agent  
- Pipeline debugger agent
- Example ETL pipelines and validation

**👉 [Data Project Guide: data_project/DATA_PROJECT_GUIDE.md](data_project/DATA_PROJECT_GUIDE.md)**

---

## What Makes This Different?

### The Auto-Activation Breakthrough

**Problem:** Claude Code skills just sit there. You have to remember to use them.

**Solution:** UserPromptSubmit hook that:
- Analyzes your prompts
- Checks file context
- Automatically suggests relevant skills
- Works via `skill-rules.json` configuration

**Result:** Skills activate when you need them, not when you remember them.

### Production-Tested Patterns

These aren't theoretical examples - they're extracted from:
- ✅ 6 microservices in production
- ✅ 50,000+ lines of TypeScript
- ✅ React frontend with complex data grids
- ✅ Sophisticated workflow engine
- ✅ 6 months of daily Claude Code use

The patterns work because they solved real problems.

### Modular Skills (500-Line Rule)

Large skills hit context limits. The solution:

```
skill-name/
  SKILL.md                  # <500 lines, high-level guide
  resources/
    topic-1.md              # <500 lines each
    topic-2.md
    topic-3.md
```

**Progressive disclosure:** Claude loads main skill first, loads resources only when needed.

---

## Repository Structure

```
.claude/
├── skills/                 # 5 production skills
│   ├── backend-dev-guidelines/  (12 resource files)
│   ├── frontend-dev-guidelines/ (11 resource files)
│   ├── skill-developer/         (7 resource files)
│   ├── route-tester/
│   ├── error-tracking/
│   └── skill-rules.json    # Skill activation configuration
├── hooks/                  # 6 hooks for automation
│   ├── skill-activation-prompt.*  (ESSENTIAL)
│   ├── post-tool-use-tracker.sh   (ESSENTIAL)
│   ├── tsc-check.sh        (optional, needs customization)
│   └── trigger-build-resolver.sh  (optional)
├── agents/                 # 10 specialized agents
│   ├── code-architecture-reviewer.md
│   ├── refactor-planner.md
│   ├── frontend-error-fixer.md
│   └── ... 7 more
└── commands/               # 3 slash commands
    ├── dev-docs.md
    └── ...

dev/
└── active/                 # Dev docs pattern examples
    └── public-infrastructure-repo/

data_project/               # Data science automation example
├── .claude/
│   ├── skills/
│   │   └── data-science-guidelines/  # Data science best practices
│   └── agents/
│       ├── data-quality-checker.md   # Data validation agent
│       └── pipeline-debugger.md      # Pipeline debugging agent
├── src/
│   ├── pipelines/          # Example ETL pipelines
│   └── validation/         # Data validation examples
└── DATA_PROJECT_GUIDE.md   # Complete guide for data projects
```

---

## Component Catalog

### 🎨 Skills (5)

| Skill | Lines | Purpose | Best For |
|-------|-------|---------|----------|
| [**skill-developer**](.claude/skills/skill-developer/) | 426 | Creating and managing skills | Meta-development |
| [**backend-dev-guidelines**](.claude/skills/backend-dev-guidelines/) | 304 | Express/Prisma/Sentry patterns | Backend APIs |
| [**frontend-dev-guidelines**](.claude/skills/frontend-dev-guidelines/) | 398 | React/MUI v7/TypeScript | React frontends |
| [**route-tester**](.claude/skills/route-tester/) | 389 | Testing authenticated routes | API testing |
| [**error-tracking**](.claude/skills/error-tracking/) | ~250 | Sentry integration | Error monitoring |

**All skills follow the modular pattern** - main file + resource files for progressive disclosure.

**👉 [How to integrate skills →](.claude/skills/README.md)**

### 🪝 Hooks (6)

| Hook | Type | Essential? | Customization |
|------|------|-----------|---------------|
| skill-activation-prompt | UserPromptSubmit | ✅ YES | ✅ None needed |
| post-tool-use-tracker | PostToolUse | ✅ YES | ✅ None needed |
| tsc-check | Stop | ⚠️ Optional | ⚠️ Heavy - monorepo only |
| trigger-build-resolver | Stop | ⚠️ Optional | ⚠️ Heavy - monorepo only |
| error-handling-reminder | Stop | ⚠️ Optional | ⚠️ Moderate |
| stop-build-check-enhanced | Stop | ⚠️ Optional | ⚠️ Moderate |

**Start with the two essential hooks** - they enable skill auto-activation and work out of the box.

**👉 [Hook setup guide →](.claude/hooks/README.md)**

### 🤖 Agents (10)

**Standalone - just copy and use!**

| Agent | Purpose |
|-------|---------|
| code-architecture-reviewer | Review code for architectural consistency |
| code-refactor-master | Plan and execute refactoring |
| documentation-architect | Generate comprehensive documentation |
| frontend-error-fixer | Debug frontend errors |
| plan-reviewer | Review development plans |
| refactor-planner | Create refactoring strategies |
| web-research-specialist | Research technical issues online |
| auth-route-tester | Test authenticated endpoints |
| auth-route-debugger | Debug auth issues |
| auto-error-resolver | Auto-fix TypeScript errors |

**👉 [How agents work →](.claude/agents/README.md)**

### 💬 Slash Commands (3)

| Command | Purpose |
|---------|---------|
| /dev-docs | Create structured dev documentation |
| /dev-docs-update | Update docs before context reset |
| /route-research-for-testing | Research route patterns for testing |

---

## Key Concepts

### Hooks + skill-rules.json = Auto-Activation

**The system:**
1. **skill-activation-prompt hook** runs on every user prompt
2. Checks **skill-rules.json** for trigger patterns
3. Suggests relevant skills automatically
4. Skills load only when needed

**This solves the #1 problem** with Claude Code skills: they don't activate on their own.

### Progressive Disclosure (500-Line Rule)

**Problem:** Large skills hit context limits

**Solution:** Modular structure
- Main SKILL.md <500 lines (overview + navigation)
- Resource files <500 lines each (deep dives)
- Claude loads incrementally as needed

**Example:** backend-dev-guidelines has 12 resource files covering routing, controllers, services, repositories, testing, etc.

### Dev Docs Pattern

**Problem:** Context resets lose project context

**Solution:** Three-file structure
- `[task]-plan.md` - Strategic plan
- `[task]-context.md` - Key decisions and files
- `[task]-tasks.md` - Checklist format

**Works with:** `/dev-docs` slash command to generate these automatically

---

## ⚠️ Important: What Won't Work As-Is

### settings.json
The included `settings.json` is an **example only**:
- Stop hooks reference specific monorepo structure
- Service names (blog-api, etc.) are examples
- MCP servers may not exist in your setup

**To use it:**
1. Extract ONLY UserPromptSubmit and PostToolUse hooks
2. Customize or skip Stop hooks
3. Update MCP server list for your setup

### Blog Domain Examples
Skills use generic blog examples (Post/Comment/User):
- These are **teaching examples**, not requirements
- Patterns work for any domain (e-commerce, SaaS, etc.)
- Adapt the patterns to your business logic

### Hook Directory Structures
Some hooks expect specific structures:
- `tsc-check.sh` expects service directories
- Customize based on YOUR project layout

---

## Integration Workflow

**Recommended approach:**

### Phase 1: Skill Activation (15 min)
1. Copy skill-activation-prompt hook
2. Copy post-tool-use-tracker hook
3. Update settings.json
4. Install hook dependencies

### Phase 2: Add First Skill (10 min)
1. Pick ONE relevant skill
2. Copy skill directory
3. Create/update skill-rules.json
4. Customize path patterns

### Phase 3: Test & Iterate (5 min)
1. Edit a file - skill should activate
2. Ask a question - skill should be suggested
3. Add more skills as needed

### Phase 4: Optional Enhancements
- Add agents you find useful
- Add slash commands
- Customize Stop hooks (advanced)

---

## Getting Help

### For Users
**Issues with integration?**
1. Check [CLAUDE_INTEGRATION_GUIDE.md](CLAUDE_INTEGRATION_GUIDE.md)
2. Ask Claude: "Why isn't [skill] activating?"
3. Open an issue with your project structure

### For Claude Code
When helping users integrate:
1. **Read CLAUDE_INTEGRATION_GUIDE.md FIRST**
2. Ask about their project structure
3. Customize, don't blindly copy
4. Verify after integration

---

## What This Solves

### Before This Infrastructure

❌ Skills don't activate automatically
❌ Have to remember which skill to use
❌ Large skills hit context limits
❌ Context resets lose project knowledge
❌ No consistency across development
❌ Manual agent invocation every time

### After This Infrastructure

✅ Skills suggest themselves based on context
✅ Hooks trigger skills at the right time
✅ Modular skills stay under context limits
✅ Dev docs preserve knowledge across resets
✅ Consistent patterns via guardrails
✅ Agents streamline complex tasks

---

## Community

**Found this useful?**

- ⭐ Star this repo
- 🐛 Report issues or suggest improvements
- 💬 Share your own skills/hooks/agents
- 📝 Contribute examples from your domain

**Background:**
This infrastructure was detailed in the viral Reddit post ["Claude Code is a Beast - Part 2"](https://www.reddit.com/r/ClaudeAI/comments/1gc4xme/claude_code_is_a_beast_part_2_the_secret_to/). After hundreds of requests, this showcase was created to help the community implement these patterns.

---

## License

MIT License - Use freely in your projects, commercial or personal.

---

## Quick Links

**📖 Documentation:**
- **[Quick Start Visual](QUICK_START_VISUAL.md)** - One-page visual guide (perfect for visual learners!)
- **[Comprehensive Guide](COMPREHENSIVE_GUIDE.md)** - Complete understanding (1000+ lines, everything explained!)
- **[Implementation Guide](IMPLEMENTATION_GUIDE.md)** - Implement in YOUR repository (step-by-step)
- **[Automation Examples](AUTOMATION_EXAMPLES.md)** - Mermaid diagrams showing automation flow
- **[Claude Integration Guide](CLAUDE_INTEGRATION_GUIDE.md)** - For AI-assisted setup
- **[Data Project Guide](data_project/DATA_PROJECT_GUIDE.md)** - Automation for data science/analytics workflows

**📂 Component Guides:**
- 🎨 [Skills Documentation](.claude/skills/README.md)
- 🪝 [Hooks Setup](.claude/hooks/README.md)
- 🤖 [Agents Guide](.claude/agents/README.md)
- 📝 [Dev Docs Pattern](dev/README.md)

**⚡ Quick Start Paths:**
1. **Visual learner?** → Read [Quick Start Visual](QUICK_START_VISUAL.md)
2. **Want deep understanding?** → Read [Comprehensive Guide](COMPREHENSIVE_GUIDE.md)
3. **Ready to implement in your repo?** → Follow [Implementation Guide](IMPLEMENTATION_GUIDE.md)
4. **See automation examples?** → View [Automation Examples](AUTOMATION_EXAMPLES.md) with mermaid diagrams
5. **Just want to try?** → Copy the two essential hooks + one skill (15 min)
