bool isVersionGreaterThan(String newVersion, String currentVersion) {
  List<String> currentV = currentVersion.split(".");
  List<String> newV = newVersion.split(".");
  bool a = false;
  for (var i = 0; i <= 2; i++) {
    a = int.parse(newV[i]) >= int.parse(currentV[i]);
    if (int.parse(newV[i]) != int.parse(currentV[i])) break;
  }
  return a;
}
