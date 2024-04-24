from uuid import UUID

"""
The UUIDs are used as an indirect mapping to enable easier changing on names. Otherwise we would have to change every occurrence.
"""


class ActionIDs:
    IV_Zugang = UUID("a8245193-5b5e-4dd0-944b-e2c47e168395")
    VOLLELEKTROLYT = UUID("eb83c9c2-0677-4f8b-b56b-1fd68f766068")
    STABILE_SEITENLAGE = UUID("055eb04d-be97-418c-9159-3161907ad9ba")


class MaterialIDs:
    IV_ZUGANG = UUID("b6c90988-3c8c-4e0f-ab60-65679d30cfc3")


class RoleIDs:
    PFLEGEFACHKRAFT = UUID("14c0946d-d06c-4c44-a2ad-71625ec1fc6c")
    ARZT = UUID("59ff24ae-9298-4a1b-88c7-5366e011f77d")
    LABORASSISTENT = UUID("66056789-afee-4c1d-9044-a7966ab3b15b")


role_map = {
    RoleIDs.PFLEGEFACHKRAFT: "Pflegefachkraft",
    RoleIDs.ARZT: "Arzt",
    RoleIDs.LABORASSISTENT: "Laborassistent",
}
