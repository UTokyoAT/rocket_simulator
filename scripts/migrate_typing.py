"""プロジェクト内のすべての.pyファイルを更新するスクリプト"""

import sys
from collections.abc import Generator
from pathlib import Path


def find_python_files(root_path: Path) -> Generator[Path, None, None]:
    """
    指定されたディレクトリ配下のすべての.pyファイルを再帰的に検索する

    Args:
        root_path: 検索開始ディレクトリ

    Yields:
        Path: .pyファイルのパス
    """
    # 除外するディレクトリ
    exclude_dirs = {"__pycache__", ".git", ".venv", "venv", ".pytest_cache", ".ruff_cache", "output", ".DS_Store"}

    for path in root_path.rglob("*.py"):
        # 除外ディレクトリに含まれるファイルはスキップ
        if any(exclude_dir in path.parts for exclude_dir in exclude_dirs):
            continue
        yield path


def transform_code(content: str) -> str:
    """
    Pythonコードの内容を変換する関数

    Args:
        content: 元のPythonコードの文字列

    Returns:
        str: 変換後のPythonコードの文字列
    """
    lines = content.split("\n")
    modified_lines = []

    # NPVectorのインポートが必要かどうかを判定
    needs_npvector_import = False
    has_npvector_import = "from src.util.type import NPVector" in content

    for line in lines:
        # src.util.type.py自体は変換しない
        if "NPVector = np.ndarray" in line:
            modified_lines.append(line)
            continue

        # すべての np.ndarray を NPVector に変換
        if "np.ndarray" in line:
            # np.ndarray[tuple[int], np.dtype[np.float64]] を NPVector に変換
            if "np.ndarray[tuple[int], np.dtype[np.float64]]" in line:
                modified_line = line.replace("np.ndarray[tuple[int], np.dtype[np.float64]]", "NPVector")
                modified_lines.append(modified_line)
                needs_npvector_import = True
                continue

            # その他のすべての np.ndarray を NPVector に変換
            modified_line = line.replace("np.ndarray", "NPVector")
            modified_lines.append(modified_line)
            needs_npvector_import = True
            continue

        # import numpy as np の後にNPVectorのインポートを追加
        if "import numpy as np" in line and needs_npvector_import and not has_npvector_import:
            modified_lines.append(line)
            modified_lines.append("from src.util.type import NPVector")
            has_npvector_import = True
            continue

        modified_lines.append(line)

    # ファイルの最初の方にNPVectorのインポートを追加（numpy importが見つからなかった場合）
    if needs_npvector_import and not has_npvector_import:
        # import文の最後に追加
        import_section_end = 0
        for i, line in enumerate(modified_lines):
            if line.startswith("import ") or line.startswith("from "):
                import_section_end = i

        if import_section_end > 0:
            modified_lines.insert(import_section_end + 1, "from src.util.type import NPVector")
        else:
            # import文がない場合は最初に追加
            modified_lines.insert(0, "from src.util.type import NPVector")
            modified_lines.insert(1, "")

    return "\n".join(modified_lines)


def update_file(file_path: Path, dry_run: bool = False) -> bool:
    """
    指定されたファイルを更新する

    Args:
        file_path: 更新するファイルのパス
        dry_run: True の場合は実際には更新せず、変更内容を表示のみ

    Returns:
        bool: ファイルが変更されたかどうか
    """
    try:
        # ファイルを読み込み
        with open(file_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        # 変換関数を適用
        transformed_content = transform_code(original_content)

        # 変更があるかチェック
        if original_content == transformed_content:
            print(f"No changes needed: {file_path}")
            return False

        if dry_run:
            print(f"Would update: {file_path}")
            print("--- Original ---")
            print(original_content[:200] + "..." if len(original_content) > 200 else original_content)
            print("--- Transformed ---")
            print(transformed_content[:200] + "..." if len(transformed_content) > 200 else transformed_content)
            print("-" * 50)
            return True

        # ファイルを更新
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(transformed_content)

        print(f"Updated: {file_path}")
        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """メイン関数"""
    import argparse

    parser = argparse.ArgumentParser(description="プロジェクト内のすべての.pyファイルを更新")
    parser.add_argument("--dry-run", action="store_true", help="実際には更新せず、変更内容を表示のみ")
    parser.add_argument("--root", type=str, default=".", help="検索開始ディレクトリ（デフォルト: 現在のディレクトリ）")

    args = parser.parse_args()

    root_path = Path(args.root).resolve()

    if not root_path.exists():
        print(f"Error: Directory {root_path} does not exist")
        sys.exit(1)

    print(f"Searching for Python files in: {root_path}")
    print(f"Dry run mode: {args.dry_run}")
    print("-" * 50)

    # すべての.pyファイルを検索
    python_files = list(find_python_files(root_path))
    print(f"Found {len(python_files)} Python files")

    if not python_files:
        print("No Python files found")
        return

    # 各ファイルを処理
    updated_count = 0
    for file_path in python_files:
        if update_file(file_path, dry_run=args.dry_run):
            updated_count += 1

    print("-" * 50)
    if args.dry_run:
        print(f"Dry run completed. {updated_count} files would be updated.")
    else:
        print(f"Migration completed. {updated_count} files were updated.")


if __name__ == "__main__":
    main()
