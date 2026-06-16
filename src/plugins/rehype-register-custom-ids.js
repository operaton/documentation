export default function rehypeRegisterCustomIds() {
  return (tree, file) => {
    const anchors = new Set(file.data.anchors || []);

    function getMdxJsxId(node) {
      return node.attributes?.find(
        (attribute) => attribute.type === 'mdxJsxAttribute' && attribute.name === 'id',
      )?.value;
    }

    function visit(node) {
      if (node && typeof node === 'object') {
        if (node.type === 'element' && node.properties?.id) {
          anchors.add(node.properties.id);
        }

        const mdxJsxId = getMdxJsxId(node);
        if (typeof mdxJsxId === 'string') {
          anchors.add(mdxJsxId);
        }
        if (Array.isArray(node.children)) {
          node.children.forEach(visit);
        }
      }
    }

    visit(tree);

    file.data.anchors = Array.from(anchors);
  };
}
