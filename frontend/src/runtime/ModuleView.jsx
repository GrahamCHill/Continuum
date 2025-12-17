import WidgetRenderer from "./WidgetRenderer";

/**
 * Renders a module using its declarative widgets.
 */
export default function ModuleView({ module }) {
  return (
    <div className="module-view">
      <h2>{module.name}</h2>
      <p>{module.description}</p>

      {module.widgets.map((widget) => (
        <WidgetRenderer
          key={widget.id}
          widget={widget}
        />
      ))}
    </div>
  );
}
