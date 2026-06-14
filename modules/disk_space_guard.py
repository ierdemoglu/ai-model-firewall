import os
import shutil
from .base_module import BaseSecurityModule

class DiskSpaceGuardModule(BaseSecurityModule):
    MIN_FREE_SPACE_GB = 5

    @property
    def name(self) -> str:
        return "Disk Space Guard"

    def _get_free_space_gb(self, path: str) -> float:
        try:
            total, used, free = shutil.disk_usage(path)
            return free / (1024 ** 3)
        except Exception:
            return 9999

    def scan(self, file_path: str) -> dict:
        try:
            file_size = os.path.getsize(file_path)
            file_size_gb = file_size / (1024 ** 3)
            target_dir = os.path.dirname(file_path) or "."
            free_space = self._get_free_space_gb(target_dir)
            required_space = file_size_gb + self.MIN_FREE_SPACE_GB
            if free_space < required_space:
                return {"success": False, "message": f"Insufficient disk space! {required_space:.1f} GB required."}
            return {"success": True, "message": f"Sufficient disk space ({free_space:.1f} GB free)."}
        except Exception as e:
            return {"success": True, "message": f"Disk check failed: {e}"}
