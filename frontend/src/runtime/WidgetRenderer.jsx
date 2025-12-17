import DiagramEditor from "./DiagramEditor";

/**
 * Renders widgets based on their declared type.
 * This is a fixed, finite runtime.
 */
export default function WidgetRenderer({ widget }) {
  switch (widget.type) {
    case "diagram":
      return (
        <DiagramEditor
          endpoint={widget.data_endpoint}
        />
      );

    case "collection":
      return (
        <CollectionRenderer
          endpoint={widget.data_endpoint}
          layout={widget.layout}
        />
      );

    case "iframe":
      return (
        <iframe
          src={widget.iframe_src}
          style={{ width: "100%", height: "100%", border: "none" }}
        />
      );

    default:
      return <div>Unknown widget type: {widget.type}</div>;
  }
}
