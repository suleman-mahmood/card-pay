String croppedDescription(String description) {
  const contentLength = 30;
  if (description.length < contentLength) {
    return description;
  }

  return "${description.substring(0, contentLength - 1)}...";
}
