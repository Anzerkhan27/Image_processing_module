# image_processing/report_models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple


class QRCodeModel(BaseModel):
    content: Optional[str] = Field(None, description="Decoded QR code content")
    bbox: Tuple[int, int, int, int] = Field(..., description="Bounding box as (x, y, width, height)")
    area: int = Field(..., description="Area of the bounding box")
    is_valid: bool = Field(..., description="Whether decoding was successful")
    quality_score: Optional[float] = Field(None, description="Optional visual clarity/confidence score")


class POIReportModel(BaseModel):
    poi_id: int = Field(..., description="Point of Interest (rock) ID")
    timestamp: str = Field(..., description="Processing time (UTC ISO format)")
    image_name: str = Field(..., description="Filename of the analyzed image")
    total_detected: int = Field(..., description="All QR candidates found")
    valid_qrs: List[QRCodeModel]
    corrupted_qrs: List[QRCodeModel]
    best_qr: Optional[QRCodeModel]
    score_estimate: Optional[float] = Field(None, description="Scoring estimate based on smallest valid QR")
