import React, { useState, useEffect } from 'react';
import '../App.css';
import changelogData from '../changelog.json';

interface Update {
  id: number;
  date: string;
  title: string;
  description: string;
  type: string;
  version: string;
}

const LandingPage: React.FC = () => {
  const [updates, setUpdates] = useState<Update[]>([]);
  const [showAllUpdates, setShowAllUpdates] = useState(false);

  useEffect(() => {
    setUpdates(changelogData.updates as Update[]);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-accent-bg to-gray-100 text-text-dark font-sans">
      <header className="fixed top-0 left-0 right-0 bg-white bg-opacity-98 backdrop-blur-lg shadow-sm z-50 px-8 py-4 flex justify-center items-center">
        <div className="flex items-center gap-4">
          <img src="/logo.png" alt="Klink-dPS Logo" className="w-10 h-10 object-contain" />
          <div className="text-2xl font-bold text-text-dark">Klinik-dPS</div>
        </div>
      </header>
      
      <main className="pt-20">
        <section className="text-center py-32 px-0 bg-gradient-to-r from-primary to-secondary text-white">
          <h1 className="text-5xl font-bold mb-6 leading-tight max-w-4xl mx-auto">Digitale Patientensimulation für Krankenhäuser</h1>
          <p className="text-xl mb-12 max-w-2xl leading-relaxed opacity-95 mx-auto">
            Moderne Simulationstechnologie zur Vorbereitung auf Ausnahmesituationen in Krankenhäusern
          </p>
          <div className="flex gap-6 justify-center flex-wrap">
            <a href={process.env.NODE_ENV === 'production' ? '/simulation' : `${process.env.REACT_APP_VUE_URL}/simulation`} className="bg-white text-primary px-10 py-4 text-lg font-semibold rounded-full transition-all duration-300 shadow-lg hover:-translate-y-0.5 hover:shadow-xl no-underline inline-block">
              Simulation starten
            </a>
            <a href="https://github.com/hpi-sam/dps.training_k/" target="_blank" rel="noopener noreferrer" className="bg-transparent text-white border-2 border-white px-10 py-4 text-lg font-semibold rounded-full transition-all duration-300 hover:bg-white hover:text-primary hover:-translate-y-0.5 no-underline inline-block">
              Quellcode ansehen
            </a>
          </div>
        </section>
        
        <section className="text-center py-20 bg-accent-bg">
          <div className="max-w-6xl mx-auto px-8">
            <h2 className="text-4xl font-bold text-text-dark mb-8">Die Herausforderung</h2>
            <p className="text-center max-w-2xl mx-auto leading-relaxed text-lg mb-8">
              Krankenhäuser müssen auf Ausnahmesituationen wie Massenanfälle von Verletzten vorbereitet sein. Traditionelle Übungen sind oft zu aufwändig und komplex für den klinischen Alltag.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <div className="flex items-start gap-4 p-8 bg-white rounded-xl shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-300">
                <div className="text-4xl flex-shrink-0">⏱️</div>
                <div>
                  <h4 className="text-primary text-xl mb-2 font-semibold">Zeitaufwand</h4>
                  <p className="text-text-light leading-relaxed m-0">Traditionelle Simulationen erfordern lange Vorbereitungen</p>
                </div>
              </div>
              <div className="flex items-start gap-4 p-8 bg-white rounded-xl shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-300">
                <div className="text-4xl flex-shrink-0">🏥</div>
                <div>
                  <h4 className="text-primary text-xl mb-2 font-semibold">Komplexität</h4>
                  <p className="text-text-light leading-relaxed m-0">Bestehende Systeme sind zu komplex für regelmäßige Schulungen</p>
                </div>
              </div>
              <div className="flex items-start gap-4 p-8 bg-white rounded-xl shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-300">
                <div className="text-4xl flex-shrink-0">💰</div>
                <div>
                  <h4 className="text-primary text-xl mb-2 font-semibold">Kosten</h4>
                  <p className="text-text-light leading-relaxed m-0">Personal und Ressourcen führen zu hohen Kosten bei Vollübungen</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="py-20 bg-accent-bg">
          <div className="max-w-6xl mx-auto px-8">
            <h2 className="text-4xl font-bold text-text-dark mb-8 text-center">Unsere Lösung</h2>
            <p className="text-center max-w-2xl mx-auto leading-relaxed text-lg mb-12">
              Klinik-dPS soll dieses Problem lösen, indem die Patienten mit ihren Vitalparametern und Behandlungsoptionen auf Tablets angezeigt werden. Die Patiententablets können in einem oder mehreren Räumen verteilt werden und so ein Szenario im Krankenhaus simulieren.
            </p>
            <div className="grid gap-8">
              <div className="flex items-start gap-6 p-10 bg-white rounded-2xl shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-300 border border-gray-100">
                <div className="text-5xl flex-shrink-0">📱</div>
                <div>
                  <h3 className="text-primary text-2xl mb-4 font-semibold">Tablet-optimierte Webanwendung</h3>
                  <p className="text-text-dark leading-relaxed m-0 text-base">Jedes Tablet zeigt einen Patienten mit allen Vitalparametern und Behandlungsoptionen.</p>
                </div>
              </div>
              <div className="flex items-start gap-6 p-10 bg-white rounded-2xl shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-300 border border-gray-100">
                <div className="text-5xl flex-shrink-0">🎯</div>
                <div>
                  <h3 className="text-primary text-2xl mb-4 font-semibold">Fokussierte Interaktionen</h3>
                  <p className="text-text-dark leading-relaxed m-0 text-base">Essenzielle medizinische Entscheidungen: Triagierung, Verlegung, Personal- und Ressourcenzuweisung und Behandlung.</p>
                </div>
              </div>
              <div className="flex items-start gap-6 p-10 bg-white rounded-2xl shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-300 border border-gray-100">
                <div className="text-5xl flex-shrink-0">⚙️</div>
                <div>
                  <h3 className="text-primary text-2xl mb-4 font-semibold">Dynamische Steuerung</h3>
                  <p className="text-text-dark leading-relaxed m-0 text-base">Übungsleiter können in Echtzeit Patienten, Personal und Ressourcen anpassen.</p>
                </div>
              </div>
              <div className="flex items-start gap-6 p-10 bg-white rounded-2xl shadow-sm hover:-translate-y-1 hover:shadow-lg transition-all duration-300 border border-gray-100">
                <div className="text-5xl flex-shrink-0">📊</div>
                <div>
                  <h3 className="text-primary text-2xl mb-4 font-semibold">Komplettes Logging</h3>
                  <p className="text-text-dark leading-relaxed m-0 text-base">Alle Aktionen und Veränderungen werden protokolliert.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="py-20 bg-accent-bg">
          <div className="max-w-6xl mx-auto px-8">
            <h2 className="text-4xl font-bold text-text-dark mb-8 text-center">Neuste Updates</h2>
            <p className="text-center max-w-2xl mx-auto leading-relaxed text-lg mb-12 text-text-light">
              Die digitale Klink-dPS wurde im Rahmen eines Bachelorprojekts entwickelt, unter Open-Source-Lizenz veröffentlicht und wird seit dem gelegentlich ehrenamtlich weiterentwickelt.
            </p>
            <div className="grid gap-4 max-w-5xl mx-auto">
              {updates.slice(0, showAllUpdates ? updates.length : 1).map((update) => (
                <div key={update.id} className="bg-white rounded-xl p-4 border-l-4 border-primary transition-all duration-300 shadow-sm hover:-translate-y-0.5 hover:shadow-lg">
                  <div className="flex justify-between items-start mb-2 pb-1 border-b border-gray-200">
                    <h3 className="text-text-dark text-lg font-semibold leading-tight flex-1">{update.title}</h3>
                    <div className="bg-primary text-white px-2 py-1 rounded-full text-xs font-semibold uppercase tracking-wide ml-4">{update.version}</div>
                  </div>
                  <div className="pl-1">
                    <p className="text-text-dark leading-relaxed mb-2 text-sm">{update.description}</p>
                    <div className="text-text-light text-xs font-medium opacity-70">{new Date(update.date).toLocaleDateString('de-DE', { 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}</div>
                  </div>
                </div>
              ))}
              {updates.length > 1 && (
                <button 
                  className="bg-transparent text-primary border-2 border-primary px-6 py-3 rounded-full text-sm font-semibold transition-all duration-300 mt-4 w-full max-w-xs mx-auto block hover:bg-primary hover:text-white hover:-translate-y-0.5 hover:shadow-lg"
                  onClick={() => setShowAllUpdates(!showAllUpdates)}
                >
                  {showAllUpdates ? 'Weniger anzeigen' : `${updates.length - 1} weitere Updates anzeigen`}
                </button>
              )}
            </div>
          </div>
        </section>

        <section className="py-20 bg-accent-bg">
          <div className="max-w-6xl mx-auto px-8">
            <h2 className="text-4xl font-bold text-text-dark mb-12 text-center">Weitere Informationen</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <a href="https://manv-simulation.de/" target="_blank" rel="noopener noreferrer" className="no-underline text-inherit transition-transform duration-300 hover:-translate-y-1">
                <div className="bg-white p-10 rounded-2xl text-center transition-all duration-300 shadow-sm hover:shadow-lg h-full border border-gray-100">
                  <div className="text-5xl mb-6">🏥</div>
                  <h3 className="text-primary text-2xl mb-4 font-semibold">MANV Simulation</h3>
                  <p className="text-text-light leading-relaxed m-0 text-sm">Überblick über digitale Simulationssysteme</p>
                </div>
              </a>
              <a href="https://www.tele-task.de/lecture/video/10757/" target="_blank" rel="noopener noreferrer" className="no-underline text-inherit transition-transform duration-300 hover:-translate-y-1">
                <div className="bg-white p-10 rounded-2xl text-center transition-all duration-300 shadow-sm hover:shadow-lg h-full border border-gray-100">
                  <div className="text-5xl mb-6">📹</div>
                  <h3 className="text-primary text-2xl mb-4 font-semibold">Projektpräsentation</h3>
                  <p className="text-text-light leading-relaxed m-0 text-sm">7-Minuten Überblick über Klinik-dPS</p>
                </div>
              </a>
              <a href="https://github.com/hpi-sam/dps.training_k/" target="_blank" rel="noopener noreferrer" className="no-underline text-inherit transition-transform duration-300 hover:-translate-y-1">
                <div className="bg-white p-10 rounded-2xl text-center transition-all duration-300 shadow-sm hover:shadow-lg h-full border border-gray-100">
                  <div className="text-5xl mb-6">💻</div>
                  <h3 className="text-primary text-2xl mb-4 font-semibold">Technische Dokumentation</h3>
                  <p className="text-text-light leading-relaxed m-0 text-sm">Quellcode und Implementierungsdetails</p>
                </div>
              </a>
            </div>
          </div>
        </section>

        <section className="bg-gradient-to-r from-secondary to-primary text-white py-20">
          <div className="max-w-6xl mx-auto px-8">
            <h2 className="text-4xl font-bold text-white mb-8 text-center" style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.3)' }}>Kontakt & Zusammenarbeit</h2>
            <div className="text-center">
              <p className="mb-6 text-lg">
                Wir sind offen für Zusammenarbeit mit Krankenhäusern, Notfallorganisationen und 
                akademischen Partnern zur Weiterentwicklung der digitalen Patientensimulation.
              </p>
              <div className="flex flex-col items-center gap-2">
                <span className="text-white text-xl font-semibold no-underline px-4 py-2 border-2 border-white rounded-full transition-all duration-300 hover:bg-white hover:text-primary">bp2023hg1[at]hpi.de</span>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default LandingPage;
