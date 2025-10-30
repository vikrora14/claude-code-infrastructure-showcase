"""
Tests for ETL pipeline.

Demonstrates testing best practices for data pipelines.
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pipelines.etl_pipeline import UserDataPipeline, PipelineConfig


@pytest.fixture
def sample_csv(tmp_path):
    """Create sample CSV file for testing."""
    data = """user_id,email,age
1,user1@example.com,25
2,user2@example.com,30
3,user3@example.com,35
1,duplicate@example.com,40
4,user4@example.com,
"""
    csv_path = tmp_path / "test_input.csv"
    csv_path.write_text(data)
    return csv_path


@pytest.fixture
def pipeline_config(sample_csv, tmp_path):
    """Create pipeline configuration."""
    return PipelineConfig(
        input_path=sample_csv,
        output_path=tmp_path / "output.parquet",
        log_level="INFO"
    )


@pytest.fixture
def pipeline(pipeline_config):
    """Create pipeline instance."""
    return UserDataPipeline(pipeline_config)


class TestDataExtraction:
    """Test data extraction stage."""
    
    def test_extract_reads_csv(self, pipeline):
        """Test that extract reads CSV correctly."""
        df = pipeline.extract()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'user_id' in df.columns
        assert 'email' in df.columns
        assert 'age' in df.columns
    
    def test_extract_raises_on_missing_file(self, tmp_path):
        """Test that extract raises error if file doesn't exist."""
        config = PipelineConfig(
            input_path=tmp_path / "nonexistent.csv",
            output_path=tmp_path / "output.parquet"
        )
        pipeline = UserDataPipeline(config)
        
        with pytest.raises(FileNotFoundError):
            pipeline.extract()


class TestDataTransformation:
    """Test data transformation stage."""
    
    def test_transform_removes_duplicates(self, pipeline):
        """Test that duplicates are removed."""
        df = pipeline.extract()
        initial_len = len(df)
        
        df = pipeline.transform(df)
        
        # Should have fewer rows after removing duplicates
        assert len(df) < initial_len
        # Should have no duplicate user_ids
        assert df['user_id'].duplicated().sum() == 0
    
    def test_transform_handles_missing_values(self, pipeline):
        """Test that missing values are handled."""
        df = pipeline.extract()
        df = pipeline.transform(df)
        
        # Required fields should have no nulls
        assert df['user_id'].isnull().sum() == 0
        assert df['email'].isnull().sum() == 0
        # Age nulls should be filled with median
        assert df['age'].isnull().sum() == 0
    
    def test_transform_creates_age_groups(self, pipeline):
        """Test that age groups are created."""
        df = pipeline.extract()
        df = pipeline.transform(df)
        
        assert 'age_group' in df.columns
        # Should have valid age group values
        valid_groups = ['<18', '18-30', '30-50', '50+']
        assert all(df['age_group'].isin(valid_groups))
    
    def test_transform_extracts_email_domain(self, pipeline):
        """Test that email domain is extracted."""
        df = pipeline.extract()
        df = pipeline.transform(df)
        
        assert 'email_domain' in df.columns
        # All should be 'example.com' for test data
        assert (df['email_domain'] == 'example.com').all()


class TestDataLoading:
    """Test data loading stage."""
    
    def test_load_creates_parquet(self, pipeline, tmp_path):
        """Test that load creates parquet file."""
        df = pipeline.extract()
        df = pipeline.transform(df)
        
        pipeline.load(df)
        
        output_path = tmp_path / "output.parquet"
        assert output_path.exists()
    
    def test_load_creates_directory_if_needed(self, pipeline, tmp_path):
        """Test that load creates output directory."""
        # Create config with nested output path
        nested_path = tmp_path / "nested" / "dir" / "output.parquet"
        config = PipelineConfig(
            input_path=pipeline.config.input_path,
            output_path=nested_path
        )
        pipeline_nested = UserDataPipeline(config)
        
        df = pipeline_nested.extract()
        df = pipeline_nested.transform(df)
        pipeline_nested.load(df)
        
        assert nested_path.exists()
    
    def test_load_preserves_data(self, pipeline, tmp_path):
        """Test that loaded data matches transformed data."""
        df = pipeline.extract()
        df = pipeline.transform(df)
        
        pipeline.load(df)
        
        # Read back the data
        loaded_df = pd.read_parquet(tmp_path / "output.parquet")
        
        # Should have same shape
        assert loaded_df.shape == df.shape
        # Should have same columns
        assert set(loaded_df.columns) == set(df.columns)


class TestFullPipeline:
    """Test complete pipeline execution."""
    
    def test_pipeline_runs_end_to_end(self, pipeline, tmp_path):
        """Test that full pipeline executes successfully."""
        pipeline.run()
        
        # Output should exist
        output_path = tmp_path / "output.parquet"
        assert output_path.exists()
        
        # Output should be valid
        df = pd.read_parquet(output_path)
        assert len(df) > 0
        assert 'user_id' in df.columns
        assert 'age_group' in df.columns
        assert 'email_domain' in df.columns
    
    def test_pipeline_raises_on_error(self, tmp_path):
        """Test that pipeline raises errors appropriately."""
        config = PipelineConfig(
            input_path=tmp_path / "nonexistent.csv",
            output_path=tmp_path / "output.parquet"
        )
        pipeline = UserDataPipeline(config)
        
        with pytest.raises(FileNotFoundError):
            pipeline.run()


class TestDataValidation:
    """Test data validation logic."""
    
    def test_validation_rejects_invalid_ages(self, pipeline):
        """Test that invalid ages are removed."""
        # Create test data with invalid ages
        df = pd.DataFrame({
            'user_id': [1, 2, 3, 4],
            'email': ['a@test.com', 'b@test.com', 'c@test.com', 'd@test.com'],
            'age': [25, -5, 150, 30]  # -5 and 150 are invalid
        })
        
        df = pipeline._validate_data(df)
        
        # Invalid ages should be filtered out
        assert len(df) == 2
        assert all((df['age'] >= 0) & (df['age'] <= 120))
    
    def test_validation_requires_columns(self, pipeline):
        """Test that required columns are checked."""
        df = pd.DataFrame({
            'user_id': [1, 2, 3],
            # Missing 'email' and 'age'
        })
        
        with pytest.raises(ValueError, match="Missing required columns"):
            pipeline._validate_data(df)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
