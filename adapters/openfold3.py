import shutil
from pathlib import Path

def run(sequence, output_dir, mode="mock"):
    output_path = Path(output_dir) / "prediction.pdb"
    
    if mode == "mock":
        # Create a dummy PDB file
        output_path.touch()
        return output_path
    
    # PRODUCTION: Call the actual OpenFold-3 CLI
    # This is where you would import openfold3.inference if running inside python
    # or subprocess.run() if calling the CLI.
    # For now, we stub the production call to fail if not implemented.
    raise NotImplementedError("Production mode requires GPU/Camber environment")
