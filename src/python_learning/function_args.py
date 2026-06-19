# A bare `*` marks the start of keyword-only arguments.
# Everything after `*` MUST be passed by keyword (name=value), not positionally.

def encode_and_build_envelope(
    audio_bytes: bytes,
    *,                              # everything after here is keyword-only
    source_app: str,
    transcribe: bool,
    use_online_transcription: bool,
) -> bytes:
    header = f"{source_app}|{transcribe}|{use_online_transcription}".encode()
    return header + b"\n" + audio_bytes


# A leading `/` marks positional-only arguments (the mirror of `*`).
def power(base, exp, /):             # base and exp CANNOT be passed by keyword
    return base ** exp


def main() -> None:
    raw = b"\x00\x01\x02"

    # OK: audio_bytes positional, the rest by keyword
    print(encode_and_build_envelope(
        raw,
        source_app="recorder",
        transcribe=True,
        use_online_transcription=False,
    ))

    # OK: audio_bytes by keyword too
    print(encode_and_build_envelope(
        audio_bytes=raw,
        source_app="recorder",
        transcribe=True,
        use_online_transcription=False,
    ))

    # TypeError: keyword-only args passed positionally
    try:
        encode_and_build_envelope(raw, "recorder", True, False)  # type: ignore[misc]
    except TypeError as e:
        print("TypeError:", e)

    # positional-only: OK positionally, TypeError by keyword
    print(power(2, 10))
    try:
        power(base=2, exp=10)  # type: ignore[call-arg]
    except TypeError as e:
        print("TypeError:", e)


if __name__ == "__main__":
    main()
