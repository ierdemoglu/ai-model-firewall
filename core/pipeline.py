from typing import List, Dict, Any
from modules.base_module import BaseSecurityModule
from modules.hf_hash_check import HFHashCheckModule
from modules.virustotal_check import VirusTotalCheckModule
from modules.model_integrity_check import ModelIntegrityCheckModule
from modules.pickle_scanner import PickleScannerModule
from modules.disk_space_guard import DiskSpaceGuardModule

class SecurityPipeline:
    def __init__(self):
        self.modules: List[BaseSecurityModule] = [
            DiskSpaceGuardModule(),
            HFHashCheckModule(),
            VirusTotalCheckModule(),
            PickleScannerModule(),
            ModelIntegrityCheckModule(),
        ]

    def execute(self, file_path: str) -> Dict[str, Any]:
        for module in self.modules:
            try:
                result = module.scan(file_path)
                if not result.get("success", False):
                    return {"safe": False, "reason": result.get("message"), "module": module.name}
            except Exception as e:
                return {"safe": False, "reason": str(e), "module": module.name}
        return {"safe": True, "message": "Tüm testler geçti", "module": "All"}