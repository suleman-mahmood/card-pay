from dataclasses import dataclass

@dataclass(frozen=True)
class VendorQrIdDTO:
    id: str
    full_name: str
    qr_id: str
