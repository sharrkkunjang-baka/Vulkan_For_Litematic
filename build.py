"""Build against an existing Minecraft 26.3 Fabric installation, without downloading anything."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minecraft-jar", required=True, type=Path)
    parser.add_argument("--litematica-jar", required=True, type=Path)
    parser.add_argument("--libraries", required=True, type=Path)
    parser.add_argument("--javac", default="javac", help="JDK 25 compiler (defaults to PATH)")
    args = parser.parse_args()
    classpath = [args.minecraft_jar, args.litematica_jar]
    for pattern in ("net/fabricmc/sponge-mixin/*/sponge-mixin-*.jar",
                    "org/apache/commons/commons-lang3/*/commons-lang3-*.jar"):
        matches = sorted(p for p in args.libraries.glob(pattern)
                         if not p.name.endswith(("-sources.jar", "-javadoc.jar")))
        if not matches:
            parser.error(f"missing {pattern} in {args.libraries}")
        classpath.append(matches[-1])
    for path in classpath:
        if not path.is_file():
            parser.error(f"missing {path}")
    build_dir = ROOT / "build"
    build_dir.mkdir(exist_ok=True)
    output = build_dir / "Vulkan_For_Litematic.jar"
    resources = ROOT / "src/main/resources"
    sources = sorted((ROOT / "src/main/java").rglob("*.java"))
    with tempfile.TemporaryDirectory(prefix="classes-", dir=build_dir) as temp:
        classes = Path(temp)
        subprocess.run([args.javac, "--release", "25", "-proc:none", "-encoding", "UTF-8",
                        "-classpath", os.pathsep.join(map(str, classpath)),
                        "-d", str(classes), *map(str, sources)], check=True)
        with ZipFile(output, "w", ZIP_DEFLATED) as jar:
            for base in (classes, resources):
                for path in sorted(base.rglob("*")):
                    if path.is_file():
                        jar.write(path, path.relative_to(base).as_posix())
            jar.write(ROOT / "LICENSE", "LICENSE")
    print(output)


if __name__ == "__main__":
    main()
