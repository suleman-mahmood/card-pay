from dataclasses import dataclass


@dataclass(frozen=True)
class CheckpointsDTO:
    verified_phone_otp: bool
    verified_closed_loop: bool
    pin_setup: bool
