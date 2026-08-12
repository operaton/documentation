// Mermaid initialization for Docusaurus
// Docusaurus renders mermaid blocks as <pre><code class="language-mermaid">,
// but Mermaid.js expects <div class="mermaid">. This script converts them.
(function () {
  function convertAndRender() {
    if (typeof window.mermaid === 'undefined') return;

    // Find all code blocks with language-mermaid class
    var codeBlocks = document.querySelectorAll('code.language-mermaid');
    codeBlocks.forEach(function (code) {
      var pre = code.parentElement;
      if (!pre || pre.dataset.mermaidConverted) return;

      // Create a div.mermaid to replace the pre block
      var div = document.createElement('div');
      div.className = 'mermaid';
      div.textContent = code.textContent;
      pre.parentNode.replaceChild(div, pre);
    });

    // Run mermaid on all .mermaid divs that haven't been processed yet
    var unprocessed = document.querySelectorAll('.mermaid:not([data-processed])');
    if (unprocessed.length > 0) {
      window.mermaid.run({ nodes: unprocessed });
    }
  }

  function waitForMermaid(attempts) {
    if (typeof window.mermaid !== 'undefined') {
      window.mermaid.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose' });
      convertAndRender();
    } else if (attempts > 0) {
      setTimeout(function () { waitForMermaid(attempts - 1); }, 100);
    }
  }

  // Run on initial load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { waitForMermaid(50); });
  } else {
    waitForMermaid(50);
  }

  // Re-run on SPA navigation (Docusaurus changes the DOM when navigating)
  var lastUrl = location.href;
  new MutationObserver(function () {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      setTimeout(function () { waitForMermaid(20); }, 300);
    }
  }).observe(document.body, { childList: true, subtree: true });
})();
