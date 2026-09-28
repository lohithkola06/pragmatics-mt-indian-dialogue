import { useEffect, useRef, useState } from 'react';
import Markdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';
import { DOC_ENTRIES } from '../data';
import { resolveLink } from '../lib/mdLinks';

// Loaded with this lazily imported module, so the markdown stack and the doc
// texts stay out of the main bundle.
const rawDocs = import.meta.glob('../generated/guidelines/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>;

const DOCS = DOC_ENTRIES.map((entry) => ({
  ...entry,
  text: rawDocs[`../generated/guidelines/${entry.file}`] ?? '',
}));

type Props = { initialFile: string; onClose: () => void };

/** Full-screen reader for the synced guideline docs. Esc closes it. */
export default function GuidelinesViewer({ initialFile, onClose }: Props) {
  const [file, setFile] = useState(initialFile);
  const closeRef = useRef<HTMLButtonElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const doc = DOCS.find((d) => d.file === file) ?? DOCS[0];

  useEffect(() => {
    closeRef.current?.focus();
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', onKey);
    const previous = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      window.removeEventListener('keydown', onKey);
      document.body.style.overflow = previous;
    };
  }, [onClose]);

  useEffect(() => {
    contentRef.current?.scrollTo({ top: 0 });
  }, [file]);

  return (
    <div className="viewer" role="dialog" aria-modal="true" aria-label="Guidelines">
      <div className="viewer-head">
        <h2>Guidelines</h2>
        <button ref={closeRef} className="btn btn-small" onClick={onClose}>
          Close <span className="muted small">(Esc)</span>
        </button>
      </div>
      <div className="viewer-body">
        <nav className="viewer-nav" aria-label="Guideline documents">
          {DOCS.map((d) => (
            <button key={d.file} aria-current={d.file === doc.file} onClick={() => setFile(d.file)}>
              {d.title}
            </button>
          ))}
        </nav>
        <div className="viewer-content" ref={contentRef}>
          <article className="md">
            <Markdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeRaw]}
              components={{
                a: ({ href, children }) => {
                  const target = resolveLink(href ?? '', doc.source_path, DOCS);
                  if (target.kind === 'doc') {
                    return (
                      <button className="link-btn" onClick={() => setFile(target.file)}>
                        {children}
                      </button>
                    );
                  }
                  if (target.kind === 'external') {
                    return (
                      <a href={target.href} target="_blank" rel="noreferrer">
                        {children}
                      </a>
                    );
                  }
                  if (target.kind === 'anchor') return <a href={`#${target.id}`}>{children}</a>;
                  return <span className="plain-link">{children}</span>;
                },
              }}
            >
              {doc.text}
            </Markdown>
          </article>
        </div>
      </div>
    </div>
  );
}
