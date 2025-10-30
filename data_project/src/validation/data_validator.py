"""
Data validation module using Pandera.

Demonstrates schema validation, data quality checks, and validation reports.
"""

import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check
from typing import Dict, List
from datetime import datetime
import logging


# Define schema for user data
class UserDataSchema(pa.SchemaModel):
    """Schema for user data validation."""
    
    user_id: int = pa.Field(gt=0, unique=True, description="Unique user identifier")
    email: str = pa.Field(str_matches=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="Valid email address")
    age: int = pa.Field(ge=0, le=120, description="User age between 0 and 120")
    created_at: pd.Timestamp = pa.Field(description="Account creation timestamp")
    status: str = pa.Field(isin=['active', 'inactive', 'pending'], description="Account status")
    
    class Config:
        """Schema configuration."""
        strict = True
        coerce = True


class DataValidator:
    """
    Comprehensive data validation.
    
    Validates data against schemas and runs quality checks.
    """
    
    def __init__(self, schema: pa.DataFrameSchema):
        self.schema = schema
        self.logger = logging.getLogger(__name__)
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []
    
    def validate(self, df: pd.DataFrame, lazy: bool = True) -> Dict:
        """
        Run comprehensive validation.
        
        Args:
            df: DataFrame to validate
            lazy: If True, collect all errors before raising
        
        Returns:
            Dict with validation results
        """
        self.logger.info("Starting data validation")
        
        results = {
            'schema_valid': self._validate_schema(df, lazy),
            'quality_metrics': self._check_quality(df),
            'completeness': self._check_completeness(df),
            'consistency': self._check_consistency(df),
            'errors': self.errors,
            'warnings': self.warnings,
            'overall_pass': len(self.errors) == 0
        }
        
        self.logger.info(f"Validation complete. Pass: {results['overall_pass']}")
        return results
    
    def _validate_schema(self, df: pd.DataFrame, lazy: bool = True) -> bool:
        """Validate DataFrame against schema."""
        try:
            self.schema.validate(df, lazy=lazy)
            self.logger.info("Schema validation passed")
            return True
        except pa.errors.SchemaErrors as e:
            self.logger.error("Schema validation failed")
            for case in e.failure_cases.to_dict('records'):
                self.errors.append({
                    'type': 'schema_error',
                    'column': case.get('column'),
                    'check': case.get('check'),
                    'index': case.get('index')
                })
            return False
        except Exception as e:
            self.logger.error(f"Unexpected validation error: {e}")
            self.errors.append({
                'type': 'unexpected_error',
                'message': str(e)
            })
            return False
    
    def _check_quality(self, df: pd.DataFrame) -> Dict:
        """Calculate data quality metrics."""
        total_cells = len(df) * len(df.columns)
        null_cells = df.isnull().sum().sum()
        
        metrics = {
            'completeness': 1 - (null_cells / total_cells) if total_cells > 0 else 0,
            'uniqueness': df.nunique().sum() / len(df) if len(df) > 0 else 0,
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'null_count': int(null_cells),
            'duplicate_rows': len(df) - len(df.drop_duplicates())
        }
        
        return metrics
    
    def _check_completeness(self, df: pd.DataFrame) -> Dict:
        """Check completeness of each column."""
        completeness = {}
        
        for col in df.columns:
            null_count = df[col].isnull().sum()
            null_pct = null_count / len(df) if len(df) > 0 else 0
            
            completeness[col] = {
                'null_count': int(null_count),
                'null_percentage': float(null_pct),
                'complete': null_count == 0
            }
            
            # Warn if > 10% nulls
            if null_pct > 0.1:
                self.warnings.append({
                    'type': 'high_null_rate',
                    'column': col,
                    'null_percentage': null_pct
                })
        
        return completeness
    
    def _check_consistency(self, df: pd.DataFrame) -> Dict:
        """Check data consistency."""
        consistency = {}
        
        # Check for duplicate keys
        if 'user_id' in df.columns:
            duplicates = df['user_id'].duplicated().sum()
            consistency['unique_user_ids'] = duplicates == 0
            if duplicates > 0:
                self.errors.append({
                    'type': 'duplicate_keys',
                    'column': 'user_id',
                    'count': int(duplicates)
                })
        
        # Check for logical inconsistencies
        if 'age' in df.columns and 'status' in df.columns:
            # Example: users under 18 shouldn't be 'active'
            invalid = df[(df['age'] < 18) & (df['status'] == 'active')]
            if len(invalid) > 0:
                self.warnings.append({
                    'type': 'business_rule_violation',
                    'message': 'Found users under 18 with active status',
                    'count': len(invalid)
                })
        
        return consistency
    
    def generate_report(self, results: Dict) -> str:
        """Generate human-readable validation report."""
        report = []
        report.append("=" * 60)
        report.append("DATA VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"Timestamp: {datetime.now().isoformat()}")
        report.append(f"Overall Result: {'PASS' if results['overall_pass'] else 'FAIL'}")
        report.append("")
        
        # Quality metrics
        report.append("QUALITY METRICS")
        report.append("-" * 60)
        metrics = results['quality_metrics']
        report.append(f"Total Rows: {metrics['total_rows']}")
        report.append(f"Total Columns: {metrics['total_columns']}")
        report.append(f"Completeness: {metrics['completeness']:.2%}")
        report.append(f"Duplicate Rows: {metrics['duplicate_rows']}")
        report.append(f"Null Cells: {metrics['null_count']}")
        report.append("")
        
        # Errors
        if results['errors']:
            report.append("ERRORS")
            report.append("-" * 60)
            for error in results['errors']:
                report.append(f"- {error}")
            report.append("")
        
        # Warnings
        if results['warnings']:
            report.append("WARNINGS")
            report.append("-" * 60)
            for warning in results['warnings']:
                report.append(f"- {warning}")
            report.append("")
        
        report.append("=" * 60)
        return "\n".join(report)


def validate_user_data(df: pd.DataFrame) -> Dict:
    """
    Validate user data against schema.
    
    Args:
        df: DataFrame with user data
    
    Returns:
        Validation results dictionary
    """
    validator = DataValidator(UserDataSchema.to_schema())
    results = validator.validate(df)
    
    # Print report
    print(validator.generate_report(results))
    
    return results


if __name__ == "__main__":
    # Example usage
    sample_data = pd.DataFrame({
        'user_id': [1, 2, 3],
        'email': ['user1@example.com', 'user2@example.com', 'user3@example.com'],
        'age': [25, 30, 35],
        'created_at': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
        'status': ['active', 'active', 'inactive']
    })
    
    results = validate_user_data(sample_data)
