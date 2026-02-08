import yaml
import json
import logging
import time
import os
import hashlib
from pathlib import Path
from datetime import datetime
from pipeline.adapters import openfold3, affinity

# Logger Setup
logging.basicConfig(level=logging.INFO, format="[OPERATOR] %(message)s")
logger = logging.getLogger()

class PipelineOperator:
    def __init__(self, config_path, output_base):
        self.start_time = time.time()
        self.config = self._load_config(config_path)
        
        # Deterministic Run ID
        self.run_id = self.config.get("run_id", f"run_{int(self.start_time)}")
        self.output_dir = Path(output_base) / self.run_id
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Manifest Initialization
        self.manifest = {
            "run_id": self.run_id,
            "timestamp_start": datetime.utcnow().isoformat(),
            "config_hash": self._hash_config(config_path),
            "environment": "production" if self.config['mode'] == 'production' else "mock",
            "steps": {},
            "status": "INIT"
        }

    def _load_config(self, path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _hash_config(self, path):
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def execute(self):
        try:
            # 1. Structure Prediction
            logger.info(">>> STEP 1: OpenFold-3 Inference")
            structure_file = openfold3.run(
                sequence=self.config['input']['protein_sequence'],
                output_dir=self.output_dir,
                mode=self.config['mode']
            )
            self.manifest['steps']['openfold'] = {"status": "SUCCESS", "output": str(structure_file)}

            # 2. Affinity Scoring
            logger.info(">>> STEP 2: AQAffinity Scoring")
            score_data = affinity.run(
                structure_pdb=structure_file,
                smiles=self.config['input']['ligand_smiles'],
                mode=self.config['mode']
            )
            self.manifest['steps']['affinity'] = {"status": "SUCCESS", "data": score_data}

            self.manifest['status'] = "SUCCESS"

        except Exception as e:
            logger.error(f"PIPELINE FAILED: {str(e)}")
            self.manifest['status'] = "FAILED"
            self.manifest['error'] = str(e)
            raise e
        finally:
            self._save_manifest()

    def _save_manifest(self):
        self.manifest['timestamp_end'] = datetime.utcnow().isoformat()
        self.manifest['duration_seconds'] = round(time.time() - self.start_time, 2)
        
        with open(self.output_dir / "manifest.json", "w") as f:
            json.dump(self.manifest, f, indent=2)
        logger.info(f"Manifest saved to {self.output_dir}/manifest.json")
