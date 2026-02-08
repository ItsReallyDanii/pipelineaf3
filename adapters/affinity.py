def run(structure_pdb, smiles, mode="mock"):
    if mode == "mock":
        return {"pKd": 8.5, "confidence": 0.9}
        
    # PRODUCTION: Call AQAffinity
    # from aqaffinity import predict_score
    raise NotImplementedError("Production mode requires GPU/Camber environment")
