export default function rehypeRegisterCustomIds() {
  return (tree, file) => {
    const anchors = new Set(file.data.anchors || []);

    function visit(node) {
      if (node && typeof node === 'object') {
        // Wenn das Element eine id besitzt, füge sie der Ankerliste hinzu
        if (node.type === 'element' && node.properties?.id) {
          anchors.add(node.properties.id);
        //   console.log('Found ID:', node.properties.id, 'in file:', file.path);
        }
        if (Array.isArray(node.children)) {
          node.children.forEach(visit);
        }
      }
    }

    visit(tree);

    // Docusaurus liest file.data.anchors zur Validierung ein
    file.data.anchors = Array.from(anchors);
  };
}