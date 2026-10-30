"""Java detection service for Minecraft instance launching."""

import subprocess
import shutil
import os
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class JavaInfo:
    """Information about a detected Java installation."""
    path: str
    version: str
    major_version: int
    is_jdk: bool


class JavaDetectionService:
    """Service for detecting Java installations on the system."""

    # Minimum Java version for modern Minecraft versions
    MIN_JAVA_VERSION = {
        "1.18": 17,
        "1.17": 16,
        "1.16": 11,
        "1.12": 8,
    }

    def __init__(self):
        self._java_cache: Optional[List[JavaInfo]] = None

    def detect_all(self) -> List[JavaInfo]:
        """Detect all Java installations on the system."""
        if self._java_cache is not None:
            return self._java_cache

        java_installations = []

        # Check JAVA_HOME
        java_home = os.environ.get("JAVA_HOME")
        if java_home:
            java_path = Path(java_home) / "bin" / ("java.exe" if os.name == "nt" else "java")
            if java_path.exists():
                info = self._get_java_info(str(java_path))
                if info:
                    java_installations.append(info)

        # Check PATH for java
        java_in_path = shutil.which("java")
        if java_in_path:
            info = self._get_java_info(java_in_path)
            if info and not any(j.path == info.path for j in java_installations):
                java_installations.append(info)

        # Check common installation locations
        common_paths = self._get_common_java_paths()
        for path in common_paths:
            if path.exists():
                info = self._get_java_info(str(path))
                if info and not any(j.path == info.path for j in java_installations):
                    java_installations.append(info)

        # Sort by version descending (newest first)
        java_installations.sort(key=lambda j: j.major_version, reverse=True)
        self._java_cache = java_installations
        return java_installations

    def _get_common_java_paths(self) -> List[Path]:
        """Get common Java installation paths for the current OS."""
        paths = []
        if os.name == "nt":  # Windows
            program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
            program_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
            for base in [program_files, program_files_x86]:
                java_dir = Path(base) / "Java"
                if java_dir.exists():
                    for subdir in java_dir.iterdir():
                        if subdir.is_dir():
                            paths.append(subdir / "bin" / "java.exe")
        else:  # Linux/macOS
            common_bases = [
                Path("/usr/lib/jvm"),
                Path("/usr/java"),
                Path("/Library/Java/JavaVirtualMachines"),
                Path("/opt/java"),
            ]
            for base in common_bases:
                if base.exists():
                    for subdir in base.rglob("*"):
                        if subdir.name == "java" and subdir.is_file():
                            paths.append(subdir)
        return paths

    def _get_java_info(self, java_path: str) -> Optional[JavaInfo]:
        """Get version info for a Java executable."""
        try:
            result = subprocess.run(
                [java_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            # java -version outputs to stderr
            output = result.stderr or result.stdout
            version = self._parse_java_version(output)
            if version is None:
                return None

            major_version = self._extract_major_version(version)
            is_jdk = self._check_is_jdk(java_path)

            return JavaInfo(
                path=java_path,
                version=version,
                major_version=major_version,
                is_jdk=is_jdk,
            )
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            return None

    def _parse_java_version(self, output: str) -> Optional[str]:
        """Parse Java version from java -version output."""
        # Example output: openjdk version "17.0.8" 2023-07-18
        # Or: java version "1.8.0_372"
        import re
        match = re.search(r'version\s+"([^"]+)"', output)
        if match:
            return match.group(1)
        return None

    def _extract_major_version(self, version: str) -> int:
        """Extract major version number from version string."""
        # Handle versions like "17.0.8", "1.8.0_372", "21.0.1"
        parts = version.replace("_", ".").split(".")
        if parts[0] == "1" and len(parts) > 1:
            # Old format: 1.8.0 -> major is 8
            try:
                return int(parts[1])
            except ValueError:
                return 0
        try:
            return int(parts[0])
        except ValueError:
            return 0

    def _check_is_jdk(self, java_path: str) -> bool:
        """Check if the Java installation is a JDK (has javac)."""
        java_dir = Path(java_path).parent
        javac = java_dir / ("javac.exe" if os.name == "nt" else "javac")
        return javac.exists()

    def find_suitable_java(self, minecraft_version: str) -> Optional[JavaInfo]:
        """Find the best Java installation for a given Minecraft version."""
        required_major = self._get_required_java_version(minecraft_version)
        all_java = self.detect_all()

        # Prefer JDK over JRE, then newest version
        suitable = [j for j in all_java if j.major_version >= required_major]
        if not suitable:
            return None

        # Sort: JDK first, then by version descending
        suitable.sort(key=lambda j: (not j.is_jdk, -j.major_version))
        return suitable[0]

    def _get_required_java_version(self, minecraft_version: str) -> int:
        """Get required Java major version for a Minecraft version."""
        # Parse version like "1.20.1", "1.19.4", etc.
        parts = minecraft_version.split(".")
        if len(parts) >= 2:
            try:
                major = int(parts[0])
                minor = int(parts[1])
                version_key = f"{major}.{minor}"
                if version_key in self.MIN_JAVA_VERSION:
                    return self.MIN_JAVA_VERSION[version_key]
                # For versions newer than known ones, use the highest known requirement
                if minor >= 18:
                    return 17
                if minor >= 17:
                    return 16
                if minor >= 16:
                    return 11
            except ValueError:
                pass
        return 17  # Default to Java 17 for unknown versions

    def clear_cache(self):
        """Clear the cached Java detection results."""
        self._java_cache = None


# Global instance
java_detection_service = JavaDetectionService()
