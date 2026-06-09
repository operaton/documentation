// Initialize Mermaid diagrams when the page loads
if (typeof window !== 'undefined') {
  const initMermaid = () => {
    if (typeof window.mermaid !== 'undefined') {
      window.mermaid.initialize({
        startOnLoad: true,
        theme: 'default',
        securityLevel: 'loose',
      });
      window.mermaid.contentLoaded();
    }
  };

  // Initialize on page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMermaid);
  } else {
    initMermaid();
  }

  // Re-initialize on SPA navigation (Docusaurus uses a custom router)
  const observer = new MutationObserver(() => {
    if (typeof window.mermaid !== 'undefined') {
      window.mermaid.contentLoaded();
    }
  });

  observer.observe(document.querySelector('main') || document.body, {
    childList: true,
    subtree: true,
  });
}
