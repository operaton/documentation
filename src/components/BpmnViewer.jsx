// src/components/BpmnViewer.jsx

import React, { useEffect, useRef, useState } from 'react';

/**
 * BPMN Diagram Viewer Component
 *
 * Renders BPMN diagrams inline in documentation
 * Usage: <BpmnViewer diagramPath="/bpmn/path/to/diagram.bpmn" />
 */
export default function BpmnViewer({ diagramPath, height = '400px' }) {
  const containerRef = useRef(null);
  const viewerRef = useRef(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!containerRef.current) return;

    let mounted = true;

    const initViewer = async () => {
      try {
        setLoading(true);
        setError(null);

        console.log(`[BpmnViewer] Loading diagram: ${diagramPath}`);

        // Fetch BPMN XML
        const response = await fetch(diagramPath);

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const xml = await response.text();

        // Check for 404 HTML
        if (xml.trim().startsWith('<!DOCTYPE') || xml.trim().startsWith('<html')) {
          throw new Error(`File not found at ${diagramPath} (received HTML page)`);
        }

        if (!xml.includes('bpmn') && !xml.includes('definitions')) {
          console.warn('[BpmnViewer] Response content:', xml.substring(0, 200));
          throw new Error('File does not appear to be valid BPMN XML');
        }

        console.log('[BpmnViewer] XML loaded, initializing viewer...');

        // Load bpmn-js viewer
        const BpmnJS = (await import('bpmn-js/lib/Viewer')).default;

        if (!mounted) return;

        // Destroy previous viewer
        if (viewerRef.current) {
          viewerRef.current.destroy();
        }

        // Create viewer
        const viewer = new BpmnJS({
          container: containerRef.current
        });

        viewerRef.current = viewer;

        // Import XML
        await viewer.importXML(xml);

        if (!mounted) return;

        // Reveal viewer before zoom
        setLoading(false);

        // Zoom AFTER layout stabilizes
        requestAnimationFrame(() => {
          try {
            const canvas = viewer.get('canvas');
            canvas.zoom('fit-viewport');
            console.log('[BpmnViewer] Diagram rendered successfully with zoom');
          } catch (err) {
            console.warn('[BpmnViewer] Zoom failed:', err);
          }
        });

      } catch (err) {
        console.error('[BpmnViewer] Error loading diagram:', err);
        if (mounted) {
          setError(err.message || 'Failed to load diagram');
          setLoading(false);
        }
      }
    };

    initViewer();

    return () => {
      mounted = false;
      if (viewerRef.current) {
        viewerRef.current.destroy();
        viewerRef.current = null;
      }
    };
  }, [diagramPath]);

  // --- Styles ----------------------------------------------------

  const wrapperStyle = {
    position: 'relative',
    height,
    marginBottom: '1.5rem',
    border: '1px solid var(--ifm-color-emphasis-300, #ccc)',
    borderRadius: '4px',
    overflow: 'hidden',
    backgroundColor: 'var(--ifm-background-color, #fff)'
  };

  const viewerStyle = {
    position: 'absolute',
    inset: 0,
    display: 'block'
  };

  const loadingStyle = {
    position: 'absolute',
    inset: 0,
    display: loading ? 'flex' : 'none',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'var(--ifm-color-emphasis-100, #f5f5f5)',
    color: 'var(--ifm-color-emphasis-600, #666)',
    zIndex: 10
  };

  const errorStyle = {
    padding: '1rem',
    backgroundColor: '#fff3cd',
    border: '1px solid #ffc107',
    borderRadius: '4px',
    color: '#856404'
  };

  return (
    <div style={wrapperStyle}>
      {error && (
        <div style={errorStyle}>
          <strong>⚠ Error loading diagram</strong>
          <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.9em' }}>{error}</p>
          <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.8em', opacity: 0.8 }}>
            Path: <code>{diagramPath}</code>
          </p>
        </div>
      )}

      {/* Loading overlay */}
      <div style={loadingStyle}>
        <span>Loading BPMN diagram...</span>
      </div>

      {/* Viewer container */}
      <div
        ref={containerRef}
        style={viewerStyle}
        aria-label="BPMN Diagram"
      />
    </div>
  );
}
