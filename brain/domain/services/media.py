def guess_image_content_type(file_path: str | None) -> str | None:
    """Infer the MIME type from a file path extension, returning None when unknown."""
    if not file_path:
        return None
    extension = file_path.rsplit(".", 1)[-1].lower()
    if extension in {"jpg", "jpeg"}:
        return "image/jpeg"
    if extension == "png":
        return "image/png"
    if extension == "webp":
        return "image/webp"
    return None
