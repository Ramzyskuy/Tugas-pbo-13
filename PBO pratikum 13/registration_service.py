import logging
from abc import ABC, abstractmethod

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

class IValidationRule(ABC):
    """Interface untuk aturan validasi registrasi mahasiswa."""

    @abstractmethod
    def validate(self, student: dict) -> bool:
        """
        Melakukan validasi data mahasiswa.

        Args:
            student (dict): Data mahasiswa.
        Returns:
            bool: True jika valid, False jika tidak.
        """
        pass

class SksLimitRule(IValidationRule):
    """Validasi batas maksimum SKS mahasiswa."""

    def validate(self, student: dict) -> bool:
        if student["sks"] > 24:
            logging.warning("Validasi gagal: SKS melebihi batas maksimum.")
            return False
        logging.info("Validasi SKS berhasil.")
        return True

class PrerequisiteRule(IValidationRule):
    """Validasi prasyarat mata kuliah."""

    def validate(self, student: dict) -> bool:
        if not student["prerequisite"]:
            logging.warning("Validasi gagal: Prasyarat belum terpenuhi.")
            return False
        logging.info("Validasi prasyarat berhasil.")
        return True

class RegistrationService:
    """Service utama untuk proses registrasi mahasiswa."""

    def __init__(self, rules: list[IValidationRule]):
        self.rules = rules

    def validate_registration(self, student: dict) -> bool:
        logging.info("Memulai proses validasi registrasi mahasiswa.")
        for rule in self.rules:
            if not rule.validate(student):
                logging.warning("Registrasi mahasiswa ditolak.")
                return False
        logging.info("Registrasi mahasiswa diterima.")
        return True

if __name__ == "__main__":
    student_data = {
        "sks": 22,
        "prerequisite": True
    }

    rules = [
        SksLimitRule(),
        PrerequisiteRule()
    ]

    service = RegistrationService(rules)
    service.validate_registration(student_data)
