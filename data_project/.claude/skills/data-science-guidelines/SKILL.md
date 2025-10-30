# Data Science Development Guidelines

**Version:** 1.0.0  
**Type:** Domain Skill  
**Auto-Activation:** Yes (via skill-rules.json)

---

## Purpose

This skill provides production-tested patterns and best practices for data science and analytics projects, including:
- Data pipeline development
- ETL/ELT workflows
- Data quality validation
- Model development and deployment
- Reproducibility and version control
- Performance optimization

---

## Quick Reference

### When This Skill Activates

**File Triggers:**
- Working in `*.py` files in data/ML directories
- Editing Jupyter notebooks (`*.ipynb`)
- Working with pipeline configuration files
- Editing data schema definitions

**Prompt Triggers:**
- "data pipeline", "ETL", "data processing"
- "machine learning", "model", "training"
- "data validation", "data quality"
- "data transformation", "feature engineering"

---

## Core Principles

### 1. Reproducibility First
```python
# ✅ GOOD: Version everything
import pandas as pd
from pathlib import Path
import logging

# Version data with DVC or similar
# data/raw/users_v1.2.3.csv

# Pin dependencies in requirements.txt
# pandas==2.0.0
# scikit-learn==1.3.0

# Use random seeds
import random
import numpy as np

random.seed(42)
np.random.seed(42)
```

### 2. Modular Pipeline Design
```python
# ✅ GOOD: Separate concerns
class DataPipeline:
    """Modular, testable pipeline structure."""
    
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def extract(self) -> pd.DataFrame:
        """Extract data from source."""
        self.logger.info("Extracting data...")
        return pd.read_csv(self.config['input_path'])
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply transformations."""
        self.logger.info("Transforming data...")
        df = self._clean_data(df)
        df = self._engineer_features(df)
        return df
    
    def load(self, df: pd.DataFrame) -> None:
        """Load data to destination."""
        self.logger.info("Loading data...")
        df.to_parquet(self.config['output_path'])
    
    def run(self) -> None:
        """Execute full pipeline."""
        df = self.extract()
        df = self.transform(df)
        self.load(df)
```

### 3. Data Quality Validation
```python
# ✅ GOOD: Validate at every step
from typing import Optional
import pandera as pa

class UserDataSchema(pa.SchemaModel):
    """Schema for user data validation."""
    user_id: int = pa.Field(gt=0, unique=True)
    email: str = pa.Field(str_matches=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = pa.Field(ge=0, le=120)
    created_at: pd.Timestamp
    
    class Config:
        strict = True

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate data against schema."""
    try:
        validated_df = UserDataSchema.validate(df)
        return validated_df
    except pa.errors.SchemaError as e:
        logger.error(f"Data validation failed: {e}")
        raise
```

### 4. Proper Error Handling
```python
# ✅ GOOD: Comprehensive error handling
import sys
from typing import Union

class DataProcessingError(Exception):
    """Custom exception for data processing errors."""
    pass

def process_data_safely(input_path: str) -> Union[pd.DataFrame, None]:
    """Process data with proper error handling."""
    try:
        # Validate input exists
        if not Path(input_path).exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Load and validate
        df = pd.read_csv(input_path)
        df = validate_data(df)
        
        return df
        
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        return None
    except pa.errors.SchemaError as e:
        logger.error(f"Validation error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise DataProcessingError(f"Processing failed: {e}") from e
```

### 5. Configuration Management
```python
# ✅ GOOD: Centralized configuration
from dataclasses import dataclass
from pathlib import Path
import yaml

@dataclass
class PipelineConfig:
    """Configuration for data pipeline."""
    input_path: Path
    output_path: Path
    batch_size: int = 1000
    num_workers: int = 4
    log_level: str = "INFO"
    
    @classmethod
    def from_yaml(cls, config_path: str) -> 'PipelineConfig':
        """Load config from YAML file."""
        with open(config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls(**config_dict)

# config.yaml
"""
input_path: data/raw/users.csv
output_path: data/processed/users.parquet
batch_size: 1000
num_workers: 4
log_level: INFO
"""
```

---

## Project Structure

```
data_project/
├── data/
│   ├── raw/              # Original, immutable data
│   ├── interim/          # Intermediate processing
│   ├── processed/        # Final, analysis-ready data
│   └── external/         # External data sources
├── notebooks/
│   ├── exploratory/      # EDA notebooks
│   └── reports/          # Final analysis notebooks
├── src/
│   ├── pipelines/        # Data pipeline modules
│   ├── features/         # Feature engineering
│   ├── models/           # Model training/inference
│   ├── validation/       # Data quality checks
│   └── utils/            # Utility functions
├── tests/
│   ├── test_pipelines/
│   ├── test_features/
│   └── test_validation/
├── configs/
│   ├── pipeline_config.yaml
│   └── model_config.yaml
├── scripts/
│   ├── run_pipeline.py
│   └── train_model.py
├── requirements.txt
├── setup.py
└── README.md
```

---

## Essential Patterns

