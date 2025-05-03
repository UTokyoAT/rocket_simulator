import json
import unittest
from pathlib import Path


class TestConfigDocumentation(unittest.TestCase):
    """READMEとconfigファイルの整合性を検証するテスト"""

    def setUp(self) -> None:
        """テスト実行前の準備"""
        # 必要なファイルパスを定義
        self.readme_path = Path("README.md")
        self.config_dir = Path("config_sample")
        self.config_json_path = self.config_dir / "config.json"

        # READMEの内容を読み込み
        self.readme_content = self.readme_path.read_text(encoding="utf-8")

        # config.jsonの内容を読み込み
        self.config = json.loads(self.config_json_path.read_text(encoding="utf-8"))

        # configフォルダ内のファイル一覧を取得
        self.config_files = [f.name for f in self.config_dir.iterdir() if f.is_file()]

    def test_config_keys_in_readme(self) -> None:
        """config.jsonのすべてのキーがREADME.mdに記載されていることを確認"""
        for key in self.config:
            err_msg = f"config.jsonのキー '{key}' がREADME.mdに記載されていません"
            self.assertIn(key, self.readme_content, err_msg)

    def test_config_files_in_readme(self) -> None:
        """configフォルダ内の全ファイル名がREADME.mdに記載されていることを確認"""
        for filename in self.config_files:
            err_msg = f"configフォルダのファイル '{filename}' がREADME.mdに記載されていません"
            self.assertIn(filename, self.readme_content, err_msg)


if __name__ == "__main__":
    unittest.main()
