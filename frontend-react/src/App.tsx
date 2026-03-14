import React, { useState, useEffect } from 'react';
import './App.css';
import changelogData from './changelog.json';

interface Update {
  id: number;
  date: string;
  title: string;
  description: string;
  type: string;
  version: string;
}

function App() {
  const [updates, setUpdates] = useState<Update[]>([]);
  const [showAllUpdates, setShowAllUpdates] = useState(false);

  useEffect(() => {
    setUpdates(changelogData.updates as Update[]);
  }, []);

  const getTypeIcon = (type: string) => {
    switch(type) {
      case 'feature': return '✨';
      case 'improvement': return '🚀';
      case 'bugfix': return '🐛';
      case 'performance': return '⚡';
      case 'security': return '🔒';
      default: return '📝';
    }
  };

  const getTypeColor = (type: string) => {
    switch(type) {
      case 'feature': return '#FA6C1A';
      case 'improvement': return '#1A67FA';
      case 'bugfix': return '#E74C3C';
      case 'performance': return '#27AE60';
      case 'security': return '#8E44AD';
      default: return '#666666';
    }
  };

  return (
    <div className="App">
      <header className="header">
        <div className="logo-container">
          <img src="/logo.png" alt="Klink-dPS Logo" className="logo" />
          <div className="brand-name">Klinik-dPS</div>
        </div>
      </header>
      
      <main className="main-content">
        <section className="hero-section">
          <h1 className="hero-title">Digitale Patientensimulation für Krankenhäuser</h1>
          <p className="hero-subtitle">
            Moderne Simulationstechnologie zur Vorbereitung auf Ausnahmesituationen in Krankenhäusern
          </p>
          <div className="button-group">
            <a href="https://klinik-dps.de" target="_blank" rel="noopener noreferrer" className="primary-button">
              Simulation starten
            </a>
            <a href="https://github.com/hpi-sam/dps.training_k/" target="_blank" rel="noopener noreferrer" className="secondary-button">
              Quellcode ansehen
            </a>
          </div>
        </section>
        
        <section className="problem-section">
          <div className="content-container">
            <h2>Die Herausforderung</h2>
            <p className="problem-text">
              Krankenhäuser müssen auf Ausnahmesituationen wie Massenanfälle von Verletzten vorbereitet sein. Traditionelle Übungen sind oft zu aufwändig und komplex für den klinischen Alltag.
            </p>
            <br />
            <div className="problem-points">
              <div className="problem-point">
                <div className="point-icon">⏱️</div>
                <div>
                  <h4>Zeitaufwand</h4>
                  <p>Traditionelle Simulationen erfordern lange Vorbereitungen</p>
                </div>
              </div>
              <div className="problem-point">
                <div className="point-icon">🏥</div>
                <div>
                  <h4>Komplexität</h4>
                  <p>Bestehende Systeme sind zu komplex für regelmäßige Schulungen</p>
                </div>
              </div>
              <div className="problem-point">
                <div className="point-icon">💰</div>
                <div>
                  <h4>Kosten</h4>
                  <p>Personal und Ressourcen führen zu hohen Kosten bei Vollübungen</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="solution-section">
          <div className="content-container">
            <h2>Unsere Lösung</h2>
            <p className="solution-text">
              Klinik-dPS soll dieses Problem lösen, indem die Patienten mit ihren Vitalparametern und Behandlungsoptionen auf Tablets angezeigt werden. Die Patiententablets können in einem oder mehreren Räumen verteilt werden und so ein Szenario im Krankenhaus simulieren.
            </p>
            <div className="solution-content">
              <div className="solution-feature">
                <div className="feature-icon">📱</div>
                <div>
                  <h3>Tablet-optimierte Webanwendung</h3>
                  <p>Jedes Tablet zeigt einen Patienten mit allen Vitalparametern und Behandlungsoptionen.</p>
                </div>
              </div>
              <div className="solution-feature">
                <div className="feature-icon">🎯</div>
                <div>
                  <h3>Fokussierte Interaktionen</h3>
                  <p>Essenzielle medizinische Entscheidungen: Triagierung, Verlegung, Personal- und Ressourcenzuweisung und Behandlung.</p>
                </div>
              </div>
              <div className="solution-feature">
                <div className="feature-icon">⚙️</div>
                <div>
                  <h3>Dynamische Steuerung</h3>
                  <p>Übungsleiter können in Echtzeit Patienten, Personal und Ressourcen anpassen.</p>
                </div>
              </div>
              <div className="solution-feature">
                <div className="feature-icon">📊</div>
                <div>
                  <h3>Komplettes Logging</h3>
                  <p>Alle Aktionen und Veränderungen werden protokolliert.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="updates-section">
          <div className="content-container">
            <h2>Neuste Updates</h2>
            <p className="updates-text">
              Die digitale Klink-dPS wurde im Rahmen eines Bachelorprojekts entwickelt, unter Open-Source-Lizenz veröffentlicht und wird seit dem gelegentlich ehrenamtlich weiterentwickelt.
            </p>
            <div className="changelog-container">
              {updates.slice(0, showAllUpdates ? updates.length : 1).map((update) => (
                <div key={update.id} className="changelog-item">
                  <div className="changelog-header">
                    <h3 className="changelog-title">{update.title}</h3>
                    <div className="changelog-version">{update.version}</div>
                  </div>
                  <div className="changelog-content">
                    <p className="changelog-description">{update.description}</p>
                    <div className="changelog-date">{new Date(update.date).toLocaleDateString('de-DE', { 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}</div>
                  </div>
                </div>
              ))}
              {updates.length > 1 && (
                <button 
                  className="expand-button"
                  onClick={() => setShowAllUpdates(!showAllUpdates)}
                >
                  {showAllUpdates ? 'Weniger anzeigen' : `${updates.length - 1} weitere Updates anzeigen`}
                </button>
              )}
            </div>
          </div>
        </section>

        <section className="links-section">
          <div className="content-container">
            <h2>Weitere Informationen</h2>
            <div className="links-grid">
              <a href="https://manv-simulation.de/" target="_blank" rel="noopener noreferrer" className="info-link">
                <div className="link-card">
                  <div className="link-icon">🏥</div>
                  <h3>MANV Simulation</h3>
                  <p>Überblick über digitale Simulationssysteme</p>
                </div>
              </a>
              <a href="https://www.tele-task.de/lecture/video/10757/" target="_blank" rel="noopener noreferrer" className="info-link">
                <div className="link-card">
                  <div className="link-icon">📹</div>
                  <h3>Projektpräsentation</h3>
                  <p>7-Minuten Überblick über Klinik-dPS</p>
                </div>
              </a>
              <a href="https://github.com/hpi-sam/dps.training_k/" target="_blank" rel="noopener noreferrer" className="info-link">
                <div className="link-card">
                  <div className="link-icon">💻</div>
                  <h3>Technische Dokumentation</h3>
                  <p>Quellcode und Implementierungsdetails</p>
                </div>
              </a>
            </div>
          </div>
        </section>

        <section className="contact-section">
          <div className="content-container">
            <h2>Kontakt & Zusammenarbeit</h2>
            <div className="contact-content">
              <p>
                Wir sind offen für Zusammenarbeit mit Krankenhäusern, Notfallorganisationen und 
                akademischen Partnern zur Weiterentwicklung der digitalen Patientensimulation.
              </p>
              <div className="contact-info">
                <span className="contact-email">bp2023hg1[at]hpi.de</span>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
