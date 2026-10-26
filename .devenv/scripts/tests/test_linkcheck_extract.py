import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from linkcheck.extract import extract_files, extract_text, iter_doc_files, parse_destination
from linkcheck.models import Link


def raws(text):
    return [(link.line, link.raw) for link in extract_text(text, "docs/x.md")]


class TestParseDestination(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(parse_destination("[a](b.md) rest", 4), "b.md")

    def test_balanced_parentheses(self):
        text = "[s](https://en.wikipedia.org/wiki/Salt_(cryptography)) x"
        self.assertEqual(parse_destination(text, 4), "https://en.wikipedia.org/wiki/Salt_(cryptography)")

    def test_title_is_dropped(self):
        self.assertEqual(parse_destination('[a](b.md "Title")', 4), "b.md")

    def test_angle_brackets(self):
        self.assertEqual(parse_destination("[a](<my file.md>)", 4), "my file.md")


class TestExtractText(unittest.TestCase):
    def test_inline_link_and_image_with_line_numbers(self):
        text = "intro\n[a](one.md) and ![i](/img/x.png)\n"
        self.assertEqual(raws(text), [(2, "one.md"), (2, "/img/x.png")])

    def test_image_nested_in_link(self):
        self.assertEqual(raws("[![alt](/img/a.png)](https://x.org/)"),
                         [(1, "/img/a.png"), (1, "https://x.org/")])

    def test_javadoc_anchor_with_parentheses(self):
        text = "[m](https://docs.operaton.org/reference/latest/javadoc/A.html#m(java.lang.String,java.util.Date))"
        self.assertEqual(raws(text),
                         [(1, "https://docs.operaton.org/reference/latest/javadoc/A.html#m(java.lang.String,java.util.Date)")])

    def test_reference_definition(self):
        text = "See [JDK][get-jdk].\n\n[get-jdk]: https://www.oracle.com/java/ \"Oracle\"\n"
        self.assertEqual(raws(text), [(3, "https://www.oracle.com/java/")])

    def test_footnote_definition_ignored(self):
        self.assertEqual(raws("[^1]: some note text"), [])

    def test_html_attributes(self):
        text = '<a href="https://a.org/">a</a> <img src=\'/img/b.png\' />'
        self.assertEqual(raws(text), [(1, "https://a.org/"), (1, "/img/b.png")])

    def test_jsx_expression_ignored(self):
        self.assertEqual(raws("<a href={siteConfig.customFields.javaDocUrl}>x</a>"), [])

    def test_autolink(self):
        self.assertEqual(raws("Go to <https://operaton.org/>."), [(1, "https://operaton.org/")])

    def test_angle_destination_not_double_counted(self):
        self.assertEqual(raws("[a](<https://a.org/>)"), [(1, "https://a.org/")])

    def test_frontmatter_ignored(self):
        text = "---\ntitle: '[x](nope.md)'\n---\n[a](yes.md)\n"
        self.assertEqual(raws(text), [(4, "yes.md")])

    def test_fenced_code_ignored(self):
        text = "```java\n[a](nope.md)\n```\n[b](yes.md)\n"
        self.assertEqual(raws(text), [(4, "yes.md")])

    def test_indented_fence_in_list_ignored(self):
        text = "1. Step\n   ```xml\n   <a href=\"http://nope\"/>\n   ```\n2. [b](yes.md)\n"
        self.assertEqual(raws(text), [(5, "yes.md")])

    def test_longer_fence_needs_longer_close(self):
        text = "````md\n```\n[a](nope.md)\n```\n````\n[b](yes.md)\n"
        self.assertEqual(raws(text), [(6, "yes.md")])

    def test_inline_code_ignored(self):
        self.assertEqual(raws("`[a](nope.md)` and ``x `[b](no.md)` y`` [c](yes.md)"), [(1, "yes.md")])

    def test_html_comments_ignored(self):
        text = "<!-- [a](nope.md) --> [b](yes.md)\n<!--\n[c](nope.md)\n-->\n[d](yes2.md)\n"
        self.assertEqual(raws(text), [(1, "yes.md"), (5, "yes2.md")])

    def test_empty_destination_ignored(self):
        self.assertEqual(raws("[a]()"), [])

    def test_link_carries_file(self):
        self.assertEqual(extract_text("[a](b.md)", "docs/q.md"), [Link("docs/q.md", 1, "b.md")])


class TestExtractFiles(unittest.TestCase):
    def test_iter_and_extract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs" / "sub").mkdir(parents=True)
            (root / "docs" / "a.md").write_text("[x](sub/b.mdx)\n", encoding="utf-8")
            (root / "docs" / "sub" / "b.mdx").write_text("\n[y](https://y.org/)\n", encoding="utf-8")
            (root / "docs" / "c.txt").write_text("[z](no.md)", encoding="utf-8")
            files = iter_doc_files(root / "docs")
            self.assertEqual([p.name for p in files], ["a.md", "b.mdx"])
            self.assertEqual(extract_files(root, files), [
                Link("docs/a.md", 1, "sub/b.mdx"),
                Link("docs/sub/b.mdx", 2, "https://y.org/"),
            ])


if __name__ == "__main__":
    unittest.main()
