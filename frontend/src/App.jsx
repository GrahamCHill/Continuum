import { useEffect, useState } from "react";
import "./App.css";

/**
 * Root application shell.
 * Acts as a runtime for dynamically discovered modules.
 */
function App() {
  const [modules, setModules] = useState([]);
  const [activeModule, setActiveModule] = useState(null);

  useEffect(() => {
    fetch("/api/modules")
      .then((r) => r.json())
      .then((data) => {
        setModules(data);
        if (data.length > 0) {
          setActiveModule(data[0]);
        }
      })
      .catch(console.error);
  }, []);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h3>Modules</h3>
        {modules.map((m) => (
          <button
            key={m.id}
            onClick={() => setActiveModule(m)}
            className={activeModule?.id === m.id ? "active" : ""}
          >
            {m.name}
          </button>
        ))}
      </aside>

      <main className="main-content">
        {activeModule ? (
          <ModuleView module={activeModule} />
        ) : (
          <p>No modules available</p>
        )}
      </main>
    </div>
  );
}

export default App;
