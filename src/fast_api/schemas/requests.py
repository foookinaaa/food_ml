from pydantic import BaseModel


class FeatureRequest(BaseModel):
    """
    Model for query
    """

    tree_dbh: int
    curb_loc: bool
    steward: int
    guards: int
    sidewalk: bool
    problems: int
    root_stone: bool
    root_grate: bool
    root_other: bool
    trunk_wire: bool
    trnk_light: bool
    trnk_other: bool
    brch_light: bool
    brch_shoe: bool
    brch_other: bool
    spc_common: str
    zip_city: str
    borough: str
    user_type: str

    class Config:
        """Model example."""

        json_schema_extra = {
            "example": {
                "tree_dbh": 22,
                "curb_loc": 1,
                "steward": 0,
                "guards": 0,
                "sidewalk": 1,
                "problems": 1,
                "root_stone": 0,
                "root_grate": 0,
                "root_other": 0,
                "trunk_wire": 0,
                "trnk_light": 0,
                "trnk_other": 0,
                "brch_light": 1,
                "brch_shoe": 0,
                "brch_other": 0,
                "spc_common": "green ash",
                "zip_city": "Ozone Park",
                "borough": "Queens",
                "user_type": "NYC Parks Staff",
            }
        }
