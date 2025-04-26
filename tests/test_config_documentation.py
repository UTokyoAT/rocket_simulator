import json
import os
import unittest


class TestConfigDocumentation(unittest.TestCase):
    """configファイルとREADMEの整合性をテストするクラス"""

    def setUp(self):
        # READMEファイルを読み込む
        with open("README.md", encoding="utf-8") as f:
            self.readme_content = f.read()

        # config.jsonファイルを読み込む
        with open("config/config.json", encoding="utf-8") as f:
            self.config = json.load(f)

        # configフォルダ内のファイル一覧を取得
        self.config_files = [
            f for f in os.listdir("config") if os.path.isfile(os.path.join("config", f))
        ]

    def test_config_keys_in_readme(self):
        """config.jsonのすべてのキーがREADME.mdに含まれることを確認するテスト"""
        for key in self.config.keys():
            self.assertIn(
                key,
                self.readme_content,
                f"config.jsonのキー '{key}' がREADME.mdに記載されていません",
            )

    def test_config_files_in_readme(self):
        """configフォルダにある全ファイルの名前がREADME.mdに含まれることを確認するテスト"""
        for filename in self.config_files:
            self.assertIn(
                filename,
                self.readme_content,
                f"configフォルダのファイル '{filename}' がREADME.mdに記載されていません",
            )


if __name__ == "__main__":
    unittest.main()
