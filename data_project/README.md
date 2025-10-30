# Data Project - Efficiency and Automation Example

**Demonstrating Claude Code automation for data science and analytics workflows.**

---

## What's This?

This directory shows how to apply the automation patterns from the Claude Code Infrastructure Showcase to **data engineering and data science projects**.

Instead of the blog domain examples (Post/Comment/User), this focuses on:
- 📊 Data pipelines and ETL workflows
- 🔍 Data quality validation
- 🤖 ML model development
- 📈 Analytics and reporting
- ⚡ Performance optimization

---

## Quick Start

### 1. View the Example

```bash
# Explore the structure
tree data_project/

# Read the comprehensive guide
cat DATA_PROJECT_GUIDE.md

# Check out the sample pipeline
cat src/pipelines/etl_pipeline.py

# View the data validation example
cat src/validation/data_validator.py
```

### 2. Copy to Your Project

```bash
# Copy automation infrastructure
cp -r data_project/.claude /path/to/your/data/project/

# Update paths in skill-rules.json to match your structure
nano /path/to/your/data/project/.claude/skills/skill-rules.json
```

### 3. Test It

```bash
# In your project, ask Claude:
"Create a data pipeline for customer analytics"

# The data-science-guidelines skill will auto-activate
# You'll get production-ready pipeline code with:
# ✅ Modular design
# ✅ Logging
# ✅ Validation
# ✅ Error handling
# ✅ Configuration management
```

---

## What's Included

### 🎨 Skills

- **data-science-guidelines** - Comprehensive data science best practices
  - ETL patterns
  - Data validation
  - Feature engineering
  - Performance optimization
  - Testing guidelines

### 🤖 Agents

- **data-quality-checker** - Validates data, checks quality, generates reports
- **pipeline-debugger** - Debugs failed pipelines, identifies bottlenecks

### 📝 Example Code

- **etl_pipeline.py** - Production-ready ETL pipeline with best practices
- **data_validator.py** - Data validation using Pandera schemas

### ⚙️ Configuration

- **skill-rules.json** - Auto-activation rules for data projects
- Pre-configured for Python, Jupyter notebooks, data directories

---

## Key Features

### Auto-Activation

**File triggers:**
- `data_project/**/*.py`
- `notebooks/**/*.ipynb`
- Pipeline and validation scripts

**Keyword triggers:**
- "data pipeline", "ETL", "machine learning"
- "data validation", "feature engineering"
- "model training", "data processing"

**Code pattern triggers:**
- `import pandas`, `import numpy`
- `class.*Pipeline`, `def.*transform`
- `from sklearn`, `pd.DataFrame`

### Specialized Agents

**Data Quality Checker:**
```
@data-quality-checker Validate customer_data.csv against schema
```

**Pipeline Debugger:**
```
@pipeline-debugger ETL is running out of memory, need optimization
```

---

## Benefits

### Time Savings

| Task | Before | After | Saved |
|------|--------|-------|-------|
| Create ETL | 2-3 hrs | 15 min | 90% |
| Validate data | 30 min | 2 min | 93% |
| Debug pipeline | 1-2 hrs | 15 min | 87% |
| Add logging | 20 min | Auto | 100% |

**Total:** 10-15 hours saved per week

### Quality Improvements

- ✅ Consistent patterns across all pipelines
- ✅ Production-ready code from the start
- ✅ Comprehensive error handling
- ✅ Built-in validation and logging
- ✅ Optimized performance

---

## Documentation

📖 **[DATA_PROJECT_GUIDE.md](DATA_PROJECT_GUIDE.md)** - Complete implementation guide

Covers:
- Getting started
- Automation features in detail
- Best practices demonstrated
- Common workflows
- Integration guide
- Troubleshooting

---

## Example Workflow

**Before automation:**
```
1. Write ETL code from scratch
2. Realize you forgot logging
3. Add validation after bugs appear
4. Refactor for better error handling
5. Add configuration management
6. Debug for 2 hours
```
**Time:** 3-4 hours, inconsistent quality

**With automation:**
```
1. Ask: "Create ETL pipeline for users"
2. Get production-ready code instantly
3. Run and verify
```
**Time:** 15 minutes, consistent quality

---

## Integration Steps

### For Your Existing Data Project

1. **Copy automation:**
   ```bash
   cp -r data_project/.claude /your/project/
   ```

2. **Update paths** in `.claude/skills/skill-rules.json`

3. **Test:**
   - Edit a Python file
   - Ask about data pipelines
   - Skill should auto-activate

4. **Customize:**
   - Add your specific patterns
   - Create custom agents
   - Share with team

---

## Stack Support

**Languages:** Python (primary example)
**Libraries:** pandas, numpy, scikit-learn, pandera
**Tools:** Jupyter, pytest, logging

**Adaptable to:**
- R (tidyverse, dplyr)
- Scala (Spark)
- SQL (dbt, Airflow)
- Any data stack

Just update skill-rules.json patterns!

---

## Learn More

- **[Main README](../README.md)** - About the infrastructure showcase
- **[IMPLEMENTATION_GUIDE](../IMPLEMENTATION_GUIDE.md)** - How to implement in your repo
- **[AUTOMATION_EXAMPLES](../AUTOMATION_EXAMPLES.md)** - Visual diagrams of automation flow
- **[COMPREHENSIVE_GUIDE](../COMPREHENSIVE_GUIDE.md)** - Deep dive into all features

---

## Questions?

**"How do I adapt this for my stack?"**
→ See DATA_PROJECT_GUIDE.md section "Integration with Existing Projects"

**"Can I use this with Spark/Airflow/dbt?"**
→ Yes! The patterns apply to any data stack. Update file patterns in skill-rules.json.

**"How do I create custom agents?"**
→ See examples in `.claude/agents/` and follow the same structure.

**"Skills not activating?"**
→ Check DATA_PROJECT_GUIDE.md "Troubleshooting" section

---

## License

MIT - Use freely in your data projects!

---

**Transform your data engineering workflow with automation. Start building efficient, production-ready pipelines today!** 🚀
