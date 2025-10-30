"""
Sample ETL Pipeline demonstrating best practices.

This pipeline extracts user data, transforms it, and loads to output.
Demonstrates: modular design, logging, validation, error handling.
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass
import yaml


@dataclass
class PipelineConfig:
    """Pipeline configuration."""
    input_path: Path
    output_path: Path
    log_level: str = "INFO"
    batch_size: int = 1000


class UserDataPipeline:
    """
    ETL Pipeline for user data processing.
    
    Follows modular design pattern with separate extract, transform, load stages.
    Includes logging, validation, and error handling.
    """
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Configure logging."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def extract(self) -> pd.DataFrame:
        """
        Extract data from source.
        
        Returns:
            DataFrame with raw user data
        
        Raises:
            FileNotFoundError: If input file doesn't exist
        """
        self.logger.info(f"Extracting data from {self.config.input_path}")
        
        if not Path(self.config.input_path).exists():
            raise FileNotFoundError(f"Input file not found: {self.config.input_path}")
        
        df = pd.read_csv(self.config.input_path)
        self.logger.info(f"Extracted {len(df)} rows")
        
        return df
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform data.
        
        Args:
            df: Raw DataFrame
        
        Returns:
            Transformed DataFrame
        """
        self.logger.info("Starting data transformation")
        
        # Clean data
        df = self._clean_data(df)
        
        # Validate
        df = self._validate_data(df)
        
        # Engineer features
        df = self._engineer_features(df)
        
        self.logger.info(f"Transformation complete. Final shape: {df.shape}")
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean raw data."""
        self.logger.info("Cleaning data")
        
        # Remove duplicates
        initial_len = len(df)
        df = df.drop_duplicates(subset=['user_id'])
        self.logger.info(f"Removed {initial_len - len(df)} duplicates")
        
        # Handle missing values
        df = df.dropna(subset=['user_id', 'email'])
        df['age'] = df['age'].fillna(df['age'].median())
        
        return df
    
    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate data quality."""
        self.logger.info("Validating data")
        
        # Check required columns
        required_cols = ['user_id', 'email', 'age']
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Validate data types
        if not pd.api.types.is_integer_dtype(df['user_id']):
            df['user_id'] = df['user_id'].astype(int)
        
        # Validate ranges
        invalid_ages = df[(df['age'] < 0) | (df['age'] > 120)]
        if len(invalid_ages) > 0:
            self.logger.warning(f"Found {len(invalid_ages)} records with invalid age")
            df = df[(df['age'] >= 0) & (df['age'] <= 120)]
        
        return df
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer new features."""
        self.logger.info("Engineering features")
        
        # Create age groups
        df['age_group'] = pd.cut(
            df['age'], 
            bins=[0, 18, 30, 50, 120], 
            labels=['<18', '18-30', '30-50', '50+']
        )
        
        # Extract email domain
        df['email_domain'] = df['email'].str.split('@').str[1]
        
        return df
    
    def load(self, df: pd.DataFrame) -> None:
        """
        Load data to destination.
        
        Args:
            df: Transformed DataFrame
        """
        self.logger.info(f"Loading data to {self.config.output_path}")
        
        # Create output directory if needed
        Path(self.config.output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save as parquet for efficiency
        df.to_parquet(self.config.output_path, index=False)
        
        self.logger.info(f"Successfully loaded {len(df)} rows")
    
    def run(self) -> None:
        """Execute full pipeline."""
        try:
            self.logger.info("Starting ETL pipeline")
            
            # Extract
            df = self.extract()
            
            # Transform
            df = self.transform(df)
            
            # Load
            self.load(df)
            
            self.logger.info("Pipeline completed successfully")
            
        except Exception as e:
            self.logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            raise


def main():
    """Main entry point."""
    # Load configuration
    config = PipelineConfig(
        input_path=Path("data/raw/users.csv"),
        output_path=Path("data/processed/users.parquet"),
        log_level="INFO"
    )
    
    # Run pipeline
    pipeline = UserDataPipeline(config)
    pipeline.run()


if __name__ == "__main__":
    main()