### Pattern 1: Pipeline with Logging
```python
import logging
from datetime import datetime
from pathlib import Path

def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """Setup logging configuration."""
    Path(log_dir).mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/pipeline_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)
```

### Pattern 2: Batch Processing
```python
from typing import Iterator, List
import numpy as np

def batch_processor(
    data: pd.DataFrame,
    batch_size: int = 1000
) -> Iterator[pd.DataFrame]:
    """Process data in batches for memory efficiency."""
    num_batches = int(np.ceil(len(data) / batch_size))
    
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, len(data))
        
        batch = data.iloc[start_idx:end_idx]
        yield batch

# Usage
for batch in batch_processor(large_df, batch_size=1000):
    processed_batch = transform_data(batch)
    save_batch(processed_batch)
```

### Pattern 3: Data Versioning
```python
from datetime import datetime
from pathlib import Path

class VersionedDataset:
    """Manage versioned datasets."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
    
    def save(self, df: pd.DataFrame, name: str, version: str = None) -> str:
        """Save dataset with version."""
        if version is None:
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        versioned_path = self.base_path / f"{name}_v{version}.parquet"
        df.to_parquet(versioned_path)
        
        # Also save as latest
        latest_path = self.base_path / f"{name}_latest.parquet"
        df.to_parquet(latest_path)
        
        return str(versioned_path)
    
    def load(self, name: str, version: str = "latest") -> pd.DataFrame:
        """Load specific version of dataset."""
        if version == "latest":
            path = self.base_path / f"{name}_latest.parquet"
        else:
            path = self.base_path / f"{name}_v{version}.parquet"
        
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")
        
        return pd.read_parquet(path)
```

---

## Testing Data Pipelines

### Unit Tests
```python
import pytest
import pandas as pd
from src.pipelines.etl import DataPipeline

@pytest.fixture
def sample_data():
    """Fixture providing sample data."""
    return pd.DataFrame({
        'user_id': [1, 2, 3],
        'email': ['a@test.com', 'b@test.com', 'c@test.com'],
        'age': [25, 30, 35]
    })

def test_data_extraction(sample_data):
    """Test data extraction."""
    pipeline = DataPipeline(config={'input_path': 'test_data.csv'})
    result = pipeline.extract()
    
    assert isinstance(result, pd.DataFrame)
    assert not result.empty

def test_data_transformation(sample_data):
    """Test data transformation."""
    pipeline = DataPipeline(config={})
    result = pipeline.transform(sample_data)
    
    assert len(result) == len(sample_data)
    assert 'email' in result.columns
```

### Integration Tests
```python
def test_full_pipeline():
    """Test complete pipeline execution."""
    config = {
        'input_path': 'tests/fixtures/test_input.csv',
        'output_path': 'tests/output/test_output.parquet'
    }
    
    pipeline = DataPipeline(config)
    pipeline.run()
    
    # Verify output exists and is valid
    output = pd.read_parquet(config['output_path'])
    assert not output.empty
    assert all(col in output.columns for col in ['user_id', 'email', 'age'])
```

---

## Performance Optimization

### 1. Use Efficient Data Types
```python
# ✅ GOOD: Optimize dtypes
def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame memory usage."""
    # Convert object columns to category if low cardinality
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype('category')
    
    # Downcast numeric types
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    return df
```

### 2. Parallel Processing
```python
from multiprocessing import Pool
from typing import Callable

def parallel_apply(
    df: pd.DataFrame,
    func: Callable,
    num_workers: int = 4
) -> pd.DataFrame:
    """Apply function in parallel."""
    chunks = np.array_split(df, num_workers)
    
    with Pool(num_workers) as pool:
        results = pool.map(func, chunks)
    
    return pd.concat(results, ignore_index=True)
```

---

## Resources

For detailed patterns, see the resources directory:
- `etl-patterns.md` - ETL pipeline patterns
- `data-validation.md` - Data quality checks
- `feature-engineering.md` - Feature creation patterns
- `model-patterns.md` - ML model patterns
- `testing-guidelines.md` - Testing data code
- `performance-optimization.md` - Performance tips

---

## Anti-Patterns to Avoid

### ❌ BAD: Hardcoded paths
```python
df = pd.read_csv('/Users/john/data/users.csv')  # Don't do this!
```

### ❌ BAD: No data validation
```python
df = pd.read_csv('data.csv')
df['age'] = df['age'] * 2  # What if age is null or negative?
```

### ❌ BAD: Loading entire dataset into memory
```python
df = pd.read_csv('10GB_file.csv')  # Will crash!
```

### ❌ BAD: No logging
```python
def process_data(df):
    # Silent failures are the worst!
    return df.dropna()
```

---

## Integration with Claude Code

This skill auto-activates when:
- Editing Python files in data/ML project directories
- Working with Jupyter notebooks
- Mentioning data pipeline, ETL, or ML keywords
- Creating data processing scripts

Use this skill to ensure your data pipelines are:
- ✅ Reproducible
- ✅ Testable
- ✅ Validated
- ✅ Performant
- ✅ Production-ready
