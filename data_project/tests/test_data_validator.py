"""
Tests for data validator.

Demonstrates testing data validation logic.
"""

import pytest
import pandas as pd
import pandera as pa
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from validation.data_validator import DataValidator, UserDataSchema


@pytest.fixture
def valid_data():
    """Create valid sample data."""
    return pd.DataFrame({
        'user_id': [1, 2, 3],
        'email': ['user1@example.com', 'user2@example.com', 'user3@example.com'],
        'age': [25, 30, 35],
        'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
        'status': ['active', 'active', 'inactive']
    })


@pytest.fixture
def invalid_data():
    """Create invalid sample data."""
    return pd.DataFrame({
        'user_id': [1, 2, -1],  # -1 is invalid (must be > 0)
        'email': ['user1@example.com', 'invalid-email', 'user3@example.com'],
        'age': [25, 150, 35],  # 150 is invalid (must be <= 120)
        'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
        'status': ['active', 'invalid_status', 'inactive']  # invalid_status is invalid
    })


@pytest.fixture
def validator():
    """Create validator instance."""
    return DataValidator(UserDataSchema.to_schema())


class TestSchemaValidation:
    """Test schema validation."""
    
    def test_validate_accepts_valid_data(self, validator, valid_data):
        """Test that valid data passes validation."""
        results = validator.validate(valid_data)
        
        assert results['schema_valid'] is True
        assert results['overall_pass'] is True
        assert len(results['errors']) == 0
    
    def test_validate_rejects_invalid_data(self, validator, invalid_data):
        """Test that invalid data fails validation."""
        results = validator.validate(invalid_data)
        
        assert results['schema_valid'] is False
        assert results['overall_pass'] is False
        assert len(results['errors']) > 0
    
    def test_validate_detects_negative_user_id(self, validator):
        """Test that negative user IDs are caught."""
        df = pd.DataFrame({
            'user_id': [-1, 2, 3],
            'email': ['a@test.com', 'b@test.com', 'c@test.com'],
            'age': [25, 30, 35],
            'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'status': ['active', 'active', 'inactive']
        })
        
        results = validator.validate(df)
        
        assert results['schema_valid'] is False
        assert any('user_id' in str(e) for e in results['errors'])
    
    def test_validate_detects_invalid_email(self, validator):
        """Test that invalid email format is caught."""
        df = pd.DataFrame({
            'user_id': [1, 2, 3],
            'email': ['valid@test.com', 'not-an-email', 'valid@test.com'],
            'age': [25, 30, 35],
            'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'status': ['active', 'active', 'inactive']
        })
        
        results = validator.validate(df)
        
        assert results['schema_valid'] is False
        assert any('email' in str(e) for e in results['errors'])
    
    def test_validate_detects_age_out_of_range(self, validator):
        """Test that age outside valid range is caught."""
        df = pd.DataFrame({
            'user_id': [1, 2, 3],
            'email': ['a@test.com', 'b@test.com', 'c@test.com'],
            'age': [25, 150, 35],  # 150 > 120
            'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'status': ['active', 'active', 'inactive']
        })
        
        results = validator.validate(df)
        
        assert results['schema_valid'] is False
        assert any('age' in str(e) for e in results['errors'])


class TestQualityMetrics:
    """Test quality metrics calculation."""
    
    def test_completeness_metric(self, validator, valid_data):
        """Test completeness metric calculation."""
        results = validator.validate(valid_data)
        
        # Valid data should have 100% completeness
        assert results['quality_metrics']['completeness'] == 1.0
    
    def test_completeness_with_nulls(self, validator):
        """Test completeness with null values."""
        df = pd.DataFrame({
            'user_id': [1, 2, None],
            'email': ['a@test.com', None, 'c@test.com'],
            'age': [25, 30, 35],
            'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'status': ['active', 'active', None]
        })
        
        results = validator.validate(df, lazy=True)
        
        # Should have < 100% completeness
        assert results['quality_metrics']['completeness'] < 1.0
    
    def test_duplicate_detection(self, validator, valid_data):
        """Test duplicate row detection."""
        # Add duplicate row
        df = pd.concat([valid_data, valid_data.iloc[[0]]], ignore_index=True)
        
        results = validator.validate(df, lazy=True)
        
        # Should detect duplicate
        assert results['quality_metrics']['duplicate_rows'] > 0
    
    def test_null_count_metric(self, validator, valid_data):
        """Test null count metric."""
        results = validator.validate(valid_data)
        
        # Valid data should have 0 nulls
        assert results['quality_metrics']['null_count'] == 0


class TestCompletenessChecks:
    """Test completeness checking."""
    
    def test_completeness_per_column(self, validator, valid_data):
        """Test per-column completeness."""
        results = validator.validate(valid_data)
        
        completeness = results['completeness']
        
        # All columns should be complete
        for col in valid_data.columns:
            assert completeness[col]['complete'] == True  # Use == instead of is
            assert completeness[col]['null_count'] == 0
    
    def test_warns_on_high_null_rate(self, validator):
        """Test that high null rate triggers warning."""
        # Create data with >10% nulls in age column
        df = pd.DataFrame({
            'user_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'email': ['a@test.com'] * 10,
            'age': [25, None, None, None, 30, 35, 40, 45, 50, 55],
            'created_at': pd.to_datetime(['2024-01-01'] * 10),
            'status': ['active'] * 10
        })
        
        results = validator.validate(df, lazy=True)
        
        # Should have warning about high null rate
        assert any('high_null_rate' in str(w) for w in results['warnings'])


class TestConsistencyChecks:
    """Test consistency checking."""
    
    def test_detects_duplicate_keys(self, validator):
        """Test detection of duplicate user IDs."""
        df = pd.DataFrame({
            'user_id': [1, 1, 3],  # Duplicate user_id
            'email': ['a@test.com', 'b@test.com', 'c@test.com'],
            'age': [25, 30, 35],
            'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
            'status': ['active', 'active', 'inactive']
        })
        
        results = validator.validate(df, lazy=True)
        
        # Should have error about duplicate keys
        assert any('duplicate_keys' in str(e.get('type')) for e in results['errors'])


class TestReportGeneration:
    """Test validation report generation."""
    
    def test_generate_report_for_valid_data(self, validator, valid_data):
        """Test report generation for valid data."""
        results = validator.validate(valid_data)
        report = validator.generate_report(results)
        
        assert 'DATA VALIDATION REPORT' in report
        assert 'PASS' in report
        assert 'QUALITY METRICS' in report
    
    def test_generate_report_for_invalid_data(self, validator, invalid_data):
        """Test report generation for invalid data."""
        results = validator.validate(invalid_data, lazy=True)
        report = validator.generate_report(results)
        
        assert 'DATA VALIDATION REPORT' in report
        assert 'FAIL' in report
        assert 'ERRORS' in report
    
    def test_report_includes_metrics(self, validator, valid_data):
        """Test that report includes metrics."""
        results = validator.validate(valid_data)
        report = validator.generate_report(results)
        
        assert 'Total Rows:' in report
        assert 'Total Columns:' in report
        assert 'Completeness:' in report


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
