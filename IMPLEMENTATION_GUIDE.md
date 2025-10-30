# Implementing Claude Code Automation in Your Repository

This guide shows you how to implement the auto-activation system from this showcase into another repository that currently has no automations.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step-by-Step Implementation](#step-by-step-implementation)
3. [Tech Stack Adaptation](#tech-stack-adaptation)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

**Before you start:**

- ✅ You have Claude Code installed and working
- ✅ You have cloned this showcase repository
- ✅ You have access to the target repository where you want to add automation
- ✅ You have ~30 minutes for setup

**Clone this showcase repo if you haven't:**
```bash
git clone https://github.com/vikrora14/claude-code-infrastructure-showcase.git
cd claude-code-infrastructure-showcase
```

---

## Step-by-Step Implementation

### Step 1: Prepare Your Target Repository

Navigate to the repository where you want to add automations:

```bash
cd /path/to/your-target-repository

# Create the .claude directory structure
mkdir -p .claude/hooks
mkdir -p .claude/skills
mkdir -p .claude/agents
mkdir -p .claude/commands
```

### Step 2: Copy Essential Hooks

These two hooks enable the auto-activation magic:

```bash
# Set paths (adjust these to your actual paths)
SHOWCASE_PATH="/path/to/claude-code-infrastructure-showcase"
TARGET_PATH="/path/to/your-target-repository"

# Copy skill-activation-prompt hook (TypeScript version)
cp "$SHOWCASE_PATH/.claude/hooks/skill-activation-prompt.sh" \
   "$TARGET_PATH/.claude/hooks/"

cp "$SHOWCASE_PATH/.claude/hooks/skill-activation-prompt.ts" \
   "$TARGET_PATH/.claude/hooks/"

# Copy post-tool-use-tracker hook
cp "$SHOWCASE_PATH/.claude/hooks/post-tool-use-tracker.sh" \
   "$TARGET_PATH/.claude/hooks/"

# Make them executable
chmod +x "$TARGET_PATH/.claude/hooks/"*.sh

# Verify they're executable
ls -la "$TARGET_PATH/.claude/hooks/"*.sh
# Should show: -rwxr-xr-x
```

### Step 3: Install Hook Dependencies

The TypeScript hook needs Node.js packages:

```bash
cd "$TARGET_PATH/.claude/hooks"

# Copy package.json if it exists in showcase
if [ -f "$SHOWCASE_PATH/.claude/hooks/package.json" ]; then
    cp "$SHOWCASE_PATH/.claude/hooks/package.json" .
    npm install
else
    # Create minimal package.json
    cat > package.json << 'EOF'
{
  "name": "claude-hooks",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
EOF
    npm install
fi

cd "$TARGET_PATH"
```

### Step 4: Create or Update settings.json

```bash
cd "$TARGET_PATH"

# Check if settings.json exists
if [ -f ".claude/settings.json" ]; then
    echo "settings.json exists - you'll need to merge manually"
    echo "See the configuration below"
else
    # Create new settings.json
    cat > .claude/settings.json << 'EOF'
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
EOF
    echo "Created .claude/settings.json"
fi
```

**If settings.json already exists**, add these sections manually:

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

### Step 5: Copy Your First Skill

Choose a skill based on your tech stack:

**Option A: Node.js/Express Backend**
```bash
cp -r "$SHOWCASE_PATH/.claude/skills/backend-dev-guidelines" \
      "$TARGET_PATH/.claude/skills/"
```

**Option B: React Frontend**
```bash
cp -r "$SHOWCASE_PATH/.claude/skills/frontend-dev-guidelines" \
      "$TARGET_PATH/.claude/skills/"
```

**Option C: Both**
```bash
cp -r "$SHOWCASE_PATH/.claude/skills/backend-dev-guidelines" \
      "$TARGET_PATH/.claude/skills/"
cp -r "$SHOWCASE_PATH/.claude/skills/frontend-dev-guidelines" \
      "$TARGET_PATH/.claude/skills/"
```

**Option D: Universal Meta-Skill**
```bash
cp -r "$SHOWCASE_PATH/.claude/skills/skill-developer" \
      "$TARGET_PATH/.claude/skills/"
```

### Step 6: Create skill-rules.json

This is the **most important** step - it tells the hooks when to activate skills.

```bash
cd "$TARGET_PATH/.claude/skills"

# Copy the template
cp "$SHOWCASE_PATH/.claude/skills/skill-rules.json" .

# Now edit it to match YOUR project structure
nano skill-rules.json
```

**CRITICAL: Update the pathPatterns to match YOUR project!**

Here's an example configuration. **You MUST customize this:**

```json
{
  "backend-dev-guidelines": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "promptTriggers": {
      "keywords": [
        "backend", "API", "route", "endpoint", "controller", 
        "service", "repository", "database", "Prisma", "Express"
      ],
      "intentPatterns": [
        "creat(e|ing) .* (route|endpoint|controller|service)",
        "implement .* API",
        "add .* (authentication|validation|error handling)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "YOUR_BACKEND_PATH/**/*.ts",
        "YOUR_API_PATH/**/*.ts"
      ],
      "contentPatterns": [
        "import.*prisma",
        "import.*express",
        "extends BaseController"
      ]
    }
  },
  "frontend-dev-guidelines": {
    "type": "guardrail",
    "enforcement": "block",
    "priority": "high",
    "promptTriggers": {
      "keywords": [
        "React", "component", "MUI", "DataGrid", "frontend",
        "UI", "form", "validation", "routing"
      ],
      "intentPatterns": [
        "creat(e|ing) .* component",
        "build .* (form|page|view)",
        "add .* (grid|table|list)"
      ]
    },
    "fileTriggers": {
      "pathPatterns": [
        "YOUR_FRONTEND_PATH/**/*.tsx",
        "YOUR_COMPONENTS_PATH/**/*.tsx"
      ],
      "contentPatterns": [
        "import.*@mui",
        "import.*react",
        "useSuspenseQuery"
      ]
    }
  }
}
```

**Common path patterns by project structure:**

**Single Application:**
```json
{
  "pathPatterns": [
    "src/**/*.ts",           // All TypeScript files in src
    "src/api/**/*.ts",       // Backend in src/api
    "src/components/**/*.tsx" // Frontend components
  ]
}
```

**Monorepo with packages:**
```json
{
  "pathPatterns": [
    "packages/*/src/**/*.ts",
    "packages/backend/src/**/*.ts",
    "packages/frontend/src/**/*.tsx"
  ]
}
```

**Monorepo with apps:**
```json
{
  "pathPatterns": [
    "apps/api/src/**/*.ts",
    "apps/web/src/**/*.tsx",
    "libs/*/src/**/*.ts"
  ]
}
```

**Separate backend/frontend directories:**
```json
{
  "pathPatterns": [
    "backend/src/**/*.ts",
    "frontend/src/**/*.tsx"
  ]
}
```

### Step 7: Analyze YOUR Project Structure

Before finalizing skill-rules.json, analyze your project:

```bash
cd "$TARGET_PATH"

# Show directory structure
tree -L 3 -d -I 'node_modules|dist|build'

# Or if tree is not installed:
find . -type d -not -path '*/node_modules/*' -not -path '*/dist/*' \
  -not -path '*/.git/*' | head -30

# Find TypeScript files
find . -name "*.ts" -not -path '*/node_modules/*' | head -10

# Find React files
find . -name "*.tsx" -not -path '*/node_modules/*' | head -10
```

Use this information to set the correct pathPatterns in skill-rules.json.

### Step 8: Validate Configuration

```bash
cd "$TARGET_PATH"

# Validate skill-rules.json is valid JSON
cat .claude/skills/skill-rules.json | jq .
# Should output formatted JSON without errors

# Validate settings.json is valid JSON
cat .claude/settings.json | jq .
# Should output formatted JSON without errors

# Check hooks are executable
ls -la .claude/hooks/*.sh | grep rwx
# Should show -rwxr-xr-x for all .sh files

# Check hook dependencies installed
ls .claude/hooks/node_modules/
# Should show typescript and other packages
```

### Step 9: Test the Automation

**Test 1: File Trigger**
```bash
cd "$TARGET_PATH"

# Edit a file that should trigger a skill
# Example: If you have backend-dev-guidelines with path "src/api/**/*.ts"
# Open a file like: src/api/routes/users.ts

# The hook should detect this and suggest the skill
```

**Test 2: Prompt Trigger**

Ask Claude Code:
```
"How do I create a new API endpoint?"
```

You should see Claude mention using the backend-dev-guidelines skill.

**Test 3: Check Hook Output**

```bash
# Manually run the hook to test
cd "$TARGET_PATH"
./.claude/hooks/skill-activation-prompt.sh

# Should run without errors
```

### Step 10: Add More Components (Optional)

**Add useful agents:**
```bash
# Copy all agents (they work standalone)
cp "$SHOWCASE_PATH/.claude/agents/"*.md "$TARGET_PATH/.claude/agents/"

# Or copy specific ones
cp "$SHOWCASE_PATH/.claude/agents/code-architecture-reviewer.md" \
   "$TARGET_PATH/.claude/agents/"
cp "$SHOWCASE_PATH/.claude/agents/documentation-architect.md" \
   "$TARGET_PATH/.claude/agents/"
```

**Add more skills:**
```bash
# Add route-tester if you have JWT auth
cp -r "$SHOWCASE_PATH/.claude/skills/route-tester" \
      "$TARGET_PATH/.claude/skills/"

# Add error-tracking if you use Sentry
cp -r "$SHOWCASE_PATH/.claude/skills/error-tracking" \
      "$TARGET_PATH/.claude/skills/"

# Add skill-developer (useful for creating custom skills)
cp -r "$SHOWCASE_PATH/.claude/skills/skill-developer" \
      "$TARGET_PATH/.claude/skills/"
```

Remember to add entries for new skills in skill-rules.json!

### Step 11: Commit to Repository

```bash
cd "$TARGET_PATH"

# Add .claude directory to git
git add .claude/

# Commit
git commit -m "Add Claude Code auto-activation infrastructure

- Essential hooks for skill auto-activation
- backend-dev-guidelines skill
- frontend-dev-guidelines skill
- skill-rules.json configured for project structure
- settings.json with hook configurations"

# Push
git push
```

---

## Tech Stack Adaptation

### If Your Stack Differs from the Examples

The showcase uses **Node.js/Express** and **React/MUI**. Here's how to adapt for other stacks:

#### Python/Django Backend

1. Copy backend-dev-guidelines as a template:
```bash
cp -r "$SHOWCASE_PATH/.claude/skills/backend-dev-guidelines" \
      "$TARGET_PATH/.claude/skills/django-dev-guidelines"
```

2. Edit the skill files to replace:
   - Express routes → Django views
   - Prisma → Django ORM
   - BaseController → Django CBV/FBV patterns
   - Keep: Layered architecture concept, error handling philosophy

3. Update skill-rules.json:
```json
{
  "django-dev-guidelines": {
    "fileTriggers": {
      "pathPatterns": [
        "**/views.py",
        "**/models.py",
        "**/serializers.py",
        "apps/**/*.py"
      ],
      "contentPatterns": [
        "from django",
        "class.*View",
        "def.*view"
      ]
    }
  }
}
```

#### Vue.js Frontend

1. Copy frontend-dev-guidelines as a template:
```bash
cp -r "$SHOWCASE_PATH/.claude/skills/frontend-dev-guidelines" \
      "$TARGET_PATH/.claude/skills/vue-dev-guidelines"
```

2. Edit to replace:
   - React → Vue
   - MUI → Vuetify/PrimeVue
   - useSuspenseQuery → Vue composables
   - Keep: File organization, performance patterns

3. Update skill-rules.json:
```json
{
  "vue-dev-guidelines": {
    "fileTriggers": {
      "pathPatterns": [
        "src/**/*.vue",
        "src/components/**/*.vue"
      ],
      "contentPatterns": [
        "import.*vue",
        "defineComponent",
        "setup\\("
      ]
    }
  }
}
```

#### Go Backend

1. Create custom skill based on backend-dev-guidelines structure:
```bash
mkdir -p "$TARGET_PATH/.claude/skills/go-dev-guidelines"
mkdir -p "$TARGET_PATH/.claude/skills/go-dev-guidelines/resources"
```

2. Create SKILL.md with Go patterns:
   - HTTP handler patterns
   - Middleware
   - Error handling
   - Database access (GORM/sqlx)

3. Update skill-rules.json:
```json
{
  "go-dev-guidelines": {
    "fileTriggers": {
      "pathPatterns": [
        "**/*.go",
        "cmd/**/*.go",
        "internal/**/*.go"
      ],
      "contentPatterns": [
        "func.*Handler",
        "http\\.Handler",
        "gin\\."
      ]
    }
  }
}
```

---

## Verification

### Checklist

After implementation, verify:

- [ ] `.claude/hooks/` directory exists with executable .sh files
- [ ] `.claude/skills/` directory contains at least one skill
- [ ] `.claude/skills/skill-rules.json` exists with YOUR paths
- [ ] `.claude/settings.json` configured with hooks
- [ ] Hook dependencies installed (`node_modules/` in hooks directory)
- [ ] Hooks are executable (`ls -la .claude/hooks/*.sh` shows `rwx`)
- [ ] skill-rules.json is valid JSON (`cat .claude/skills/skill-rules.json | jq .`)
- [ ] settings.json is valid JSON (`cat .claude/settings.json | jq .`)
- [ ] Editing a relevant file triggers skill suggestion
- [ ] Asking about the skill topic triggers suggestion

### Manual Testing

**Test the hook directly:**
```bash
cd /path/to/your-target-repository

# Test skill-activation-prompt hook
./.claude/hooks/skill-activation-prompt.sh
echo $?
# Should exit with 0 (success)

# Test post-tool-use-tracker hook
./.claude/hooks/post-tool-use-tracker.sh
echo $?
# Should exit with 0 (success)
```

**Test with Claude:**

1. Open a file that should trigger a skill (e.g., backend TypeScript file)
2. Ask: "How should I structure a new API endpoint?"
3. Claude should mention the skill automatically
4. If not, check troubleshooting below

---

## Troubleshooting

### Skills Not Activating

**Problem:** Skills don't suggest automatically

**Solutions:**

1. **Check hook execution:**
```bash
# Test hook manually
./.claude/hooks/skill-activation-prompt.sh

# Check for errors in output
```

2. **Verify pathPatterns match:**
```bash
# Find your actual file paths
find . -name "*.ts" -not -path '*/node_modules/*' | head -10

# Make sure these paths match patterns in skill-rules.json
```

3. **Check hooks are executable:**
```bash
ls -la .claude/hooks/*.sh
# Must show: -rwxr-xr-x

# If not:
chmod +x .claude/hooks/*.sh
```

4. **Validate JSON files:**
```bash
# Test skill-rules.json
cat .claude/skills/skill-rules.json | jq .

# Test settings.json
cat .claude/settings.json | jq .

# Both should parse without errors
```

5. **Check Claude Code recognizes settings:**
   - Restart Claude Code
   - Ensure you're working in the project root
   - Check Claude Code output for hook errors

### Hook Dependency Errors

**Problem:** TypeScript errors when running hook

**Solution:**
```bash
cd .claude/hooks

# Install dependencies
npm install

# If package.json missing, check Step 3 above
```

### Path Pattern Not Matching

**Problem:** File edits don't trigger skills

**Debug:**
```bash
# Find where your files actually are
find . -type f -name "*.ts" -o -name "*.tsx" | grep -v node_modules | head -20

# Update skill-rules.json pathPatterns to match these actual paths
```

**Example fix:**

If your backend is in `server/src/` but skill-rules.json has `api/**/*.ts`:

```json
{
  "pathPatterns": [
    "server/src/**/*.ts"  // Update to actual path
  ]
}
```

### Hook Runs But Doesn't Inject

**Problem:** Hook executes but skill doesn't appear

**Check:**

1. Make sure skill directory exists:
```bash
ls -la .claude/skills/backend-dev-guidelines/
```

2. Check skill has SKILL.md file:
```bash
cat .claude/skills/backend-dev-guidelines/SKILL.md | head -20
```

3. Verify skill name matches in skill-rules.json:
```json
{
  "backend-dev-guidelines": {  // Must match directory name
    // ...
  }
}
```

---

## Summary

You've now implemented the auto-activation system in your repository! 

**What you have:**
- ✅ Hooks that automatically detect context
- ✅ Skills that activate based on files and prompts
- ✅ Configuration tailored to your project structure
- ✅ Optional agents for complex tasks

**Next steps:**
1. Use the system daily and observe skill activations
2. Add more skills as you identify patterns
3. Create custom skills for your specific domain
4. Share skills with your team

**Remember:**
- Skills auto-activate based on skill-rules.json
- Update pathPatterns when your project structure changes
- Add new skills incrementally (don't add all at once)
- Use enforcement: "suggest" for guidance, "block" for guardrails

---

## Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Review COMPREHENSIVE_GUIDE.md in the showcase repo
3. Read CLAUDE_INTEGRATION_GUIDE.md for Claude-specific help
4. Open an issue in the showcase repository

**The automation is now working in your repository! 🎉**
