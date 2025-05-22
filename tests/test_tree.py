from utils import file_tree


def test_generate_tree_output_creates_expected_structure(tmp_path):
    # Arrange
    file_tree.create_project_structure(
        tmp_path,
        {
            "test_dir": ["a.txt", "b.txt"],
            "sub": ["c.txt"],
        },
    )

    # Act
    output = file_tree.generate_tree_output(tmp_path)

    # Assert
    assert "test_dir/" in output
    assert "    a.txt" in output
    assert "    b.txt" in output
    assert "sub/" in output
    assert "    c.txt" in output
