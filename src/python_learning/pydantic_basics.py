# Pydantic: define a schema as a class; get validation, coercion, and JSON for free.
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, field_validator

# --- 1. Basic model ----------------------------------------------------------
class Address(BaseModel):
    street: str
    city: str
    zip_code: str = Field(pattern=r"^\d{5}$")       # constraint via Field

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")
    age: int = Field(ge=0, le=150)                   # ge=>=, le=<=
    signed_up: datetime = Field(default_factory=datetime.now)
    tags: list[str] = []
    address: Address | None = None                   # nested model

    # Custom validator: runs after type coercion
    @field_validator("name")
    @classmethod
    def name_must_be_titlecased(cls, v: str) -> str:
        return v.title()

SEPARATOR = '\n'  + "-" * 30

def main() -> None:
    # --- 2. Construction validates & coerces -------------------------------
    # "42" becomes 42, "30" becomes 30 — pydantic coerces compatible types.
    u = User(
        id="42",                                     # type: ignore[arg-type]
        name="alice smith",
        email="alice@example.com",
        age="30",                                    # type: ignore[arg-type]
        tags=["admin", "beta"],
        address={"street": "1 Main St", "city": "NYC", "zip_code": "10001"},
    )
    print(f"USER:\n{u}")
    print(f"\nname was title-cased: {u.name}")
    print(SEPARATOR)

    # --- 3. Serialization --------------------------------------------------
    print(f"\nDICT:\n{u.model_dump()}")                            # -> dict
    print(f"\nJSON:\n{u.model_dump_json(indent=2)}")               # -> JSON string
    print(SEPARATOR)

    # --- 4. Parsing from dict / JSON --------------------------------------
    raw = '{"id": 1, "name": "bob", "email": "b@x.com", "age": 25}'
    u2 = User.model_validate_json(raw)
    print(f"\nPARSED:\n{u2}")
    print(SEPARATOR)

    # --- 5. Validation errors are structured ------------------------------
    try:
        User(id="not-a-number", name="", email="bad", age=999)
    except ValidationError as e:
        print(f"\nERROR:\n{e}")                                     # human-readable
        print(e.errors())                            # list[dict] — programmatic


if __name__ == "__main__":
    main()
