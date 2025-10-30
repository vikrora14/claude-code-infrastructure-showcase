"""
Script to run ETL pipeline with configuration.

Usage:
    python scripts/run_pipeline.py --config configs/pipeline_config.yaml
"""

import argparse
import logging
from pathlib import Path
import sys
import yaml

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pipelines.etl_pipeline import UserDataPipeline, PipelineConfig


def setup_logging(log_level: str = "INFO", log_dir: str = "logs"):
    """Setup logging configuration."""
    Path(log_dir).mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{log_dir}/pipeline.log"),
            logging.StreamHandler()
        ]
    )


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Run ETL pipeline')
    parser.add_argument(
        '--config',
        type=str,
        default='configs/pipeline_config.yaml',
        help='Path to configuration file'
    )
    args = parser.parse_args()
    
    # Load configuration
    config_dict = load_config(args.config)
    
    # Setup logging
    setup_logging(
        log_level=config_dict.get('log_level', 'INFO'),
        log_dir=config_dict.get('log_dir', 'logs')
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting pipeline with config: {args.config}")
    
    # Create pipeline configuration
    pipeline_config = PipelineConfig(
        input_path=Path(config_dict['input_path']),
        output_path=Path(config_dict['output_path']),
        log_level=config_dict.get('log_level', 'INFO'),
        batch_size=config_dict.get('batch_size', 1000)
    )
    
    # Run pipeline
    try:
        pipeline = UserDataPipeline(pipeline_config)
        pipeline.run()
        logger.info("Pipeline completed successfully!")
        return 0
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
